"""
Collection of Cypher queries for writing and reading the resulting
Neo4j graph database.
"""

from typing import Any, Dict, List, Set, Tuple, Union

import neo4j
from util.stopwatch import Stopwatch


def connected_terms(driver: neo4j.Driver, term_ids: list[str], species_id: int):
    """improved version of get_terms_connected_by_overlap
    returns: terms, source, target, score"""
    if species_id == 10090:
        species = "Mus_Musculus"
    elif species_id == 9606:
        species = "Homo_Sapiens"

    query = f"""
        MATCH (source:FT:{species})-[association:OVERLAP]->(target:FT:{species})
        WHERE source.Term IN {term_ids}
            AND target.Term IN {term_ids}
        RETURN source.Term AS source, target.Term AS target, toInteger(round(association.Score,2)*100) AS score;
        """
    with driver.session() as session:
        result = session.run(query).data()
        driver.close()
        return result


def get_terms_connected_by_overlap(driver: neo4j.Driver, term_ids: list[str], species_id: int):
    """:returns: terms, source, target, score"""
    if species_id == 10090:
        species = "Mus_Musculus"
    elif species_id == 9606:
        species = "Homo_Sapiens"

    query = f"""
        MATCH (source:FT:{species})-[association:OVERLAP]->(target:FT:{species})
        WHERE source.Term IN {term_ids}
            AND target.Term IN {term_ids}
        RETURN source, target, association.Score AS score;
        """
    with driver.session() as session:
        result = session.run(query)
        # custom conversion is needed because otherwise it takes 10s with neo4j (for unknown reasons)
        return _convert_to_connection_info_score(result=result, _int=False, protein=False)


def get_protein_ids_for_names(
    driver: neo4j.Driver, names: list[str], species_id: int
) -> Tuple[list, list[str], dict[str, str]]:
    """
    Returns: protein, protein_id and a dictionary of format (Symbol: Alias) of all the symbols found from aliases
    """
    # unsafe parameters because otherwise this query takes 10s with neo4j for unknown reasons
    if species_id == 10090:
        species = "Mus_Musculus"
    elif species_id == 9606:
        species = "Homo_Sapiens"
    names = [i.upper() for i in names]
    query = f"""
        MATCH (n:TG:Mus_Musculus) WHERE n.ALIAS IS NOT NULL
        WITH n, apoc.convert.fromJsonList(n.ALIAS) AS alias_list
        WITH n, [x IN alias_list WHERE x IN {names}] AS matches
        UNWIND matches AS match
        RETURN n.SYMBOL AS symbol, match AS found_alias
    """
    # Retrieve all the symbols that correspond to aliases found in names
    with driver.session() as session:
        result = session.run(query)
        symbols_set, aliases_set, mapping, symbol_alias = _convert_to_symbol_alias(result)
    # To make less calls to the database, remove the aliases and add their corresponding symbol
    genes_set = set(names)
    result_names = list(genes_set - aliases_set) + list(symbols_set - genes_set)

    query = f"""
        MATCH (protein:Protein:{species})
        WHERE protein.SYMBOL IN {result_names}
            OR protein.ENSEMBL_PROTEIN IN {result_names}
        RETURN protein, protein.ENSEMBL_PROTEIN AS id, protein.SYMBOL as symbol
    """
    with driver.session() as session:
        result = session.run(query)
        protein, id = _convert_to_protein_id(result, symbol_alias)
        return protein, id, mapping


def get_protein_neighbours(
    driver: neo4j.Driver, protein_ids: list[str], threshold: int, species_id: int
) -> Tuple[List[str], List[str], List[str], List[Union[int, float]]]:
    """
    :returns: proteins, source_ids, target_ids, scores
    """
    if species_id == 10090:
        species = "Mus_Musculus"
    elif species_id == 9606:
        species = "Homo_Sapiens"

    # unsafe parameters because otherwise this query takes 10s with neo4j for unknown reasons
    query = f"""
        MATCH (source:Protein:{species})-[association:STRING]->(target:Protein:{species})
        WHERE source.ENSEMBL_PROTEIN IN {protein_ids}
            AND target.ENSEMBL_PROTEIN IN {protein_ids}
            AND association.combined >= {threshold}
        RETURN source, target, association.combined AS score
    """

    with driver.session() as session:
        result = session.run(query)
        return _convert_to_connection_info_score(result=result, _int=True, protein=True)


def get_protein_associations(
    driver: neo4j.Driver, protein_ids: list[str], threshold: int, species_id: int
) -> Tuple[List[str], List[str], List[str], List[Union[int, float]]]:
    """
    :returns: proteins (nodes), source_ids, target_ids, score
    """
    if species_id == 10090:
        species = "Mus_Musculus"
    elif species_id == 9606:
        species = "Homo_Sapiens"

    # unsafe parameters are needed because otherwise this query takes 10s with neo4j for unknown reasons
    query = f"""
        MATCH (source:Protein:{species})-[association:STRING]->(target:Protein:{species})
        WHERE source.ENSEMBL_PROTEIN IN {protein_ids}
            AND target.ENSEMBL_PROTEIN IN {protein_ids}
            AND association.Score >= {threshold}
        RETURN source, target, association.Score AS score
    """
    with driver.session() as session:
        result = session.run(query)
        return _convert_to_connection_info_score(result=result, _int=True, protein=True)


