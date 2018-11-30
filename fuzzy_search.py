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
    species name.
    """
    return search_q_gram_index(query, species_index)

# ========================= Protein =========================

from indexing import create_protein_q_gram_index
protein_index = create_protein_q_gram_index()

def search_protein(query, species_id=None):
    """
    Retrieve top-matching proteins for a given
    protein name.
    """
    def condition(item):
        _, _, item_species_id = item
        return species_id == item_species_id

    return search_q_gram_index(query, protein_index, condition if (species_id is not None) else None)

# ========================= Pathway =========================

from indexing import create_pathway_q_gram_index
pathway_index = create_pathway_q_gram_index()

def search_pathway(query, species_id=None):
    """
    Retrieve top-matching pathways for a given
    pathway name.
    """
    def condition(item):
        _, _, item_species_id = item
        return species_id == item_species_id

    return search_q_gram_index(query, pathway_index, condition if (species_id is not None) else None)


if __name__ == "__main__":
    while True:
        query = input("Species > ")
        result = search_species(query)
        species_name, kegg_id, ncbi_id = result[0]
        print(result)
        print()

        query = input("Protein > ")
        print("Without species ID:", search_protein(query))
        print("With species ID:", search_protein(query, species_id=ncbi_id))
        print()

        query = input("Pathway > ")
        print("Without species ID:", search_pathway(query))
        print("With species ID:", search_pathway(query, species_id=ncbi_id))
        print()