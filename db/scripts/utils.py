import pandas as pd
from neo4j import GraphDatabase, RoutingControl


class Reformatter:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def run(self, input: str, mode: str):
        if mode == "tf":
            return self.run_timeframes(input=input)

    def run_timeframes(self, input: str):
        s = input.replace(self.prefix, "").split(sep="_")
        return "-".join([p.replace("wt", "") for p in s])


def read_creds():
    # TODO: Read Creds yaml
    return "neo4j://localhost:7687", ("neo4j", "pgdb")


def execute_query(query: str, read: bool):
    uri, auth = read_creds()
    with GraphDatabase.driver(uri, auth=auth) as driver:
        if not read:
            return driver.execute_query(query)
        else:
            return driver.execute_query(query, RoutingControl.READ)