def get_enrichment_terms(driver: neo4j.Driver, species_id: int) -> list[dict[str, Any]]:
    if species_id == 10090:
        species = "Mus_Musculus"
    elif species_id == 9606:
        species = "Homo_Sapiens"

    query = f"""
        MATCH (term:FT:{species})
        RETURN term.Term AS id, split(term.Term, "~")[0] as clean, term.Name AS name, term.Category AS category, term.Symbols AS symbols
    """

    with driver.session() as session:
        result = session.run(query).data()
        driver.close()
        return result


def get_number_of_genes(driver: neo4j.Driver, species_id: int) -> int:
    if species_id == 10090:
        species = "Mus_Musculus"
    elif species_id == 9606:
        species = "Homo_Sapiens"

    query = f"""
        MATCH (n:TG:{species})
        RETURN count(n) AS num_genes
    """
    with driver.session() as session:
        result = session.run(query)
        num_genes = result.single(strict=True)["num_genes"]
        driver.close()
        return int(num_genes)


def _convert_to_protein_id(result: neo4j.Result, symbol_alias: dict) -> Tuple[list, list[str]]:
    proteins, ids = list(), list()
    for row in result:
        proteins.append(row["protein"])
        ids.append(row["id"])
    return proteins, ids


def _convert_to_symbol_alias(
    result: neo4j.Result,
) -> Tuple[Set[str], Set[str], Dict[str, str], Dict[str, str]]:
    symbols = set()
    aliases = set()
    symbol_aliases = {}
    mapping = {}
    for row in result:
        symbol = row["symbol"]
        alias = row["found_alias"]
        symbol_aliases[symbol] = row["found_alias"]
        symbols.add(symbol)
        aliases.add(alias)
        # Only add the (symbol: alias) if the symbol isnt there already
        if row["symbol"] not in mapping:
            mapping[symbol] = alias
    return symbols, aliases, mapping, symbol_aliases


def _convert_to_connection_info_score(
    result: neo4j.Result, _int: bool, protein: bool
) -> Tuple[List[str], List[str], List[str], List[Union[int, float]]]:
    nodes: List[str] = []
    source: List[str] = []
    target: List[str] = []
    score: List[Union[int, float]] = []

    for row in result:
        nodes.append(row["source"])
        nodes.append(row["target"])
        if protein:
            source.append(row["source"].get("ENSEMBL_PROTEIN"))
            target.append(row["target"].get("ENSEMBL_PROTEIN"))
        else:
            source.append(row["source"].get("Term"))
            target.append(row["target"].get("Term"))
        if _int:
            score.append(int(row["score"]))
        else:
            score.append(float(row["score"]))

    return nodes, source, target, score


def get_abstracts(driver, species, query: list) -> list:
    neo4j_query = f"""
        MATCH (n:TG:{species})-[:REFERENCES]->(a:abstract)
        WHERE n.SYMBOL in {query}
        WITH percentileCont(a.times_cited, 0.85) AS top_15_threshold, count(a) as total_abstracts

        // Case 1: More than 2000 abstracts are returned. Take the top 15% and limit to 2000 hits
        MATCH (n:TG:{species})-[:REFERENCES]->(a:abstract)
        WHERE total_abstracts >= 2000 AND n.SYMBOL in {query} AND a.times_cited >= top_15_threshold
        RETURN DISTINCT a.PMID AS PMID,
        a.abstract AS abstract,
        a.title AS title,
        a.times_cited AS times_cited,
        a.published AS published,
        a.cited_by AS citations
        ORDER BY a.times_cited DESC LIMIT 2000
        UNION

        // Case 2: Less than 2000 abstracts are returned. Return all abstracts
        MATCH (n:TG:{species})-[:REFERENCES]->(a:abstract)
        WHERE n.SYMBOL in {query}
        WITH count(a) as total_abstracts

        MATCH (n:TG:{species})-[:REFERENCES]->(a:abstract)
        WHERE total_abstracts < 2000 AND n.SYMBOL in {query}
        RETURN DISTINCT a.PMID AS PMID,
        a.abstract AS abstract,
        a.title AS title,
        a.times_cited AS times_cited,
        a.published AS published,
        a.cited_by AS citations
        """
    with driver.session() as session:
        result = session.run(neo4j_query).data()
        driver.close()
        return result


def fetch_vector_embeddings(driver, pmids: list) -> list:
    stopwatch = Stopwatch()
    neo4j_query = f"""
    MATCH (a:abstract) where a.PMID in {pmids}
    RETURN DISTINCT a.PMID as PMID, a.abstractEmbedding as abstractEmbedding
    """
    with driver.session() as session:
        result = session.run(neo4j_query).data()
        driver.close()
        stopwatch.round("Fetching embeddings")
        return result
