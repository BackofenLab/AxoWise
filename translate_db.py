import sys
import argparse
import os.path

import sql_queries as SQL
import cypher_queries as Cypher
import database
from utils import pair_generator, rstrip_line_generator, read_table, batches, concat, lines

def main():
    # Parse CLI arguments
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
        "--kegg_organism_id",
        type = str,
        help = "KEGG organism ID",
        default = "hsa"
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
    KOID = args.kegg_organism_id

    protein_ensembl_ids_set = set()
    protein_ids_set = set()
    if args.protein_list is not None:
        protein_ensembl_ids_set = set(lines(os.path.abspath(args.protein_list)))
        print(len(protein_ensembl_ids_set), "protein external IDs loaded.")

    species = args.species_name

    # Useful functions
    score_channel_map = {
        6: "coexpression",
        8: "experiments",
        10: "database",
        12: "textmining",
        14: "neighborhood",
        15: "fusion",
        16: "cooccurence"
    }

    # Maps evidence channel ids to channel names (score_channel_map values)
    def decode_evidence_scores(evidence_scores):
        params = { channel: None for channel in score_channel_map.values()}
        for score_id, score in evidence_scores:
            if score_id not in score_channel_map:
                continue

            score_type = score_channel_map[score_id]
            params[score_type] = score
        return params

    # Connect to the databases
    postgres_connection, neo4j_graph = database.connect(credentials_path = args.credentials)

    # Get the species id
    species_id = SQL.get_species_id(postgres_connection, species)
    if species_id is None:
        print("Species not found!")
        sys.exit(1)

    # Clean the Neo4j database
    print("Cleaning the old data from Neo4j database...")
    neo4j_graph.delete_all()

    # Read KEGG data
    # Compounds
    if not args.skip_compounds:
        compounds = dict()
        for id, name in read_table("KEGG/data/kegg_compounds.{}.tsv".format(KOID), (str, str), delimiter = "\t", header = True):
            compounds[id] = {
                "id": id,
                "name": name
            }

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
    if not args.skip_diseases:
        diseases = dict()
        for id, name in read_table("KEGG/data/kegg_diseases.{}.tsv".format(KOID), (str, str), delimiter = "\t", header = True):
            diseases[id] = {
                "id": id,
                "name": name
            }

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
    if not args.skip_drugs:
        drugs = dict()
        for id, name in read_table("KEGG/data/kegg_drugs.{}.tsv".format(KOID), (str, str), delimiter = "\t", header = True):
            drugs[id] = {
                "id": id,
                "name": name
            }

        print("Creating drugs...")
        num_drugs = 0
        for batch in batches(drugs.values(), batch_size = 1024):
            num_drugs += len(batch)
            print("{}".format(num_drugs), end = "\r")
            Cypher.add_drug(neo4j_graph, {
                "batch": batch
            })
        print()

    # Create KEGG data index
    Cypher.create_kegg_index(neo4j_graph)

    # Pathways
    pathways = list()
    pathway2classes = dict()
    pathway2diseases = dict()
    pathway2drugs = dict()
    pathway2compounds = dict()

    gene2pathways = dict()

    for id, name, description, classes, genes_external_ids, diseases_ids, drugs_ids, compounds_ids in read_table(
        "KEGG/data/kegg_pathways.{}.tsv".format(KOID),
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

    print("Creating pathways and connecting them to classes...")
    num_pathways = 0
    for batch in batches(pathways, batch_size = 1024):
        num_pathways += len(batch)
        print("{}".format(num_pathways), end = "\r")
        Cypher.add_pathway(neo4j_graph, {
            "batch": batch
        })
    print()

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

    # STRING
    # Get all proteins
    proteins = SQL.get_proteins(
        postgres_connection,
        species_id = species_id
    )
    if args.protein_list is not None:
        def filter_proteins(protein):
            valid = protein["external_id"] in protein_ensembl_ids_set
            if valid:
                protein_ids_set.add(protein["id"])
            return valid

        proteins = filter(filter_proteins, proteins)

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

    if args.protein_list is not None:
        # Get protein - protein functional prediction
        actions = SQL.get_actions(
            postgres_connection,
            species_id = species_id
        )

    print("Creating proteins...")
    num_proteins = 0
    for batch in batches(proteins, batch_size = 1024):
        num_proteins += len(batch)
        print("{}".format(num_proteins), end = "\r")
        Cypher.add_protein(neo4j_graph, {
            "batch": batch
        })
    print()
    # Create protein index
    Cypher.create_protein_index(neo4j_graph)

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

    if args.protein_list is None:
        print("Creating protein - protein actions...")
        num_actions = 0
        for batch in batches(actions, batch_size = 16384):
            num_actions += len(batch)
            print("{}".format(num_actions), end = "\r")
            Cypher.add_action(neo4j_graph, {
                "batch": batch
            })
        print()

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

    print("Done!")

    # Close the PostgreSQL connection
    postgres_connection.close()

if __name__ == "__main__":
    main()