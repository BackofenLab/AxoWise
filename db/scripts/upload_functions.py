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
    merge: bool = True,
):
    """
    Common function to create nodes in the Neo4j Database (MERGE not CREATE)

    Variables:
        source_file -> Name of file in neo4j import directory
        type_ -> Type of node (e.g. TG, Context, ...)
        id -> Identifier of node (TG / TF is ENSEMBL, OR is nearest_index)
        reformat_values -> List of Tuples, where 0 -> Name of Value, 1 -> Function to reformat
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

    if merge:
        into_db_query = "MERGE (t:{} {} ) {}".format(type_, id_str, set_values_query)
    else:
        into_db_query = "CREATE (t:{} {} ) {}".format(type_, id_str, set_values_query)

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

    match_db_query = "MATCH (t:{} {} )".format(type_, id_str)

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 500, parallel: true}} )'.format(
        load_data_query, match_db_query + " " + set_values_query
    )

    execute_query(query=per_iter, read=False, driver=driver)
    pass


@time_function
def create_relationship(
    source_file: str,
    type_: str,
    between: tuple[str],
    node_types: tuple[str],
    values: list[str],
    reformat_values: list[tuple[str]],
    driver: Driver,
    merge: bool = True,
    bidirectional: bool = False,
):
    """
    Common function to create edges in Neo4j Database (both MERGE and CREATE possible, see merge flag)

    Variables:
        source_file -> Name of file in neo4j import directory
        type_ -> Type of relationship (e.g. HAS, DE, ...)
        between -> Comparing value names (0 -> Origin of relationship, 1 -> Destination of relationship; x.0 -> Value in DB, x.1 Value in CSV
        node_types -> Nodetypes (0 -> Origin of relationship, 1 -> Destination of relationship)
        values -> Column names in csv that need to be added as properties
        reformat_values -> List of Tuples, where 0 -> Name of Value, 1 -> Function to reformat
        merge -> Use CREATE or MERGE
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

    match_nodes = "MATCH (r:{}_temp), (m:{}), (n:{}){}{}{}{} RETURN r, m, n".format(
        type_,
        node_types[0],
        node_types[1],
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

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 500, parallel: true}} )'.format(
        match_nodes, create_edge_query
    )

    execute_query(query=per_iter, read=False, driver=driver)

    match_temp_nodes = "MATCH (r:{}_temp) RETURN r".format(type_)
    delete_temp_nodes = "DELETE r"

    per_iter = 'CALL apoc.periodic.iterate("{}", "{}", {{batchSize: 500, parallel: true}} )'.format(
        match_temp_nodes, delete_temp_nodes
    )

    execute_query(query=per_iter, read=False, driver=driver)

    return
