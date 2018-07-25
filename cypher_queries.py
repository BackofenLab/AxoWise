
def update_protein(graph, id, external_id, annotation, preferred_name):
    # Create the node if the node does not exist, else match it
    query = """
        MERGE (n:Protein {
            id: {id},
            external_id: {external_id},
            annotation: {annotation},
            preferred_name: {preferred_name}
        })
    """
    params = dict(
            id = id,
            external_id = external_id,
            annotation = annotation,
            preferred_name = preferred_name
    )
    graph.run(query, params)