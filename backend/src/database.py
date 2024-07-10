"""
Connection interface towards the Neo4j databases.
"""

import os

import neo4j
from dotenv import load_dotenv
from flask import g


def get_driver() -> neo4j.Driver:
    """
    :return: neo4j-driver object that is needed when calling functions of `queries.py`
    """
    if "db" not in g:
        # Load environment variables from .env file
        load_dotenv()

        # set config
        NEO4J_HOST = os.getenv("NEO4J_HOST")
        NEO4J_PORT = os.getenv("NEO4J_PORT")
        NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
        NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
        # connect
        uri = f"bolt://{NEO4J_HOST}:{NEO4J_PORT}"
        g.db = neo4j.GraphDatabase.driver(uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    return g.db
