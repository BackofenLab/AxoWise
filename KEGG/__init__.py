
import os.path

species = list()
with open(os.path.join(os.path.dirname(__file__), "data", "kegg_genomes.txt")) as kegg_genomes:
    for line in kegg_genomes:
        line = line.rstrip()
        mapping = line.split("\t")[1]
        if "; " not in mapping:
            continue

        ids, name = mapping.split("; ")
        ids = ids.split(", ")
        kegg_id, ncbi_id = ids[0], ids[-1]
        species.append((name, kegg_id, int(ncbi_id)))

def get_species_identifiers(query_name):
    for entry in species:
        name, kegg_id, ncbi_id = entry
        if query_name.lower() in name.lower():
            return entry
    return None, None, None
