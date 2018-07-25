
def get_pathways(cursor, species_id = 10090, protein1 = None, protein2 = None):
    narrow = (protein1 is not None) and (protein2 is not None)
    query = """
        SELECT sets_items1.item_id, sets_items2.item_id,
               proteins1.protein_external_id, proteins2.protein_external_id,
               proteins1.annotation, proteins2.annotation,
               sets_items1.preferred_name, sets_items2.preferred_name,
               actions_sets.mode,
               sets.set_id,
               sets.title,
               sets.comment,
               sets.collection_id
        FROM evidence.sets_items AS sets_items1
        CROSS JOIN evidence.sets_items AS sets_items2
        JOIN evidence.actions_sets AS actions_sets ON actions_sets.item_id_a = sets_items1.item_id
                                                   AND actions_sets.item_id_b = sets_items2.item_id
        JOIN evidence.sets AS sets ON sets_items1.set_id = sets.set_id
                                   AND sets_items2.set_id = sets.set_id
        JOIN items.proteins AS proteins1 ON sets_items1.item_id = proteins1.protein_id
        JOIN items.proteins AS proteins2 ON sets_items2.item_id = proteins2.protein_id
        WHERE sets_items1.species_id = %s
        """ + ("AND sets_items1.preferred_name = %s AND sets_items2.preferred_name = %s;" if narrow else ";")
    cursor.execute(
        query,
        (species_id, protein1, protein2) if narrow else (species_id,)
    )
    result = cursor.fetchall()
    for row in result:
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
            "set_id": row[9],
            "title": row[10],
            "comment": row[11],
            "collection_id": row[12]
        }

def get_species_id(cursor, compact_species_name):
    cursor.execute("""
        SELECT species_id
        FROM items.species
        WHERE compact_name = %s;
        """,
        (compact_species_name,)
    )
    return cursor.fetchone()
