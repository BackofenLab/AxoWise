
/*

items.proteins:
    protein_id - internal protein identifier
    protein_external_id - taxonomy identifier and name of protein concatenated.
    species_id - taxonomy identifier
    protein_checksum - checksum of the protein sequence
    protein_size - length of the protein (in amino acids)
    annotation - description of the functionality of protein
    preferred_name - the preferred name of STRING (e.g. "amiF")
    annotation_word_vectors - internal use only: enables full-text searching

network.node_node_links:
    node_id_a - internal identifier (equivalent to protein_id)
    node_id_b - internal identifier (equivalent to protein_id)
    node_type_b - taxonomy identifier (equivalent to species_id)
    combined_score - the combined score of all the evidence scores (including transferred scores)
    evidence_score - the scores of the individual channels represented as a list of score types and
                    their score. For example, {{4,626}} means that coocurrance score (4) is 0.626.
                    The types of score can be found in table network.score_types.

network.actions:
    item_id_a - internal protein identifier
    item_id_b - internal protein identifier
    mode - type of interaction:
           "reaction",
           "expression",
           "activation",
           "ptmod"(post-translational modifications),
           "binding",
           "catalysis"
    action - the effect of the action ("inhibition", "activation")
    a_is_acting - the directionality of the action if applicable (1 gives that item_id_a is acting upon item_id_b)
    score - the best combined score of all interactions in string

network.score_types:
    score_id - internal identifier
    score_type - the type of the score, see below

    score_type  name
    1           equiv_nscore
    2           equiv_nscore_transferred
    3           equiv_fscore
    4           equiv_pscore
    5           equiv_hscore
    6           array_score
    7           array_score_transferred
    8           experimental_score
    9           experimental_score_transferred
    10          database_score
    11          database_score_transferred
    12          textmining_score
    13          textmining_score_transferred
    14          neighborhood_score (deprecated)
    15          fusion_score (deprecated)
    16          cooccurence_score (deprecated)

*/

SELECT proteins1.preferred_name,
       proteins2.preferred_name, 
       links.combined_score,
       links.evidence_score
FROM items.proteins AS proteins1
JOIN network.node_node_links AS links
     ON links.node_id_a = proteins1.protein_id
JOIN items.proteins AS proteins2
     ON links.node_id_b = proteins2.protein_id
WHERE proteins1.species_id = 9606 OR
      proteins1.species_id = 10090;

-- Homo sapiens (9606) or Mus musculus (10090)

