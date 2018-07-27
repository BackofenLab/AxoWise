import psycopg2
import py2neo

import sql_queries as SQL
import cypher_queries as Cypher
from connect_db import connect

# Connect to the databases
postgres, neo4j_graph = connect()
postgres_connection, postgres_cursor = postgres

# STRING
print("Reading the STRING database...")
species_id = SQL.get_species_id(postgres_cursor, "Mus musculus")[0]
relationships = SQL.get_relationships(postgres_cursor, species_id = species_id, limit = 1000)

# Neo4j
Cypher.delete_all(neo4j_graph)

print("Writing to the Neo4j database...")
for progress, item in relationships:
    print("{:6.2f} %".format(progress * 100), end = "\r")
    Cypher.update_proteins_and_action(neo4j_graph, item)
print()

Cypher.remove_redundant_properties(neo4j_graph)

print("Done!")

postgres_cursor.close()
postgres_connection.close()