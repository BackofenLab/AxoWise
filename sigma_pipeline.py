
import jar
import fuzzy_search
import cypher_queries as Cypher
import database
import pandas as pd

with open("../genes.clean.txt", "r") as f:
    genes = list(map(lambda line: line.rstrip("\n"), f))

proteins = fuzzy_search.search_protein_list(genes, species_id=9606)
protein_ids = sorted(list(map(lambda p: p.id, proteins)))
print(len(protein_ids))

query = """
    MATCH (source:Protein)-[association:ASSOCIATION]-(target:Protein)
    WHERE association.combined >= {threshold} AND source.id IN {protein_ids} AND source.id IN {protein_ids} AND source.id < target.id
    RETURN source, target, association.combined AS score
"""

param_dict = dict(
    protein_ids=protein_ids,
    threshold=400
)

import time
start = time.time()
data =  database.neo4j_graph.data(query, param_dict)
end = time.time()
print(end - start, "s")

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

import io
nodes_csv = io.StringIO()
edges_csv = io.StringIO()
nodes.to_csv(nodes_csv, index=False)
edges.to_csv(edges_csv, index=False)

stdin = f"{nodes_csv.getvalue()}\n{edges_csv.getvalue()}"

stdout = jar.pipe_call("gephi-backend/out/artifacts/gephi_backend_jar/gephi.backend.jar", stdin)
print(stdout)