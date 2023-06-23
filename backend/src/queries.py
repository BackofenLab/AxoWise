"""
Collection of Cypher queries for writing and reading the resulting
Neo4j graph database.
"""
from typing import Any

import neo4j
import numpy as np


def get_terms_connected_by_kappa(driver: neo4j.Driver, term_ids: list[str]):
    """:returns: terms, source, target, score"""
    parameters = {
        "term_ids": term_ids
    }
    query = f"""
        MATCH (source:Terms)-[association:KAPPA]->(target:Terms)
        WHERE source.external_id IN {term_ids} 
            AND target.external_id IN {term_ids}
        WITH 
            collect(source) + collect(target) as terms_all,
            collect(source.external_id) as term_ids_source, 
            collect(target.external_id) as term_ids_target, 
            collect(association.score) as association_scores
        RETURN {{
            terms: terms_all,
            source_ids: term_ids_source,
            target_ids: term_ids_target,
            scores: association_scores
        }};
        """
    with driver.session() as session:
        result = session.run(query, parameters).single(strict=True).value()
        scores = np.array(result["scores"], dtype=np.float32)  # floats are not converted automatically
        return result["terms"], result["source_ids"], result["target_ids"], scores


def get_protein_ids_for_names(driver: neo4j.Driver, names: list[str], species_id: int) -> list[str]:
    parameters = {
        "species_id": species_id,
        "names": [n.upper() for n in names]
    }
    query = f"""
        MATCH (protein:Protein)
        WHERE protein.species_id = $species_id
            AND protein.name IN {parameters["names"]} 
        WITH collect(protein.external_id) AS ids
        RETURN ids
    """
    with driver.session() as session:
        return session.run(query, parameters).single(strict=True).value()


def get_protein_neighbours(
        driver: neo4j.Driver, protein_ids: list[str], threshold: int
) -> (list[str], list[str], list[str], list[int]):
    """
    :returns: proteins, source_ids, target_ids, scores
    """
    parameters = {
        "protein_ids": protein_ids,
        "threshold": threshold
    }
    query = f"""
        MATCH (source:Protein)-[association:ASSOCIATION]-(target:Protein)
        WHERE source.external_id IN {parameters["protein_ids"]}
            OR target.external_id IN {parameters["protein_ids"]}
            AND association.combined >= $threshold
        WITH 
            collect(source) + collect(target) as proteins_all,
            collect(source.external_id) as protein_ids_source, 
            collect(target.external_id) as protein_ids_target, 
            collect(association.combined) as association_scores
        RETURN {{
            proteins: proteins_all,
            source_ids: protein_ids_source,
            target_ids: protein_ids_target,
            scores: association_scores
        }}
    """
    with driver.session() as session:
        result = session.run(query, parameters).single(strict=True).value()
        return result["proteins"], result["source_ids"], result["target_ids"], result["scores"]


def get_protein_associations(
        driver: neo4j.Driver, protein_ids: list[str], threshold: int
) -> (list[str], list[str], list[str], list[int]):
    """
    :returns: proteins (nodes), source_ids, target_ids, score
    """
    parameters = {
        "protein_ids": protein_ids,
        "threshold": threshold
    }
    query = f"""
        MATCH (source:Protein)-[association:ASSOCIATION]->(target:Protein)
        WHERE source.external_id IN {parameters["protein_ids"]}
            AND target.external_id IN {parameters["protein_ids"]}
            AND association.combined >= $threshold
        WITH 
            collect(source) + collect(target) as proteins_all,
            collect(source.external_id) as protein_ids_source, 
            collect(target.external_id) as protein_ids_target, 
            collect(association.combined) as association_scores
        RETURN {{
            proteins: proteins_all,
            source_ids: protein_ids_source,
            target_ids: protein_ids_target,
            scores: association_scores
        }}
    """
    with driver.session() as session:
        result = session.run(query, parameters).single(strict=True).value()
        return result["proteins"], result["source_ids"], result["target_ids"], result["scores"]


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
