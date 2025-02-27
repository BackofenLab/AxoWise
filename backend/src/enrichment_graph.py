import io
import json
import os

import database
import graph
import jar
import pandas as pd
import queries
from dotenv import load_dotenv
from util.stopwatch import Stopwatch

# =============== Functional Term Graph ======================

# Load .env file
load_dotenv()
_BACKEND_JAR_PATH = os.getenv("_BACKEND_JAR_PATH")


def get_functional_graph(list_enrichment, species_id):
    stopwatch = Stopwatch()

    list_term = []
    if list_enrichment is not None:
        list_term = [i["id"] for i in list_enrichment]

    driver = database.get_driver()

    # Execute the query and retrieve the CSV data
    edges = pd.DataFrame(queries.connected_terms(driver, list_term, species_id))

    stopwatch.round("Neo4j")

    if len(edges) == 0:
        return

    nodes = pd.DataFrame(list_enrichment).rename(columns={"id": "external_id"}).drop_duplicates(subset="external_id")
    # Create nk_graph and needed stats
    nk_graph, node_mapping = graph.nk_graph(nodes, edges)
    pagerank = graph.pagerank(nk_graph)
    betweenness = graph.betweenness(nk_graph)
    ec = graph.eigenvector_centrality(nk_graph)

    # ____________________________________________________________

    # no data from database, return from here
    # TO-DO Front end response to be handled
    if edges.empty:
        return json.dumps([])

    # Creating only the main Graph and exclude not connected subgraphs
    nodes_sub = graph.create_nodes_subgraph(nk_graph, nodes)

    stopwatch.round("Enrichment")

    if len(nodes.index) == 0:
        sigmajs_data = {"nodes": [], "edges": []}
    else:
        # Build a standard input string for Gephi's backend
        nodes_csv = io.StringIO()
        edges_csv = io.StringIO()

        # JAR accepts only id
        nodes["external_id"].to_csv(nodes_csv, index=False, header=True)

        # JAR accepts source, target, score
        edges.to_csv(edges_csv, index=False, header=True)

        stdin = f"{nodes_csv.getvalue()}\n{edges_csv.getvalue()}"
        stdout = jar.pipe_call(_BACKEND_JAR_PATH, stdin)

        sigmajs_data = json.loads(stdout)

    stopwatch.round("Gephi")

    # Create a dictionary mapping ENSEMBL IDs to rows in `nodes`
    ensembl_to_node = dict(zip(nodes["external_id"], nodes.itertuples(index=False)))

    for node in sigmajs_data["nodes"]:
        ensembl_id = node["id"]
        df_node = ensembl_to_node.get(ensembl_id)
        if df_node:
            if ensembl_id in node_mapping:
                mapped_node_id = node_mapping[ensembl_id]
                # Use node mapping to add corresponding values of betweenness and pagerank
                node["attributes"]["Eigenvector Centrality"] = str(ec[mapped_node_id])
                node["attributes"]["Betweenness Centrality"] = str(betweenness[mapped_node_id])
                node["attributes"]["PageRank"] = str(pagerank[mapped_node_id])
            node["attributes"]["Ensembl ID"] = df_node.external_id
            node["attributes"]["Name"] = df_node.name
            node["label"] = df_node.name  # Comment this out if you want no node labels displayed
            node["attributes"]["Category"] = df_node.category
            node["attributes"]["FDR"] = df_node.fdr_rate
            node["attributes"]["P Value"] = df_node.p_value

    sub_proteins = []
    ensembl_sub = set(nodes_sub["external_id"])
    for node in sigmajs_data["nodes"]:
        if node["attributes"]["Ensembl ID"] in ensembl_sub:
            sub_proteins.append(node["attributes"]["Ensembl ID"])
        else:
            node["color"] = "rgb(255,255,153)"

    for edge in sigmajs_data["edges"]:
        if edge["source"] not in ensembl_sub and edge["target"] not in ensembl_sub:
            edge["color"] = "rgba(255,255,153,0.2)"

    sigmajs_data["subgraph"] = sub_proteins

    stopwatch.round("End")
    stopwatch.total("get_functional_graph")

    return json.dumps(sigmajs_data)
