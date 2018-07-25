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
species_id = SQL.get_species_id(postgre_cursor, "Homo sapiens")[0]
relationships = SQL.get_relationships(postgre_cursor, species_id = species_id)
for item in relationships:
    # Create proteins if they do not exist
    Cypher.update_protein(graph, item["id1"], item["external_id1"], item["annotation1"], item["preferred_name1"])
    Cypher.update_protein(graph, item["id2"], item["external_id2"], item["annotation2"], item["preferred_name2"])

# Close communication with the database
postgre_cursor.close()
postgre_connection.close()
