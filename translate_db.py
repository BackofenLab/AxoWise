import sys
import argparse
import os.path

import sql_queries as SQL
import cypher_queries as Cypher
import database
from utils import pair_generator, rstrip_line_generator, read_table, batches, concat, lines

from KEGG import get_species_identifiers

def parse_cli_args():
    args_parser = argparse.ArgumentParser(
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )

    args_parser.add_argument(
        "--credentials",
        type = str,
        help = "Path to the credentials JSON file that will be used",
        default = "credentials.json"
    )

    args_parser.add_argument(
        "--species_name",
        type = str,
        help = "Species name",
        default = "Homo sapiens"
    )

    args_parser.add_argument(
        "--protein_list",
        type = str,
        help = "Path to the file containing protein Ensembl IDs"
    )

    args_parser.add_argument(
        "--combined_score_threshold",
        type = int,
        help = "Threshold above which the associations between proteins will be considered"
    )

    args_parser.add_argument(
        "--skip_drugs",
        type = bool,
        help = "Do not add drugs to the resulting graph database",
        default = False
    )

    args_parser.add_argument(
        "--skip_compounds",
        type = bool,
        help = "Do not add compounds to the resulting graph database",
        default = False
    )

    args_parser.add_argument(
        "--skip_diseases",
        type = bool,
        help = "Do not add diseases to the resulting graph database",
        default = False
    )

    args = args_parser.parse_args()
    return args

def read_proteins_list(args):
    protein_ensembl_ids_set = set()
    if args.protein_list is not None:
        protein_ensembl_ids_set = set(lines(os.path.abspath(args.protein_list)))
        print(len(protein_ensembl_ids_set), "protein external IDs loaded.")
    return protein_ensembl_ids_set

def decode_evidence_scores(evidence_scores):
    """
    Maps evidence channel IDs to channel names.
    """

    score_channel_map = {
        6: "coexpression",
        8: "experiments",
        10: "database",
        12: "textmining",
        14: "neighborhood",
        15: "fusion",
        16: "cooccurence"
    }

    params = { channel: None for channel in score_channel_map.values()}
    for score_id, score in evidence_scores:
        if score_id not in score_channel_map:
            continue

        score_type = score_channel_map[score_id]
        params[score_type] = score
    return params

# ======================================== KEGG ========================================
# Compounds
def read_kegg_compounds(args, kegg_id):
    compounds = dict()
    if not args.skip_compounds:
        for id, name in read_table("KEGG/data/kegg_compounds.{}.tsv".format(kegg_id), (str, str), delimiter = "\t", header = True):
            compounds[id] = {
                "id": id,
                "name": name
            }
    return compounds

def write_kegg_compounds(neo4j_graph, compounds):
    print("Creating compounds...")
    num_compounds = 0
    for batch in batches(compounds.values(), batch_size = 1024):
        num_compounds += len(batch)
        print("{}".format(num_compounds), end = "\r")
        Cypher.add_compound(neo4j_graph, {
            "batch": batch
        })
    print()

# Diseases
def read_kegg_diseases(args, kegg_id):
    diseases = dict()
    if not args.skip_diseases:
        for id, name in read_table("KEGG/data/kegg_diseases.{}.tsv".format(kegg_id), (str, str), delimiter = "\t", header = True):
            diseases[id] = {
                "id": id,
                "name": name
            }

    return diseases

def write_kegg_diseases(neo4j_graph, diseases):
    print("Creating diseases...")
    num_diseases = 0
    for batch in batches(diseases.values(), batch_size = 1024):
        num_diseases += len(batch)
        print("{}".format(num_diseases), end = "\r")
        Cypher.add_disease(neo4j_graph, {
            "batch": batch
        })
    print()

# Drugs
def read_kegg_drugs(args, kegg_id):
    drugs = dict()
    if not args.skip_drugs:
        for id, name in read_table("KEGG/data/kegg_drugs.{}.tsv".format(kegg_id), (str, str), delimiter = "\t", header = True):
            drugs[id] = {
                "id": id,
                "name": name
            }
    return drugs

def write_kegg_drugs(neo4j_graph, drugs):
    print("Creating drugs...")
    num_drugs = 0
    for batch in batches(drugs.values(), batch_size = 1024):
        num_drugs += len(batch)
        print("{}".format(num_drugs), end = "\r")
        Cypher.add_drug(neo4j_graph, {
            "batch": batch
        })
    print()

# Pathways
def read_kegg_pathways(kegg_id):
    pathways = list()
    pathway2classes = dict()
    pathway2diseases = dict()
    pathway2drugs = dict()
    pathway2compounds = dict()

    gene2pathways = dict()

    for id, name, description, classes, genes_external_ids, diseases_ids, drugs_ids, compounds_ids in read_table(
        "KEGG/data/kegg_pathways.{}.tsv".format(kegg_id),
        (str, str, str, str, str, str, str, str),
        delimiter = "\t",
        header = True
    ):
        pathway_dict = {
            "id": id,
            "name": name,
            "description": description
        }
        pathway2classes[id] = classes.split(";")
        pathway2diseases[id] = diseases_ids.split(";")
        pathway2drugs[id] = drugs_ids.split(";")
        pathway2compounds[id] = compounds_ids.split(";")

        pathway_dict["class"] = pathway2classes[id][-1]
        pathways.append(pathway_dict)

        for gene_external_id in genes_external_ids.split(";"):
            if gene_external_id not in gene2pathways:
                gene2pathways[gene_external_id] = list()

            gene2pathways[gene_external_id].append(id)

    return (
        pathways,
        pathway2classes,
        pathway2diseases,
        pathway2drugs,
        pathway2compounds,
        gene2pathways
    )

