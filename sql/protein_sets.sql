
SELECT actions_sets.item_id_a, actions_sets.item_id_b, proteins1.preferred_name, proteins2.preferred_name, actions_sets.mode, sets_items1.set_id, sets.title 
FROM evidence.sets_items AS sets_items1
CROSS JOIN evidence.sets_items AS sets_items2
JOIN evidence.actions_sets AS actions_sets ON actions_sets.item_id_a = sets_items1.item_id
                                           AND actions_sets.item_id_b = sets_items2.item_id
JOIN evidence.sets AS sets ON sets_items1.set_id = sets.set_id
                           AND sets_items2.set_id = sets.set_id
JOIN items.proteins AS proteins1 ON actions_sets.item_id_a = proteins1.protein_id
JOIN items.proteins AS proteins2 ON actions_sets.item_id_b = proteins2.protein_id
WHERE sets_items1.species_id = 10090 AND sets_items2.species_id = 10090 -- AND title <> 'protein-protein interaction'
LIMIT 1000;
