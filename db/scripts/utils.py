import pandas as pd
import yaml
import csv
import os
from time import time
from neo4j import GraphDatabase, RoutingControl, Driver


class Reformatter:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def run(self, input: str, mode: str):
        if mode == "tf":
            return self.run_timeframes(input=input)

    def run_timeframes(self, input: str):
        s = input.replace(self.prefix, "").split(sep="_")
        return "-".join([p.replace("wt", "") for p in s])


def read_creds(credentials_path: str):
    with open(credentials_path, "rt", encoding="utf-8") as credentials_file:
        credentials = yaml.load(credentials_file, Loader=yaml.FullLoader)

    neo4j = credentials["neo4j"]
    return "neo4j://{}:{}".format(neo4j["host"], neo4j["port"]), (neo4j["username"], neo4j["password"])


def start_driver():
    uri, auth = read_creds(credentials_path=os.getenv("_DEFAULT_CREDENTIALS_PATH"))
    driver = GraphDatabase.driver(uri, auth=auth)
    driver.verify_connectivity()
    return driver


def stop_driver(driver: Driver):
    driver.close()


def execute_query(query: str, read: bool, driver: Driver):
    if os.getenv("_UPDATE_NEO4J") == str(True):
        if not read:
            return driver.execute_query(query)
        else:
            return driver.execute_query(query, RoutingControl.READ)
    else:
        print(query)
        return [{"id": 0}], None, None


def save_df_to_csv(file_name: str, df: pd.DataFrame, override_prod: bool = False):
    if os.getenv("_PRODUCTION") == str(True) or override_prod:
        df.to_csv(os.getenv("_NEO4J_IMPORT_PATH") + file_name, index=False)
    else:
        df.iloc[: int(os.getenv("_DEV_MAX_REL"))].to_csv(os.getenv("_NEO4J_IMPORT_PATH") + file_name, index=False)


def time_function(function):
    def timing(**variables):
        start_time = time()
        result = function(**variables)
        end_time = time()
        if os.getenv("_TIME_FUNCTIONS") == str(True):
            with open(os.getenv("_FUNCTION_TIME_PATH"), "a", newline="\n") as csvfile:
                writer = csv.writer(csvfile, delimiter="\t")
                writer.writerow([function.__name__, end_time - start_time])
        return result

    return timing


def print_update(update_type: str, text: str, color: str):
    colors = {
        "orange": "\033[0;33m",
        "blue": "\033[0;34m",
        "pink": "\033[0;35m",
        "cyan": "\033[0;36m",
        "none": "\033[0m",
    }
    if os.getenv("_SILENT") != str(True):
        print("{}{}{}:{}{}".format(colors[color], update_type, colors["none"], " " * (14 - len(update_type)), text))


@time_function
def get_consistent_entries(comparing_genes: pd.DataFrame, complete: pd.DataFrame, mode: int):
    comparing_genes_filter = comparing_genes.filter(items=["ENSEMBL"]).drop_duplicates(ignore_index=True)
    ensembl_genes = complete.filter(items=["ENSEMBL"]).drop_duplicates(ignore_index=True)
    not_included = comparing_genes[
        comparing_genes["ENSEMBL"].isin(set(comparing_genes_filter["ENSEMBL"]).difference(ensembl_genes["ENSEMBL"]))
    ]
    not_included.to_csv(
        "../source/not_included_{}.csv".format("string" if mode == 0 else "exp"), mode="a", header=False, index=False
    )

    return comparing_genes[
        ~comparing_genes["ENSEMBL"].isin(set(comparing_genes["ENSEMBL"]).difference(ensembl_genes["ENSEMBL"]))
    ]
