"""
Collection of SQL queries for reading the STRING's PostgreSQL database.
"""

class QueryBuilder:
    """
    Class containing static methods for building the SQL query strings
    from the given parameters.
    """

    @staticmethod
    def proteins_query(species_id):
        """
        Builds an SQL query for retrieving proteins
        for a species defined by 'species_id'.
        """

        query = """
            SELECT protein_id,
                   protein_external_id,
                   preferred_name,
                   annotation
            FROM items.proteins
            WHERE species_id = %s;
        """

        params = (species_id,)

        return query, params

    @staticmethod
    def associations_query(species_id):
        """
        Builds an SQL query for retrieving protein - protein
        associations for a species defined by 'species_id'.
        """

        query = """
            SELECT node_node_links.node_id_a, node_node_links.node_id_b,
                   node_node_links.combined_score,
                   node_node_links.evidence_scores
            FROM network.node_node_links AS node_node_links
            JOIN items.proteins AS proteins ON proteins.protein_id = node_node_links.node_id_a
            WHERE proteins.species_id = %s AND
                  node_id_a < node_id_b;
        """

        params = (species_id,)

        return query, params

    @staticmethod
    def actions_query(species_id):
        """
        Builds an SQL query for retrieving protein - protein
        actions for a species defined by 'species_id'.
        """

        query = """
            SELECT item_id_a,
                   item_id_b,
                   mode,
                   score
            FROM network.actions AS actions
            JOIN items.proteins AS proteins ON actions.item_id_a = proteins.protein_id
            WHERE proteins.species_id = %s AND
                  item_id_a < item_id_b;
        """

        params = (species_id,)

        return query, params

    @staticmethod
    def species_id_query(compact_species_name):
        """
        Builds an SQL query for retrieving species ID
        from a species name ('compact_species_name').
        """

        query = """
            SELECT species_id
            FROM items.species
            WHERE UPPER(compact_name) = UPPER(%s);
        """

        params = (compact_species_name,)

        return query, params


def get_proteins(postgres_connection, species_id):
    """
    Queries the database specified by postgres_connection and for each protein
    yields the following:
    - internal id
    - external_id
    - preferred name
    - annotation
    """

    cursor = postgres_connection.cursor(name="proteins")
    query, params = QueryBuilder.proteins_query(species_id)
    cursor.execute(query, params)

    while True:
        rows = cursor.fetchmany(size=4096)
        if not rows: # if rows is empty
            break

        for row in rows:
            yield {
                "id": row[0],
                "external_id": row[1],
                "preferred_name": row[2],
                "annotation": row[3].strip()
            }

    cursor.close()

def get_associations(postgres_connection, species_id):
    """
    Queries the database specified by postgres_connection and for each pair
    of proteins yields an association, i.e.:
    - internal ids
    - combined score
    - scores per evidence channels
    """

    cursor = postgres_connection.cursor(name="associations")
    query, params = QueryBuilder.associations_query(species_id)
    cursor.execute(query, params)

    while True:
        rows = cursor.fetchmany(size=4096)
        if not rows: # if rows is empty
            break

        for row in rows:
            yield {
                "id1": row[0],
                "id2": row[1],
                "combined_score": row[2],
                "evidence_scores": row[3]
            }

    cursor.close()

def get_actions(postgres_connection, species_id):
    """
    Queries the database specified by postgres_connection and for each pair
    of proteins yields an action, i.e.:
    - internal ids
    - mode (activation, binding, catalysis etc.)
    - score
    """

    cursor = postgres_connection.cursor(name="actions")
    query, params = QueryBuilder.actions_query(species_id)
    cursor.execute(query, params)

    while True:
        rows = cursor.fetchmany(size=4096)
        if not rows: # if rows is empty
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
    return species_id[0] if species_id is not None else None
