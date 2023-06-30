import pandas as pd
import neo4j
import pprint
from utils import start_driver, stop_driver, execute_query, generate_props

def match_edge(
    node_types: tuple[str],
    node_props: tuple[list[tuple[str]]],
    edge_type: str,
    edge_props: tuple[str],
    reformat_values: dict[str],
    bidirectional: bool = False,
    node_ids:tuple[str] = ["", ""],
    edge_id:str = ""
):
    source_type, target_type = node_types
    source_props, target_props = node_props
    source_id, target_id = node_ids

    arrow = "" if bidirectional else ">"
    edge_type = ":" + edge_type if len(edge_type) else ""
    source_type = ":" + source_type if len(source_type) else ""
    target_type = ":" + target_type if len(target_type) else ""

    generate_query = f"MATCH (n{source_id}{source_type})-[e{edge_id}{edge_type}]-{arrow}(m{target_id}{target_type}) "

    props_query, where = generate_props(source=source_props, item=f"n{source_id}", reformat_values=reformat_values, where=True)
    generate_query += props_query
    props_query, where = generate_props(source=target_props, item=f"m{target_id}", reformat_values=reformat_values, where=where)
    generate_query += props_query
    props_query, where = generate_props(source=edge_props, item=f"e{edge_id}", reformat_values=reformat_values, where=where)
    generate_query += props_query
    return generate_query

def get_edges(
    node_types: tuple[str],
    node_props: tuple[list[tuple[str]]],
    edge_type: str,
    edge_props: tuple[str],
    reformat_values: dict[str],
    driver: neo4j.Driver,
    bidirectional: bool = False,
):
    generate_query = match_edge(
        node_types=node_types, 
        node_props=node_props, 
        edge_type=edge_type, 
        edge_props=edge_props, 
        reformat_values=reformat_values,
        bidirectional=bidirectional
    )
    generate_query += "RETURN e"

    return execute_query(query=generate_query, driver=driver, read=True)

def get_nodes(
    type_: str,
    props: tuple[str],
    reformat_values: list[tuple[str]],
    driver: neo4j.Driver,   
):
    query = f"MATCH (n:{type_}) "
    props = generate_props(source=props, item="n", reformat_values=reformat_values, where=True)
    where = len(props) > 0
    query += "WHERE " if where else ""
    query += props
    query += "RETURN n"
    return execute_query(query=query, read=True, driver=driver)

def get_connected_nodes(
    node_types: tuple[str],
    node_props: tuple[list[tuple[str]]],
    edge_type: str,
    edge_props: tuple[str],
    reformat_values: dict[str],
    driver: neo4j.Driver,
    bidirectional: bool = False,
):

    generate_query = match_edge(
        node_types=node_types, 
        node_props=node_props, 
        edge_type=edge_type, 
        edge_props=edge_props, 
        reformat_values=reformat_values,
        bidirectional=bidirectional
    )
    generate_query += "RETURN m"
    
    return execute_query(query=generate_query, read=True, driver=driver)

