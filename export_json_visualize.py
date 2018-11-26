
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
        entry["protein1"]["type"] = "protein"
        G.add_node(entry["protein1"]["id"], **entry["protein1"])

        entry["protein2"]["type"] = "protein"
        G.add_node(entry["protein2"]["id"], **entry["protein2"])
        
        G.add_edge(entry["protein1"]["id"], entry["protein2"]["id"], **entry["association"])

        # if entry["action"] is not None:
        #     entry["action"]["type"] = "action"
        #     action_id = str(entry["protein"]["id"]) + entry["action"]["mode"] + str(entry["other"]["id"])
        #     G.add_node(action_id, **entry["action"])
        #     G.add_edge(entry["protein"]["id"], action_id)
        #     G.add_edge(entry["other"]["id"], action_id)

        if entry["pathways"] is not None:
            for pathway in entry["pathways"]:
                pathway["type"] = "pathway"
                G.add_node(pathway["id"], **pathway)
                G.add_edge(pathway["id"], entry["protein1"]["id"])
                G.add_edge(pathway["id"], entry["protein2"]["id"])

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
        "--credentials",
        type = str,
        help = "Path to the credentials JSON file that will be used",
        default = "tests/credentials.test.json"
    )

    args = args_parser.parse_args()

    # Connect to the databases
    postgres_connection, neo4j_graph = database.connect(credentials_path = args.credentials)
    postgres_connection.close()

    subgraph = Cypher.search_proteins(neo4j_graph, [
        "SFPI1",
        "FOSB",
        "MLXIPL",
        "ELK3",
        "FLI1",
        "IL10",
        "IRF1",
        "NFIC",
        "SREBF1",
        "ID2",
        "HIF1A",
        "FOS",
        "MYC",
        "TEF",
        "RUNX1",
        "ATF1",
        "TFEB",
        "BACH1",
        "ATF3",
        "BATF3",
        "BHLHE41",
        "IL10RA",
        "SMAD3",
        "ZFP281",
        "CCL5",
        "CREB3L2",
        "BATF",
        "ERF",
        "KLF9",
        "ZFP691",
        "JUN",
        "KLF7",
        "XBP1",
        "FOXO1",
        "JDP2",
        "CREB1",
        "JUNB",
        "CEBPG",
        "NFIL3",
        "SP100",
        "STAT1",
        "KLF13",
        "EGR1",
        "CEBPB",
        "NFKB2",
        "RXRA",
        "TFE3",
        "ETV5",
        "ETV6",
        "NFE2L1",
        "STAT2",
        "CENPB",
        "RELB",
        "CEBPA",
        "MAFB",
        "SP3",
        "REL",
        "KLF4",
        "BACH2",
        "MAF",
        "ATF4",
        "NFIX",
        "CCR5",
        "IRF9",
        "TGIF1",
        "USF2"
    ])

    # Export graph JSON that can be read to visualize it
    data = neo4j_to_json(subgraph)
    with open("visualize/subgraph.json", "w") as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":
    main()
