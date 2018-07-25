import psycopg2
import py2neo

from queries import get_pathways, get_species_id

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
species_id = get_species_id(postgre_cursor, "Homo sapiens")[0]
pathways = get_pathways(postgre_cursor, species_id = species_id, protein1 = "CCR5", protein2 = "CCL5")
for row in pathways:
    id1, id2, name1, name2, mode, collection_id, title, comment = row
    print(row)

# Close communication with the database
postgre_cursor.close()
postgre_connection.close()
