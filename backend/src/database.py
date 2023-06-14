"""
Connection interface towards the PostgreSQL and Neo4j databases.
"""

from pathlib import Path

import neo4j
from flask import g
from neo4j import GraphDatabase

_DEFAULT_CREDENTIALS_PATH = Path(__file__).parent / Path("../../credentials.yml")


def get_driver() -> neo4j.Driver:
    if "db" not in g:
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "pgdb"
        g.db = GraphDatabase.driver(uri, auth=(username, password))
    return g.db
