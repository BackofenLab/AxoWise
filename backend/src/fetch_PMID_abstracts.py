import os

import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
# set config
NEO4J_HOST = os.getenv("NEO4J_HOST")
NEO4J_PORT = os.getenv("NEO4J_PORT")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
# connect
uri = f"bolt://{NEO4J_HOST}:{NEO4J_PORT}"

# Create a Neo4j driver instance
driver = GraphDatabase.driver(uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


# Function to execute a query
def run_query(query):
    with driver.session() as session:
        res = session.run(query)
        return res.data()


# Create a Neo4j driver instance
driver = GraphDatabase.driver(uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
query = """match(n:abstract) return n.PMID as PMID, n.abstract as abstract"""
results = run_query(query)


# Create csv file of PMIDS, Abstracts
df = pd.DataFrame(results)
df.to_csv("PMID_abstracts.csv", index=False)
print("Completed fetching Abstracts")
driver.close()
