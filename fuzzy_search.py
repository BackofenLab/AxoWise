"""
Collection of functions that handle user queries and
suggest top matches based on fuzzy search techniques.
"""

# ========================= Species =========================
from indexing import create_species_q_gram_index, search_species_q_gram_index

species_index = create_species_q_gram_index()

def search_species(query):
    """
    Retrieve top-matching species for a given
    species name or NCBI ID.
    """
    return search_species_q_gram_index(query, species_index)

# ========================= Protein =========================

def search_protein(query):
    """
    Retrieve top-matching proteins for a given
    protein name or Ensembl ID.
    """
    pass

# ========================= Pathway =========================

def search_pathway(query):
    """
    Retrieve top-matching pathways for a given
    pathway name or KEGG ID.
    """
    pass
