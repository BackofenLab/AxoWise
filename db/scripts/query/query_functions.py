import neo4j
from utils import execute_query, time_function


def get_tg_ensembl_by_symbol(list: list[str], type: str, driver: neo4j.Driver):
    query = f""" 
    MATCH (n:{type})
        WHERE n.SYMBOL IN {list}
    RETURN n.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    return [i[0] for i in result]


def get_tg_by_correlation_tf(tf: str, subset: list[str], positive: bool, threshold: float, driver: neo4j.Driver):
    query = f"""
    MATCH (n:TF)-[c:CORRELATION]->(g:TG)
        WHERE n.ENSEMBL = "{tf}"
            AND g.ENSEMBL IN {subset}
            AND c.Correlation {">" if positive else "<"}= {threshold}
    RETURN g.ENSEMBL, c.Correlation, c.p
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


def get_tg_by_link_ft(ft: str, subset: list[str], driver: neo4j.Driver):
    # TODO: change external_id to Term
    query = f"""
    MATCH (n:FT)<-[:LINK]-(g:TG)
        WHERE n.external_id = "{ft}"
            AND g.ENSEMBL IN {subset}
    RETURN g.ENSEMBL, n.Term
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return [i[0] for i in result]


def get_tg_by_de_under_contexts(
    contexts: list[str], subset: list[str], positive: bool, threshold: float, driver: neo4j.Driver
):
    query = f"""
    MATCH (n:Context)-[d:DE]->(g:TG)
        WHERE n.Context IN {contexts}
            AND g.ENSEMBL IN {subset}
            AND d.Value {">" if positive else "<"}= {threshold}
        RETURN n.Context, d.Value, d.p, g.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


def get_or_by_distance_to_tg(subset: list[str], driver: neo4j.Driver):
    query = f"""
    MATCH (n:OR)-[d:DISTANCE]->(g:TG)
        WHERE g.ENSEMBL IN {subset}
    RETURN n.id, d.Distance, g.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    return result


def get_or_by_motif_to_tf(tf: str, subset: list[str], driver: neo4j.Driver):
    query = f"""
    MATCH (n:TF)-[d:MOTIF]->(m:OR)
        WHERE n.ENSEMBL = "{tf}"
            AND m.id IN {subset}
        RETURN n.ENSEMBL, d.Motif, m.id
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


def get_or_by_da_under_contexts(
    contexts: list[str], subset: list[str], positive: bool, threshold: float, driver: neo4j.Driver
):
    query = f"""
    MATCH (n:Context)-[d:DA]->(m:OR)
        WHERE n.Context IN {contexts}
            AND m.id IN {subset}
            AND d.Value {">" if positive else "<"}= {threshold}
        RETURN n.Context, d.Value, d.p, m.id
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


@time_function
def query_1(list: list[str], threshold: float, driver: neo4j.Driver):
    query = f"""
    MATCH (n:TF:Mus_Musculus)-[:MOTIF]->(:OR:Mus_Musculus)-[c:CORRELATION]->(m:TG:Mus_Musculus)
        WHERE n.ENSEMBL IN {list}
            AND c.Correlation >= {threshold}
        RETURN n.ENSEMBL, m.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    return result


@time_function
def query_2(list: list[str], threshold: float, driver: neo4j.Driver):
    query = f"""
    MATCH (n:TF:Mus_Musculus)-[c:CORRELATION]->(m:TG:Mus_Musculus)
        WHERE n.ENSEMBL IN {list}
            AND c.Correlation >= {threshold}
    RETURN n.ENSEMBL, m.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


@time_function
def query_3(list: list[str], threshold: float, driver: neo4j.Driver):
    query = f"""
    MATCH (n:OR:Mus_Musculus)-[c:CORRELATION]->(m:TG:Mus_Musculus)
        WHERE n.id IN {list}
            AND c.Correlation >= {threshold}
    RETURN n.id, m.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


@time_function
def query_4(list: list[str], driver: neo4j.Driver):
    query = f"""
    MATCH (s:Source:Mus_Musculus)-[:HAS]->(c:Context:Mus_Musculus)-[v:VALUE]->(m:TG:Mus_Musculus)
        WHERE s.id IN {list}
    RETURN s.id, c.Context, v.Value, m.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


@time_function
def query_5(list: list[str], driver: neo4j.Driver):
    query = f"""
    MATCH (s:Source:Mus_Musculus)-[:HAS]->(c:Context:Mus_Musculus)-[v:VALUE]->(m:OR:Mus_Musculus)
        WHERE s.id IN {list}
    RETURN s.id, c.Context, v.Value, m.id
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


@time_function
def query_6(list: list[str], driver: neo4j.Driver):
    query = f"""
    MATCH (s:Celltype:Mus_Musculus)-[:HAS|IS*]->(:Source:Mus_Musculus)-[:HAS]->(t:Context:Mus_Musculus)-[v:VALUE]->(m:OR:Mus_Musculus)
        WHERE s.name IN {list}
    RETURN s.name, t.Context, v.Value, m.id
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


@time_function
def query_7(list: list[str], threshold: float, driver: neo4j.Driver):
    query = f"""
    MATCH (n:TF:Mus_Musculus)-[c:CORRELATION]->(m:TG:Mus_Musculus)
        WHERE m.ENSEMBL IN {list}
            AND c.Correlation >= {threshold}
    RETURN n.ENSEMBL, m.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


@time_function
def query_8(list: list[str], threshold: float, driver: neo4j.Driver):
    query = f"""
    MATCH (n:OR:Mus_Musculus)-[c:CORRELATION]->(m:TG:Mus_Musculus)
        WHERE m.ENSEMBL IN {list}
            AND c.Correlation >= {threshold}
    RETURN n.id, m.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    return result


# ---------------------- NOT FOR PRODUCTION ----------------------
# Used by Christina to get TGs correlated with list of TFs
def get_tf_correlated_tg(tf: str, subset: list[str], driver: neo4j.Driver):
    query = f"""
    MATCH (n:TF)-[c:CORRELATION]->(g:TG)
        WHERE n.ENSEMBL = "{tf}"
            AND g.ENSEMBL IN {subset}
    RETURN n.SYMBOL, g.SYMBOL, c.Correlation, c.p
    """
    result = execute_query(query=query, read=True, driver=driver)
    return result
