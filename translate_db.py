import psycopg2
import py2neo

import sql_queries as SQL
import cypher_queries as Cypher
from connect_db import connect

# Connect to the databases
postgres, neo4j_graph = connect()
postgres_connection, postgres_cursor = postgres

# Read the STRING database
species_id = SQL.get_species_id(postgres_cursor, "Mus musculus")[0]
relationships = SQL.get_relationships(postgres_cursor, species_id = species_id, limit = 100)

Cypher.delete_all(neo4j_graph)
for idx, item in enumerate(relationships):
    # Create proteins if they do not exist
    Cypher.update_proteins_and_action(neo4j_graph, item)

Cypher.remove_redundant_properties(neo4j_graph)

# Close communication with the database
postgres_cursor.close()
postgres_cursor.close()
