from utils import time_function, execute_query
from neo4j import Driver


@time_function
def create_nodes(
    source_file: str,
    type_: str,
    id: str,
    values: list[str],
    reformat_values: list[tuple[str]],
    driver: Driver,
    species: str,
    merge: bool = True,
):
    """
    Generates and runs Query to upload nodes to the DB. Uses execute_query()

    Input
    - source_file (String): Filename where data is (same as in save_df_to_csv())
    - type_ (String): Type of node (e.g. "TG", "TG:TF", etc.)
    - id (String): unique identifier of node (e.g. "ENSEMBL" for TG nodes)
    - values (List[String]): include all properties without node identifier (e.g. ["SYMBOL", "annotation"])
    - reformat_values (List[Tuple[String]]): Values for be formatted from String to Integer/Float using Cypher functions (computed by get_values_reformat()) e.g. [("Correlation", "toFloat")]
    - species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
    - driver (neo4j Driver): Started Neo4j driver (can be done with start_driver())
    - merge (bool): If True "MERGE" is used, else "CREATE" is used (Default: True)
    """
    # TODO: Use upload functions instead of hardcoding query

    id_str = "{" + "{}: map.{}".format(id, id) + "}"
    load_data_query = "LOAD CSV WITH HEADERS from 'file:///{}' AS map RETURN map".format(source_file)

    comparing_reformat_values = [v[0] for v in reformat_values]
    set_values_query = " ".join(
        [""] + ["SET t.{} = map.{}".format(v, v) for v in values if v not in comparing_reformat_values]
    )
    set_values_query += " ".join(
        [""] + ["SET t.{} = {}(map.{})".format(v[0], v[1], v[0]) for v in reformat_values if v[0] in values]
    )

    if merge:
        into_db_query = "MERGE (t:{}:{} {} ) {}".format(type_, species, id_str, set_values_query)
    else:
        into_db_query = "CREATE (t:{}:{} {} ) {}".format(type_, species, id_str, set_values_query)

    # For large numbers of nodes, using apoc.periodic.iterate
    # For info, see: https://neo4j.com/labs/apoc/4.2/overview/apoc.periodic/apoc.periodic.iterate/

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 500, parallel: true}} )'.format(
        load_data_query, into_db_query
    )

    execute_query(query=per_iter, read=False, driver=driver)
    return


@time_function
def update_nodes(
    source_file: str,
    type_: str,
    id: str,
    values: list[str],
    reformat_values: list[tuple[str]],
    additional_label: str,
    species: str,
    driver: Driver,
):
    """
    Updates properties of nodes, (+ Currently only adds label)

    Variables:
        source_file -> Name of file in neo4j import directory
        type_ -> Type of node (e.g. TG, Context, ...)
        id -> Identifier of node (TG / TF is ENSEMBL, OR is nearest_index)
        reformat_values -> List of Tuples, where 0 -> Name of Value, 1 -> Function to reformat
        additional_label -> Label to be added to nodes
    """

    id_str = "{" + "{}: map.{}".format(id, id) + "}"
    load_data_query = "LOAD CSV WITH HEADERS from 'file:///{}' AS map RETURN map".format(source_file)

    comparing_reformat_values = [v[0] for v in reformat_values]
    set_values_query = " ".join(
        [""] + ["SET t.{} = map.{}".format(v, v) for v in values if v not in comparing_reformat_values]
    )
    set_values_query += " ".join(
        [""] + ["SET t.{} = {}(map.{})".format(v[0], v[1], v[0]) for v in reformat_values if v[0] in values]
    )

    if additional_label != "":
        set_values_query += "SET t:{}".format(additional_label)

    match_db_query = "MATCH (t:{}:{} {} )".format(type_, species, id_str)

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 500, parallel: true}} )'.format(
        load_data_query, match_db_query + " " + set_values_query
    )

    execute_query(query=per_iter, read=False, driver=driver)
    return


