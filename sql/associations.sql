
/*
Get associations in-between nodes containing
the scores per channel and the combined score

Fields:
    node_id_a
    node_type_b
    node_id_b
    combined_score
    evidence_scores [ ]
*/

SELECT node_id_a, node_type_b, node_id_b, combined_score, evidence_scores
FROM node_node_links;
