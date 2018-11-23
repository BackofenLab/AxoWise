
import os
import os.path
import pickle

_index_dir = "index"

# Proteins
def create_pickled_proteins(proteins, kegg_id):
    protein2id = dict()
    for protein in proteins:
        protein2id[protein["preferred_name"]] = protein["id"]

    os.makedirs(_index_dir, exist_ok=True)

    path = os.path.join(_index_dir, f"proteins.{kegg_id}.pkl.gz")
    with open(path, "wb") as file:
        pickle.dump(protein2id, file, pickle.HIGHEST_PROTOCOL)

def open_pickled_proteins(kegg_id):
    protein2id = dict()

    path = os.path.join(_index_dir, f"proteins.{kegg_id}.pkl.gz")
    with open(path, "rb") as file:
        protein2id = pickle.load(file)

    return protein2id

# Pathways
def create_pickled_pathways(pathways, kegg_id):
    pathway2id = dict()
    for pathway in pathways:
        pathway2id[pathway["name"]] = pathway["id"]

    os.makedirs(_index_dir, exist_ok=True)

    path = os.path.join(_index_dir, f"pathways.{kegg_id}.pkl.gz")
    with open(path, "wb") as file:
        pickle.dump(pathway2id, file, pickle.HIGHEST_PROTOCOL)

def open_pickled_pathways(kegg_id):
    pathway2id = dict()

    path = os.path.join(_index_dir, f"pathways.{kegg_id}.pkl.gz")
    with open(path, "rb") as file:
        pathway2id = pickle.load(file)

    return pathway2id