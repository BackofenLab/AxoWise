
import argparse
import plotly.plotly as plotly

import database
import cypher_queries as Cypher

def main():
    # Parse CLI arguments
    args_parser = argparse.ArgumentParser(
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )

    args_parser.add_argument(
        "--protein",
        type = str,
        help = "Protein for which a subgraph will be visualized",
        default = "Ccr5"
    )

    args_parser.add_argument(
        "--credentials",
        type = str,
        help = "Path to the credentials JSON file that will be used",
        default = "credentials.json"
    )

    args = args_parser.parse_args()

    # Connect to the databases
    postgres_connection, neo4j_graph = database.connect(credentials_path = args.credentials)
    postgres_connection.close()

    subgraph = Cypher.get_protein_subgraph(neo4j_graph, args.protein)

    # TODO Use plotly to visualize a protein network

if __name__ == "__main__":
    main()
