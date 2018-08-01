
class QueryBuilder:

    @staticmethod
    def associations_query(species_id, protein1 = None, protein2 = None, limit = None):
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
        """
        query += ("AND UPPER(proteins1.preferred_name) = UPPER(%s) AND UPPER(proteins2.preferred_name) = UPPER(%s)" if narrow else "")
        query += ("LIMIT %s" if limit is not None else "")
        query += ";" 

        params = (species_id,) + ((protein1, protein2,) if narrow else ()) + ((limit,) if limit is not None else ())

        return query, params

    @staticmethod
    def actions_and_pathways_query(species_id, protein1 = None, protein2 = None, limit = None):
        narrow = (protein1 is not None) and (protein2 is not None)

        query = """
            SELECT proteins1.protein_id, proteins2.protein_id,
                actions.mode,
                actions.score,
                sets.set_id,
                sets.title,
                sets.comment,
                collections.collection_id
            FROM network.actions AS actions
            JOIN items.proteins AS proteins1 ON actions.item_id_a = proteins1.protein_id
            JOIN items.proteins AS proteins2 ON actions.item_id_b = proteins2.protein_id
            LEFT JOIN evidence.actions_sets AS actions_sets ON actions_sets.item_id_a = proteins1.protein_id
                                                            AND actions_sets.item_id_b = proteins2.protein_id
                                                            AND actions_sets.mode = actions.mode
            JOIN evidence.sets_items AS sets_items1 ON sets_items1.item_id = proteins1.protein_id
                                                    AND sets_items1.species_id = proteins1.species_id
            JOIN evidence.sets_items AS sets_items2 ON sets_items2.item_id = proteins2.protein_id
                                                    AND sets_items1.set_id = sets_items2.set_id
                                                    AND sets_items1.species_id = proteins1.species_id
            JOIN evidence.sets AS sets ON sets_items1.set_id = sets.set_id
            JOIN evidence.collections AS collections ON sets.collection_id = collections.collection_id
            WHERE proteins1.species_id = %s
        """
        query += ("AND UPPER(proteins1.preferred_name) = UPPER(%s) AND UPPER(proteins2.preferred_name) = UPPER(%s)" if narrow else "")
        query += ("LIMIT %s" if limit is not None else "")
        query += ";"

        params = (species_id,) + ((protein1, protein2,) if narrow else ()) + ((limit,) if limit is not None else ())

        return query, params

    @staticmethod
    def species_id_query(compact_species_name):
        query = """
            SELECT species_id
            FROM items.species
            WHERE UPPER(compact_name) = UPPER(%s);
        """

        params = (compact_species_name,)

        return query, params


def get_associations(postgres_connection, species_id, protein1 = None, protein2 = None, limit = None):
    """
    Queries the database specified by postgres_connection and for each pair
    of proteins yields an association, i.e.:
    - internal ids
    - external ids
    - annotations
    - combined score
    - scores per evidence channels

    The query can be narrowed by specifying names of proteins: protein1 and protein2.
    To limit the number of fetched rows, provide limit as an integer.
    """

    cursor = postgres_connection.cursor(name = "associations")
    query, params = QueryBuilder.associations_query(species_id, protein1, protein2, limit)
    cursor.execute(query, params)

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

def get_actions_and_pathways(postgres_connection, species_id, protein1 = None, protein2 = None, limit = None):
    """
    Queries the database specified by postgres_connection and for each pair
    of proteins yields an action and a pathway, i.e.:
    - internal ids
    - mode (activation, binding, catalysis etc.)
    - score
    - set id
    - title (type of the pathway)
    - comment (pathway description)
    - collection id

    The query can be narrowed by specifying names of proteins: protein1 and protein2.
    To limit the number of fetched rows, provide limit as an integer.
    """

    cursor = postgres_connection.cursor(name = "actions_and_pathways")
    query, params = QueryBuilder.actions_and_pathways_query(species_id, protein1, protein2, limit)
    cursor.execute(query, params)

    while True:
        row = cursor.fetchone()
        if row is None:
            break

        yield {
            "id1": row[0],
            "id2": row[1],
            "mode": row[2],
            "score": row[3],
            "set_id": row[4],
            "title": row[5],
            "comment": row[6],
            "collection_id": row[7]
        }

    cursor.close()

def get_species_id(postgres_connection, compact_species_name):
    """
    Queries the database specified by postgres_connection and returns
    the internal id of species defined by compact_species_name.
    If such species are not matched, None is returned.
    """

    cursor = postgres_connection.cursor()
    query, params = QueryBuilder.species_id_query(compact_species_name)
    cursor.execute(query, params)
    species_id = cursor.fetchone()
    cursor.close()
    return (species_id[0] if species_id is not None else None)
