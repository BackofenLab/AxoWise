import pandas as pd
from numpy import isnan
from numpy import isnan
from utils import execute_query


def create_study_cell_source_meancount():
def create_study_cell_source_meancount():
    create_study_query = "MERGE (s:Study {number: 1})"
    create_celltype_query = "MERGE (c:Celltype {number: 1})"
    create_source_query = "MERGE (s)-[:HAS]->(o:Source)<-[:HAS]-(c)"
    create_meancount = "MERGE (m:MeanCount)"
    return_ids = "RETURN id(o) AS id_source"

    query = (
        create_study_query
        + " "
        + create_celltype_query
        + " "
        + create_source_query
        + " "
        + create_meancount
        + " "
        + return_ids
    )
    result, summary, _ = execute_query(query=query, read=False)
    return result[0]["id_source"]


def create_nodes(source_file: str, type_: str, id: str):
    # Identifier; For TG / TF is ENSEMBL, OR is SYMBOL
    id_str = "{" + "{}: map.{}".format(id, id) + "}"
    load_data_query = 'LOAD CSV WITH HEADERS from "file:///{}" AS map RETURN map'.format(source_file)
    merge_into_db_query = "MERGE (t:{} {} ) SET t = map".format(type_, id_str)

    # For large numbers of nodes, using apoc.periodic.iterate
    # For info, see: https://neo4j.com/labs/apoc/4.2/overview/apoc.periodic/apoc.periodic.iterate/

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 5000}} )'.format(
        load_data_query, merge_into_db_query
    )

    execute_query(query=per_iter, read=False)
    create_meancount = "MERGE (m:MeanCount)"
    return_ids = "RETURN id(o) AS id_source"

    query = create_study_query + " " + create_celltype_query + " " + create_source_query + " " + create_meancount + " " + return_ids
    result, summary, _ = execute_query(query=query, read=False)
    return result[0]["id_source"]


def create_nodes(source_file:str, type_: str, id:str):
    
    # Identifier; For TG / TF is ENSEMBL, OR is SYMBOL
    id_str = '{' + '{}: map.{}'.format(id, id) + '}'
    load_data_query = 'LOAD CSV WITH HEADERS from "file:///{}" AS map RETURN map'.format(source_file)
    merge_into_db_query = 'MERGE (t:{} {} ) SET t = map'.format(type_, id_str)
    
    # For large numbers of nodes, using apoc.periodic.iterate
    # For info, see: https://neo4j.com/labs/apoc/4.2/overview/apoc.periodic/apoc.periodic.iterate/

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 5000}} )'.format(load_data_query, merge_into_db_query)
    
    execute_query(query=per_iter, read=False)
    return


def create_relationship():
    # TODO: Maybe with trick of generating nodes first, then relationships? Could also do apoc periodic iterate, more clear
    pass


def get_node(by_value: str):
    # TODO: DO we need this? Could just do the matching in create_relationship()
    pass


def create_tg_nodes(nodes: pd.DataFrame):
    print("Creating Target Gene nodes...")
    nodes.to_csv("/usr/local/bin/neo4j/import/tg.csv", index=False)
    create_nodes(source_file="tg.csv", type_="TG", id="ENSEMBL")


def create_tf_nodes(nodes: pd.DataFrame):
    print("Creating Transcription Factor nodes ...")
    # create new Transcription Factor node for every new TF
    nodes.to_csv("/usr/local/bin/neo4j/import/tf.csv", index=False)
    create_nodes(source_file="tf.csv", type_="TF", id="ENSEMBL")


def create_or_nodes(nodes: pd.DataFrame):
    print("Creating Open Region nodes ...")
    # create new Open Region node for every new OR
    nodes.to_csv("/usr/local/bin/neo4j/import/or.csv", index=False)
    create_nodes(source_file="or.csv", type_="OR", id="SYMBOL")


def create_context(context: pd.DataFrame, source: int):
    print("Creating Context nodes ...")

    # create Context node for every new context
    nodes = context["Context"].unique()
    node_df = pd.DataFrame.from_records(data=[{"value": c} for c in nodes])
    print(node_df)

    # node_df.to_csv("/usr/local/bin/neo4j/import/context.csv", index=False)
    # create_nodes(source_file="context.csv", type_="Context", id="value")

    # Create edges for DE/DA values
    create_relationship()


def extend_db_from_experiment(
    tg_nodes: pd.DataFrame,
    tf_nodes: pd.DataFrame,
    or_nodes: pd.DataFrame,
    de_values: pd.DataFrame,
    da_values: pd.DataFrame,
):
    id_source = create_study_cell_source_meancount()
    # create_tg_nodes(nodes=tg_nodes)
    # create_tf_nodes(nodes=tf_nodes)
    # create_or_nodes(nodes=or_nodes)
    create_context(context=de_values, source=id_source)
    create_context(context=da_values, source=id_source)
    return

