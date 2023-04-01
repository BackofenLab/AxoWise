"""
Collection of functions that handle user queries and
suggest top match based on direct search techniques.
"""

from indexing import create_species_q_gram_index, get_protein_connection
from indexing import search_q_gram_index

# ========================= Species =========================
_SPECIES_INDEX = create_species_q_gram_index()

def search_species(query):
    """
    Retrieve top-matching species for a given
    species name.
    """
    return search_q_gram_index(query, _SPECIES_INDEX)

# ========================= Protein =========================
protein_list = get_protein_connection()


def search_protein_list(query_list, species_id):
    """
    Retrieve a single protein for each
    protein name in the given list.
    """
    
    result = list()
    for query in query_list:       
        proteinset = protein_list[query.upper()]
        for items in map(lambda p: p.species_id, proteinset):
            if (proteinset != set()): 
                if( items == species_id ):
                    result.append(list(protein_list[query.upper()]).pop())
    return result