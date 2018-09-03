
import os
import api

import sys
sys.path.append("..")
import utils

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
for id1, id2, organism_name, taxonomy in utils.read_table(organisms, (str, str, str, str), "\t"):
    print(organism_name)
    pathways = api.pathways(id2)

    for pathway_id, pathway_name in utils.read_table(pathways, (str, str), "\t"):
        print(pathway_name)
        pathway = api.pathway(pathway_id, kgml = False)

        pathway_path = os.path.join(PATHWAYS_DIR, pathway_id)
        with open(pathway_path, mode = "w", encoding = "utf-8") as pathway_file:
            pathway_file.write(pathway)
