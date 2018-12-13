"""
Collection of functions that handle user queries and
suggest top matches based on fuzzy search techniques.
"""

from indexing import create_species_q_gram_index
from indexing import create_protein_q_gram_index
from indexing import create_pathway_q_gram_index
from indexing import create_class_q_gram_index
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
_PROTEIN_INDEX = create_protein_q_gram_index()

def search_protein(query, species_id=None):
    """
    Retrieve top-matching proteins for a given
    protein name.
    """
    def condition(item):
        _, _, item_species_id = item
        return species_id == item_species_id

    return search_q_gram_index(
        query,
        _PROTEIN_INDEX,
        condition if (species_id is not None) else None
    )

# ========================= Pathway =========================
_PATHWAY_INDEX = create_pathway_q_gram_index()

def search_pathway(query, species_id=None):
    """
    Retrieve top-matching pathways for a given
    pathway name.
    """
    def condition(item):
        _, _, item_species_id = item
        return species_id == item_species_id

    return search_q_gram_index(
        query,
        _PATHWAY_INDEX,
        condition if (species_id is not None) else None
    )

# ========================= Class =========================
_CLASS_INDEX = create_class_q_gram_index()

def search_class(query):
    """
    Retrieve top-matching pathway class names
    for a given class name.
    """
    return search_q_gram_index(query, _CLASS_INDEX)
