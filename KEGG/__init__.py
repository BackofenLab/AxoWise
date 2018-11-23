
import os.path
from fuzzywuzzy import process

species2ids = dict()
with open(os.path.join(os.path.dirname(__file__), "data", "kegg_genomes.txt")) as kegg_genomes:
    for line in kegg_genomes:
        line = line.rstrip()
        mapping = line.split("\t")[1]
        if "; " not in mapping:
            continue

        ids, name = mapping.split("; ")
        ids = ids.split(", ")
        kegg_id, ncbi_id = ids[0], ids[-1]
        species2ids[name] = (kegg_id, int(ncbi_id))

def fuzzy_search_species(query_name):
    return sorted(
        process.extract(query_name, species2ids.keys()),
        key=lambda r: 1 if ("(" not in r[0]) or (")" not in r[0]) else 0
    )

def get_species_identifiers(query_name):
    results = fuzzy_search_species(query_name)
    name, score = results[0]
    return (name, *species2ids[name])
