
import os
import os.path
import pickle
from collections import defaultdict

_INDEX_DIR = "index"

# Proteins
def create_pickled_proteins(proteins, kegg_id):
    protein2id = dict()
    for protein in proteins:
        protein2id[protein["preferred_name"]] = protein["id"]

    os.makedirs(_INDEX_DIR, exist_ok=True)

    path = os.path.join(_INDEX_DIR, f"proteins.{kegg_id}.pkl.gz")
    with open(path, "wb") as file:
        pickle.dump(protein2id, file, pickle.HIGHEST_PROTOCOL)

def open_pickled_proteins(kegg_id):
    protein2id = dict()

    path = os.path.join(_INDEX_DIR, f"proteins.{kegg_id}.pkl.gz")
    with open(path, "rb") as file:
        protein2id = pickle.load(file)

    return protein2id

# Pathways
def create_pickled_pathways(pathways, kegg_id):
    pathway2id = dict()
    for pathway in pathways:
        pathway2id[pathway["name"]] = pathway["id"]

    os.makedirs(_INDEX_DIR, exist_ok=True)

    path = os.path.join(_INDEX_DIR, f"pathways.{kegg_id}.pkl.gz")
    with open(path, "wb") as file:
        pickle.dump(pathway2id, file, pickle.HIGHEST_PROTOCOL)

def open_pickled_pathways(kegg_id):
    pathway2id = dict()

    path = os.path.join(_INDEX_DIR, f"pathways.{kegg_id}.pkl.gz")
    with open(path, "rb") as file:
        pathway2id = pickle.load(file)

    return pathway2id

# Species q-gram index

_Q_GRAM_PAD_CHAR = "$"

def make_q_grams(string, q=3):
    """
    Generate padded q-grams from a given string.
    """
    q_grams = list()

    padding = "".join([_Q_GRAM_PAD_CHAR for _ in range(q-1)])
    string_padded = padding + string + padding

    for i in range(len(string_padded) - 3):
        q_grams.append(string_padded[i : i + 3])

    return q_grams

def create_species_q_gram_index():
    """
    Create a q-gram index for species names.
    """

    index = defaultdict(set)
    with open(os.path.join(os.path.dirname(__file__), "KEGG", "data", "kegg_genomes.txt")) as kegg_genomes:
        for line in kegg_genomes:
            line = line.rstrip()
            mapping = line.split("\t")[1]
            if "; " not in mapping:
                continue

            ids, name = mapping.split("; ")
            ids = ids.split(", ")
            kegg_id, ncbi_id = ids[0], ids[-1]
            # (name, kegg_id, ncbi_id)
            for q_gram in make_q_grams(name.lower()):
                index[q_gram].add((name, kegg_id, int(ncbi_id)))

    return index

def search_species_q_gram_index(query, index, top=5):
    """
    Retrieve the best 'top' results for a species query
    based on a given q-gram index.
    """

    q_grams = make_q_grams(query.strip().strip(_Q_GRAM_PAD_CHAR).lower())

    counts = defaultdict(int)
    for species_set in map(lambda q_gram: index[q_gram], q_grams):
        for species in species_set:
            counts[species] += 1

    return list(map(
        lambda item: item[0],
        sorted(counts.items(), key=lambda item: item[1], reverse=True)
    ))[:top]

if __name__ == "__main__":
    index = create_species_q_gram_index()
    while True:
        query = input("> ")
        print(search_species_q_gram_index(query, index))
