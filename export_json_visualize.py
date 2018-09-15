
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
        entry["protein"]["type"] = "protein"
        G.add_node(entry["protein"]["id"], **entry["protein"])

        if entry["other"] is not None:
            entry["other"]["type"] = "protein"
            G.add_node(entry["other"]["id"], **entry["other"])
            G.add_edge(entry["protein"]["id"], entry["other"]["id"], **entry["association"])

        if entry["action"] is not None:
            entry["action"]["type"] = "action"
            action_id = str(entry["protein"]["id"]) + entry["action"]["mode"] + str(entry["other"]["id"])
            G.add_node(action_id, **entry["action"])
            G.add_edge(entry["protein"]["id"], action_id)
            G.add_edge(entry["other"]["id"], action_id)

        if entry["pathway"] is not None:
            entry["pathway"]["type"] = "pathway"
            G.add_node(entry["pathway"]["id"], **entry["pathway"])
            G.add_edge(entry["pathway"]["id"], entry["protein"]["id"])
            G.add_edge(entry["pathway"]["id"], entry["other"]["id"])

            if entry["drug"] is not None:
                entry["drug"]["type"] = "drug"
                G.add_node(entry["drug"]["id"], **entry["drug"])
                G.add_edge(entry["drug"]["id"], entry["pathway"]["id"])

            if entry["disease"] is not None:
                entry["disease"]["type"] = "disease"
                G.add_node(entry["disease"]["id"], **entry["disease"])
                G.add_edge(entry["disease"]["id"], entry["pathway"]["id"])

            if entry["compound"] is not None:
                entry["compound"]["type"] = "compound"
                G.add_node(entry["compound"]["id"], **entry["compound"])
                G.add_edge(entry["compound"]["id"], entry["pathway"]["id"])

    # Add node positions
    pos = nx.spring_layout(G)

    for n in G:
        x, y = pos[n]
        G.node[n]["x"] = x
        G.node[n]["y"] = y

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
