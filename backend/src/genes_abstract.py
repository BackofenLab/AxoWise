import os

import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase
from summarization.meilisearch_inhouse import meilisearch_query


def neo4j_driver():
    load_dotenv()
    # set config
    NEO4J_HOST = os.getenv("NEO4J_HOST")
    NEO4J_PORT = os.getenv("NEO4J_PORT")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    # connect
    print(NEO4J_HOST)
    uri = f"bolt://{NEO4J_HOST}:{NEO4J_PORT}"
    # Create a Neo4j driver instance
    driver = GraphDatabase.driver(uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    return driver


# Function to execute a query
def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        # Close the driver connection when done
        return [record for record in result]


def format_and_save_df(genes):
    # Dataframe of mouse and human genes
    df = pd.DataFrame({"symbol": genes})

    # Drop duplicates that occur due to mixing of multiple organisms
    df = df.drop_duplicates(subset="symbol", keep="first")

    # Export the Dataframe
    df.to_csv("genes.csv", index=False)
    return df


def create_gene_abstracts(df, chunk_size=100000):
    genes_for_csv = []
    abstracts = []
    file_index = 0

    for i in list(df["symbol"]):
        res = meilisearch_query.get_results(100000000, i)["hits"]
        genes_for_csv.extend([i] * len(res))
        for j in res:
            abstracts.append(j)

        # Check if the current chunk size has been reached
        if len(genes_for_csv) >= chunk_size:
            # Create a DataFrame for the current chunk
            genes_abstracts_df = pd.DataFrame({"symbol": genes_for_csv, "abstracts": abstracts})

            # Write the DataFrame to a CSV file
            genes_abstracts_df.to_csv(f"genes_abstracts_{file_index}.gz", index=False)

            # Increment file index and reset lists
            file_index += 1
            genes_for_csv = []
            abstracts = []

    # Handle any remaining rows not written to file
    if genes_for_csv:
        genes_abstracts_df = pd.DataFrame({"symbol": genes_for_csv, "abstracts": abstracts})
        genes_abstracts_df.to_csv(f"genes_abstracts_{file_index}.gz", index=False)


driver = neo4j_driver()
query = "MATCH (p:TG) RETURN p.SYMBOL AS symbol"
results = run_query(driver, query)
driver.close()
genes = [i["symbol"] for i in results]
df = format_and_save_df(genes)
create_gene_abstracts(df)
