
import os
import api
import parse
import argparse

import sys
sys.path.append("..")
from utils import read_table

# Parse CLI arguments
args_parser = argparse.ArgumentParser(
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
)

args_parser.add_argument(
    "--kegg_organism_id",
    type = str,
    help = "Download KEGG pathways only for this organism",
    default = "hsa" # Homo sapiens
)

args_parser.add_argument(
    "--string_organism_id",
    type = str,
    help = "Map KEGG pathways to this STRING organism",
    default = "9606" # Homo sapiens
)

args = args_parser.parse_args()

# Directory for saving the data
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok = True)

# Pathways
print("Downloading pathways for: {}".format(args.kegg_organism_id))
pathways_file = open(os.path.join(DATA_DIR, "kegg_pathways.{}.tsv".format(args.kegg_organism_id)), mode = "w", encoding = "utf-8")

pathways = api.pathways(args.kegg_organism_id)

# Get the pathway
pathway_table = list(read_table(pathways, (str, str), "\t"))
for idx, (pathway_id, pathway_name) in enumerate(pathway_table):
    pathway = api.pathway(pathway_id, kgml = True)

    # Parse KGML
    pathway_title, gene_ids = parse.parse_KGML(pathway)
    print("[{} / {}]".format(idx + 1, len(pathway_table)), pathway_title)
    print("\tGenes:", len(gene_ids))

    # Map KEGG identifiers to STRING external identifiers
    kegg2external = dict()
    for mapped_identifiers, idx_offset in api.map_identifiers_to_STRING(gene_ids, args.string_organism_id):
        for idx, external_id, species_id, species_name, preferred_name, annotation in read_table(
            mapped_identifiers,
            (int, str, int, str, str, str),
            delimiter = "\t"
        ):
            gene_id = gene_ids[idx + idx_offset]
            if gene_id in kegg2external:
                print("\tMapping for {} not unique!".format(gene_id))
            else:
                kegg2external[gene_id] = external_id
    
    num_not_mapped = len(gene_ids) - len(kegg2external)
    if num_not_mapped > 0:
        print("\t{} gene(s) could not be mapped to STRING external ID!".format(num_not_mapped))

    # Save the pathway
    # TODO Add more info: DESCRIPTION, DISEASE, DRUG, COMPOUND (parse flat file)
    genes_column = ";".join(kegg2external.values())
    pathways_file.write("{}\t{}\t{}\n".format(pathway_id, pathway_title, genes_column))

pathways_file.close()