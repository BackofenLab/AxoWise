"""
Collection of functions that handle user queries and
suggest top matches based on fuzzy search techniques.
"""

# ========================= Species =========================
from indexing import create_species_q_gram_index, search_q_gram_index

species_index = create_species_q_gram_index()

def search_species(query):
    """
    Retrieve top-matching species for a given
    species name or NCBI ID.
    """
    return search_q_gram_index(query, species_index)

# ========================= Protein =========================
from indexing import create_protein_q_gram_index

protein_index = create_protein_q_gram_index()

def search_protein(query):
    """
    Retrieve top-matching proteins for a given
    protein name or Ensembl ID.
    """
    return search_q_gram_index(query, protein_index)

# ========================= Pathway =========================
from indexing import create_pathway_q_gram_index

pathway_index = create_pathway_q_gram_index()

def search_pathway(query):
    """
    Retrieve top-matching pathways for a given
    pathway name or KEGG ID.
    """
    return search_q_gram_index(query, pathway_index)


if __name__ == "__main__":
    while True:
        query = input("Species > ")
        print(search_species(query))

        query = input("Protein > ")
        print(search_protein(query))

        query = input("Pathway > ")
        print(search_pathway(query))