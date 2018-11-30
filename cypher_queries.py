"""
Collection of Cypher queries for writing and reading the resulting
Neo4j graph database.
"""

# ========================= Creating queries =========================

def add_compound(graph, params):
    """
    Create a compound with the specified id and
    name.
    """

    query = """
        UNWIND {batch} as entry
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
        UNWIND {batch} as entry
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
        UNWIND {batch} as entry
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
        UNWIND {batch} as entry
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
        UNWIND {batch} as entry
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
        UNWIND {batch} as entry
        CREATE (protein:Protein {
            id: entry.id,
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
        UNWIND {batch} as entry
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
        UNWIND {batch} as entry

        MATCH (protein1:Protein {
            id: entry.id1
        })

        MATCH (protein2:Protein {
            id: entry.id2
        })

        CREATE (protein1)-[a:ASSOCIATION {
            experiments: entry.experiments,
            database: entry.database,
            textmining: entry.textmining,
            coexpression: entry.coexpression,
            neighborhood: entry.neighborhood,
            fusion: entry.fusion,
            cooccurence: entry.cooccurence,
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
        UNWIND {batch} as entry

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
        UNWIND {batch} as entry

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
        UNWIND {batch} as entry

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
        UNWIND {batch} as entry

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
        "CREATE CONSTRAINT ON (pathway:Pathway) ASSERT pathway.id IS UNIQUE",
        # Compound
        "CREATE CONSTRAINT ON (compound:Compound) ASSERT compound.id IS UNIQUE",
        # Drug
        "CREATE CONSTRAINT ON (drug:Drug) ASSERT drug.id IS UNIQUE",
        # Disease
        "CREATE CONSTRAINT ON (disease:Disease) ASSERT disease.id IS UNIQUE"
    ]

    for query in queries:
        graph.run(query)

def create_protein_index(graph):
    """
    Creates 'Protein' node index on the attribute 'name'.
    """

    queries = [
        "CREATE INDEX ON :Protein(name)"
    ]

    for query in queries:
        graph.run(query)

def create_kegg_index(graph):
    """
    Creates KEGG data node indexes:
    - for 'Protein' on 'name'
    - for 'Class' on 'name'
    """

    queries = [
        "CREATE INDEX ON :Pathway(name)",
        "CREATE INDEX ON :Class(name)"
    ]

    for query in queries:
        graph.run(query)

# ========================= Search queries =========================

def get_protein_subgraph(graph, protein_id, threshold=0):
    """
    For the given protein, return the Neo4j subgraph
    of the protein, all other associated proteins and
    the common pathways.
    """

    # Neo4j query
    query = """
        MATCH (protein:Protein {
            id: {protein_id}
        })
        USING INDEX protein:Protein(id)
        WITH protein
        MATCH (protein)-[association:ASSOCIATION]-(other:Protein)
        WHERE association.combined >= {threshold}
        WITH protein, association, other
        MATCH (protein)-[:IN]->(pathway:Pathway)<-[:IN]-(other)
        RETURN protein, association, other, COLLECT(pathway) AS pathways
    """

    param_dict = dict(
        protein_id=protein_id,
        threshold=threshold
    )
    return graph.run(query, param_dict)

def get_proteins_subgraph(graph, protein_ids, threshold=0):
    """
    For the given list of proteins, return the Neo4j
    subgraph of the proteins, all associations between
    them and common pathways.
    """

    # Neo4j query
    query = """
        MATCH (protein1:Protein)
        WHERE protein1.id IN {protein_ids}
        WITH protein1
        MATCH (protein2:Protein)
        WHERE protein2.id in {protein_ids}
        WITH protein1, protein2
        MATCH (protein1)-[association:ASSOCIATION]->(protein2)
        WHERE association.combined >= {threshold}
        WITH protein1, association, protein2
        OPTIONAL MATCH (protein1)-[:IN]->(pathway:Pathway)<-[:IN]-(protein2)
        RETURN protein1, association, protein2, COLLECT(pathway) AS pathways
    """

    param_dict = dict(
        protein_ids=protein_ids,
        threshold=threshold
    )
    return graph.run(query, param_dict)

def get_pathway_subgraph(graph, pathway_id):
    """
    For the given pathway, return the Neo4j subgraph
    of the pathway, all contained proteins and
    the class hierarchy of the pathway.
    """

    # Neo4j query
    query = """
        MATCH (pathway:Pathway {
            id: {pathway_id}
        })
        USING INDEX pathway:Pathway(id)
        WITH pathway
        MATCH (class:Class)<-[:IN*]-(pathway)<-[:IN]-(protein:Protein)
        RETURN pathway, COLLECT(DISTINCT class) AS classes, COLLECT(DISTINCT protein) as proteins
    """

    param_dict = dict(pathway_id=pathway_id)
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
        MATCH (class)<-[:IN*]-(pathway:Pathway)
        RETURN class, COLLECT(DISTINCT pathway) as pathways
    """

    param_dict = dict(name=name)
    return graph.run(query, param_dict)
