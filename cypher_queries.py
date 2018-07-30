
def update_proteins_and_action(graph, params):
    # Create the node if the node does not exist, else match it
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

        MERGE (action:Action {
            mode: {mode},
            id1: {id1},
            id2: {id2}
        }) ON CREATE SET action.score = {score}
           ON MATCH SET action.score = CASE action.score
                                       WHEN {score} > action.score
                                       THEN action.score = {score}
                                       ELSE action.score
                                       END

        MERGE (protein1)-[:IN]->(action)
        MERGE (protein2)-[:IN]->(action)

        MERGE (pathway:Pathway {
            set_id: {set_id},
            collection_id: {collection_id},
            comment: {comment},
            title: {title}
        })

        MERGE (action)-[:IN]->(pathway)

    """
    graph.run(query, params)

def get_protein_subgraph(graph, preferred_name):
    query = """
        MATCH (protein:Protein {
            preferred_name: {preferred_name}
        })-[association:ASSOCIATION]-(other:Protein)
        MATCH (protein)-[:IN]-(action:Action)
        MATCH (action)-[:IN]-(pathway:Pathway)
        RETURN *
    """
    return graph.data(query, dict(
        preferred_name = preferred_name
    ))

def update_associations(graph, params):
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
    """
    graph.run(query, params)

def remove_redundant_properties(graph):
    query = """
        MATCH (action:Action)
        REMOVE action.id1, action.id2
    """
    graph.run(query)

def delete_all(graph):
    query = "MATCH (n) DETACH DELETE (n)"
    graph.run(query)
