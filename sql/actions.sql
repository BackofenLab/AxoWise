/*

network.actions:
    item_id_a - internal protein identifier
    item_id_b - internal protein identifier
    mode - type of interaction ("reaction", "expression", "activation", "ptmod"(post-translational modifications),
           "binding", "catalysis")
    action - the effect of the action ("inhibition", "activation")
    a_is_acting - the directionality of the action if applicable (1 gives that item_id_a is acting upon item_id_b)
    score - the best combined score of all interactions in string

*/

SELECT item_id_a, item_id_b, mode, action, score
FROM actions;
