import neo4j
from utils import execute_query


def get_tg_ensembl_by_symbol(gene_list: list[str], driver: neo4j.Driver):
    query = f""" 
    MATCH (n:TG)
        WHERE n.SYMBOL IN {gene_list}
    RETURN n.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    pass


def get_tg_by_correlation_tfs(tf: str, subset: list[str], positive: bool, threshold: float, driver: neo4j.Driver):
    query = f"""
    MATCH (n:TF)-[c:CORRELATION]->(g:TG)
        WHERE n.ENSEMBL = {tf}
            AND g.ENSEMBL IN {subset}
            AND c.Correlation {">" if positive else "<"}= {threshold}
    RETURN g.ENSEMBL, c.Correlation, c.p
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    pass


def get_tg_by_link_ft(ft: str, subset: list[str], driver: neo4j.Driver):
    query = f"""
    MATCH (n:FT)-[:LINK]->(g:TG)
        WHERE n.Term = {ft}
            AND g.ENSEMBL IN {subset}
    RETURN g.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    pass


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
    pass


def get_or_by_distance_to_tg(subset: list[str], driver: neo4j.Driver):
    query = f"""
    MATCH (n:OR)-[d:DISTANCE]->(g:TG)
        WHERE g.ENSEMBL IN {subset}
    RETURN n, d.Distance, g.ENSEMBL
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    pass


def get_or_by_motif_to_tf(tf: str, subset: list[str], driver: neo4j.Driver):
    query = f"""
    MATCH (n:TF)-[d:MOTIF]->(m:OR)
        WHERE n.ENSEMBL = {tf}
            AND m.id IN {subset}
        RETURN n.ENSEMBL, d.Motif, m.id
    """
    result = execute_query(query=query, read=True, driver=driver)
    # TODO
    pass


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
    pass
