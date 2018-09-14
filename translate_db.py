import sys
import psycopg2
import py2neo
import argparse

import sql_queries as SQL
import cypher_queries as Cypher
import database
from utils import pair_generator, rstrip_line_generator, read_table

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

    args = args_parser.parse_args()

    # Parse the standard input (until EOF)
    input_stdin = sys.stdin.read()
    lines = input_stdin.split("\n")
    lines.remove("")

    only_species = (len(lines) == 1)

    if not only_species and len(lines) < 3:
        print(
            """
            Expected format (species and optionally at least two proteins):
            <species name>
            [<protein> ...]
            """
        )
        sys.exit(1)

    species = lines[0]
    proteins = lines[1:]

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

    # Read KEGG data
    compounds = dict()
    for id, name in read_table("KEGG/data/kegg_compounds.mmu.tsv", (str, str), delimiter = "\t", header = True):
        compounds[id] = name

    diseases = dict()
    for id, name in read_table("KEGG/data/kegg_diseases.mmu.tsv", (str, str), delimiter = "\t", header = True):
        diseases[id] = name

    drugs = dict()
    for id, name in read_table("KEGG/data/kegg_drugs.mmu.tsv", (str, str), delimiter = "\t", header = True):
        drugs[id] = name

    genes2pathways = dict()
    for id, name, description, classes, genes_external_ids, diseases_ids, drugs_ids, compounds_ids in read_table(
        "KEGG/data/kegg_pathways.mmu.tsv",
        (str, str, str, str, str, str, str, str),
        delimiter = "\t",
        header = True
    ):
        for gene_external_id in genes_external_ids.split(";"):
            if gene_external_id not in genes2pathways:
                genes2pathways[gene_external_id] = list()

            genes2pathways[gene_external_id].append((
                id,
                name,
                description,
                classes.split(";"),
                diseases_ids.split(";"),
                drugs_ids.split(";"),
                compounds_ids.split(";")
            ))

    # Connect to the databases
    postgres_connection, neo4j_graph = database.connect(credentials_path = args.credentials)

    # Get the species id
    species_id = SQL.get_species_id(postgres_connection, species)
    if species_id is None:
        print("Species not found!")
        sys.exit(1)


    # Clear the Neo4j database
    Cypher.delete_all(neo4j_graph)

    # Translate the database for all species proteins
    if only_species:
        # STRING
        # Get protein - protein association
        associations = SQL.get_associations(
            postgres_connection,
            species_id = species_id
        )
        # Get protein - protein functional prediction
        actions_and_pathways = SQL.get_actions_and_pathways(
            postgres_connection,
            species_id = species_id
        )

        # Neo4j
        print("Writing associations...")
        for idx, item in enumerate(associations):
            print("{}".format(idx + 1), end = "\r")
            item = {**item, **decode_evidence_scores(item["evidence_scores"])}
            del item["evidence_scores"]
            Cypher.update_associations(neo4j_graph, item)
        print()

        print("Writing actions & pathways...")
        for idx, item in enumerate(actions_and_pathways):
            print("{}".format(idx + 1), end = "\r")
            Cypher.update_proteins_and_action(neo4j_graph, item)
        print()

    # Translate the database only for specified proteins
    else:
        # For each pair of proteins...
        for protein1, protein2 in pair_generator(proteins):
            print("{} <---> {}".format(protein1, protein2))
            # STRING
            # Get protein - protein association
            associations = SQL.get_associations(
                postgres_connection,
                species_id = species_id,
                protein1 = protein1, protein2 = protein2
            )
            # Get protein - protein functional prediction
            actions_and_pathways = SQL.get_actions_and_pathways(
                postgres_connection,
                species_id = species_id,
                protein1 = protein1, protein2 = protein2
            )

            # Neo4j
            print("Writing associations...")
            for idx, item in enumerate(associations):
                print("{}".format(idx + 1), end = "\r")
                item = {**item, **decode_evidence_scores(item["evidence_scores"])}
                del item["evidence_scores"]
                Cypher.update_associations(neo4j_graph, item)
            print()

            print("Writing actions & pathways...")
            for idx, item in enumerate(actions_and_pathways):
                print("{}".format(idx + 1), end = "\r")
                Cypher.update_proteins_and_action(neo4j_graph, item)
            print()

    # Remove redundant properties of nodes used to correctly construct the graph
    Cypher.remove_redundant_properties(neo4j_graph)

    print("Done!")

    # Close the PostgreSQL connection
    postgres_connection.close()

if __name__ == "__main__":
    main()