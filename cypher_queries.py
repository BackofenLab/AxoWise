
def add_compound(graph, params):

    query = """
        UNWIND {batch} as entry
        CREATE (compound:Compound {
            id: entry.id,
            name: entry.name
        })
    """
    graph.run(query, params)

def add_disease(graph, params):

    query = """
        UNWIND {batch} as entry
        CREATE (disease:Disease {
            id: entry.id,
            name: entry.name
        })
    """
    graph.run(query, params)

def add_drug(graph, params):

    query = """
        UNWIND {batch} as entry
        CREATE (drug:Drug {
            id: entry.id,
            name: entry.name
        })
    """
    graph.run(query, params)

def add_protein(graph, params):
    """
    Create a protein with the specified id, external id,
    preferred name and annotation.
    """

    query = """
        UNWIND {batch} as entry
        CREATE (protein:Protein {
            id: entry.id,
            external_id: entry.external_id,
            preferred_name: entry.preferred_name,
            annotation: entry.annotation
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

def get_protein_subgraph(graph, preferred_name):
    """
    For the given protein, return the Neo4j subgraph
    of the protein and all other associated proteins.
    """

    query = """
        MATCH (protein:Protein {
            preferred_name: {preferred_name}
        })

        OPTIONAL MATCH (protein)-[association:ASSOCIATION]-(other:Protein)

        OPTIONAL MATCH (protein)-[action:ACTION]-(other)

        OPTIONAL MATCH (protein)-[:IN]->(pathway:Pathway)
        OPTIONAL MATCH (other)-[:IN]->(pathway)

        OPTIONAL MATCH (drug:Drug)-[:IN]->(pathway)
        OPTIONAL MATCH (disease:Disease)-[:IN]->(pathway)
        OPTIONAL MATCH (compound:Compound)-[:IN]->(pathway)

        RETURN protein, other, association, action, pathway, drug, disease, compound
    """

    param_dict = dict(
        preferred_name = preferred_name
    )

    return graph.data(query, param_dict)

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

def update_pathways(graph, params):
    """
    For each protein in the pathway collection, create / update (merge)
    the pathway and associated classes, compounds, drugs and diseases.
    """

    query = """
        UNWIND {batch} as entry

        MATCH (protein1:Protein {
            external_id: entry.external_id
        })

        FOREACH (p1 IN entry.pathways1 |
            MERGE (pathway1:Pathway {
                id: p1.id,
                name: p1.name,
                description: p1.description
            })
            CREATE (protein1)-[:IN]->(pathway1)

            MERGE (fClass:Class {
                name: p1.classes[length(p1.classes) - 1]
            })
            MERGE (pathway1)-[:IN]->(fClass)
            FOREACH (i IN RANGE(length(p1.classes) - 1, 1) |
                MERGE (cClass:Class {
                        name: p1.classes[i]
                })
                MERGE (nClass:Class {
                        name: p1.classes[i - 1]
                })
                MERGE (cClass)-[:IN]->(nClass)
            )

            FOREACH (dis1 IN p1.diseases |
                MERGE (disease1:Disease {
                    id: dis1.id,
                    name: dis1.name
                })
                MERGE (disease1)-[:IN]->(pathway1)
            )

            FOREACH (dr1 IN p1.drugs |
                MERGE (drug1:Drug {
                    id: dr1.id,
                    name: dr1.name
                })
                MERGE (drug1)-[:IN]->(pathway1)
            )

            FOREACH (com1 IN p1.compounds |
                MERGE (compound1:Compound {
                    id: com1.id,
                    name: com1.name
                })
                MERGE (compound1)-[:IN]->(pathway1)
            )
        )
    """
    graph.run(query, params)

# def remove_redundant_properties(graph):
#     """
#     Remove redundant properties of nodes or edges that have been previously
#     used to correctly construct the graph.
#     """

#     query = """
#         MATCH (action:Action)
#         REMOVE action.id1, action.id2
#     """
#     graph.run(query)

def create_protein_index(graph):

    query = """
        CREATE INDEX ON :Protein(id)
    """

    graph.run(query)

def delete_all(graph):
    """
    Delete all nodes and edges from a Neo4j graph.
    """

    query = "MATCH (n) DETACH DELETE (n)"
    graph.run(query)
