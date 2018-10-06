
class QueryBuilder:

    @staticmethod
    def proteins_query():
        query = """
            SELECT protein_id,
                   protein_external_id,
                   preferred_name,
                   annotation
            FROM items.proteins;
        """

        return query

    @staticmethod
    def associations_query(species_id):
        # narrow = (protein1 is not None) and (protein2 is not None)

        query = """
            SELECT node_node_links.node_id_a, node_node_links.node_id_b,
                   node_node_links.combined_score,
                   node_node_links.evidence_scores
            FROM network.node_node_links AS node_node_links
            JOIN items.proteins AS proteins ON proteins.protein_id = node_node_links.node_id_a
            WHERE proteins.species_id = %s;
        """
        # query += ("AND UPPER(proteins1.preferred_name) = UPPER(%s) AND UPPER(proteins2.preferred_name) = UPPER(%s)" if narrow else "")
        # query += ("LIMIT %s" if limit is not None else "")
        # query += ";"

        # params = (species_id,) + ((protein1, protein2,) if narrow else ()) + ((limit,) if limit is not None else ())
        params = (species_id,)

        return query, params

    @staticmethod
    def actions_query(species_id, protein1 = None, protein2 = None, limit = None):
        narrow = (protein1 is not None) and (protein2 is not None)

        query = """
            SELECT item_id_a,
                   item_id_b,
                   mode,
                   score
            FROM network.actions AS actions
            JOIN items.proteins AS proteins1 ON actions.item_id_a = proteins1.protein_id
            JOIN items.proteins AS proteins2 ON actions.item_id_b = proteins2.protein_id
            WHERE proteins1.species_id = %s
              AND proteins1.species_id = proteins2.species_id
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


def get_proteins(postgres_connection):
    """
    Queries the database specified by postgres_connection and for each protein
    yields the following:
    - internal id
    - external_id
    - preferred name
    - annotation
    """

    cursor = postgres_connection.cursor(name = "proteins")
    query = QueryBuilder.proteins_query()
    cursor.execute(query)

    while True:
        rows = cursor.fetchmany(size = 4096)
        if len(rows) == 0:
            break

        for row in rows:
            yield {
                "id": row[0],
                "external_id": row[1],
                "preferred_name": row[2],
                "annotation": row[3]
            }
    
    cursor.close()

def get_associations(postgres_connection, species_id):
    """
    Queries the database specified by postgres_connection and for each pair
    of proteins yields an association, i.e.:
    - internal ids
    - combined score
    - scores per evidence channels

    The query can be narrowed by specifying names of proteins: protein1 and protein2.
    To limit the number of fetched rows, provide limit as an integer.
    """

    cursor = postgres_connection.cursor(name = "associations")
    query, params = QueryBuilder.associations_query(species_id)
    cursor.execute(query, params)

    while True:
        rows = cursor.fetchmany(size = 4096)
        if len(rows) == 0:
            break

        for row in rows:
            yield {
                "id1": row[0],
                "id2": row[1],
                "combined_score": row[2],
                "evidence_scores": row[3]
            }
    
    cursor.close()

def get_actions(postgres_connection, species_id, protein1 = None, protein2 = None, limit = None):
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
    query, params = QueryBuilder.actions_query(species_id, protein1, protein2, limit)
    cursor.execute(query, params)

    while True:
        rows = cursor.fetchmany(size = 4096)
        if len(rows) == 0:
            break

        for row in rows:
            yield {
                "id1": row[0],
                "id2": row[1],
                "mode": row[2],
                "score": row[3]
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
