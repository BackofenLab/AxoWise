import sys
import psycopg2
import py2neo

import sql_queries as SQL
import cypher_queries as Cypher
from connect_db import connect
from utils import pair_generator, rstrip_line_generator

# Parse standard input

import fileinput

lines = list(rstrip_line_generator(fileinput.input(), skip_empty = True))

if len(lines) < 3:
    print(
        """
        Expected format (species and at least two proteins):
        <species name>
        <protein>
        <protein>
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

def decode_evidence_scores(evidence_scores):
    params = { channel: None for channel in score_channel_map.values()}
    for score_id, score in evidence_scores:
        if score_id not in score_channel_map:
            continue

        score_type = score_channel_map[score_id]
        params[score_type] = score
    return params


# Connect to the databases
postgres_connection, neo4j_graph = connect()

species_id = SQL.get_species_id(postgres_connection, species)
if species_id is None:
    print("Species not found!")
    sys.exit(1)


Cypher.delete_all(neo4j_graph)

for protein1, protein2 in pair_generator(proteins):
	print("{} <---> {}".format(protein1, protein2))
	# STRING
	associations = SQL.get_associations(
	    postgres_connection,
	    species_id = species_id,
	    protein1 = protein1, protein2 = protein2
	)
	actions_and_pathways = SQL.get_actions_and_pathways(
	    postgres_connection,
	    species_id = species_id,
	    protein1 = protein1, protein2 = protein2
	)

	# Neo4j
	print("Writing associations...")
	for idx, item in enumerate(associations):
	    # print("{}".format(idx + 1), end = "\r")
	    item = {**item, **decode_evidence_scores(item["evidence_scores"])}
	    del item["evidence_scores"]
	    print(item)
	    Cypher.update_associations(neo4j_graph, item)
	print()

	print("Writing actions & pathways...")
	for idx, item in enumerate(actions_and_pathways):
	    # print("{}".format(idx + 1), end = "\r")
	    print(item)
	    Cypher.update_proteins_and_action(neo4j_graph, item)
	print()

Cypher.remove_redundant_properties(neo4j_graph)

print("Done!")

postgres_connection.close()
