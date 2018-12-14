import os.path
import json
from flask import Flask, Response, request, send_from_directory

import fuzzy_search
import database
import cypher_queries as Cypher

app = Flask(__name__)

# ====================== Index page ======================

@app.route("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "demo.html")

# ====================== Fuzzy search API ======================

# Species

def species_to_dict(species):
    return list(map(lambda s: {
        "species_name": s[0],
        "kegg_id": s[1],
        "ncbi_id": s[2]
    }, species))

@app.route("/api/search/species", methods=["GET"])
def search_species_api():
    query = request.args.get("query")
    results = fuzzy_search.search_species(query)
    return_object = species_to_dict(results)
    return Response(json.dumps(return_object), mimetype="application/json")

# Protein

def proteins_to_dicts(proteins):
    return list(map(lambda r: {
        "protein_name": r[0],
        "protein_id": r[1],
        "species_id": r[2]
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
    protein_list = query.split(";")
    results = fuzzy_search.search_protein_list(protein_list)
    return_object = proteins_to_dicts(results)
    return Response(json.dumps(return_object), mimetype="application/json")

# Pathway

def pathways_to_dicts(pathways):
    return list(map(lambda p: {
        "pathway_name": p[0],
        "pathway_id": p[1],
        "species_id": p[2]
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
        "class_name": c
    }, classes))    

@app.route("/api/search/class", methods=["GET"])
def search_class_api():
    query = request.args.get("query")
    results = fuzzy_search.search_class(query)
    return_object = classes_to_dicts(results)
    return Response(json.dumps(return_object), mimetype="application/json")

# ====================== Subgraph API ======================
neo4j_graph = database.connect_neo4j()

@app.route("/api/subgraph/protein")
def protein_subgraph_api():
    protein_id = int(request.args.get("protein_id"))
    cursor = Cypher.get_protein_subgraph(neo4j_graph, protein_id)
    return Response(json.dumps(cursor.data()), mimetype="application/json")

@app.route("/api/subgraph/pathway")
def pathway_subgraph_api():
    pathway_id = request.args.get("pathway_id")
    cursor = Cypher.get_pathway_subgraph(neo4j_graph, pathway_id)
    return Response(json.dumps(cursor.data()), mimetype="application/json")

if __name__ == "__main__":
    app.run()
