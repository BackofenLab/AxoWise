
def update_proteins_and_action(graph, params):
    """
    For an existing protein - protein pair, create / update (merge) the given
    action associated with the given pathway.

    If the action's "mode" is the same, the action is updated only if the current
    provided score is higher than the previous.
    """
    
    query = """
        MATCH (protein1:Protein {
            id: {id1}
        })

        MATCH (protein2:Protein {
            id: {id2}
        })

        MERGE (protein1)-[action:ACTION {
            mode: {mode},
            id1: {id1},
            id2: {id2}
        }]->(protein2)
            ON CREATE SET action.score = {score}
            ON MATCH SET action.score = CASE action.score
                                       WHEN {score} > action.score
                                       THEN action.score = {score}
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

def update_associations_and_pathways(graph, params):
    """
    For a given protein - protein pair, create / update (merge) the proteins
    and the association between them.
    """

    query = """
        MERGE (protein1:Protein {
            id: {id1},
            external_id: {external_id1},
            annotation: {annotation1},
            preferred_name: {preferred_name1}
        })

        MERGE (protein2:Protein {
            id: {id2},
            external_id: {external_id2},
            annotation: {annotation2},
            preferred_name: {preferred_name2}
        })

        CREATE (protein1)-[a:ASSOCIATION {
            experiments: {experiments},
            database: {database},
            textmining: {textmining},
            coexpression: {coexpression},
            neighborhood: {neighborhood},
            fusion: {fusion},
            cooccurence: {cooccurence},
            combined: {combined_score}
        }]->(protein2)


        FOREACH (p1 IN {pathways1} |
            MERGE (pathway1:Pathway {
                id: p1.id,
                name: p1.name,
                description: p1.description
            })
            MERGE (protein1)-[:IN]->(pathway1)

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


        FOREACH (p2 IN {pathways2} |
            MERGE (pathway2:Pathway {
                id: p2.id,
                name: p2.name,
                description: p2.description
            })
            MERGE (protein2)-[:IN]->(pathway2)

            MERGE (fClass:Class {
                name: p2.classes[length(p2.classes) - 1]
            })
            MERGE (pathway2)-[:IN]->(fClass)
            FOREACH (i IN RANGE(length(p2.classes) - 1, 1) |
                MERGE (cClass:Class {
                        name: p2.classes[i]
                })
                MERGE (nClass:Class {
                        name: p2.classes[i - 1]
                })
                MERGE (cClass)-[:IN]->(nClass)
            )

            FOREACH (dis2 IN p2.diseases |
                MERGE (disease2:Disease {
                    id: dis2.id,
                    name: dis2.name
                })
                MERGE (disease2)-[:IN]->(pathway2)
            )

            FOREACH (dr2 IN p2.drugs |
                MERGE (drug2:Drug {
                    id: dr2.id,
                    name: dr2.name
                })
                MERGE (drug2)-[:IN]->(pathway2)
            )

            FOREACH (com2 IN p2.compounds |
                MERGE (compound2:Compound {
                    id: com2.id,
                    name: com2.name
                })
                MERGE (compound2)-[:IN]->(pathway2)
            )
        )

    """
    graph.run(query, params)

def remove_redundant_properties(graph):
    """
    Remove redundant properties of nodes or edges that have been previously
    used to correctly construct the graph.
    """

    query = """
        MATCH (action:Action)
        REMOVE action.id1, action.id2
    """
    graph.run(query)

def delete_all(graph):
    """
    Delete all nodes and edges from a Neo4j graph.
    """

    query = "MATCH (n) DETACH DELETE (n)"
    graph.run(query)
