
import json
import psycopg2
import py2neo

def connect(credentials_path = "credentials.json"):
    with open(credentials_path, "rt", encoding = "utf-8") as credentials_file:
        credentials = json.load(credentials_file)
    
    postgres = credentials["postgres"]
    neo4j = credentials["neo4j"]

    # Connect to the PostgreSQL database
    postgres_connection = psycopg2.connect(
        dbname = postgres["database"],
        user = postgres["user"],
        password = postgres["pw"],
        port = postgres["port"],
        host = postgres["host"]
    )
    postgres_cursor = postgres_connection.cursor()

    # Connect to the Neo4j database
    neo4j_graph = py2neo.Graph(
        host = neo4j["host"],
        https_port = neo4j["port"],
        password = neo4j["pw"]
    )

    return (postgres_connection, postgres_cursor), neo4j_graph
