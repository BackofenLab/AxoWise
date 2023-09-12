"""
Collection of Cypher queries for writing and reading the resulting
Neo4j graph database.
"""
from typing import Any

import neo4j


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
            AND NOT source.Category IN ["GOCC", "GOMF", "GOBP"]
            AND NOT target.Category IN ["GOCC", "GOMF", "GOBP"]
        RETURN source, target, association.Score AS score;
        """
    with driver.session() as session:
        result = session.run(query)
        # custom conversion is needed because otherwise it takes 10s with neo4j (for unknown reasons)
        return _convert_to_connection_info_score(result=result, _int=False, protein=False)


def get_protein_ids_for_names(driver: neo4j.Driver, names: list[str], species_id: int) -> list[str]:
    # unsafe parameters because otherwise this query takes 10s with neo4j for unknown reasons
    if species_id == 10090:
        species = "Mus_Musculus"
    elif species_id == 9606:
        species = "Homo_Sapiens"

    query = f"""
        MATCH (protein:Protein:{species})
        WHERE protein.SYMBOL IN {str([n.title() for n in names])} 
        WITH collect(protein.ENSEMBL) AS ids
        RETURN ids
    """
    with driver.session() as session:
        return session.run(query).single(strict=True).value()


def get_protein_neighbours(
    driver: neo4j.Driver, protein_ids: list[str], threshold: int, species_id: int
) -> (list[str], list[str], list[str], list[int]):
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
        WHERE source.ENSEMBL IN {protein_ids}
            AND target.ENSEMBL IN {protein_ids}
            AND association.combined >= {threshold}
        RETURN source, target, association.combined AS score
    """

    with driver.session() as session:
        result = session.run(query).single(strict=True).value()
        return _convert_to_connection_info_score(result=result, _int=True, protein=False)


def get_protein_associations(
    driver: neo4j.Driver, protein_ids: list[str], threshold: int, species_id: int
) -> (list[str], list[str], list[str], list[int]):
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
        WHERE source.ENSEMBL IN {protein_ids}
            AND target.ENSEMBL IN {protein_ids}
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
        RETURN term.Term AS id, term.Name AS name, term.Category AS category, term.Proteins AS proteins
    """

    with driver.session() as session:
        result = session.run(query)
        return result.data()


def get_number_of_proteins(driver: neo4j.Driver, species_id: int) -> int:
    if species_id == 10090:
        species = "Mus_Musculus"
    elif species_id == 9606:
        species = "Homo_Sapiens"

    query = f"""
        MATCH (n:Protein:{species})
        RETURN count(n) AS num_proteins
    """
    with driver.session() as session:
        result = session.run(query)
        num_proteins = result.single(strict=True)["num_proteins"]
        return int(num_proteins)


def _convert_to_connection_info_score(result: neo4j.Result, _int: bool, protein:bool) -> (list[str], list[str], list[str], list[int]):
    nodes, source, target, score = list(), list(), list(), list()

    for row in result:
        nodes.append(row["source"])
        nodes.append(row["target"])
        if protein:
            source.append(row["source"].get("ENSEMBL"))
            target.append(row["target"].get("ENSEMBL"))
        else:
            source.append(row["source"].get("Term"))
            target.append(row["target"].get("Term"))
        if _int:
            score.append(int(row["score"]))
        else:
            score.append(float(row["score"]))

    return nodes, source, target, score