def write_kegg_pathways(neo4j_graph, pathways):
    print("Creating pathways and connecting them to classes...")
    num_pathways = 0
    for batch in batches(pathways, batch_size = 1024):
        num_pathways += len(batch)
        print("{}".format(num_pathways), end = "\r")
        Cypher.add_pathway(neo4j_graph, {
            "batch": batch
        })
    print()

# Classes
def write_classes(neo4j_graph, pathway2classes):
    print("Creating classes and class hierarchy...")
    num_classes = 0
    class_chains = list(pathway2classes.values())
    class_pairs = set()
    for chain in class_chains:
        for i in range(len(chain) - 1):
            parent = chain[i]
            child = chain[i + 1]
            class_pairs.add((parent, child))

    class_pairs = map(
        lambda pair: {
            "name_parent": pair[0],
            "name_child": pair[1]
        },
        class_pairs
    )
    for batch in batches(class_pairs, batch_size = 32):
        num_classes += len(batch)
        print("{}".format(num_classes), end = "\r")
        Cypher.add_class_parent_and_child(neo4j_graph, {
            "batch": batch
        })
    print()

# Associations
def connect_compounds_and_pathways(args, neo4j_graph, pathway2compounds):
    if not args.skip_compounds:
        print("Connecting compounds and pathways...")
        num_compound_pathway_connections = 0
        for pathway_id in pathway2compounds:
            pathway_compound_list = map(
                lambda compound_id: {
                    "compound_id": compound_id,
                    "pathway_id": pathway_id
                },
                pathway2compounds[pathway_id]
            )
            for batch in batches(pathway_compound_list, batch_size = 1024):
                num_compound_pathway_connections += len(batch)
                print("{}".format(num_compound_pathway_connections), end = "\r")
                Cypher.connect_compound_and_pathway(neo4j_graph, {
                    "batch": batch
                })
        print()

def connect_diseases_and_pathways(args, neo4j_graph, pathway2diseases):
    if not args.skip_diseases:
        print("Connecting diseases and pathways...")
        num_disease_pathway_connections = 0
        for pathway_id in pathway2diseases:
            pathway_disease_list = map(
                lambda disease_id: {
                    "disease_id": disease_id,
                    "pathway_id": pathway_id
                },
                pathway2diseases[pathway_id]
            )
            for batch in batches(pathway_disease_list, batch_size = 1024):
                num_disease_pathway_connections += len(batch)
                print("{}".format(num_disease_pathway_connections), end = "\r")
                Cypher.connect_disease_and_pathway(neo4j_graph, {
                    "batch": batch
                })
        print()

def connect_drugs_and_pathways(args, neo4j_graph, pathway2drugs):
    if not args.skip_drugs:
        print("Connecting drugs and pathways...")
        num_drug_pathway_connections = 0
        for pathway_id in pathway2drugs:
            pathway_drug_list = map(
                lambda drug_id: {
                    "drug_id": drug_id,
                    "pathway_id": pathway_id
                },
                pathway2drugs[pathway_id]
            )
            for batch in batches(pathway_drug_list, batch_size = 1024):
                num_drug_pathway_connections += len(batch)
                print("{}".format(num_drug_pathway_connections), end = "\r")
                Cypher.connect_drug_and_pathway(neo4j_graph, {
                    "batch": batch
                })
        print()

# ======================================== STRING ========================================
# Proteins
def read_string_proteins(args, postgres_connection, species_id, protein_ensembl_ids_set):
    proteins = SQL.get_proteins(
    postgres_connection,
    species_id = species_id
    )
    protein_ids_set = set()
    if args.protein_list is not None:
        def filter_proteins(protein):
            valid = protein["external_id"] in protein_ensembl_ids_set
            if valid:
                protein_ids_set.add(protein["id"])
            return valid

        proteins = filter(filter_proteins, proteins)

    return proteins, protein_ids_set

def write_string_proteins(neo4j_graph, proteins):
    print("Creating proteins...")
    num_proteins = 0
    for batch in batches(proteins, batch_size = 1024):
        num_proteins += len(batch)
        print("{}".format(num_proteins), end = "\r")
        Cypher.add_protein(neo4j_graph, {
            "batch": batch
        })
    print()

# Associations
def read_string_associations(args, postgres_connection, species_id, protein_ids_set):
    # Get protein - protein association
    associations = SQL.get_associations(
        postgres_connection,
        species_id = species_id
    )
    if args.protein_list is not None:
        def filter_associations(association):
            if args.combined_score_threshold is None:
                above_threshold = True
            else:
                above_threshold = association["combined_score"] >= args.combined_score_threshold
            in_list = association["id1"] in protein_ids_set and association["id2"] in protein_ids_set
            return above_threshold and in_list

        associations = filter(filter_associations, associations)

    return associations

