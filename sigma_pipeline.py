
import io
import json
import time
from contextlib import contextmanager

import pandas as pd

import cypher_queries as Cypher
import database
import fuzzy_search
import jar


@contextmanager
def measure_time(what):
    start = time.time()
    yield
    end = time.time()
    print(f"[{what}] {end - start:.2f} s")

with open("../genes.clean.txt", "r") as f:
    genes = list(map(lambda line: line.rstrip("\n"), f))

with measure_time("Fuzzy search"):
    proteins = fuzzy_search.search_protein_list(genes, species_id=9606)

protein_ids = list(map(lambda p: p.id, proteins))

query = """
    MATCH (source:Protein)-[association:ASSOCIATION]->(target:Protein)
    WHERE source.id IN {protein_ids} AND target.id IN {protein_ids} AND association.combined >= {threshold}
    RETURN source, target, association.combined AS score
"""

param_dict = dict(
    protein_ids=protein_ids,
    threshold=600
)


with measure_time("Cypher query"):
    data =  database.neo4j_graph.data(query, param_dict)

with measure_time("pandas DataFrames"):
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
    edges = pd.DataFrame({
        "source": source,
        "target": target,
        "score": score
    })

with measure_time("CSV"):
    nodes_csv = io.StringIO()
    edges_csv = io.StringIO()

    # NODES
    nodes = nodes.drop_duplicates(subset="id")
    # JAR accepts only id
    nodes["id"].to_csv(nodes_csv, index=False, header=True)

    # EDGES
    edges = edges.drop_duplicates(subset=["source", "target"])
    # JAR accepts source, target, score
    edges.to_csv(edges_csv, index=False, header=True)

    stdin = f"{nodes_csv.getvalue()}\n{edges_csv.getvalue()}"

with measure_time("JAR"):
    stdout = jar.pipe_call("gephi-backend/out/artifacts/gephi_backend_jar/gephi.backend.jar", stdin)

sigmajs_data = json.loads(stdout)
