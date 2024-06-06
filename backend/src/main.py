import ast
import io
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import os.path
import sys

import pandas as pd
import networkit as nk
from flask import Flask, Response, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from multiprocessing import Process

import database
import enrichment
import enrichment_graph
import citation_graph
from summarization import article_graph as summarization
import graph
import jar
import queries
import signal
from util.stopwatch import Stopwatch

app = Flask(__name__)

# ====================== Index page ======================

_SCRIPT_DIR = os.path.dirname(__file__)
_SERVE_DIR = "../../frontend/dist"
_INDEX_FILE = "index.html"
_BACKEND_JAR_PATH = "../gephi/target/gephi.backend-1.0-SNAPSHOT.jar"


@app.route("/")
def index():
    return send_from_directory(os.path.join(_SCRIPT_DIR, _SERVE_DIR), _INDEX_FILE)


# ====================== Other files ======================


@app.route("/<path:path>")
def files(path):
    return send_from_directory(os.path.join(_SCRIPT_DIR, _SERVE_DIR), path)


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

    # STRING API functional enrichment
    """df_enrichment = stringdb.functional_enrichment(proteins, species_id)

    list_enrichment = list()
    for _, row in df_enrichment.iterrows():
        list_enrichment.append(dict(
            id=row["term"],
            proteins=row["inputGenes"].split(","),
            name=row["description"],
            category=row["category"],
            p_value=row["p_value"],
            fdr_rate=row["fdr"]
        ))"""

    json_str = json.dumps(list_enrichment.to_dict("records"), ensure_ascii=False, separators=(",", ":"))
    return Response(json_str, mimetype="application/json")


# ====================== Meillisearch ======================
# TODO Refactor this
# Request comes from ContextSection.vue
@app.route("/api/subgraph/context", methods=["POST"])
def proteins_context():
    '''tokenizer = AutoTokenizer.from_pretrained("lxyuan/distilbart-finetuned-summarization")  # abstractive very few words
    model = AutoModelForSeq2SeqLM.from_pretrained("lxyuan/distilbart-finetuned-summarization")
    model = model.to("cuda")'''
    base, context, rank, limit = request.form.get("base"), request.form.get("context"), request.form.get("rank"), 500
    query = f'"{base}" "{context}"'
    # in-house context summary
    edges, nodes = summarization.create_citations_graph(limit, query, None, None)
    graph = citation_graph.get_citation_graph(nodes,edges)
    return Response(graph, mimetype="application/json")


@app.route("/api/subgraph/summary", methods=["POST"])
def abstract_summary():
    abstracts = request.form.get("abstracts")
    print(abstracts)

    response = """Lorem ipsum dolor sit amet. Sit tempora illo est excepturi rerum et ratione sint ut explicabo magnam in esse magni. Non odit ipsum et quia fuga aut galisum natus in commodi perspiciatis et quae mollitia.
                Ut ipsam praesentium ut quibusdam molestiae est voluptatem obcaecati nam alias dignissimos non voluptas Quis eos possimus quae. Hic iusto repellat et iste eligendi ab laudantium perspiciatis. At sequi deserunt et dolorum nihil et voluptatem Quis est nobis omnis. At optio architecto ut rerum iste vel iure placeat vel quas quia sit galisum quos aut accusamus aperiam aut nostrum delectus.
                Ut ducimus tempore nam autem voluptatem et fugit saepe ut modi voluptas. Id quisquam quidem aut quam molestiae sit culpa quia hic molestiae tempore ad distinctio voluptatem est vitae harum. Quo officiis maxime non blanditiis molestias 33 quis galisum."""
    return Response(response, mimetype="application/json")


