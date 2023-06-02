"""
Collection of Cypher queries for writing and reading the resulting
Neo4j graph database.
"""

# ========================= Creating queries =========================

from utils import batches
from ast import literal_eval
import uuid
import subprocess

TERM_FILE = uuid.uuid4()


def add_compound(graph, params):
    """
    Create a compound with the specified id and
    name.
    """

    query = """
        UNWIND $batch as entry
        MERGE (compound:Compound {
            id: entry.id,
            name: entry.name
        })
    """
    graph.run(query, params)


def add_disease(graph, params):
    """
    Create a disease with the specified id and
    name.
    """

    query = """
        UNWIND $batch as entry
        MERGE (disease:Disease {
            id: entry.id,
            name: entry.name
        })
    """
    graph.run(query, params)


def add_drug(graph, params):
    """
    Create a drug with the specified id and
    name.
    """

    query = """
        UNWIND $batch as entry
        MERGE (drug:Drug {
            id: entry.id,
            name: entry.name
        })
    """
    graph.run(query, params)


def add_class_parent_and_child(graph, params):
    """
    Create parent - child relationship between
    two pathway classes.
    """

    query = """
        UNWIND $batch as entry
        MERGE (parent:Class {
            name: entry.name_parent
        })
        MERGE (child:Class {
            name: entry.name_child
        })
        MERGE (child)-[:IN]->(parent)
    """
    graph.run(query, params)


def add_pathway(graph, params):
    """
    Create a pathway with the specified id, name,
    description and species to which it belongs.
    After that, connect it to the corresponding class.
    """

    query = """
        UNWIND $batch as entry
        MATCH (class:Class {
            name: entry.class
        })
        CREATE (pathway:Pathway {
            id: entry.id,
            name: entry.name,
            description: entry.description,
            species_id: entry.species_id
        })-[:IN]->(class)
    """

    graph.run(query, params)


def add_protein(graph, params):
    """
    Create a protein with the specified id, external id,
    name, description and species to which it belongs.
    """

    query = """
        UNWIND $batch as entry
        CREATE (protein:Protein {
            external_id: entry.external_id,
            name: toUpper(entry.preferred_name),
            description: entry.annotation,
            species_id: entry.species_id
        })
    """
    graph.run(query, params)


def add_action(graph, params):
    """
    For an existing protein - protein pair, create / update (merge) the given
    action associated with the given pathway.

    If the action's "mode" is the same, the action is updated only if the current
    provided score is higher than the previous.
    """

    query = """
        UNWIND $batch as entry
        MATCH (protein1:Protein {
            id: entry.id1
        })

        MATCH (protein2:Protein {
            id: entry.id2
        })

        MERGE (protein1)-[action:ACTION {
            mode: entry.mode
        }]->(protein2)
            ON CREATE SET action.score = entry.score
            ON MATCH SET action.score = CASE action.score
                                       WHEN entry.score > action.score
                                       THEN action.score = entry.score
                                       ELSE action.score
                                       END
    """
    graph.run(query, params)


def add_association(graph, params):
    """
    For an existing protein - protein pair, create the association
    between them.
    """

    query = """
        UNWIND $batch as entry

        MATCH (protein1:Protein {
            external_id: entry.id1
        })

        MATCH (protein2:Protein {
            external_id: entry.id2
        })

        CREATE (protein1)-[a:ASSOCIATION {
            combined: entry.combined_score
        }]->(protein2)
    """
    graph.run(query, params)


# ========================= Connecting queries =========================


def connect_protein_and_pathway(graph, params):
    """
    Creates IN association for the given protein and
    pathway.
    """

    query = """
        UNWIND $batch as entry

        MATCH (protein:Protein {
            external_id: entry.protein_external_id
        })

        MATCH(pathway:Pathway {
            id: entry.pathway_id
        })

        CREATE (protein)-[:IN]->(pathway)
    """
    graph.run(query, params)


def connect_compound_and_pathway(graph, params):
    """
    Creates IN association for the given compound and
    pathway.
    """

    query = """
        UNWIND $batch as entry

        MATCH (compound:Compound {
            id: entry.compound_id
        })

        MATCH (pathway:Pathway {
            id: entry.pathway_id
        })

        CREATE (compound)-[:IN]->(pathway)
    """
    graph.run(query, params)


def connect_disease_and_pathway(graph, params):
    """
    Creates IN association for the given disease and
    pathway.
    """

    query = """
        UNWIND $batch as entry

        MATCH (disease:Disease {
            id: entry.disease_id
        })

        MATCH (pathway:Pathway {
            id: entry.pathway_id
        })

        CREATE (disease)-[:IN]->(pathway)
    """
    graph.run(query, params)


