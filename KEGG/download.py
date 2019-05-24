
import argparse
import os
import sys

sys.path.append("..")

from KEGG import api
from KEGG import parse
import fuzzy_search
from utils import read_table, exit_on


def parse_cli_args():

    parser = argparse.ArgumentParser(
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "species_name",
        type = str,
        help = "Species name (e.g. Homo sapiens / human)",
    )

    return parser.parse_args()

@exit_on(KeyboardInterrupt)
def main():
    # Parse CLI arguments
    args = parse_cli_args()

    # Fuzzy search for species
    species_name, kegg_id, ncbi_id = fuzzy_search.search_species(args.species_name)[0]
    print("Downloading KEGG data for {}.".format(species_name))
    input("Press any key to continue...")

    # Directory for saving the data
    DATA_DIR = "data"
    os.makedirs(DATA_DIR, exist_ok = True)

    # Diseases, drugs & compounds
    diseases_file = open(os.path.join(DATA_DIR, "kegg_diseases.{}.tsv".format(kegg_id)), mode = "w", encoding = "utf-8")
    drugs_file = open(os.path.join(DATA_DIR, "kegg_drugs.{}.tsv".format(kegg_id)), mode = "w", encoding = "utf-8")
    compounds_file = open(os.path.join(DATA_DIR, "kegg_compounds.{}.tsv".format(kegg_id)), mode = "w", encoding = "utf-8")

    written_diseases = set()
    written_drugs = set()
    written_compounds = set()

    # Pathways
    print("Downloading pathways for: {}".format(kegg_id))
    pathways_file = open(os.path.join(DATA_DIR, "kegg_pathways.{}.tsv".format(kegg_id)), mode = "w", encoding = "utf-8")

    # Write headers
    diseases_file.write("\t".join(["id", "name"]) + "\n")
    drugs_file.write("\t".join(["id", "name"]) + "\n")
    compounds_file.write("\t".join(["id", "name"]) + "\n")
    pathways_file.write("\t".join([
        "id",
        "name",
        "description",
        "classes",
        "genes_external_ids",
        "diseases_ids",
        "drugs_ids",
        "compounds_ids"
    ]) + "\n")


    pathways = api.pathways(kegg_id)

    # Get the pathway
    pathway_table = list(read_table(pathways, (str, str), "\t"))
    for idx, (pathway_id, pathway_name) in enumerate(pathway_table):
        pathway = api.pathway(pathway_id, kgml = False)

        # Parse the KEGG pathway flat file
        pathway_parsed = parse.parse_flat_file(pathway)
        pathway_title = pathway_parsed[0]
        pathway_description = pathway_parsed[1]
        pathway_classes = pathway_parsed[2]
        pathway_diseases = pathway_parsed[3]
        pathway_drugs = pathway_parsed[4]
        pathway_genes = pathway_parsed[5]
        pathway_compounds = pathway_parsed[6]

        print("[{} / {}]".format(idx + 1, len(pathway_table)), pathway_title)

        # Description
        has_description = pathway_description is not None

        # Classes
        has_classes = pathway_classes is not None

        # Genes
        has_genes = pathway_genes is not None
        if has_genes:
            gene_ids, gene_short_names, gene_long_names = zip(*pathway_genes)
            gene_ids = list(map(lambda gene_id: "{}:{}".format(kegg_id, gene_id), list(gene_ids)))
            print("\tGenes:", len(gene_ids))

            # Map KEGG gene identifiers to STRING external identifiers
            kegg2external = dict()
            for mapped_identifiers, idx_offset in api.map_identifiers_to_STRING(gene_ids, ncbi_id):
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

        # Diseases
        has_diseases = pathway_diseases is not None
        if has_diseases:
            disease_ids, disease_names = zip(*pathway_diseases)
            for disease in pathway_diseases:
                if disease not in written_diseases:
                    diseases_file.write("{}\t{}\n".format(*disease))
                    written_diseases.add(disease)

        # Drugs
        has_drugs = pathway_drugs is not None
        if has_drugs:
            drug_ids, drug_names = zip(*pathway_drugs)
            for drug in pathway_drugs:
                if drug not in written_drugs:
                    drugs_file.write("{}\t{}\n".format(*drug))
                    written_drugs.add(drug)

        # Compounds
        has_compounds = pathway_compounds is not None
        if has_compounds:
            compound_ids, compound_names = zip(*pathway_compounds)
            for compound in pathway_compounds:
                if compound not in written_compounds:
                    compounds_file.write("{}\t{}\n".format(*compound))
                    written_compounds.add(compound)

        # Save the pathway
        description_column = pathway_description if has_description else ""
        genes_column = ";".join(kegg2external.values()) if has_genes else ""
        classes_column = ";".join(pathway_classes) if has_classes else ""
        diseases_column = ";".join(disease_ids) if has_diseases else ""
        drugs_column = ";".join(drug_ids) if has_drugs else ""
        compounds_column = ";".join(compound_ids) if has_compounds else ""
        pathways_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                pathway_id,
                pathway_title,
                description_column,
                classes_column,
                genes_column,
                diseases_column,
                drugs_column,
                compounds_column
            )
        )

    pathways_file.close()
    diseases_file.close()
    drugs_file.close()
    compounds_file.close()

if __name__ == "__main__":
    main()