# ====================== Subgraph API ======================
# request comes from home.js
# TODO Refactor this
@app.route("/api/subgraph/proteins", methods=["POST"])
def proteins_subgraph_api():
    driver = database.get_driver()
    stopwatch = Stopwatch()

    # Queried proteins
    if not request.files.get("file"):
        protein_names = request.form.get("proteins").split(";")
        protein_names = list(filter(None, protein_names))
    else:
        panda_file = pd.read_csv(request.files.get("file"))
        protein_names = panda_file["SYMBOL"].to_list()
    input_mapping = {}
    for i in protein_names:
        input_mapping[i.upper()] = i
    species_id = int(request.form.get("species_id"))
    # DColoumns
    selected_d = request.form.get("selected_d").split(",") if request.form.get("selected_d") else None
    threshold = int(float(request.form.get("threshold")) * 1000)

    proteins, protein_ids, symbol_alias_mapping = queries.get_protein_ids_for_names(driver, protein_names, species_id)
    keys = list(symbol_alias_mapping.keys())
    for num, i in enumerate(symbol_alias_mapping.values()):
        if i in input_mapping:
            input_mapping[keys[num]] = input_mapping[i]
    stopwatch.round("Setup")

    if len(protein_ids) > 1:
        proteins, source, target, score = queries.get_protein_associations(driver, protein_ids, threshold, species_id)
    else:
        proteins, source, target, score = queries.get_protein_neighbours(driver, protein_ids, threshold, species_id)

    stopwatch.round("Neo4j")

    nodes = (
        pd.DataFrame(proteins).rename(columns={"ENSEMBL_PROTEIN": "external_id"}).drop_duplicates(subset="external_id")
    )

    edges = pd.DataFrame({"source": source, "target": target, "score": score})
    edges = edges.drop_duplicates(subset=["source", "target"])

    # Check if there is no data from database, return from here
    if edges.empty:
        return Response(json.dumps([]), mimetype="application/json")

    # Networkit related (graph and parameters)
    nk_graph, node_mapping = graph.nk_graph(nodes, edges)
    betweenness = graph.betweenness(nk_graph)
    pagerank = graph.pagerank(nk_graph)

    stopwatch.round("Parsing")

    # Creating only the main Graph and exclude not connected subgraphs
    nodes_sub = graph.create_nodes_subgraph(nk_graph, nodes)

    stopwatch.round("DValue")

    # D-Value categorize via percentage
    if not (request.files.get("file") is None):
        panda_file.rename(columns={"SYMBOL": "name"}, inplace=True)

    stopwatch.round("Enrichment")

    if len(nodes.index) == 0:
        sigmajs_data = {"nodes": [], "edges": [], "settings": []}
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
        sigmajs_data["settings"] = {}

    stopwatch.round("Gephi")

    # Create a dictionary mapping ENSEMBL IDs to rows in `nodes`
    ensembl_to_node = dict(zip(nodes["external_id"], nodes.itertuples(index=False)))

    # Iterate over nodes in `sigmajs_data` and update their attributes
    sigmajs_data["settings"]["gene_alias_mapping"] = symbol_alias_mapping
    for node in sigmajs_data["nodes"]:
        ensembl_id = node["id"]
        df_node = ensembl_to_node.get(ensembl_id)
        if df_node:
            symbol_value = df_node.SYMBOL
            if ensembl_id in node_mapping:
                mapped_node_id = node_mapping[ensembl_id]
                # Use node mapping to add corresponding values of betweenness and pagerank
                node["attributes"]["Betweenness Centrality"] = str(betweenness[mapped_node_id])
                node["attributes"]["PageRank"] = str(pagerank[mapped_node_id])
            node["attributes"]["Description"] = df_node.annotation
            node["attributes"]["Ensembl ID"] = df_node.external_id
            node["attributes"]["Ensembl Gene ID"] = df_node.ENSEMBL_GENE
            node["attributes"]["Name"] = input_mapping[symbol_value]
            if symbol_value in symbol_alias_mapping:
                node["attributes"]["Alias"] = symbol_value
            else:
                node["attributes"]["Alias"] = "not found"
            # Alias attribute
            """if symbol_value in all_symbols:
                node["attributes"]["Alias"] = all_symbols[symbol_value]
            else:
                node["attributes"]["Alias"] = ["No alias"]"""
            if not (request.files.get("file") is None):
                if selected_d != None:
                    for column in selected_d:
                        if symbol_value in symbol_alias_mapping:
                            # If a symbol was found through its alias we have
                            # to keep the alias name so the value can be taken
                            # from the input file correctly
                            symbol_value = symbol_alias_mapping[symbol_value]
                        node["attributes"][column] = panda_file.loc[
                            panda_file["name"] == input_mapping[symbol_value], column
                        ].item()
            node["label"] = input_mapping[symbol_value]
            node["species"] = str(10090)

    # Identify subgraph nodes and update their attributes
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

    # Update sigmajs_data with subgraph and other attributes as needed
    if request.form.get("selected_d"):
        sigmajs_data["dvalues"] = selected_d
    sigmajs_data["subgraph"] = sub_proteins

    stopwatch.round("End")
    stopwatch.total("proteins_subgraph_api")

    json_str = json.dumps(sigmajs_data)

    return Response(json_str, mimetype="application/json")


# =============== Functional Term Graph ======================


# TODO Refactor this
@app.route("/api/subgraph/terms", methods=["POST"])
def terms_subgraph_api():
    stopwatch = Stopwatch()

    # Functional terms
    list_enrichment = ast.literal_eval(request.form.get("func-terms"))
    species_id = int(request.form.get("species_id"))

    json_str = enrichment_graph.get_functional_graph(list_enrichment=list_enrichment, species_id=species_id)

    stopwatch.total("terms_subgraph_api")

    return Response(json_str, mimetype="application/json")


# =============== Citation Graph ======================


# TODO Refactor this
# @app.route("/api/subgraph/citation", methods=["POST"])
# def citation_subgraph_api():
#     stopwatch = Stopwatch()

#     # Functional terms
#     list_enrichment = ast.literal_eval(request.form.get("func-terms"))

#     json_str = citation_graph.get_citation_graph(list_enrichment=list_enrichment)

#     stopwatch.total("citation_subgraph_api")

#     return Response(json_str, mimetype="application/json")


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
    if "--server" in sys.argv:
        app.run(host="0.0.0.0", port=80)
    else:
        app.run()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    flask_process = Process(target=run_flask)
    flask_process.start()
