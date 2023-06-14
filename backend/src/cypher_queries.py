"""
Collection of Cypher queries for writing and reading the resulting
Neo4j graph database.
"""
from typing import List, Any

import neo4j


def get_protein_list(graph):
    """
    Retrieve a list of proteins including the protein ID
    and the protein name.
    """

    query = """
        MATCH (protein:Protein)
        RETURN protein.external_id AS id,
               protein.name AS name,
               protein.species_id AS species_id
    """

    return graph.run(query)


def get_enrichment_terms(driver: neo4j.Driver) -> list[dict[str, Any]]:
    query = """
        MATCH (term:Terms)
        RETURN term.external_id AS id, term.name AS name, term.category AS category, term.proteins AS proteins
    """

    with driver.session() as session:
        result = session.run(query)
        return _convert_to_dict(result)


def get_number_of_proteins(driver: neo4j.Driver) -> int:
    query = """
        MATCH (n:Protein)
        RETURN count(n) AS num_proteins
    """
    with driver.session() as session:
        result = session.run(query)
        num_proteins = result.single(strict=True)["num_proteins"]
        return int(num_proteins)


def _convert_to_dict(result: neo4j.Result) -> list[dict[str, Any]]:
    records: List[neo4j.Record] = list(result)
    return [x.data() for x in records]

