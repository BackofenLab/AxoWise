"""
Connection interface towards the PostgreSQL and Neo4j databases.
"""

import yaml
import psycopg2
import py2neo

_DEFAULT_CREDENTIALS_PATH = "credentials.yml"

def connect_neo4j(credentials_path=_DEFAULT_CREDENTIALS_PATH):
    """
    Connects to the Neo4j database described in credentials
    file ('credentials_path') and returns a 'Graph' object.
    """

    with open(credentials_path, "rt", encoding="utf-8") as credentials_file:
        credentials = yaml.load(credentials_file)

    neo4j = credentials["neo4j"]

    # Connect to the Neo4j database
    neo4j_graph = py2neo.Graph(
        host=neo4j["host"],
        https_port=neo4j["port"],
        password=neo4j["pw"]
    )

    connected = False
    while not connected:
        try:
            neo4j_graph.run("RETURN 0")
            connected = True
        except Exception as e:
            import time
            print(f"{e}. Retrying...")
            time.sleep(10)

    return neo4j_graph

def connect_postgres(credentials_path=_DEFAULT_CREDENTIALS_PATH):
    """
    Connects to the PostgreSQL database described in credentials
    file ('credentials_path') and returns a 'connection' object.
    """

    with open(credentials_path, "rt", encoding="utf-8") as credentials_file:
        credentials = yaml.load(credentials_file)

    postgres = credentials["postgres"]

    # Connect to the PostgreSQL database
    postgres_connection = psycopg2.connect(
        dbname=postgres["database"],
        user=postgres["user"],
        password=postgres["pw"],
        port=postgres["port"],
        host=postgres["host"]
    )

    return postgres_connection

def connect(credentials_path=_DEFAULT_CREDENTIALS_PATH):
    """
    Connects to the PostgreSQL and Neo4j databases described
    in credentials file ('credentials_path').
    Returns:
    - 'connection' object for PostgreSQL database
    - 'Graph' object for Neo4j database
    """

    postgres_connection = connect_postgres(credentials_path)
    neo4j_graph = connect_neo4j(credentials_path)
    return postgres_connection, neo4j_graph