@time_function
def create_relationship(
    source_file: str,
    type_: str,
    between: tuple[tuple[str]],
    node_types: tuple[str],
    values: list[str],
    reformat_values: list[tuple[str]],
    species: str,
    driver: Driver,
    merge: bool = True,
    bidirectional: bool = False,
):
    """
    Generates and runs Query to upload edges to the DB. Uses execute_query()

    Input
    - source_file (String): Filename where data is (same as in save_df_to_csv())
    - type_ (String): Edge type (e.g. "CORRELATION")
    - between (Tuple[Tuple[String]]): Node identifiers of nodes between which the edge is to be created Form is ((<Database ID for Node 1>, <Column name in csv for Database ID for Node 1>), (<Database ID for Node 2>, <Column name in csv for Database ID for Node 2>)) (e.g. (("ENSEMBL", "ENSEMBL_TF"), ("ENSEMBL", "ENSEMBL_TG")) from create_correlation())
    - node_types (Tuple[String]): Node types between which the edge is to be created
    - values (List[String]): Values include all properties without node identifiers
    - reformat_values: (List[Tuple[String]]): Values for be formatted from String to Integer/Float using Cypher
    - species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
    - driver (neo4j Driver): Started Neo4j driver (can be done with start_driver())
    - merge (bool): If True "MERGE" is used, else "CREATE" is used (Default: True)
    - bidirectional (bool): If True Query is of form -[]-, else -[]->. Not unidirectionality is highly recommended (Default: False)

    """

    comparing_reformat_values = [v[0] for v in reformat_values]
    m_info = (
        "SET r.m_{} = {}map.{}{}".format(
            between[0][0],
            ""
            if between[0][1] not in comparing_reformat_values
            else reformat_values[comparing_reformat_values.index(between[0][1])][1] + "(",
            between[0][1],
            "" if between[0][1] not in comparing_reformat_values else ")",
        )
        if len(between[0]) == 2
        else ""
    )
    n_info = (
        "SET r.n_{} = {}map.{}{}".format(
            between[1][0],
            ""
            if between[1][1] not in comparing_reformat_values
            else reformat_values[comparing_reformat_values.index(between[1][1])][1] + "(",
            between[1][1],
            "" if between[1][1] not in comparing_reformat_values else ")",
        )
        if len(between[1]) == 2
        else ""
    )

    set_values_query = " ".join(
        [""] + ["SET r.{} = map.{}".format(v, v) for v in values if v not in comparing_reformat_values]
    )
    set_values_query += " ".join(
        [""] + ["SET r.{} = {}(map.{})".format(v[0], v[1], v[0]) for v in reformat_values if v[0] in values]
    )

    load_data_query = "LOAD CSV WITH HEADERS from 'file:///{}' AS map RETURN map".format(
        source_file,
    )

    create_temp_nodes = "CREATE (r:{}_temp) {}".format(type_, set_values_query + " " + m_info + " " + n_info)

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 500, parallel: true}} )'.format(
        load_data_query, create_temp_nodes
    )
    execute_query(query=per_iter, read=False, driver=driver)

    where_query_m = (
        "r.m_{} = m.{}".format(
            between[0][0],
            between[0][0],
        )
        if len(between[0]) == 2
        else ""
    )

    where_query_n = (
        "r.n_{} = n.{}".format(
            between[1][0],
            between[1][0],
        )
        if len(between[1]) == 2
        else ""
    )

    match_nodes = "MATCH (r:{}_temp), (m:{}:{}), (n:{}:{}){}{}{}{} RETURN r, m, n".format(
        type_,
        node_types[0],
        species,
        node_types[1],
        species,
        " WHERE " if where_query_n != "" or where_query_m != "" else "",
        where_query_m,
        " AND " if where_query_n != "" and where_query_m != "" else "",
        where_query_n,
    )

    set_values_query = " ".join([""] + ["SET e.{} = r.{}".format(v, v) for v in values])

    if merge:
        create_edge_query = "MERGE (m)-[e:{}]-{}(n)".format(type_, "" if bidirectional else ">") + set_values_query
    else:
        create_edge_query = "CREATE (m)-[e:{}]->(n)".format(type_) + set_values_query

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 500}} )'.format(match_nodes, create_edge_query)

    execute_query(query=per_iter, read=False, driver=driver)

    match_temp_nodes = "MATCH (r:{}_temp) RETURN r".format(type_)
    delete_temp_nodes = "DELETE r"

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 500, parallel: true}})'.format(
        match_temp_nodes, delete_temp_nodes
    )

    execute_query(query=per_iter, read=False, driver=driver)
    return
