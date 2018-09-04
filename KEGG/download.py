
import os
import api
import parse

import sys
sys.path.append("..")
from utils import read_table

# Directory for saving the data
DATA_DIR = "data"
PATHWAYS_DIR = os.path.join(DATA_DIR, "pathways")
os.makedirs(DATA_DIR, exist_ok = True)
os.makedirs(PATHWAYS_DIR, exist_ok = True)

# Organisms
print("Downloading organisms list...")
organisms = api.organisms()
organisms_path = os.path.join(DATA_DIR, "organisms.tsv")
with open(organisms_path, mode = "w", encoding = "utf-8") as organisms_file:
    organisms_file.write(organisms)

# Pathways
print("Downloading pathways...")
kegg2external_file = open(os.path.join(DATA_DIR, "kegg2external.tsv"), mode = "w", encoding = "utf-8")
for id1, id2, organism_name, taxonomy in read_table(organisms, (str, str, str, str), "\t"):
    print(organism_name)
    pathways = api.pathways(id2)

    # Get the pathway
    for pathway_id, pathway_name in read_table(pathways, (str, str), "\t"):
        pathway = api.pathway(pathway_id, kgml = True)

        pathway_path = os.path.join(PATHWAYS_DIR, pathway_id)
        with open(pathway_path, mode = "w", encoding = "utf-8") as pathway_file:
            pathway_file.write(pathway)

        # Parse KGML
        pathway_title, gene_ids = parse.parse_KGML(pathway)
        print(pathway_title)
        print("Number of genes:", len(gene_ids))

        # Map KEGG identifiers to STRING external identifiers        
        mapped_identifiers = api.map_identifiers_to_STRING(gene_ids)

        kegg2external = dict()
        for idx, external_id, species_id, species_name, preferred_name, annotation in read_table(
            mapped_identifiers,
            (int, str, int, str, str, str),
            delimiter = "\t"
        ):
            assert gene_ids[idx] not in kegg2external # Make sure the mapping is unique
            kegg2external[gene_ids[idx]] = external_id
        
        num_not_mapped = len(gene_ids) - len(kegg2external)
        if num_not_mapped > 0:
            print("{} gene(s) could not be mapped to STRING external ID!".format(num_not_mapped))

        # Save the mappings
        for mapping in kegg2external.items():
            kegg2external_file.write("{}\t{}\n".format(*mapping))

kegg2external_file.close()