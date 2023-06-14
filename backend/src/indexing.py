"""
Collection of functions for creating and searching
q-gram indexes for various entities.
"""
import os
import os.path
from collections import defaultdict, namedtuple

import database
import queries

# ========================= q-gram index =========================

_Q_GRAM_PAD_CHAR = "$"


def make_q_grams(string, q=3):
    """
    Generate padded q-grams from a given string.
    :param string: string to work with
    :param q: length of padding applied left and right
    :returns: q-grams
    """
    q_grams = list()

    padding = _Q_GRAM_PAD_CHAR * (q - 1)
    string_padded = padding + string + padding

    for i in range(len(string_padded) - q + 1):
        q_grams.append(string_padded[i: i + q])

    return q_grams


def search_q_gram_index(query, index, condition=None, top=5):
    """
    Retrieve the best 'top' results for a query
    based on a given q-gram index.
    """
    assert top > 0

    q_grams = make_q_grams(query.strip().strip(_Q_GRAM_PAD_CHAR).lower())

    counts = defaultdict(int)
    for item_set in map(lambda q_gram: index[q_gram], q_grams):
        if condition is not None:
            item_set = filter(condition, item_set)

        for item in item_set:
            counts[item] += 1

    if top == 1:
        return [max(counts.items(), key=lambda item: item[1])[0]]

    return list(map(lambda item: item[0], sorted(counts.items(), key=lambda item: item[1], reverse=True)))[:top]


#  ========================= Protein =========================

Protein = namedtuple("Protein", ["id", "name", "species_id"])


def get_protein_connection() -> dict:
    """
    Direct neo4j search of the given proteins.

    :returns: id of the given string
    """
    neo4j_graph = database.connect_neo4j()

    protein_list = defaultdict(set)
    for row in queries.get_protein_list(neo4j_graph):
        protein = Protein(**row)
        protein_list[row["name"]].add(protein)

    return protein_list


# ========================= Species =========================

Species = namedtuple("Species", ["name", "kegg_id", "ncbi_id"])


def create_species_q_gram_index() -> dict:
    """
    Create a q-gram index for species names.

    :returns: index
    """

    index = defaultdict(set)
    genomes_file_path = os.path.join(os.path.dirname(__file__), "../../scraping/KEGG", "data", "kegg_genomes.txt")
    with open(genomes_file_path) as kegg_genomes:
        for line in kegg_genomes:
            line = line.rstrip()
            mapping = line.split("\t")[1]
            if "; " not in mapping:
                continue

            ids, species_name = mapping.split("; ")
            ids = ids.split(", ")
            kegg_id, ncbi_id = ids[0], ids[-1]

            species = Species(species_name, kegg_id, int(ncbi_id))
            for q_gram in make_q_grams(species.name.lower()):
                index[q_gram].add(species)

    return index
