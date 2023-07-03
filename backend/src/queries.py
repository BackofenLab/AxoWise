"""
Collection of Cypher queries for writing and reading the resulting
Neo4j graph database.
"""
from typing import Any

import neo4j


def get_terms_connected_by_kappa(driver: neo4j.Driver, term_ids: list[str]):
    """:returns: terms, source, target, score"""
    query = f"""
        MATCH (source:Terms)-[association:KAPPA]->(target:Terms)
        WHERE source.external_id IN {term_ids}
        AND target.external_id IN {term_ids}
        RETURN source, target, association.score AS score;
        """
    with driver.session() as session:
        result = session.run(query)
        # custom conversion is needed because otherwise it takes 10s with neo4j (for unknown reasons)
        return _convert_to_connection_info_score(result=result, _int=False)


def get_protein_ids_for_names(driver: neo4j.Driver, names: list[str], species_id: int) -> list[str]:
    # unsafe parameters because otherwise this query takes 10s with neo4j for unknown reasons
    query = f"""
        MATCH (protein:Protein)
        WHERE protein.species_id = {species_id}
            AND protein.name IN {str([n.upper() for n in names])} 
        WITH collect(protein.external_id) AS ids
        RETURN ids
    """
    with driver.session() as session:
        return session.run(query).single(strict=True).value()


def get_protein_neighbours(
    driver: neo4j.Driver, protein_ids: list[str], threshold: int
) -> (list[str], list[str], list[str], list[int]):
    """
    :returns: proteins, source_ids, target_ids, scores
    """
    # unsafe parameters because otherwise this query takes 10s with neo4j for unknown reasons
    query = f"""
        MATCH (source:Protein)-[association:ASSOCIATION]->(target:Protein)
        WHERE source.external_id IN {protein_ids}
            AND target.external_id IN {protein_ids}
            AND association.combined >= {threshold}
        RETURN source, target, association.combined AS score
    """

    with driver.session() as session:
        result = session.run(query).single(strict=True).value()
        return _convert_to_connection_info_score(result=result, _int=True)


def get_protein_associations(
    driver: neo4j.Driver, protein_ids: list[str], threshold: int
) -> (list[str], list[str], list[str], list[int]):
    """
    :returns: proteins (nodes), source_ids, target_ids, score
    """
    # unsafe parameters are needed because otherwise this query takes 10s with neo4j for unknown reasons
    query = f"""
        MATCH (source:Protein)-[association:ASSOCIATION]->(target:Protein)
        WHERE source.external_id IN {protein_ids}
            AND target.external_id IN {protein_ids}
            AND association.combined >= {threshold}
        RETURN source, target, association.combined AS score
    """
    with driver.session() as session:
        result = session.run(query)
        return _convert_to_connection_info_score(result=result, _int=True)


def get_enrichment_terms(driver: neo4j.Driver) -> list[dict[str, Any]]:
    query = """
        MATCH (term:Terms)
        RETURN term.external_id AS id, term.name AS name, term.category AS category, term.proteins AS proteins
    """

    with driver.session() as session:
        result = session.run(query)
        return result.data()


def get_number_of_proteins(driver: neo4j.Driver) -> int:
    query = """
        MATCH (n:Protein)
        RETURN count(n) AS num_proteins
    """
    with driver.session() as session:
        result = session.run(query)
        num_proteins = result.single(strict=True)["num_proteins"]
        return int(num_proteins)


def _convert_to_connection_info_score(result: neo4j.Result, _int:bool) -> (list[str], list[str], list[str], list[int]):
    nodes, source, target, score = list(), list(), list(), list()

    for row in result:
        nodes.append(row["source"])
        nodes.append(row["target"])
        source.append(row["source"].get("external_id"))
        target.append(row["target"].get("external_id"))
        if _int: 
            score.append(int(row["score"]))
        else:
            score.append(float(row["score"]))

    return nodes, source, target, score
