import psycopg2
import py2neo

from queries import get_pathways

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
results = get_pathways(postgre_cursor, protein1 = "Ccr5", protein2 = "Ccl5")
for row in results:
    print(row)

# Close communication with the database
postgre_cursor.close()
postgre_connection.close()