def write_string_associations(neo4j_graph, associations):
    print("Creating protein - protein associations...")
    num_associations = 0
    for batch in batches(associations, batch_size = 16384):
        num_associations += len(batch)
        print("{}".format(num_associations), end = "\r")

        def map_batch_item(item):
            item = {**item, **decode_evidence_scores(item["evidence_scores"])}
            del item["evidence_scores"]
            return item

        batch = list(map(map_batch_item, batch))

        Cypher.add_association(neo4j_graph, {
            "batch": batch
        })
    print()

def read_string_actions(postgres_connection, species_id):
    # Get protein - protein functional prediction
    actions = SQL.get_actions(
        postgres_connection,
        species_id = species_id
    )

    return actions

def write_string_actions(neo4j_graph, actions):
    print("Creating protein - protein actions...")
    num_actions = 0
    for batch in batches(actions, batch_size = 16384):
        num_actions += len(batch)
        print("{}".format(num_actions), end = "\r")
        Cypher.add_action(neo4j_graph, {
            "batch": batch
        })
    print()

def connect_proteins_and_pathways(args, neo4j_graph, gene2pathways, protein_ensembl_ids_set):
    print("Connecting proteins and pathways...")
    num_protein_pathway_connections = 0
    def map_gene_to_pathways(gene_external_id):
        if gene_external_id not in gene2pathways:
            return []
        return map(lambda pathway_id: {
            "pathway_id": pathway_id,
            "protein_external_id": gene_external_id
        }, gene2pathways[gene_external_id])

    if args.protein_list is not None:
        external_id_source = protein_ensembl_ids_set
    else:
        external_id_source = gene2pathways.keys()

    gene_pathway_lists = map(lambda geid: map_gene_to_pathways(geid), external_id_source)
    gene_pathway_list = concat(gene_pathway_lists)

    for batch in batches(gene_pathway_list, batch_size = 4096):
        num_protein_pathway_connections += len(batch)
        print("{}".format(num_protein_pathway_connections), end = "\r")
        Cypher.connect_protein_and_pathway(neo4j_graph, {
            "batch": batch
        })
    print()

def main():

    # Parse the CLI arguments
    args = parse_cli_args()

    # Get species IDs from the name
    species_name, kegg_id, ncbi_id = get_species_identifiers(args.species_name)
    species_id = ncbi_id
    if species_id is None:
        print("Species not found!")
        sys.exit(1)
    else:
        print("Translating the database for {}.".format(species_name))

    # Read the provided list of proteins (if available)
    protein_ensembl_ids_set = read_proteins_list(args)

    # Connect to the databases
    postgres_connection, neo4j_graph = database.connect(credentials_path = args.credentials)

    # Clean the Neo4j database
    print("Cleaning the old data from Neo4j database...")
    neo4j_graph.delete_all()

    # ======================================== KEGG ========================================
    # Compounds
    compounds = read_kegg_compounds(args, kegg_id)
    write_kegg_compounds(neo4j_graph, compounds)

    # Diseases
    diseases = read_kegg_diseases(args, kegg_id)
    write_kegg_diseases(neo4j_graph, diseases)

    # Drugs
    drugs = read_kegg_drugs(args, kegg_id)
    write_kegg_drugs(neo4j_graph, drugs)

    # Create KEGG data index
    Cypher.create_kegg_index(neo4j_graph)

    # Read pathways
    pathways, pathway2classes, pathway2diseases, pathway2drugs, pathway2compounds, gene2pathways = read_kegg_pathways(kegg_id)

    # Classes
    write_classes(neo4j_graph, pathway2classes)

    # Create pathways
    write_kegg_pathways(neo4j_graph, pathways)

    # Compound <-> Pathway
    connect_compounds_and_pathways(args, neo4j_graph, pathway2compounds)

    # Disease <-> Pathway
    connect_diseases_and_pathways(args, neo4j_graph, pathway2diseases)

    # Drug <-> Pathway
    connect_drugs_and_pathways(args, neo4j_graph, pathway2drugs)

    # ======================================== STRING ========================================
    # Proteins
    proteins, protein_ids_set = read_string_proteins(args, postgres_connection, species_id, protein_ensembl_ids_set)
    write_string_proteins(neo4j_graph, proteins)
    Cypher.create_protein_index(neo4j_graph)

    # Associations
    associations = read_string_associations(args, postgres_connection, species_id, protein_ids_set)
    write_string_associations(neo4j_graph, associations)

    # Actions
    actions = read_string_actions(postgres_connection, species_id)
    write_string_actions(neo4j_graph, actions)

    # ======================================== Merge STRING and KEGG ========================================
    connect_proteins_and_pathways(args, neo4j_graph, gene2pathways, protein_ensembl_ids_set)

    # Close the PostgreSQL connection
    postgres_connection.close()

    print("Done!")

if __name__ == "__main__":
    main()