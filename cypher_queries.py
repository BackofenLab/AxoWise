
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
            mode: {mode}
        }) ON CREATE SET action.score = null

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
