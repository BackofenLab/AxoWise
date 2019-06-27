import json
import os.path
import io
from collections import defaultdict

import networkx as nx
from flask import Flask, Response, request, send_from_directory
from networkx.readwrite import json_graph
import pandas as pd
import jar
import stringdb

import cypher_queries as Cypher
import database
import fuzzy_search
from layout import shell_layout

app = Flask(__name__)

# ====================== Index page ======================

_SCRIPT_DIR = os.path.dirname(__file__)
_SERVE_DIR = "frontend"
_INDEX_FILE = "index.html"
_BACKEND_JAR_PATH = "gephi-backend/out/artifacts/gephi_backend_jar/gephi.backend.jar"

@app.route("/")
def index():
    return send_from_directory(os.path.join(_SCRIPT_DIR, _SERVE_DIR), _INDEX_FILE)

# ====================== Other files ======================

@app.route("/<path:path>")
def files(path):
    return send_from_directory(os.path.join(_SCRIPT_DIR, _SERVE_DIR), path)

# ====================== Subgraph API ======================

# TODO Refactor this
@app.route("/api/subgraph/proteins", methods=["POST"])
def proteins_subgraph_api():
    # Queried proteins
    query_proteins = request.form.get("proteins").split(";")
    query_proteins = list(filter(None, query_proteins))

    # Species
    species_id = int(request.form.get("species_id"))

    # Threshold
    threshold = int(float(request.form.get("threshold")) * 1000)

    # Fuzzy search mapping
    proteins = fuzzy_search.search_protein_list(query_proteins, species_id=species_id)
    protein_ids = list(map(lambda p: p.id, proteins))

    # Query the database
    query = """
        MATCH (source:Protein)-[association:ASSOCIATION]->(target:Protein)
        WHERE source.id IN {protein_ids} AND target.id IN {protein_ids} AND association.combined >= {threshold}
        RETURN source, target, association.combined AS score
    """

    param_dict = dict(
        protein_ids=protein_ids,
        threshold=threshold
    )

    data = database.neo4j_graph.data(query, param_dict)

    # pandas DataFrames for nodes and edges
    proteins = set()
    source, target, score = list(), list(), list()
    for row in data:
        source.append(row["source"]["id"])
        target.append(row["target"]["id"])
        score.append(row["score"])
        proteins.add(row["source"])
        proteins.add(row["target"])

    proteins = list(map(dict, proteins))

    nodes = pd.DataFrame(proteins)
    nodes = nodes.drop_duplicates(subset="id") # TODO `nodes` can be empty

    edges = pd.DataFrame({
        "source": source,
        "target": target,
        "score": score
    })
    edges = edges.drop_duplicates(subset=["source", "target"]) # TODO edges` can be empty

    # Functional enrichment
    external_ids = nodes["external_id"].tolist()
    df_enrichment = stringdb.functional_enrichment(external_ids, species_id)

    list_enrichment = list()
    for _, row in df_enrichment.iterrows():
        list_enrichment.append(dict(
            id=row["term"],
            proteins=row["inputGenes"].split(","),
            name=row["description"],
            p_value=row["p_value"]
        ))

    if len(nodes.index) == 0:
        sigmajs_data = {
            "nodes": [],
            "edges": []
        }
    else:
        # Build a standard input string for Gephi's backend
        nodes_csv = io.StringIO()
        edges_csv = io.StringIO()

        # JAR accepts only id
        nodes["id"].to_csv(nodes_csv, index=False, header=True)
        # JAR accepts source, target, score
        edges.to_csv(edges_csv, index=False, header=True)

        stdin = f"{nodes_csv.getvalue()}\n{edges_csv.getvalue()}"
        stdout = jar.pipe_call(_BACKEND_JAR_PATH, stdin)

        sigmajs_data = json.loads(stdout)

    for node in sigmajs_data["nodes"]:
        df_node = nodes[nodes["id"] == int(node["id"])].iloc[0]
        node["attributes"]["Description"] = df_node["description"]
        node["attributes"]["Ensembl ID"] = df_node["external_id"]
        node["attributes"]["Name"] = df_node["name"]
        node["label"] = df_node["name"]

    sigmajs_data["enrichment"] = list_enrichment

    json_str = json.dumps(sigmajs_data)

    return Response(json_str, mimetype="application/json")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )
