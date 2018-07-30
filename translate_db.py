import psycopg2
import py2neo

import sql_queries as SQL
import cypher_queries as Cypher
from connect_db import connect

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

# STRING
print("Reading the STRING database...")
score_types = SQL.get_score_types(postgres_connection)
species_id = SQL.get_species_id(postgres_connection, "Mus musculus")
actions_and_pathways = SQL.get_actions_and_pathways(postgres_connection, species_id = species_id, protein1 = "Ccl5", protein2 = "Ccr5")
associations = SQL.get_associations(postgres_connection, species_id = species_id, protein1 = "Ccl5", protein2 = "Ccr5")

# Neo4j
Cypher.delete_all(neo4j_graph)

print("Writing to the Neo4j database...")

print("Actions & pathways")
for idx, item in enumerate(actions_and_pathways):
    print("{}".format(idx + 1), end = "\r")
    Cypher.update_proteins_and_action(neo4j_graph, item)
print()

print("Associations")
for idx, item in enumerate(associations):
    print("{}".format(idx + 1), end = "\r")
    item = {**item, **decode_evidence_scores(item["evidence_scores"])}
    del item["evidence_scores"]
    Cypher.update_associations(neo4j_graph, item)
print()

Cypher.remove_redundant_properties(neo4j_graph)

print("Done!")

postgres_connection.close()