def get_correlated_tf_tg(itemset:list[str], limit:float, driver:neo4j.Driver, mode:tuple[bool] = (True, True, True)):
    both, pos, neg = mode
    generated_query_both = ""
    generated_query_pos = ""
    generated_query_neg = ""
    for index, symbol in enumerate(itemset):
        if index == 0:
            generated_query_both += match_edge(
                node_types=("TF", "TG"), 
                node_props=({"AND": [("SYMBOL", symbol, "=")]}, dict()), 
                edge_type="CORRELATION", 
                edge_props={"OR": [("Correlation", limit, ">="), ("Correlation", -limit, "<=")]}, 
                reformat_values={"SYMBOL": ("'", "'")},
                bidirectional=False,
                node_ids=(str(index), ""), 
                edge_id=str(index)
            )
            generated_query_pos += match_edge(
                node_types=("TF", "TG"), 
                node_props=({"AND": [("SYMBOL", symbol, "=")]}, dict()), 
                edge_type="CORRELATION", 
                edge_props={"AND": [("Correlation", limit, ">=")]}, 
                reformat_values={"SYMBOL": ("'", "'")},
                bidirectional=False,
                node_ids=(str(index), ""), 
                edge_id=str(index)
            )
            generated_query_neg += match_edge(
                node_types=("TF", "TG"), 
                node_props=({"AND": [("SYMBOL", symbol, "=")]}, dict()), 
                edge_type="CORRELATION", 
                edge_props={"AND": [("Correlation", -limit, "<=")]}, 
                reformat_values={"SYMBOL": ("'", "'")},
                bidirectional=False,
                node_ids=(str(index), ""), 
                edge_id=str(index)
            )
        else:
            generated_query_both += match_edge(
                node_types=("TF", ""), 
                node_props=({"AND": [("SYMBOL", symbol, "=")]}, dict()), 
                edge_type="CORRELATION", 
                edge_props={"OR": [("Correlation", limit, ">="), ("Correlation", -limit, "<=")]}, 
                reformat_values={"SYMBOL": ("'", "'")},
                bidirectional=False,
                node_ids=(str(index), ""), 
                edge_id=str(index)
            )
            generated_query_pos += match_edge(
                node_types=("TF", ""), 
                node_props=({"AND": [("SYMBOL", symbol, "=")]}, dict()), 
                edge_type="CORRELATION", 
                edge_props={"AND": [("Correlation", limit, ">=")]}, 
                reformat_values={"SYMBOL": ("'", "'")},
                bidirectional=False,
                node_ids=(str(index), ""), 
                edge_id=str(index)
            )
            generated_query_neg += match_edge(
                node_types=("TF", ""), 
                node_props=({"AND": [("SYMBOL", symbol, "=")]}, dict()), 
                edge_type="CORRELATION", 
                edge_props={"AND": [("Correlation", -limit, "<=")]}, 
                reformat_values={"SYMBOL": ("'", "'")},
                bidirectional=False,
                node_ids=(str(index), ""), 
                edge_id=str(index)
            )
    generated_query_both += " RETURN m.ENSEMBL as ensembl"
    generated_query_pos += " RETURN m.ENSEMBL as ensembl"
    generated_query_neg += " RETURN m.ENSEMBL as ensembl"

    if both:
        query_df_both = execute_query(generated_query_both, read=True, driver=driver)
    else:
        query_df_both = None
    if pos:
        query_df_pos = execute_query(generated_query_pos, read=True, driver=driver)
    else:
        query_df_pos = None
    if neg:
        query_df_neg = execute_query(generated_query_neg, read=True, driver=driver)
    else:
        query_df_neg = None
    return query_df_both, query_df_pos, query_df_neg


def check_for_similarily_correlated(df: pd.DataFrame, driver: neo4j.Driver):
    symbols = [i.split(", ") for i in df["itemset"]]
    lst = []
    for i in symbols:
        lst.append([i, get_correlated_tf_tg(itemset=i, limit=0.75, driver=driver, mode=(True, True, True))])
    return lst

def test():
    driver = start_driver()
    df = pd.read_csv("../source/christina/TF_rules.csv")
    pprint(check_for_similarily_correlated(df=df, driver=driver))

    # print(
    #     get_connected_nodes(
    #     node_types=("TF", "TG"), 
    #     node_props=({"AND": [("SYMBOL", "Klf6", "=")]}, dict()), 
    #     edge_type="CORRELATION", 
    #     reformat_values={"SYMBOL": ("'", "'")},
    #     edge_props={"OR": [("Correlation", "0.75", ">=")]}, 
    #     driver=driver
    # ))

    # print(
    #     get_edges(
    #     node_types=("TF", "TG"), 
    #     node_props=({"AND": [("SYMBOL", "Klf6", "=")]}, dict()), 
    #     edge_type="CORRELATION", 
    #     reformat_values={"SYMBOL": ("'", "'")},
    #     edge_props={"OR": [("Correlation", "0.75", ">=")]}, 
    #     driver=driver
    # ))
    stop_driver(driver=driver)
