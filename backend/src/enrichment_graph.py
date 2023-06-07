import csv
import io
import json
import os
import sys
import time
import uuid
import subprocess
import pandas as pd
import jar
import graph_utilities
import database

# =============== Functional Term Graph ======================

_BACKEND_JAR_PATH = "../gephi/target/gephi.backend-1.0-SNAPSHOT.jar"


def get_functional_graph(list_enrichment):
    t_begin = time.time()

    list_term = []
    if list_enrichment is not None:
        list_term = [i["id"] for i in list_enrichment]

    driver = database.get_driver()

    # Execute the query and retrieve the CSV data
    with driver.session() as session:
        query = f"""
            MATCH (source:Terms)-[association:KAPPA]->(target:Terms)
            WHERE source.external_id IN {str(list_term)} 
            AND target.external_id IN {str(list_term)}
            RETURN source, target, association.score AS score;
            """
        result = session.run(query)
        terms, source, target, score = list(), list(), list(), list()

        return query

    query = create_query_assoc()


    with open("/tmp/query"+repr(filename)+".txt", "w") as query_text:
        query_text.write("%s" % query)

    #Timer to evaluate runtime to setup
    t_setup = time.time()
    print("Time Spent (Setup_Terms):", t_setup-t_begin)

    #Run the cypher query in cypher shell via terminal
    # TODO: change to credentials.yml
    data = subprocess.run(
        ["cypher-shell",
         "-a", "bolt://localhost:7687",
         "-u", "neo4j",
         "-p", "pgdb",
         "-f", "/tmp/query"+repr(filename)+".txt"],
        capture_output=True,
        encoding="utf-8"
    )
    os.remove('/tmp/query'+repr(filename)+'.txt')
    #Check standard output 'stdout' whether it's empty to control errors
    if not data.stdout:
        raise Exception(data.stderr)

    #Timer for Neo4j query
    t_neo4j = time.time()
    print("Time Spent (Neo4j):", t_neo4j-t_setup)

    #pandas DataFrames for nodes and edges
    csv.field_size_limit(sys.maxsize)
    terms = list()
    source, target, score, assoc_names = list(), list(), list(), list()
    with open('/tmp/'+repr(filename)+'.csv', newline='') as f:
        for row in csv.DictReader(f):
            source_row_prop = json.loads(row['source'])['properties']
            target_row_prop = json.loads(row['target'])['properties']
        for row in result:
            source_row_prop = row["source"]
            target_row_prop = row["target"]
            terms.append(source_row_prop)
            terms.append(target_row_prop)
            source.append(source_row_prop.get("external_id"))
            target.append(target_row_prop.get("external_id"))
            score.append(float(row["score"]))

    # Timer for Neo4j query
    t_neo4j = time.time()
    print("Time Spent (Neo4j):", t_neo4j - t_begin)

    nodes = pd.DataFrame(terms).drop_duplicates(subset="external_id")

    nodesterm = pd.DataFrame(list_enrichment)

    df2 = nodesterm.rename({"id": "external_id"}, axis=1)
    merged = pd.merge(df2[["external_id", "fdr_rate", "p_value"]], nodes, on="external_id")

    # Add the two columns to df2
    nodes = merged

    nodes["fdr_rate"] = nodes["fdr_rate"].fillna(0)
    nodes["p_value"] = nodes["p_value"].fillna(0)

    edges = pd.DataFrame({"source": source, "target": target, "score": score})
    edges = edges.drop_duplicates(subset=["source", "target"])  # TODO edges` can be empty

    # convert kappa scores to Integer

    edges["score"] = edges["score"].apply(lambda x: round(x, 2))
    edges["score"] = edges["score"].apply(lambda x: int(x * 100))

    # ____________________________________________________________

    # no data from database, return from here
    # TO-DO Front end response to be handled
    if edges.empty:
        return json.dumps([])

    # Creating only the main Graph and exclude not connected subgraphs
    nodes_sub = graph_utilities.create_nodes_subgraph(edges, nodes)
    # edges = graph_utilities.create_edges_subgraph(edges)

    # Timer to evaluate runtime between cypher-shell and extracting data

    # #Timer to evaluate enrichments runtime
    t_enrich = time.time()
    print("Time Spent (Enrichment):", t_enrich - t_neo4j)

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

    # Timer to evaluate runtime of calling gephi
    t_gephi = time.time()
    print("Time Spent (Gephi):", t_gephi - t_enrich)

    # Create a dictionary mapping ENSEMBL IDs to rows in `nodes`
    ensembl_to_node = dict(zip(nodes["external_id"], nodes.itertuples(index=False)))

    for node in sigmajs_data["nodes"]:
        ensembl_id = node["id"]
        df_node = ensembl_to_node.get(ensembl_id)
        if df_node:
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

    # Timer for final steps
    t_end = time.time()
    print("Time Spent (End):", t_end - t_gephi)

    return json.dumps(sigmajs_data)
