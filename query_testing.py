
import time
import database
import argparse
import cypher_queries as Cypher

def time_query(neo4j_graph, query, *args):
    start = time.time()
    cursor = query(neo4j_graph, *args)
    num_rows = 0
    for row in cursor:
        num_rows += 1
    end = time.time()
    elapsed_time = end - start
    return num_rows, elapsed_time 

def main():
    args_parser = argparse.ArgumentParser(
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )

    args_parser.add_argument(
        "--credentials",
        type = str,
        help = "Path to the credentials JSON file that will be used",
        default = "test/credentials.test.json"
    )

    args = args_parser.parse_args()

    # Connect to the databases
    postgres_connection, neo4j_graph = database.connect(credentials_path = args.credentials)
    postgres_connection.close()

    query1 = """
        MATCH (pathway:Pathway)<-[:IN]-(p1:Protein {name: "CCR5"})-[p1p2:ASSOCIATION]->(p2:Protein)-[:IN]->(pathway)
        RETURN p1, p2, p1p2, COLLECT(pathway) AS pathways
    """

    query2 = """
        MATCH (pathway:Pathway { name: "Cytokine-cytokine receptor interaction" })<-[:IN]-(other)
        WHERE NOT other:Protein
        RETURN pathway, COLLECT(other) AS compounds_diseases_drugs
    """

    query3 = """
        MATCH (class:Class)<-[:IN*]-(pathway:Pathway { name: "Cytokine-cytokine receptor interaction" })<-[:IN]-(other)
        WHERE NOT other:Protein
        RETURN pathway, COLLECT(other) AS compounds_diseases_drugs, COLLECT(DISTINCT class) AS classes
    """

    print("[Protein-centric query]")
    num_rows, elapsed_time = time_query(neo4j_graph, Cypher.search_protein, "ccr5")
    print(num_rows, "row(s) returned in", elapsed_time, "second(s)")

    print("[Pathway-centric query]")
    num_rows, elapsed_time = time_query(neo4j_graph, Cypher.search_pathway, "chemokine signaling pathway")
    print(num_rows, "row(s) returned in", elapsed_time, "second(s)")

if __name__ == "__main__":
    main()