"""
Connection interface towards the Neo4j databases.
"""
from pathlib import Path
from typing import Any

import neo4j
import yaml
from flask import g

_CONFIG_PATH = Path(__file__).parent / Path("../../config.yml")


def get_driver() -> neo4j.Driver:
    """
    :return: neo4j-driver object that is needed when calling functions of `queries.py`
    """
    if "db" not in g:
        # read config
        config = _get_neo4j_config(_CONFIG_PATH)
        # set config
        uri = f'bolt://{config["host"]}:{config["port"]}'
        username = config["username"]
        password = config["password"]
        # connect
        g.db = neo4j.GraphDatabase.driver(uri, auth=(username, password))
    return g.db


def _get_neo4j_config(path: Path) -> dict[str, Any]:
    with open(path, "rt", encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config["neo4j"]
