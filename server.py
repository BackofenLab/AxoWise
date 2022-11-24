import ast
from asyncio import subprocess
import random
import subprocess
import json
import os.path
import io
from collections import defaultdict
import csv
from sys import stderr
from threading import Timer
from unicodedata import category
import math

# import networkx as nx
from flask import Flask, Response, request, send_from_directory
# from networkx.readwrite import json_graph
import pandas as pd
import jar
import stringdb
import os

import cypher_queries as Cypher
import database
import direct_search
import fuzzy_search
from layout import shell_layout
import uuid

import graph_utilities
from werkzeug.middleware.proxy_fix import ProxyFix

import time
app = Flask(__name__)

# ====================== Index page ======================

_SCRIPT_DIR = os.path.dirname(__file__)
_SERVE_DIR = "frontend"
_INDEX_FILE = "index.html"
_BACKEND_JAR_PATH = "gephi-backend/target/gephi.backend-1.0-SNAPSHOT.jar"

@app.route("/")
def index():
    return send_from_directory(os.path.join(_SCRIPT_DIR, _SERVE_DIR), _INDEX_FILE)

# ====================== Other files ======================

@app.route("/<path:path>")
def files(path):
    return send_from_directory(os.path.join(_SCRIPT_DIR, _SERVE_DIR), path)

# ====================== Functional Enrichment ======================

# TODO Refactor this
@app.route("/api/subgraph/enrichment", methods=["POST"])
def proteins_enrichment():
    proteins = request.form.get("proteins").split(",")
    species_id = request.form.get("species_id")
    
    df_enrichment = stringdb.functional_enrichment(proteins, species_id)
    
    list_enrichment = list()
    if df_enrichment is not None:
        for _, row in df_enrichment.iterrows():
            list_enrichment.append(dict(
                id=row["term"],
                proteins=row["inputGenes"].split(","),
                name=row["description"],
                p_value=row["p_value"],
                fdr_rate=row["fdr"],
                category=row["category"]
            ))
    json_str=json.dumps(list_enrichment)  
    return Response(json_str, mimetype="application/json")

# ====================== Subgraph API ======================

