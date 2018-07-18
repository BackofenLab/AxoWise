import os.path
from utils import read_table

version = "v10.5"

species = [
    (os.path.join("STRING", "Homo sapiens"), 9606),
    (os.path.join("STRING", "Mus musculus"), 10090)
]

for species_dir, species_id in species:
    actions_filename = "{}.protein.actions.{}.txt".format(species_id, version)
    links_filename = "{}.protein.links.detailed.{}.txt".format(species_id, version)
    actions_path = os.path.join(species_dir, actions_filename)
    links_path = os.path.join(species_dir, links_filename)

    # Read actions
    # item_id_a	item_id_b	mode	action	is_directional	a_is_acting	score
    # 9606.ENSP00000000233	9606.ENSP00000263025	inhibition	inhibition	f	t	150
    actions = list(
        read_table(
            actions_path,
            (str, str, str, str, str, str, int),
            delimiter = "\t"
        )
    )
    
    # Read links
    # protein1 protein2 neighborhood fusion cooccurence coexpression experimental database textmining combined_score
    # 9606.ENSP00000000233 9606.ENSP00000263431 0 0 0 53 176 0 128 260
    links = list(
        read_table(
            links_path,
            (str, str, int, int, int, int, int, int, int, int),
            delimiter = "\t"
        )
    )