def connect_drug_and_pathway(graph, params):
    """
    Creates IN association for the given drug and
    pathway.
    """

    query = """
        UNWIND $batch as entry

        MATCH (drug:Drug {
            id: entry.drug_id
        })

        MATCH (pathway:Pathway {
            id: entry.pathway_id
        })

        CREATE (drug)-[:IN]->(pathway)
    """
    graph.run(query, params)


# ========================= Schema queries =========================


def create_constraints(graph):
    """
    Creates node constraints for the Neo4j graph database.
    """

    queries = [
        # Protein
        "CREATE CONSTRAINT ON (protein:Protein) ASSERT protein.id IS UNIQUE",
        "CREATE CONSTRAINT ON (protein:Protein) ASSERT protein.external_id IS UNIQUE",
        # Pathway
        # "CREATE CONSTRAINT ON (pathway:Pathway) ASSERT pathway.id IS UNIQUE",
        # Compound
        # "CREATE CONSTRAINT ON (compound:Compound) ASSERT compound.id IS UNIQUE",
        # Drug
        # "CREATE CONSTRAINT ON (drug:Drug) ASSERT drug.id IS UNIQUE",
        # Disease
        # "CREATE CONSTRAINT ON (disease:Disease) ASSERT disease.id IS UNIQUE"
    ]

    for query in queries:
        graph.run(query)


def create_protein_index(graph):
    """
    Creates 'Protein' node index on the attribute 'name'.
    """

    queries = ["CREATE INDEX ON :Protein(name)"]

    for query in queries:
        graph.run(query)


def create_kegg_index(graph):
    """
    Creates KEGG data node indexes:
    - for 'Protein' on 'name'
    - for 'Class' on 'name'
    """

    queries = ["CREATE INDEX ON :Pathway(name)", "CREATE INDEX ON :Class(name)"]

    for query in queries:
        graph.run(query)


# ========================= Server warm-up =========================


def warm_up(graph):
    query = """
        MATCH (n)
        OPTIONAL MATCH (n)-[r]->()
        RETURN count(n.id) + count(r.combined);
    """
    print("Warming up Neo4j...")
    graph.run(query)
    print("Done.")


# ========================= List queries =========================
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


def get_pathway_list(graph):
    """
    Retrieve a list of pathways including the pathway ID
    and the pathway name.
    """

    query = """
        MATCH (pathway:Pathway)
        RETURN pathway.id AS id,
               pathway.name AS name,
               pathway.species_id AS species_id
    """

    return graph.run(query)


def get_class_list(graph):
    """
    Retrieve a list of all available pathway
    class names.
    """

    query = """
        MATCH (class:Class)
        RETURN class.name AS name
    """

    return graph.run(query)


# ========================= Subgraph queries =========================


def get_protein_subgraph(graph, protein_id, threshold=0):
    """
    For the given protein, return the Neo4j subgraph
    of the protein, all other associated proteins and
    the common pathways.
    """

    # Neo4j query
    query = """
        MATCH (protein:Protein {
            id: $protein_id
        })
        USING INDEX protein:Protein(id)
        WITH protein
        MATCH (protein)-[:IN]->(pathway:Pathway)
        WITH protein, COLLECT(DISTINCT pathway) AS pathways
        MATCH (protein)-[association:ASSOCIATION]-(other:Protein)
        WHERE association.combined >= $threshold
        RETURN protein, pathways, COLLECT({
            combined_score: association.combined,
            other: other
        }) AS associations
    """

    assert 0 <= threshold <= 1000, "Combined score threshold should be in range [0, 1000]!"

    param_dict = dict(protein_id=protein_id, threshold=threshold)
    return graph.run(query, param_dict)


def get_proteins_subgraph(graph, protein_ids, threshold=0, external=False):
    """
    For the given list of proteins, return the Neo4j
    subgraph of the proteins, all associations between
    them and common pathways.
    """

    # Neo4j query
    query = (
        """
        MATCH (protein:Protein)
    """
        + ("WHERE protein.external_id IN $protein_ids$" if external else "WHERE protein.id IN $protein_ids")
        + """
        WITH COLLECT(protein) AS proteins
        WITH proteins, SIZE(proteins) AS num_proteins
        UNWIND RANGE(0, num_proteins - 1) AS i
        UNWIND RANGE(i + 1, num_proteins - 1) AS j
        WITH proteins, proteins[i] AS protein1, proteins[j] AS protein2
        OPTIONAL MATCH (protein1)-[association:ASSOCIATION]-(protein2)
        WHERE association.combined >= {threshold}
        WITH proteins, protein1, association, protein2
        OPTIONAL MATCH (protein1)-[:IN]->(pathway:Pathway)<-[:IN]-(protein2)
        RETURN proteins AS proteins, COLLECT(DISTINCT pathway) AS pathways, COLLECT({
            protein1_id: protein1.id,
            combined_score: association.combined,
            protein2_id: protein2.id,
            pathway_id: pathway.id
        }) AS associations
    """
    )

    assert 0 <= threshold <= 1000, "Combined score threshold should be in range [0, 1000]!"

    param_dict = dict(protein_ids=protein_ids, threshold=threshold)
    return graph.run(query, param_dict)


