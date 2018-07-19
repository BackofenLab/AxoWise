/*
Get actions in-between proteins

Fields:
    item_id_a
    item_id_b
    mode
    action
    is_directional
    a_is_acting
    actions
    score
*/

SELECT item_id_a, item_id_b, mode, action, score
FROM actions;