# TODO Refactor this
@app.route("/api/subgraph/proteins", methods=["POST"])
def proteins_subgraph_api():

    #Begin a timer to time
    t_begin = time.time()
    
    # Queried proteins
    if (not request.files.get("file")):
        query_proteins = request.form.get("proteins").split(";")
        query_proteins = list(filter(None, query_proteins))
    else:
        panda_file = pd.read_csv(request.files.get("file"))
        query_proteins = panda_file['SYMBOL'].to_list()

    # Species
    species_id = int(request.form.get("species_id"))

    # DColoumns
    selected_d = request.form.get("selected_d").split(",")

    # Threshold
    threshold = int(float(request.form.get("threshold")) * 1000)
    
    # Filename generator
    filename = uuid.uuid4()

    # Fuzzy search mapping
    proteins = direct_search.search_protein_list(query_proteins, species_id=species_id)
    protein_ids = list(map(lambda p: p.id, proteins))
    

    # Create a query to find all associations between protein_ids and create a file with all properties
    def create_query_assoc():
        
        query = """
                WITH "MATCH (source:Protein)-[association:ASSOCIATION]->(target:Protein)
                WHERE source.external_id IN
                """ + repr(protein_ids) + ' AND target.external_id IN ' + repr(protein_ids) + ' AND association.combined >= ' + repr(threshold) + """
                RETURN source, target, association.combined AS score" AS query
                CALL apoc.export.csv.query(query, "/tmp/""" + repr(filename) + """.csv", {})
                YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
                RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;
                """
        return query
        
    # Create a query to find all neighbours of a single protein_id and create a file with all properties
    def create_query_single():
        
        query = """
                WITH "MATCH (source:Protein)-[association:ASSOCIATION]-(target:Protein)
                WHERE source.external_id IN
                """ + repr(protein_ids) + 'OR target.external_id IN' + repr(protein_ids) + ' AND association.combined >= ' + repr(threshold) + """
                RETURN source, target, association.combined AS score" AS query
                CALL apoc.export.csv.query(query, "/tmp/""" + repr(filename) + """.csv", {})
                YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data
                RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;
                """
        return query

    #Decide which query to select (Option 1: associations of a set of genes) (Option 2: neighbours of a single gene)
    if(len(protein_ids)>1):
        query = create_query_assoc()
    else:
        query = create_query_single()
    
    
    with open("/tmp/query"+repr(filename)+".txt", "w") as query_text:
        query_text.write("%s" % query)
    
    #Timer to evaluate runtime to setup
    t_setup = time.time()
    print("Time Spent (Setup):", t_setup-t_begin)


    #---------Start py2neo

    # # Query the database
    # query = """
    #     MATCH (source:Protein)-[association:ASSOCIATION]->(target:Protein)
    #     WHERE source.id IN {protein_ids} AND target.id IN {protein_ids} AND association.combined >= {threshold}
    #     RETURN source, target, association.combined AS score
    # """

    # param_dict = dict(
    #     protein_ids=protein_ids,
    #     threshold=threshold
    # )

    # data = database.neo4j_graph.run(query, param_dict).data()

    # #no data from database, return from here
    # # TO-DO Front end response to be handled
    # if not data:
    #     return Response(json.dumps([]), mimetype="application/json")
    
    # #pandas DataFrames for nodes and edges
    # proteins = set()
    # source, target, score = list(), list(), list()
    # for row in data:
    #     source.append(row["source"]["id"])
    #     target.append(row["target"]["id"])
    #     score.append(row["score"])
    #     proteins.add(row["source"])
    #     proteins.add(row["target"])

    # proteins = list(map(dict, proteins))

    #---------End py2neo

    #Run the cypher query in cypher shell via terminal
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
    proteins = list()
    source, target, score, assoc_names = list(), list(), list(), list()
    with open('/tmp/'+repr(filename)+'.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_row, target_row = ast.literal_eval(row['source']), ast.literal_eval(row['target'])
            source_row_prop, target_row_prop = source_row.get('properties'), target_row.get('properties')
            source.append(source_row_prop.get('external_id'))
            target.append(target_row_prop.get('external_id'))
            score.append(int(row['score']))
            proteins.append(source_row_prop)
            proteins.append(target_row_prop)
    os.remove('/tmp/'+repr(filename)+'.csv')

    nodes = pd.DataFrame(proteins)
    nodes = nodes.drop_duplicates(subset="external_id") # TODO `nodes` can be empty
    
    

    edges = pd.DataFrame({
        "source": source,
        "target": target,
        "score": score
        
    })
    edges = edges.drop_duplicates(subset=["source", "target"]) # TODO edges` can be empty
 
    

    #no data from database, return from here
    # TO-DO Front end response to be handled
    if edges.empty:
        return Response(json.dumps([]), mimetype="application/json")
     
    #Creating only the main Graph and exclude not connected subgraphs
    nodes_sub = graph_utilities.create_nodes_subgraph(edges, nodes)
    # edges = graph_utilities.create_edges_subgraph(edges)

    #Timer to evaluate runtime between cypher-shell and extracting data
    t_parsing = time.time()
    print("Time Spent (Parsing):", t_parsing-t_neo4j)
         
    #D-Value categorize via percentage
    if not (request.files.get("file") is None):
        panda_file.rename(columns={'SYMBOL': 'name'}, inplace=True)
        panda_file['name'] = panda_file['name'].str.upper()
    
        #Timer to evaluate enrichments runtime
    t_dvalue = time.time()
    print("Time Spent (DValue):", t_dvalue-t_parsing)

    # # Functional enrichment
    # external_ids = nodes["external_id"].tolist()
    # df_enrichment = stringdb.functional_enrichment(external_ids, species_id)

    # list_enrichment = list()
    # if df_enrichment is not None:
    #     for _, row in df_enrichment.iterrows():
    #         list_enrichment.append(dict(
    #             id=row["term"],
    #             proteins=row["inputGenes"].split(","),
    #             name=row["description"],
    #             p_value=row["p_value"]
    #         ))

    # #Timer to evaluate enrichments runtime
    t_enrich = time.time()
    print("Time Spent (Enrichment):", t_enrich-t_dvalue)


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
        nodes["external_id"].to_csv(nodes_csv, index=False, header=True)
        
        # JAR accepts source, target, score
        edges.to_csv(edges_csv, index=False, header=True)

        stdin = f"{nodes_csv.getvalue()}\n{edges_csv.getvalue()}"
        stdout = jar.pipe_call(_BACKEND_JAR_PATH, stdin)

        sigmajs_data = json.loads(stdout)
    
    #Timer to evaluate runtime of calling gephi
    t_gephi = time.time()
    print("Time Spent (Gephi):", t_gephi-t_enrich)

    for node in sigmajs_data["nodes"]:
        df_node = nodes[nodes["external_id"] == node["id"]].iloc[0]
        node["attributes"]["Description"] = df_node["description"]
        node["attributes"]["Ensembl ID"] = df_node["external_id"]
        node["attributes"]["Name"] = df_node["name"]         
        if not (request.files.get("file") is None):
            for coloumn in selected_d:
                node["attributes"][coloumn] = panda_file.loc[panda_file["name"] == df_node["name"], coloumn].item()     
        node["label"] = df_node["name"]
        node["species"] = str(df_node["species_id"])
    
    sub_proteins = []
    for node in sigmajs_data["nodes"]:
        if node["attributes"]["Ensembl ID"] not in  nodes_sub.values:            
            node["color"] = 'rgb(255,255,153)'
            node["hidden"] = True
            sub_proteins.append(node["attributes"]["Ensembl ID"])
            
    sigmajs_data["dvalues"] = selected_d
    sigmajs_data["subgraph"] = sub_proteins
    
            
            

    #Timer for final steps
    t_end = time.time()
    print("Time Spent (End):", t_end-t_gephi)

    json_str = json.dumps(sigmajs_data)

    return Response(json_str, mimetype="application/json")


if __name__ == "__main__":
    
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.run()
