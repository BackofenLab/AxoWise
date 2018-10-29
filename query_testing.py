
import time
import database
import argparse
import cypher_queries as Cypher

def time_query(neo4j_graph, query):
    start = time.time()
    cursor = neo4j_graph.run(query)
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

    print("[Protein - Protein - Pathway query]")
    num_rows, elapsed_time = time_query(neo4j_graph, query1)
    print(num_rows, "row(s) returned in", elapsed_time, "second(s)")

    print("[Pathway - Compound - Drug - Disease query]")
    num_rows, elapsed_time = time_query(neo4j_graph, query2)
    print(num_rows, "row(s) returned in", elapsed_time, "second(s)")

    print("[Classes - Pathway - Compound - Drug - Disease query]")
    num_rows, elapsed_time = time_query(neo4j_graph, query3)
    print(num_rows, "row(s) returned in", elapsed_time, "second(s)")

if __name__ == "__main__":
    main()