import pandas as pd
from utils import execute_query
from main import _DEFAULT_CELLTYPE_INFO, _DEFAULT_STUDY_INFO


def create_study_cell_source_meancount():
    print("Creating Study, Celltype, Source and MeanCount nodes ...")
    study_info_str = "{" + ", ".join(["{}: '{}'".format(c, _DEFAULT_STUDY_INFO[c]) for c in _DEFAULT_STUDY_INFO]) + "}"
    celltype_info_str = (
        "{" + ", ".join(["{}: '{}'".format(c, _DEFAULT_CELLTYPE_INFO[c]) for c in _DEFAULT_CELLTYPE_INFO]) + "}"
    )

    create_study_query = "MERGE (s:Study {})".format(study_info_str)
    create_celltype_query = "MERGE (c:Celltype {})".format(celltype_info_str)
    create_source_query = "MERGE (s)-[:HAS]->(o:Source)<-[:HAS]-(c) SET o.id = id(o)"
    create_meancount = "MERGE (m:MeanCount)"
    create_source_meancount_edge = "MERGE (o)-[:HAS]->(m)"
    return_id = "RETURN id(o) AS id"

    query = (
        create_study_query
        + " "
        + create_celltype_query
        + " "
        + create_source_query
        + " "
        + create_meancount
        + " "
        + create_source_meancount_edge
        + " "
        + return_id
    )
    result, _, _ = execute_query(query=query, read=False)

    return result[0]["id"]


def create_nodes(source_file: str, type_: str, id: str):
    # Identifier; For TG / TF is ENSEMBL, OR is nearest_index
    id_str = "{" + "{}: map.{}".format(id, id) + "}"
    load_data_query = "LOAD CSV WITH HEADERS from 'file:///{}' AS map RETURN map".format(source_file)
    merge_into_db_query = "MERGE (t:{} {} ) SET t = map".format(type_, id_str)

    # For large numbers of nodes, using apoc.periodic.iterate
    # For info, see: https://neo4j.com/labs/apoc/4.2/overview/apoc.periodic/apoc.periodic.iterate/

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 5000}} )'.format(
        load_data_query, merge_into_db_query
    )

    execute_query(query=per_iter, read=False)
    return


def create_relationship(source_file: str, type_: str, between: tuple[str], node_types: list[str], values: list[str]):
    # TODO: Maybe with trick of generating nodes first, then relationships? Could also do apoc periodic iterate, more clear
    load_data_query = "LOAD CSV WITH HEADERS from 'file:///{}' AS map MATCH (m:{}), (n:{}) WHERE n.{} = map.{} AND m.{} = map.{} RETURN map, n, m".format(
        source_file, node_types[0], node_types[1], between[1][0], between[1][1], between[0][0], between[0][1]
    )
    set_values_query = " ".join([""] + ["SET e.{} = map.{}".format(v, v) for v in values])
    create_edge_query = "CREATE (m)-[e:{}]->(n)".format(type_) + set_values_query

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 5000}} )'.format(load_data_query, create_edge_query)
    print(per_iter)
    # execute_query(per_iter, read=False)


def create_tg_nodes(nodes: pd.DataFrame, source: int):
    print("Creating Target Gene nodes ...")

    mean_count = nodes.filter(items=["ENSEMBL", "mean_count"])
    mean_count["Source"] = source
    mean_count.rename(columns={"mean_count": "Value"})
    mean_count.to_csv("/usr/local/bin/neo4j/import/tg_meancount.csv", index=False)

    # create new Target Gene nodes for every new TG
    nodes.drop(columns=["mean_count"])
    nodes.to_csv("/usr/local/bin/neo4j/import/tg.csv", index=False)
    create_nodes(source_file="tg.csv", type_="TG", id="ENSEMBL")

    print("Creating MEANCOUNT edges for Target Genes ...")

    # create MeanCount edges for TGs
    create_relationship(
        source_file="tg_meancount.csv",
        type_="MEANCOUNT",
        between=(("Value", "Value"), ("ENSEMBL", "ENSEMBL")),
        node_types=("MeanCount", "TG"),
        values=["Value", "Source"],
    )


def create_tf_nodes(nodes: pd.DataFrame, source: int):
    print("Creating Transcription Factor nodes ...")

    mean_count = nodes.filter(items=["ENSEMBL", "mean_count"])
    mean_count["Source"] = source
    mean_count.rename(columns={"mean_count": "Value"})
    mean_count.to_csv("/usr/local/bin/neo4j/import/tf_meancount.csv", index=False)

    # create new Transcription Factor node for every new TF
    nodes.drop(columns=["mean_count"])
    nodes.to_csv("/usr/local/bin/neo4j/import/tf.csv", index=False)
    create_nodes(source_file="tf.csv", type_="TF:TG", id="ENSEMBL")

    print("Creating MEANCOUNT edges for Transcription Factors ...")

    # create MeanCount edges for TFs
    create_relationship(
        source_file="tf_meancount.csv",
        type_="MEANCOUNT",
        between=(("Value", "Value"), ("ENSEMBL", "ENSEMBL")),
        node_types=("MeanCount", "TF"),
        values=["Value", "Source"],
    )


def create_or_nodes(nodes: pd.DataFrame, source: int):
    print("Creating Open Region nodes ...")

    mean_count = nodes.filter(items=["nearest_index", "mean_count"])
    mean_count["Source"] = source
    mean_count.rename(columns={"mean_count": "Value"})
    mean_count.to_csv("/usr/local/bin/neo4j/import/or_meancount.csv", index=False)

    # create new Open Region node for every new OR
    nodes.drop(columns=["mean_count"])
    nodes.to_csv("/usr/local/bin/neo4j/import/or.csv", index=False)
    create_nodes(source_file="or.csv", type_="OR", id="nearest_index")

    print("Creating MEANCOUNT edges for Open Regions ...")

    # create MeanCount edges for ORs
    create_relationship(
        source_file="or_meancount.csv",
        type_="MEANCOUNT",
        between=(("Value", "Value"), ("nearest_index", "nearest_index")),
        node_types=("MeanCount", "OR"),
        values=["Value", "Source"],
    )


