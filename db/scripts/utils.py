import pandas as pd
import yaml
from neo4j import GraphDatabase, RoutingControl
from main import _DEFAULT_CREDENTIALS_PATH


class Reformatter:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def run(self, input: str, mode: str):
        if mode == "tf":
            return self.run_timeframes(input=input)

    def run_timeframes(self, input: str):
        s = input.replace(self.prefix, "").split(sep="_")
        return "-".join([p.replace("wt", "") for p in s])


def read_creds(credentials_path=_DEFAULT_CREDENTIALS_PATH):
    with open(credentials_path, "rt", encoding="utf-8") as credentials_file:
        credentials = yaml.load(credentials_file, Loader=yaml.FullLoader)

    neo4j = credentials["neo4j"]
    return "neo4j://{}:{}".format(neo4j["host"], neo4j["port"]), ("neo4j", neo4j["pw"])


def execute_query(query: str, read: bool):
    uri, auth = read_creds()
    with GraphDatabase.driver(uri, auth=auth) as driver:
        if not read:
            return driver.execute_query(query)
        else:
            return driver.execute_query(query, RoutingControl.READ)
