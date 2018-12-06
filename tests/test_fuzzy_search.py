import unittest

import context
from context import fuzzy_search

class TestFuzzySearch(unittest.TestCase):

    def test_search_species(self):

        for query in ["hom", "human", "sapiens"]:
            self.assertIn(
                ("Homo sapiens (human)", "hsa", 9606),
                fuzzy_search.search_species(query),
                query
            )

        for query in ["mouse", "mus", "mus muscul"]:
            self.assertIn(
                ("Mus musculus (house mouse)", "mmu", 10090),
                fuzzy_search.search_species(query),
                query
            )

        for query in ["chimpanz", "pan t", "Pan troglodytes"]:
            self.assertIn(
                ("Pan troglodytes (chimpanzee)", "ptr", 9598),
                fuzzy_search.search_species(query),
                query
            )

    def test_search_protein(self):

        self.assertIn(
            ("CCR5", 2111533, context.SPECIES_ID),
            fuzzy_search.search_protein("ccr5", species_id=context.SPECIES_ID)
        )

        self.assertIn(
            ("IL10", 2094384, context.SPECIES_ID),
            fuzzy_search.search_protein("Il10", species_id=context.SPECIES_ID)
        )

        self.assertIn(
            ("IL10RA", 2099183, context.SPECIES_ID),
            fuzzy_search.search_protein("il10RA", species_id=context.SPECIES_ID)
        )

        self.assertIn(
            ("CCL5", 2100220, context.SPECIES_ID),
            fuzzy_search.search_protein("CCL5", species_id=context.SPECIES_ID)
        )

    def test_search_pathway(self):

        for query in ["cytok", "Cytokine-cytokine", "cytokine interaction"]:
            self.assertIn(
                ("Cytokine-cytokine receptor interaction", "path:mmu04060", context.SPECIES_ID),
                fuzzy_search.search_pathway(query, species_id=context.SPECIES_ID),
                query
            )

        for query in ["chemokine", "chemo signaling", "chemokine pathway"]:
            self.assertIn(
                ("Chemokine signaling pathway", "path:mmu04062", context.SPECIES_ID),
                fuzzy_search.search_pathway(query, species_id=context.SPECIES_ID),
                query
            )

    def test_search_class(self):

        for klass in ["Immune diseases", "Immune system"]:
            self.assertIn(
                klass,
                fuzzy_search.search_class("immun")
            )

        for query in ["meta", "metabolism"]:
            self.assertIn(
                "Metabolism",
                fuzzy_search.search_class(query),
                query
            )


if __name__ == "__main__":
    print("Testing fuzzy search...")
    unittest.main()