
import json
import argparse
import copy
import networkx as nx
from networkx.readwrite import json_graph

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

    # Build a networkx graph
    G = nx.Graph()
    for entry in subgraph:
        G.add_node(entry["protein"]["id"], **entry["protein"])
        G.add_node(entry["other"]["id"], **entry["other"])
        G.add_edge(entry["protein"]["id"], entry["other"]["id"], **entry["association"])

        if "action" in entry:
            entry["action"]["id1"] = entry["protein"]["id"]
            entry["action"]["id2"] = entry["other"]["id"]
            G.add_node(entry["action"])
            G.add_edge(entry["protein"]["id"], entry["action"])
            G.add_edge(entry["other"]["id"], entry["action"])

            if "pathway" in entry:
                G.add_node(entry["pathway"]["set_id"], **entry["pathway"])
                G.add_edge(entry["pathway"]["set_id"], entry["action"])

    # Export graph JSON that can be read to visualize it
    data = json_graph.node_link_data(G)
    with open("visualize/subgraph.json", "w") as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":
    main()
