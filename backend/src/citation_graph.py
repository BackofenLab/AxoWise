import io
import json

import pandas as pd

import database
import graph
import jar
import queries
from util.stopwatch import Stopwatch

# =============== Functional Term Graph ======================

_BACKEND_JAR_PATH = "../gephi/target/gephi.backend-1.0-SNAPSHOT.jar"


def get_citation_graph(nodes, edges):
    stopwatch = Stopwatch()

    nodes_df = pd.DataFrame(nodes).drop_duplicates(subset="external_id")
    edges_df = pd.DataFrame(edges)

    if edges_df.empty:
        return json.dumps([])

    # Create nk_graph and needed stats
    nk_graph, node_mapping = graph.nk_graph(nodes_df, edges_df)
    pagerank = graph.pagerank(nk_graph)
    betweenness = graph.betweenness(nk_graph)
    ec = graph.eigenvector_centrality(nk_graph)

    # ____________________________________________________________

    # no data from database, return from here
    # TO-DO Front end response to be handled

    # Creating only the main Graph and exclude not connected subgraphs
    nodes_sub = graph.create_nodes_subgraph(nk_graph, nodes_df)

    stopwatch.round("Enrichment")

    if len(nodes_df.index) == 0:
        sigmajs_data = {"nodes": [], "edges": []}
    else:
        # Build a standard input string for Gephi's backend
        nodes_csv = io.StringIO()
        edges_csv = io.StringIO()

        # JAR accepts only id
        nodes_df["external_id"].to_csv(nodes_csv, index=False, header=True)

        # JAR accepts source, target, score
        edges_df.to_csv(edges_csv, index=False, header=True)

        stdin = f"{nodes_csv.getvalue()}\n{edges_csv.getvalue()}"
        stdout = jar.pipe_call(_BACKEND_JAR_PATH, stdin)

        sigmajs_data = json.loads(stdout)

    stopwatch.round("Gephi")

    # Create a dictionary mapping ENSEMBL IDs to rows in `nodes`
    ensembl_to_node = dict(zip(nodes_df["external_id"], nodes_df.itertuples(index=False)))

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
            node["label"] = df_node.external_id  # Comment this out if you want no node labels displayed
            node["attributes"]["Abstract"] = df_node.abstract
            node["attributes"]["Year"] = df_node.year
            node["attributes"]["Citation"] = df_node.cited_by
            node["attributes"]["Title"] = df_node.title

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