def get_pathway_subgraph(graph, pathway_id, threshold=0):
    """
    For the given pathway, return the Neo4j subgraph
    of the pathway, all contained proteins and
    the class hierarchy of the pathway.
    """

    # Neo4j query
    query = """
        MATCH (pathway:Pathway {
            id: $pathway_id
        })
        USING INDEX pathway:Pathway(id)
        WITH pathway
        OPTIONAL MATCH (class:Class)<-[:IN*]-(pathway)
        WITH pathway, COLLECT(DISTINCT class) AS classes
        MATCH (protein:Protein)-->(pathway)
        WITH classes, COLLECT(protein) AS proteins
        WITH classes, proteins, SIZE(proteins) AS num_proteins
        UNWIND RANGE(0, num_proteins - 1) AS i
        UNWIND RANGE(i + 1, num_proteins - 1) AS j
        WITH classes, proteins, proteins[i] AS protein1, proteins[j] AS protein2
        MATCH (protein1)-[association:ASSOCIATION]-(protein2)
        // WHERE association.combined >= $threshold
        RETURN classes, proteins, COLLECT({
            protein1_id: protein1.id,
            combined_score: association.combined,
            protein2_id: protein2.id
        }) AS associations
    """

    assert 0 <= threshold <= 1000, "Combined score threshold should be in range [0, 1000]!"

    param_dict = dict(pathway_id=pathway_id, threshold=threshold)
    return graph.run(query, param_dict)


def get_class_subgraph(graph, name):
    """
    For the given pathway class, return the Neo4j subgraph
    of the class hierarchy and pathways attached to the
    leaves of the hierarchy tree.
    """

    query = """
        MATCH (class:Class {
            name: {name}
        })
        USING INDEX class:Class(name)
        // "fuzzy" search: WHERE toUpper(class.name) =~ (".*" + toUpper({name}) + ".*")
        WITH class
        OPTIONAL MATCH (class)<-[:IN*]-(pathway:Pathway)
        RETURN class, COLLECT(DISTINCT pathway) as pathways
    """

    param_dict = dict(name=name)
    return graph.run(query, param_dict)


def get_num_proteins():
    """Use Cypher query call to get the total number of proteins
    Args:
        Right now none, default organism is mus musculus
        When more organism databases are implemented,
        add species_id to clarify from which organism
    Return:
        Number of proteins(int)
    """

    # TODO: change to credentials.yml
    data = subprocess.run(
        [
            "cypher-shell",
            "-a",
            "bolt://localhost:7687",
            "-u",
            "neo4j",
            "-p",
            "pgdb",
            "MATCH (n:Protein) RETURN count(n)",
        ],
        capture_output=True,
        encoding="utf-8",
    )

    # Check standard output 'stdout' whether it's empty to control errors
    if not data.stdout:
        raise Exception(data.stderr)

    # all proteins of organism: background proteins
    num_proteins = int(data.stdout[9:])
    return num_proteins


# number of proteins in the whole organism
NUM_PROTEINS = get_num_proteins()


def create_term_df():
    """Use Cypher query to create a dataframe with all terms and their
    properties from the database
    Args:
        Right now none, default organism is mus musculus
        When more organism databases are implemented,
        add species_id to clarify from which organism
    """

    query = (
        """
                WITH "MATCH (term:Terms)
                RETURN term.external_id AS id, term.name AS name, term.category AS category, term.proteins AS proteins"
                AS query
                CALL apoc.export.csv.query(query, "/tmp/"""
        + repr(TERM_FILE)
        + """.csv", {})
                YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
                RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;
                """
    )

    with open("/tmp/query" + repr(TERM_FILE) + ".txt", "w") as query_text:
        query_text.write("%s" % query)

    # Run the cypher query in cypher shell via terminal
    data = subprocess.run(
        [
            "cypher-shell",
            "-a",
            "bolt://localhost:7687",
            "-u",
            "neo4j",
            "-p",
            "pgdb",
            "-f",
            "/tmp/query" + repr(TERM_FILE) + ".txt",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    # Check standard output 'stdout' whether it's empty to control errors
    if not data.stdout:
        raise Exception(data.stderr)
