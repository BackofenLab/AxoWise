import psycopg2
import py2neo

import sql_queries as SQL
import cypher_queries as Cypher

# Connect to the PostgreSQL database
postgre_connection = psycopg2.connect(
    dbname = "string",
    user = "borna",
    password = "borna",
    port = 5432,
    host = "/var/run/postgresql"
)
postgre_cursor = postgre_connection.cursor()

# Connect to the Neo4j database
graph = py2neo.Graph(password = "cgdb")

# Read the STRING database
species_id = SQL.get_species_id(postgre_cursor, "Mus musculus")[0]
relationships = SQL.get_relationships(postgre_cursor, species_id = species_id, limit = 10000)

Cypher.delete_all(graph)
for idx, item in enumerate(relationships):
    # Create proteins if they do not exist
    Cypher.update_proteins_and_action(graph, item)

Cypher.remove_redundant_properties(graph)

# Close communication with the database
postgre_cursor.close()
postgre_connection.close()
