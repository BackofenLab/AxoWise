
def get_pathways(cursor, species_id = 10090, protein1 = None, protein2 = None):
    narrow = (protein1 is not None) and (protein2 is not None)
    cursor.execute("""
        SELECT sets_items1.preferred_name, sets_items2.preferred_name, actions_sets.mode, sets.set_id, sets.title, sets.comment
        FROM evidence.sets_items AS sets_items1
        CROSS JOIN evidence.sets_items AS sets_items2
        JOIN evidence.actions_sets AS actions_sets ON actions_sets.item_id_a = sets_items1.item_id
                                                   AND actions_sets.item_id_b = sets_items2.item_id
        JOIN evidence.sets AS sets ON sets_items1.set_id = sets.set_id
                                   AND sets_items2.set_id = sets.set_id
        WHERE sets_items1.species_id = %s
        """ + (" AND sets_items1.preferred_name = %s AND sets_items2.preferred_name = %s;" if narrow else ";"),
        (species_id, protein1, protein2) if narrow else (species_id,)
    )
    return cursor.fetchall()
