import json
import os.path

import networkx as nx
from flask import Flask, Response, request, send_from_directory
from networkx.readwrite import json_graph

import cypher_queries as Cypher
import database
import fuzzy_search
from layout import shell_layout

app = Flask(__name__)

# ====================== Index page ======================

_SCRIPT_DIR = os.path.dirname(__file__)
_SERVE_DIR = "frontend"
_INDEX_FILE = "index.html"

@app.route("/")
def index():
    return send_from_directory(os.path.join(_SCRIPT_DIR, _SERVE_DIR), _INDEX_FILE)

# ====================== Other files ======================

@app.route("/<path:path>")
def files(path):
    return send_from_directory(os.path.join(_SCRIPT_DIR, _SERVE_DIR), path)

# ====================== Fuzzy search API ======================

# Species

def species_to_dict(species):
    return list(map(lambda s: {
        "species_name": s.name,
        "kegg_id": s.kegg_id,
        "ncbi_id": s.ncbi_id
    }, species))

@app.route("/api/search/species", methods=["GET"])
def search_species_api():
    query = request.args.get("query")
    results = fuzzy_search.search_species(query)
    return_object = species_to_dict(results)
    return Response(json.dumps(return_object), mimetype="application/json")

# Protein

def proteins_to_dicts(proteins):
    return list(map(lambda p: {
        "protein_name": p.name,
        "protein_id": p.id,
        "species_id": p.species_id
    }, proteins))

@app.route("/api/search/protein", methods=["GET"])
def search_protein_api():
    query = request.args.get("query")
    species_id = int(request.args.get("species_id"))
    results = fuzzy_search.search_protein(query, species_id)
    return_object = proteins_to_dicts(results)
    return Response(json.dumps(return_object), mimetype="application/json")

# Protein list

@app.route("/api/search/protein_list", methods=["GET"])
def search_protein_list_api():
    query = request.args.get("query")
    protein_list = list(filter(None, query.split(";")))
    species_id = int(request.args.get("species_id"))
    results = fuzzy_search.search_protein_list(protein_list, species_id)
    return_object = proteins_to_dicts(results)
    return Response(json.dumps(return_object), mimetype="application/json")

# Pathway

def pathways_to_dicts(pathways):
    return list(map(lambda p: {
        "pathway_name": p.name,
        "pathway_id": p.id,
        "species_id": p.species_id
    }, pathways))

@app.route("/api/search/pathway", methods=["GET"])
def search_pathway_api():
    query = request.args.get("query")
    species_id = int(request.args.get("species_id"))
    results = fuzzy_search.search_pathway(query, species_id)
    return_object = pathways_to_dicts(results)
    return Response(json.dumps(return_object), mimetype="application/json")

# Class

def classes_to_dicts(classes):
    return list(map(lambda c: {
        "class_name": c.name
    }, classes))    

@app.route("/api/search/class", methods=["GET"])
def search_class_api():
    query = request.args.get("query")
    results = fuzzy_search.search_class(query)
    return_object = classes_to_dicts(results)
    return Response(json.dumps(return_object), mimetype="application/json")

# ====================== Subgraph API ======================
neo4j_graph = database.connect_neo4j()
Cypher.warm_up(neo4j_graph)

def protein_subgraph_to_nx_json(subgraph):
    G = nx.DiGraph()
    if subgraph is None:
        data = json_graph.node_link_data(G)
        return json.dumps(data)

    proteins = []
    pathways = []

    protein = subgraph["protein"]
    G.add_node(
        protein["id"],
        label=protein["name"],
        description=protein["description"],
        type=0 # Protein
    )

    proteins.append(protein["id"])

    for pathway in subgraph["pathways"]:
        G.add_node(
            pathway["id"],
            label=pathway["name"],
            description=pathway["description"],
            type=1 # Pathway
        )
        G.add_edge(
            protein["id"],
            pathway["id"],
            weight=0
        )
        pathways.append(pathway["id"])

    for association in subgraph["associations"]:
        other = association["other"]
        combined_score = association["combined_score"]

        G.add_node(
            other["id"],
            label=other["name"],
            description=other["description"],
            type=0 # Protein
        )

        G.add_edge(
            protein["id"],
            other["id"],
            weight=combined_score
        )

        proteins.append(other["id"])

    layout = shell_layout(
        G,
        nlist=[
            proteins,
            pathways
        ]
    )
    
    for node,(x,y) in layout.items():
        G.node[node]["x"] = float(x)
        G.node[node]["y"] = float(y)

    data = json_graph.node_link_data(G)
    return json.dumps(data)

@app.route("/api/subgraph/protein", methods=["POST"])
def protein_subgraph_api():
    protein_id = int(request.form.get("protein_id"))
    threshold = int(float(request.form.get("threshold")) * 1000)
    cursor = Cypher.get_protein_subgraph(neo4j_graph, protein_id, threshold)
    data = cursor.data()
    if not data:
        data = None
    else:
        data = data[0]
    data_json = protein_subgraph_to_nx_json(data)
    return Response(data_json, mimetype="application/json")

def protein_list_subgraph_to_nx_json(subgraph):
    G = nx.DiGraph()
    if subgraph is None:
        data = json_graph.node_link_data(G)
        return json.dumps(data)

    proteins = []
    pathways = []

    for protein in subgraph["proteins"]:
        G.add_node(
            protein["id"],
            label=protein["name"],
            description=protein["description"],
            type=0 # Protein
        )
        proteins.append(protein["id"])

    for pathway in subgraph["pathways"]:
        G.add_node(
            pathway["id"],
            label=pathway["name"],
            description=pathway["description"],
            type=1 # Pathway
        )
        pathways.append(pathway["id"])

    for association in subgraph["associations"]:
        combined_score = association["combined_score"]
        protein1_id = association["protein1_id"]
        protein2_id = association["protein2_id"]
        pathway_id = association["pathway_id"]
        G.add_edge(
            protein1_id,
            protein2_id,
            weight=combined_score
        )
        if pathway_id is not None:
            G.add_edge(
                protein1_id,
                pathway_id,
                weight=0
            )
            G.add_edge(
                protein2_id,
                pathway_id,
                weight=0
            )

    layout = shell_layout(
        G,
        nlist=[
            proteins,
            pathways
        ]
    )

    for node,(x,y) in layout.items():
        G.node[node]["x"] = float(x)
        G.node[node]["y"] = float(y)

    data = json_graph.node_link_data(G)
    return json.dumps(data)

@app.route("/api/subgraph/protein_list", methods=["POST"])
def protein_list_subgraph_api():
    protein_ids = list(map(int, request.form.get("protein_ids").split(";")))
    threshold = int(float(request.form.get("threshold")) * 1000)
    cursor = Cypher.get_proteins_subgraph(neo4j_graph, protein_ids, threshold)
    data = cursor.data()
    if not data:
        data = None
    else:
        data = data[0]
    data_json = protein_list_subgraph_to_nx_json(data)
    return Response(data_json, mimetype="application/json")

@app.route("/api/subgraph/pathway", methods=["POST"])
def pathway_subgraph_api():
    pathway_id = request.form.get("pathway_id")
    threshold = int(float(request.form.get("threshold")) * 1000)
    cursor = Cypher.get_pathway_subgraph(neo4j_graph, pathway_id, threshold)
    data = cursor.data()
    if not data:
        data = None
    else:
        data = data[0]
    return Response(json.dumps(data), mimetype="application/json")

if __name__ == "__main__":
    app.run(debug=True)
