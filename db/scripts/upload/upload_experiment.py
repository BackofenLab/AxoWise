import pandas as pd
from utils import time_function, print_update, save_df_to_csv, execute_query, get_values_reformat
from .upload_functions import create_nodes, create_relationship
from neo4j import Driver

_DEFAULT_CELLTYPE_INFO = {"name": "Microglia"}
_DEFAULT_STUDY_INFO = {"name": "Bulk ATAC-Seq, RNA-seq", "source": "in-house"}


@time_function
def create_study_cell_source_meancount(driver: Driver):
    """
    Creates Study, Cell, Source, and MeanCount nodes.
    """
    print_update(update_type="Node Creation", text="Study, Celltype, Source and MeanCount", color="blue")

    # Creates Map for values in Default Study / Cell info that are then added as properties to the node
    study_info_str = "{" + ", ".join(["{}: '{}'".format(c, _DEFAULT_STUDY_INFO[c]) for c in _DEFAULT_STUDY_INFO]) + "}"
    celltype_info_str = (
        "{" + ", ".join(["{}: '{}'".format(c, _DEFAULT_CELLTYPE_INFO[c]) for c in _DEFAULT_CELLTYPE_INFO]) + "}"
    )

    # Queries to be run (as one) in this function
    create_study_query = "CREATE (s:Study {})".format(study_info_str)
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
    result = execute_query(query=query, read=False, driver=driver)
    return result[0][0]


@time_function
def create_tg_meancount(mean_count: pd.DataFrame, source: int, driver: Driver):
    """
    Creates Target Gene MEANCOUNT Edges between MeanCount and TG
    """
    print_update(update_type="Edge Creation", text="MEANCOUNT for Target Genes", color="cyan")

    mean_count["Source"] = source
    mean_count = mean_count.rename(columns={"mean_count": "Value"})

    # create MeanCount edges for TGs
    values, reformat = get_values_reformat(df=mean_count, match=["ENSEMBL"])
    save_df_to_csv(file_name="tg_meancount.csv", df=mean_count)
    create_relationship(
        source_file="tg_meancount.csv",
        type_="MEANCOUNT",
        between=((), ("ENSEMBL", "ENSEMBL")),
        node_types=("MeanCount", "TG"),
        values=values,
        reformat_values=reformat,
        merge=False,
        driver=driver,
    )


@time_function
def create_tf_meancount(mean_count: pd.DataFrame, source: int, driver: Driver):
    """
    Creates Transcription MEANCOUNT Edges between MeanCount and TF, and labels Nodes with TF label
    """

    print_update(update_type="Edge Creation", text="MEANCOUNT for Transcription Factors", color="cyan")

    mean_count["Source"] = source
    mean_count = mean_count.rename(columns={"mean_count": "Value"})

    # create MeanCount edges for TFs
    values, reformat = get_values_reformat(df=mean_count, match=["ENSEMBL"])
    save_df_to_csv(file_name="tf_meancount.csv", df=mean_count)
    create_relationship(
        source_file="tf_meancount.csv",
        type_="MEANCOUNT",
        between=((), ("ENSEMBL", "ENSEMBL")),
        node_types=("MeanCount", "TF"),
        values=values,
        reformat_values=reformat,
        driver=driver,
    )


@time_function
def create_or_meancount(mean_count: pd.DataFrame, source: int, driver: Driver):
    """
    Creates MEANCOUNT edges between MeanCount and OR
    """

    # filter for MeanCount values to add later
    # mean_count = nodes.filter(items=["nearest_index", "mean_count"])
    mean_count["Source"] = source
    mean_count = mean_count.rename(columns={"mean_count": "Value"})

    print_update(update_type="Edge Creation", text="MEANCOUNT for Open Regions", color="cyan")

    # create MeanCount edges for ORs
    values, reformat = get_values_reformat(df=mean_count, match=["id"])
    save_df_to_csv(file_name="or_meancount.csv", df=mean_count)
    create_relationship(
        source_file="or_meancount.csv",
        type_="MEANCOUNT",
        between=((), ("id", "id")),
        node_types=("MeanCount", "OR"),
        values=values,
        reformat_values=reformat,
        driver=driver,
    )


@time_function
def create_context(context: pd.DataFrame, source: int, value_type: int, driver: Driver):  # value_type: 1 -> TG, 0 -> OR
    """
    Creates Context nodes from Experiment data if not already existent in DB, and DE / DA edges between Context and OR/TG
    """
    print_update(update_type="Node Creation", text="Context", color="blue")

    # create Context node for every new context
    nodes = context["Context"].unique()
    node_df = pd.DataFrame.from_records(data=[{"Context": c} for c in nodes])

    values, reformat = get_values_reformat(df=node_df, match=[])
    save_df_to_csv(file_name="context.csv", df=node_df, override_prod=True)
    create_nodes(
        source_file="context.csv", type_="Context", id="Context", values=values, reformat_values=reformat, driver=driver
    )

    print_update(update_type="Edge Creation", text="HAS for Source, Context", color="cyan")

    # create HAS edge from source to Context node for every context represented in the source
    source_edge_df = node_df
    source_edge_df["Source"] = source

    values, reformat = get_values_reformat(df=source_edge_df, match=["Source", "Context"])

    save_df_to_csv(file_name="source_context.csv", df=source_edge_df, override_prod=True)
    create_relationship(
        source_file="source_context.csv",
        type_="HAS",
        between=(("id", "Source"), ("Context", "Context")),
        node_types=("Source", "Context"),
        values=values,
        reformat_values=reformat,
        merge=True,
        driver=driver,
    )

    print_update(
        update_type="Edge Creation", text="{}".format("TG Context" if value_type == 1 else "OR Context"), color="cyan"
    )

    # Create TG/OR Context edges with Values and Source node id
    edge_df = context
    edge_df["Source"] = source

    # TG Context Edges
    if value_type == 1:
        values, reformat = get_values_reformat(df=edge_df, match=["Context", "ENSEMBL"])
        # values = list(set(list(edge_df.columns)) - set(["Context", "ENSEMBL"]))
        # reformat = [
        #     (i, "toFloat" if edge_df[i].dtype == "float64" else "toInteger")
        #     for i in values
        #     if edge_df[i].dtype != "object"
        # ]

        save_df_to_csv(file_name="tg_context.csv", df=edge_df)
        create_relationship(
            source_file="tg_context.csv",
            type_="VALUE",
            between=(("Context", "Context"), ("ENSEMBL", "ENSEMBL")),
            node_types=("Context", "TG"),
            values=values,
            reformat_values=reformat,
            merge=False,
            driver=driver,
        )

    # OR Context Edges
    elif value_type == 0:
        values, reformat = get_values_reformat(df=edge_df, match=["Context", "id"])
        # values = list(set(list(edge_df.columns)) - set(["Context", "id"]))
        # reformat = [
        #     (i, "toFloat" if edge_df[i].dtype == "float64" else "toInteger")
        #     for i in values
        #     if edge_df[i].dtype != "object"
        # ]

        save_df_to_csv(file_name="or_context.csv", df=edge_df)
        create_relationship(
            source_file="or_context.csv",
            type_="VALUE",
            between=(("Context", "Context"), ("id", "id")),
            node_types=("Context", "OR"),
            values=values,
            reformat_values=reformat,
            merge=False,
            driver=driver,
        )


@time_function
def create_correlation(
    correlation: pd.DataFrame, source: int, value_type: int, driver: Driver
):  # value_type: 1 -> TF-TG, 0 -> TG-OR
    """
    Creates CORRELATION Edges between TF / OR and TG from experiment data
    """
    print_update(
        update_type="Edge Creation",
        text="{} CORRELATION".format("TF->TG" if value_type == 1 else "OR->TG"),
        color="cyan",
    )

    correlation["Source"] = source

    # TF-TG edges
    if value_type == 1:
        values, reformat = get_values_reformat(df=correlation, match=["ENSEMBL_TF", "ENSEMBL_TG"])
        # values = list(set(list(correlation.columns)) - set(["ENSEMBL_TF", "ENSEMBL_TG"]))
        # reformat = [
        #     (i, "toFloat" if correlation[i].dtype == "float64" else "toInteger")
        #     for i in values
        #     if correlation[i].dtype != "object"
        # ]

        save_df_to_csv(file_name="tf_tg_corr.csv", df=correlation)
        create_relationship(
            source_file="tf_tg_corr.csv",
            type_="CORRELATION",
            between=(("ENSEMBL", "ENSEMBL_TF"), ("ENSEMBL", "ENSEMBL_TG")),
            node_types=("TF", "TG"),
            values=values,
            reformat_values=reformat,
            merge=False,
            driver=driver,
        )

    # OR-TG edges
    elif value_type == 0:
        values, reformat = get_values_reformat(df=correlation, match=["id", "ENSEMBL"])
        # values = list(set(list(correlation.columns)) - set(["id", "ENSEMBL"]))
        # reformat = [
        #     (i, "toFloat" if correlation[i].dtype == "float64" else "toInteger")
        #     for i in values
        #     if correlation[i].dtype != "object"
        # ]

        save_df_to_csv(file_name="or_tg_corr.csv", df=correlation)
        create_relationship(
            source_file="or_tg_corr.csv",
            type_="CORRELATION",
            between=(("id", "id"), ("ENSEMBL", "ENSEMBL")),
            node_types=("OR", "TG"),
            values=values,
            reformat_values=reformat,
            merge=False,
            driver=driver,
        )


@time_function
def extend_db_from_experiment(
    driver: Driver,
    tg_mean_count: pd.DataFrame | None = None,
    tf_mean_count: pd.DataFrame | None = None,
    or_mean_count: pd.DataFrame | None = None,
    tg_context_values: pd.DataFrame | None = None,
    or_context_values: pd.DataFrame | None = None,
    tf_tg_corr: pd.DataFrame | None = None,
    or_tg_corr: pd.DataFrame | None = None,
):
    """
    Extends Base DB with Data from Experiment
    """

    id_source = create_study_cell_source_meancount(driver=driver)

    if tg_mean_count is not None:
        create_tg_meancount(mean_count=tg_mean_count, source=id_source, driver=driver)
    if tf_mean_count is not None:
        create_tf_meancount(mean_count=tf_mean_count, source=id_source, driver=driver)
    if or_mean_count is not None:
        create_or_meancount(mean_count=or_mean_count, source=id_source, driver=driver)

    if tg_context_values is not None:
        create_context(context=tg_context_values, source=id_source, value_type=1, driver=driver)
    if or_context_values is not None:
        create_context(context=or_context_values, source=id_source, value_type=0, driver=driver)

    if tf_tg_corr is not None:
        create_correlation(correlation=tf_tg_corr, source=id_source, value_type=1, driver=driver)
    if or_tg_corr is not None:
        create_correlation(correlation=or_tg_corr, source=id_source, value_type=0, driver=driver)

    print_update(update_type="Done", text="Extending DB from Experimental Data", color="pink")
    return
