
def get_associations(postgres_connection, species_id = 10090, protein1 = None, protein2 = None, limit = None):
    cursor = postgres_connection.cursor(name = "associations")
    narrow = (protein1 is not None) and (protein2 is not None)
    query = """
        SELECT proteins1.protein_id, proteins2.protein_id,
               proteins1.protein_external_id, proteins2.protein_external_id,
               proteins1.preferred_name, proteins2.preferred_name,
               proteins1.annotation, proteins2.annotation,
               node_node_links.combined_score,
               node_node_links.evidence_scores
        FROM network.node_node_links AS node_node_links
        JOIN items.proteins AS proteins1 ON proteins1.protein_id = node_node_links.node_id_a
        JOIN items.proteins AS proteins2 ON proteins2.protein_id = node_node_links.node_id_b
        WHERE proteins1.species_id = %s
    """ + ("AND proteins1.preferred_name = %s AND proteins2.preferred_name = %s" if narrow else "") + ("LIMIT %s" if limit is not None else "") + ";" 

    cursor.execute(
        query,
        (species_id,) + ((protein1, protein2,) if narrow else ()) + ((limit,) if limit is not None else ())
    )

    while True:
        row = cursor.fetchone()
        if row is None:
            break

        yield {
            "id1": row[0],
            "id2": row[1],
            "external_id1": row[2],
            "external_id2": row[3],
            "preferred_name1": row[4],
            "preferred_name2": row[5],
            "annotation1": row[6],
            "annotation2": row[7],
            "combined_score": row[8],
            "evidence_scores": row[9]
        }
    
    cursor.close()

def get_actions_and_pathways(postgres_connection, species_id = 10090, protein1 = None, protein2 = None, limit = None):
    cursor = postgres_connection.cursor(name = "actions_and_pathways")
    narrow = (protein1 is not None) and (protein2 is not None)
    query = """
        SELECT sets_items1.item_id, sets_items2.item_id,
               proteins1.protein_external_id, proteins2.protein_external_id,
               proteins1.annotation, proteins2.annotation,
               sets_items1.preferred_name, sets_items2.preferred_name,
               actions.mode,
               actions.score,
               sets.set_id,
               sets.title,
               sets.comment,
               sets.collection_id
        FROM evidence.sets_items AS sets_items1
        JOIN evidence.sets_items AS sets_items2 ON sets_items1.item_id < sets_items2.item_id
        JOIN evidence.actions_sets AS actions_sets ON actions_sets.item_id_a = sets_items1.item_id
                                                   AND actions_sets.item_id_b = sets_items2.item_id
        JOIN evidence.sets AS sets ON sets_items1.set_id = sets.set_id
                                   AND sets_items2.set_id = sets.set_id
        RIGHT JOIN network.actions AS actions ON actions.item_id_a = actions_sets.item_id_a
                                              AND actions.item_id_b = actions_sets.item_id_b
        JOIN items.proteins AS proteins1 ON actions.item_id_a = proteins1.protein_id
        JOIN items.proteins AS proteins2 ON actions.item_id_b = proteins2.protein_id
        WHERE sets_items1.species_id = %s
        """ + ("AND proteins1.preferred_name = %s AND proteins2.preferred_name = %s" if narrow else "") + ("LIMIT %s" if limit is not None else "") + ";" 

    cursor.execute(
        query,
        (species_id,) + ((protein1, protein2,) if narrow else ()) + ((limit,) if limit is not None else ())
    )

    while True:
        row = cursor.fetchone()
        if row is None:
            break

        yield {
            "id1": row[0],
            "id2": row[1],
            "external_id1": row[2],
            "external_id2": row[3],
            "annotation1": row[4],
            "annotation2": row[5],
            "preferred_name1": row[6],
            "preferred_name2": row[7],
            "mode": row[8],
            "score": row[9],
            "set_id": row[10],
            "title": row[11],
            "comment": row[12],
            "collection_id": row[13]
        }

    cursor.close()

def get_species_id(postgres_connection, compact_species_name):
    cursor = postgres_connection.cursor()
    cursor.execute("""
        SELECT species_id
        FROM items.species
        WHERE compact_name = %s;
        """,
        (compact_species_name,)
    )
    species_id = cursor.fetchone()
    cursor.close()
    return (species_id[0] if species_id is not None else None)

def get_score_types(postgres_connection):
    cursor = postgres_connection.cursor()
    cursor.execute("""
        SELECT score_types.score_id,
               score_types.score_type
        FROM network.score_types AS score_types;
        """
    )
    return cursor.fetchall()