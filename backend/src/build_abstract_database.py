import glob
import os
import time

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
# set config
NEO4J_HOST = os.getenv("NEO4J_HOST")
NEO4J_PORT = os.getenv("NEO4J_PORT")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")

# URL
uri = f"bolt://{NEO4J_HOST}:{NEO4J_PORT}"

# Create a Neo4j driver instance
driver = GraphDatabase.driver(uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Get the citation file names needed for neo4j
csv_files = glob.glob("/home/maluuck/Documents/genes_abstracts_*.gz")
# csv_files = glob.glob("/mnt/MainBackup/for_graph_RAG/genes_abstracts_*.gz")
csv_files = [i.split("/")[-1] for i in csv_files]


# Function to execute a query
def run_query(query):
    with driver.session() as session:
        session.run(query)


index_query = "CREATE INDEX gene_index FOR (n:TG) ON (n.SYMBOL)"
run_query(index_query)
print("index created")

constraint_query = "CREATE CONSTRAINT ON (n:abstract) ASSERT n.PMID IS UNIQUE"
run_query(constraint_query)
print("constraint created")

# Loop through each file and execute the abstract node creation query
for csv_file in csv_files:
    abstract_time = time.time()
    file_url = f"file:///{csv_file}"  # Construct the correct file URL
    cypher_query = f"""
  CALL apoc.periodic.iterate(
    "LOAD CSV WITH HEADERS FROM '{file_url}' AS row RETURN row",
    "
    WITH row, apoc.convert.fromJsonMap(row.abstracts) AS abstractsMap
    MERGE (n:abstract {{PMID: abstractsMap.`PubMed ID`, title: abstractsMap.Title, published: abstractsMap.Published, abstract: abstractsMap.Abstract, cited_by: abstractsMap.`Cited by`, times_cited: toInteger(abstractsMap.`Cited number`)}})
    RETURN count(*)
    ",
    {{batchSize:1000, parallel:true, retries:10}}
  )
  """
    # Execute the query for the current file
    run_query(cypher_query)
    print(f"Processed abstracts of file: {csv_file} in {time.time()-abstract_time}")

# Loop through each file and execute the Reference creation query
for csv_file in csv_files:
    reference_time = time.time()
    file_url = f"file:///{csv_file}"  # Construct the correct file URL
    cypher_query = f"""
  CALL apoc.periodic.iterate(
    "LOAD CSV WITH HEADERS FROM '{file_url}' AS row RETURN row",
    "
    WITH row, apoc.convert.fromJsonMap(row.abstracts) AS abstractsMap
    MATCH (g:TG {{SYMBOL: row.symbol}})
    MATCH (a:abstract {{PMID: abstractsMap.`PubMed ID`}})
    MERGE (g)-[:REFERENCES]->(a)
    RETURN count(*)
    ",
    {{batchSize:1000, parallel:true, retries:10}}
  )
  """
    # Execute the query for the current file
    run_query(cypher_query)
    print(f"Processed References of file: {csv_file} in {time.time()-reference_time}")

# Loop through each file and execute the cites creation query
for csv_file in csv_files:
    cites_time = time.time()
    file_url = f"file:///{csv_file}"  # Construct the correct file URL
    cypher_query = f"""
  CALL apoc.periodic.iterate(
    "LOAD CSV WITH HEADERS FROM 'file:///genes_abstracts_0.gz' AS row RETURN row",
    "
    WITH row, apoc.convert.fromJsonMap(row.abstracts) AS abstractsMap
    MATCH (a:abstract {{PMID: abstractsMap.`PubMed ID`}})

    // Unpack the 'Cited by' field and convert it to a list
    WITH a, apoc.convert.fromJsonList(abstractsMap.`Cited by`) AS citedByList
    UNWIND citedByList AS citedPMID

    // Match the cited abstracts and create relationships
    MATCH (citedAbstract:abstract {{PMID: citedPMID}})
    MERGE (citedAbstract)-[:CITES]->(a)
    RETURN count(*)
    ",
    {{batchSize:500, parallel:false, retries:10}}
  )
  """
    # Execute the query for the current file
    run_query(cypher_query)
    print(f"Processed citation links of file: {csv_file} in {time.time()-cites_time}")
driver.close()
