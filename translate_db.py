import psycopg2
import py2neo

import sql_queries as SQL
import cypher_queries as Cypher
from connect_db import connect

# Connect to the databases
postgres_connection, neo4j_graph = connect()

# Declare a client-side cursor
default_cursor = postgres_connection.cursor()

# Declare a server-side cursor
relationships_cursor = postgres_connection.cursor(name = "server")

# STRING
print("Reading the STRING database...")
species_id = SQL.get_species_id(default_cursor, "Mus musculus")[0]
relationships = SQL.get_relationships(relationships_cursor, species_id = species_id, limit = 1000)

# Neo4j
Cypher.delete_all(neo4j_graph)

print("Writing to the Neo4j database...")
for idx, item in enumerate(relationships):
    print("{}".format(idx + 1), end = "\r")
    Cypher.update_proteins_and_action(neo4j_graph, item)
print()

Cypher.remove_redundant_properties(neo4j_graph)

print("Done!")

default_cursor.close()
relationships_cursor.close()
postgres_connection.close()