import os, sys, signal, json
import database, queries
from multiprocessing import Process

import pandas as pd
from flask import Flask, Response, request, send_from_directory
from util.stopwatch import Stopwatch
from werkzeug.middleware.proxy_fix import ProxyFix

import enrichment

app = Flask(__name__)
history = []


# ====================== Setup ======================
_SCRIPT_DIR = os.path.dirname(__file__)
_SERVE_DIR = "../../frontend/dist"
_INDEX_FILE = "index.html"

@app.route("/")
def index():
    return send_from_directory(os.path.join(_SCRIPT_DIR, _SERVE_DIR), _INDEX_FILE)

@app.route("/<path:path>")
def files(path):
    return send_from_directory(os.path.join(_SCRIPT_DIR, _SERVE_DIR), path)


# ====================== Graph API ======================
# Building graph by given node identifiers and returning the edge/node table matching neo4j database.
# Input: ['nodeIdentifier1','nodeIdentifier2','nodeIdentifier3']:JSON  
# Output: {edges:[], nodes:[]} :JSON
@app.route("/api/subgraph/proteins", methods=["POST"])
def graph_api():
    driver = database.get_driver()
    stopwatch = Stopwatch()

    ### Collecting data points sent via flask.
    ### Given input data is: proteins, species_id, threshold, file
    if not request.files.get("file"):
        protein_names = request.form.get("proteins").split(";")
        protein_names = list(filter(None, protein_names))
    else:
        panda_file = pd.read_csv(request.files.get("file"))
        protein_names = panda_file["SYMBOL"].to_list()

    species_id = int(request.form.get("species_id"))
    threshold = int(float(request.form.get("threshold")) * 1000)
    
    ### Querying input against neo4j database.
    ### Retrieving nodes, edges list from database. 
    proteins, protein_ids, symbol_alias_mapping = queries.get_protein_ids_for_names(
        driver, protein_names, species_id
    )
    
    nodes, edges = queries.get_protein_associations(
        driver, protein_ids, threshold, species_id
    )
    
    driver.close()
    stopwatch.round("Neo4j")
    
    ### Adding more attributes to nodes. e.g alias, labels 
    nodesDF = pd.DataFrame(nodes).drop_duplicates(subset="ENSEMBL_PROTEIN")
    edgesDF = pd.DataFrame(edges).drop_duplicates(subset=["source", "target"])

    nodesDF['label'] = nodesDF['SYMBOL'].map(lambda x: symbol_alias_mapping.get(x, x))
    nodesDF['alias'] = nodesDF['SYMBOL'].map(symbol_alias_mapping).fillna("")

    nodesDF.loc[~nodesDF['SYMBOL'].isin(protein_names), 'label'] = nodesDF['alias']

    ### Convert nodes, edges list to json serizalized object. 
    graph_dict = {
        "nodes": nodesDF.to_dict(orient="records"),
        "edges": edgesDF.to_dict(orient="records"),
        "settings": {"gene_alias_mapping": symbol_alias_mapping, "species": species_id}
    }
    
    stopwatch.round("End")

    json_str = json.dumps(graph_dict)

    return Response(json_str, mimetype="application/json")


# ====================== Functional Enrichment ======================
# ______functional_enrichment_STRING_________________________________
# TODO Refactor this
# Request comes from functional_enrichment.js
@app.route("/api/subgraph/enrichment", methods=["POST"])
def proteins_enrichment():
    driver = database.get_driver()
    genes = request.form.get("genes").split(",")
    symbol_alias_mapping = json.loads(request.form.get("mapping"))
    alias_symbol_mapping = {value: key for key, value in symbol_alias_mapping.items()}
    species_id = int(request.form.get("species_id"))

    # in-house functional enrichment
    list_enrichment = enrichment.functional_enrichment(
        driver, genes, species_id, symbol_alias_mapping, alias_symbol_mapping
    )

    json_str = json.dumps(
        list_enrichment.to_dict("records"), ensure_ascii=False, separators=(",", ":")
    )
    return Response(json_str, mimetype="application/json")


# # =============== Functional Term Graph ======================


# # TODO Refactor this
# @app.route("/api/subgraph/terms", methods=["POST"])
# def terms_subgraph_api():
#     stopwatch = Stopwatch()

#     # Functional terms
#     list_enrichment = ast.literal_eval(request.form.get("func-terms"))
#     species_id = int(request.form.get("species_id"))

#     json_str = enrichment_graph.get_functional_graph(
#         list_enrichment=list_enrichment, species_id=species_id
#     )

#     stopwatch.total("terms_subgraph_api")

#     return Response(json_str, mimetype="application/json")


# # =============== Citation Graph ======================


# # TODO Refactor this
# # @app.route("/api/subgraph/citation", methods=["POST"])
# # def citation_subgraph_api():
# #     stopwatch = Stopwatch()

# #     # Functional terms
# #     list_enrichment = ast.literal_eval(request.form.get("func-terms"))

# #     json_str = citation_graph.get_citation_graph(list_enrichment=list_enrichment)

# #     stopwatch.total("citation_subgraph_api")

# #     return Response(json_str, mimetype="application/json")


# Signal handler needed after changing to Networkit
def signal_handler(signum, frame):
    # Handle the KeyboardInterrupt (Ctrl+C) here
    flask_process.terminate()
    os._exit(0)


def run_flask():
    if "--pid" in sys.argv:
        with open("process.pid", "w+") as file:
            pid = f"{os.getpid()}"
            file.write(pid)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Get host and port from environment variables, with default values
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", "5000"))

    if "--server" in sys.argv:
        app.run(host=host, port=port)
    else:
        app.run()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    flask_process = Process(target=run_flask)
    flask_process.start()
