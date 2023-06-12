import pandas as pd
from json import dumps
from utils import execute_query


def create_study_cell_source():
    create_study_query = "MERGE (s:Study {number: 1})"
    create_celltype_query = "MERGE (c:Celltype {number: 1})"
    create_source_query = "MERGE (s)-[:HAS]->(o:Source)<-[:HAS]-(c)"
    return_ids = "RETURN id(s), id(c), id(o)"

    query = create_study_query + " " + create_celltype_query + " " + create_source_query + " " + return_ids
    print(query)
    execute_query(query=query, read=False)
    return


def create_nodes(nodes: pd.DataFrame, type: str):
    node_dict = nodes.to_dict("records")
    for node in node_dict:
        print(node)
        # TODO: Keys to non-strings
        query = "MERGE (n:{} {})".format(type, dumps(node))
        print(query)
        execute_query(query=query, read=False)
        return
    return


def create_tg_nodes(nodes: pd.DataFrame):
    create_nodes(nodes=nodes, type="TG")


def create_tf_nodes(nodes: pd.DataFrame):
    create_nodes(nodes=nodes, type="TF")


def create_or_nodes(nodes: pd.DataFrame):
    create_nodes(nodes=nodes, type="OR")


def extend_db_from_experiment(tg_nodes: pd.DataFrame, tf_nodes: pd.DataFrame, or_nodes: pd.DataFrame):
    create_study_cell_source()
    create_tg_nodes(nodes=tg_nodes)
    create_tf_nodes(nodes=tf_nodes)
    create_or_nodes(nodes=or_nodes)
    return
