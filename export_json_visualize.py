
import json
import argparse
import copy
import networkx as nx
from networkx.readwrite import json_graph

import database
import cypher_queries as Cypher

def neo4j_to_json(neo4j_data):
    # Build a networkx graph
    G = nx.Graph()
    for entry in neo4j_data:
        G.add_node(entry["protein"]["id"], **entry["protein"])
        G.add_node(entry["other"]["id"], **entry["other"])
        G.add_edge(entry["protein"]["id"], entry["other"]["id"], **entry["association"])

        if "action" in entry:
            action_id = str(entry["protein"]["id"]) + entry["action"]["mode"] + str(entry["other"]["id"])
            G.add_node(action_id, **entry["action"])
            G.add_edge(entry["protein"]["id"], action_id)
            G.add_edge(entry["other"]["id"], action_id)

            if "pathway" in entry:
                G.add_node(entry["pathway"]["set_id"], **entry["pathway"])
                G.add_edge(entry["pathway"]["set_id"], action_id)

    # Add node positions
    # pos = nx.spring_layout(G)

    # for n in G:
    #     x, y = pos[n]
    #     G.node[n]["x"] = x
    #     G.node[n]["y"] = y

    # Convert the networkx graph to JSON
    return json_graph.node_link_data(G)

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

    # Export graph JSON that can be read to visualize it
    data = neo4j_to_json(subgraph)
    with open("visualize/subgraph.json", "w") as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":
    main()