def create_context(context: pd.DataFrame, source: int, value_type: int):  # value_type: 1 -> DE, 0 -> DA
    print("Creating Context nodes ...")

    # create Context node for every new context
    nodes = context["Context"].unique()
    node_df = pd.DataFrame.from_records(data=[{"Value": c} for c in nodes])

    node_df.to_csv("/usr/local/bin/neo4j/import/context.csv", index=False)
    create_nodes(source_file="context.csv", type_="Context", id="Value")

    print("Connecting Source and Context nodes ...")

    # create HAS edge from source to Context node for every context represented in the source
    source_edge_df = node_df
    source_edge_df["Source"] = source
    source_edge_df.to_csv("/usr/local/bin/neo4j/import/source_context.csv", index=False)

    create_relationship(
        source_file="source_context.csv",
        type_="HAS",
        between=(("id", "Source"), ("Value", "Context")),
        node_types=["Source", "Context"],
        values=[],
    )

    print("Creating Context DE / DA edges ...")

    # Create DE/DA edges with Values and Source node id
    edge_df = context
    edge_df["Source"] = source

    # DE Edges
    if value_type == 1:
        edge_df.to_csv("/usr/local/bin/neo4j/import/de.csv", index=False)
        create_relationship(
            source_file="de.csv",
            type_="DE",
            between=(("Context", "Context"), ("ENSEMBL", "ENSEMBL")),
            node_types=("Context", "TG"),
            values=["Value", "p", "Source"],
        )

    # DA Edges
    elif value_type == 0:
        edge_df.to_csv("/usr/local/bin/neo4j/import/da.csv", index=False)
        create_relationship(
            source_file="da.csv",
            type_="DA",
            between=(("Context", "Context"), ("nearest_index", "nearest_index")),
            node_types=("Context", "OR"),
            values=["Value", "p", "Source"],
        )


def create_correlation(correlation: pd.DataFrame, source: int, value_type: int):  # value_type: 1 -> TF-TG, 0 -> TG-OR
    print("Creating CORRELATION edges ...")
    correlation["Source"] = source

    # TF-TG edges
    if value_type == 1:
        correlation.to_csv("/usr/local/bin/neo4j/import/tf_tg_corr.csv", index=False)
        create_relationship(
            source_file="tf_tg_corr.csv",
            type_="CORRELATION",
            between=(("SYMBOL", "TF"), ("ENSEMBL", "ENSEMBL")),
            node_types=("TF", "TG"),
            values=["Correlation", "Source"],
        )

    # OR-TG edges
    elif value_type == 0:
        correlation.to_csv("/usr/local/bin/neo4j/import/or_tg_corr.csv", index=False)
        create_relationship(
            source_file="or_tg_corr.csv",
            type_="CORRELATION",
            between=(("nearest_index", "nearest_index"), ("ENSEMBL", "ENSEMBL")),
            node_types=("OR", "TG"),
            values=["Correlation", "Source"],
        )


def create_motif_edges(motif: pd.DataFrame):
    print("Creating MOTIF edges ...")
    motif.to_csv("/usr/local/bin/neo4j/import/motif.csv", index=False)
    create_relationship(
        source_file="motif.csv",
        type_="MOTIF",
        between=(("SYMBOL", "TF"), ("peaks", "nearest_index")),
        node_types=("TF", "OR"),
        values=["Motif"],
    )


def create_distance_edges(distance: pd.DataFrame):
    print("Creating DISTANCE edges ...")
    distance.to_csv("/usr/local/bin/neo4j/import/distance.csv", index=False)
    create_relationship(
        source_file="distance.csv",
        type_="DISTANCE",
        between=(("nearest_index", "nearest_index"), ("ENSEMBL", "nearest_ENSEMBL")),
        node_types=("OR", "TG"),
        values=["Distance"],
    )


def create_string_edges():
    print("Creating STRING ASSOCIATION edges ...")
    # TODO
    pass


def create_functional():
    print("Creating Functional Term nodes ...")
    # TODO

    print("Creating OVERLAP edges ...")
    # TODO
    pass


def extend_db_from_experiment(
    tg_nodes: pd.DataFrame,
    tf_nodes: pd.DataFrame,
    or_nodes: pd.DataFrame,
    de_values: pd.DataFrame,
    da_values: pd.DataFrame,
    tf_tg_corr: pd.DataFrame,
    tg_or_corr: pd.DataFrame,
    motif: pd.DataFrame,
    distance: pd.DataFrame,
):
    id_source = create_study_cell_source_meancount()
    create_tg_nodes(nodes=tg_nodes, source=id_source)
    create_tf_nodes(nodes=tf_nodes, source=id_source)
    create_or_nodes(nodes=or_nodes, source=id_source)

    # TODO: Make Value and p a Float value not String
    create_context(context=de_values, source=id_source, value_type=1)
    create_context(context=da_values, source=id_source, value_type=0)

    create_correlation(correlation=tf_tg_corr, source=id_source, value_type=1)
    create_correlation(correlation=tg_or_corr, source=id_source, value_type=0)

    create_motif_edges(motif=motif)
    create_distance_edges(distance=distance)
    return


def setup_db_external_info():
    create_functional()
    create_string_edges()


def first_setup():
    extend_db_from_experiment()
    setup_db_external_info()
