"""
Collection of functions for creating and searching
q-gram indexes for various entities.
"""

import os
import os.path
from collections import defaultdict

import cypher_queries as Cypher
import database

# ========================= q-gram index =========================

_Q_GRAM_PAD_CHAR = "$"

def make_q_grams(string, q=3):
    """
    Generate padded q-grams from a given string.
    """
    q_grams = list()

    padding = _Q_GRAM_PAD_CHAR * (q - 1)
    string_padded = padding + string + padding

    for i in range(len(string_padded) - q + 1):
        q_grams.append(string_padded[i : i + q])

    return q_grams

def search_q_gram_index(query, index, condition=None, top=5):
    """
    Retrieve the best 'top' results for a query
    based on a given q-gram index.
    """

    q_grams = make_q_grams(query.strip().strip(_Q_GRAM_PAD_CHAR).lower())

    counts = defaultdict(int)
    for item_set in map(lambda q_gram: index[q_gram], q_grams):
        if condition is not None:
            item_set = filter(condition, item_set)

        for item in item_set:
            counts[item] += 1

    return list(map(
        lambda item: item[0],
        sorted(counts.items(), key=lambda item: item[1], reverse=True)
    ))[:top]

#  ========================= Protein =========================

def create_protein_q_gram_index():
    """
    Create a q-gram index for protein names.
    """

    neo4j_graph = database.connect_neo4j()

    index = defaultdict(set)
    for protein in Cypher.get_protein_list(neo4j_graph):
        protein_id, protein_name, species_id = protein["id"], protein["name"], protein["species_id"]
        for q_gram in make_q_grams(protein_name.lower()):
            index[q_gram].add((protein_id, protein_name, species_id))

    return index

# ========================= Pathway =========================

def create_pathway_q_gram_index():
    """
    Create a q-gram index for pathway names.
    """

    neo4j_graph = database.connect_neo4j()

    index = defaultdict(set)
    for pathway in Cypher.get_pathway_list(neo4j_graph):
        pathway_id, pathway_name, species_id = pathway["id"], pathway["name"], pathway["species_id"]
        for q_gram in make_q_grams(pathway_name.lower()):
            index[q_gram].add((pathway_id, pathway_name, species_id))

    return index

# ========================= Species =========================

def create_species_q_gram_index():
    """
    Create a q-gram index for species names.
    """

    index = defaultdict(set)
    genomes_file_path = os.path.join(os.path.dirname(__file__), "KEGG", "data", "kegg_genomes.txt")
    with open(genomes_file_path) as kegg_genomes:
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

# ========================= Class =========================

def create_class_q_gram_index():
    """
    Create a q-gram index for pathway class names.
    """

    neo4j_graph = database.connect_neo4j()

    index = defaultdict(set)
    for klass in Cypher.get_class_list(neo4j_graph):
        name = klass["name"]
        for q_gram in make_q_grams(name.lower()):
            index[q_gram].add(name)

    return index
