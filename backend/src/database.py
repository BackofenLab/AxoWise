"""
Connection interface towards the PostgreSQL and Neo4j databases.
"""

from pathlib import Path

import psycopg2
import py2neo
import yaml
from neo4j import GraphDatabase, Neo4jDriver

from flask import g, current_app

_DEFAULT_CREDENTIALS_PATH = Path(__file__).parent / Path("../../credentials.yml")

neo4j_graph = None
postgres_connection = None


def get_driver() -> Neo4jDriver:
    if "db" not in g:
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "pgdb"
        g.db = GraphDatabase.driver(uri, auth=(username, password))
    return g.db


def connect_neo4j(credentials_path=_DEFAULT_CREDENTIALS_PATH):
    """
    Connects to the Neo4j database described in credentials
    file ('credentials_path') and returns a 'Graph' object.
    """
    global neo4j_graph

    with open(credentials_path, "rt", encoding="utf-8") as credentials_file:
        credentials = yaml.load(credentials_file, Loader=yaml.FullLoader)

    neo4j = credentials["neo4j"]

    # Connect to the Neo4j database
    neo4j_graph = py2neo.Graph(host=neo4j["host"], port=neo4j["port"], password=neo4j["pw"], scheme="bolt")

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
    global postgres_connection

    with open(credentials_path, "rt", encoding="utf-8") as credentials_file:
        credentials = yaml.load(credentials_file, Loader=yaml.FullLoader)

    postgres = credentials["postgres"]

    # Connect to the PostgreSQL database
    postgres_connection = psycopg2.connect(
        dbname=postgres["database"],
        user=postgres["user"],
        password=postgres["pw"],
        port=postgres["port"],
        host=postgres["host"],
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
    global neo4j_graph, postgres_connection

    postgres_connection = connect_postgres(credentials_path)
    neo4j_graph = connect_neo4j(credentials_path)
    return postgres_connection, neo4j_graph
