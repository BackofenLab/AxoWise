import unittest
import random

import context
from context import fuzzy_search, indexing

class TestFuzzySearch(unittest.TestCase):

    def test_search_species(self):

        for query in ["hom", "human", "sapiens"]:
            self.assertIn(
                indexing.Species("Homo sapiens (human)", "hsa", 9606),
                fuzzy_search.search_species(query),
                query
            )

        for query in ["mouse", "mus", "mus muscul"]:
            self.assertIn(
                indexing.Species("Mus musculus (house mouse)", "mmu", 10090),
                fuzzy_search.search_species(query),
                query
            )

        for query in ["chimpanz", "pan t", "Pan troglodytes"]:
            self.assertIn(
                indexing.Species("Pan troglodytes (chimpanzee)", "ptr", 9598),
                fuzzy_search.search_species(query),
                query
            )

    def test_search_protein(self):

        self.assertIn(
            indexing.Protein(2111533, "CCR5", context.SPECIES_ID),
            fuzzy_search.search_protein("ccr5", species_id=context.SPECIES_ID)
        )

        self.assertIn(
            indexing.Protein(2094384, "IL10", context.SPECIES_ID),
            fuzzy_search.search_protein("Il10", species_id=context.SPECIES_ID)
        )

        self.assertIn(
            indexing.Protein(2099183, "IL10RA", context.SPECIES_ID),
            fuzzy_search.search_protein("il10RA", species_id=context.SPECIES_ID)
        )

        self.assertIn(
            indexing.Protein(2100220, "CCL5", context.SPECIES_ID),
            fuzzy_search.search_protein("CCL5", species_id=context.SPECIES_ID)
        )

    def test_search_protein_list(self):

        def randomize_case(string):
            result = ""
            for character in string:
                if random.choice([True, False]):
                    result += character.lower()
                else:
                    result += character.upper()
            return result

        proteins = list(map(lambda p: indexing.Protein(*p), [
            (2093346, "SFPI1", 10090),
            (2093526, "FOSB", 10090),
            (2093704, "MLXIPL", 10090),
            (2093960, "ELK3", 10090),
            (2094351, "FLI1", 10090),
            (2094384, "IL10", 10090),
            (2094594, "IRF1", 10090),
            (2094875, "NFIC", 10090),
            (2094987, "SREBF1", 10090),
            (2095028, "ID2", 10090),
            (2095207, "HIF1A", 10090),
            (2095256, "FOS", 10090),
            (2095683, "MYC", 10090),
            (2095696, "TEF", 10090),
            (2095905, "RUNX1", 10090),
            (2095940, "ATF1", 10090),
            (2096088, "TFEB", 10090),
            (2096699, "BACH1", 10090),
            (2097050, "ATF3", 10090),
            (2097051, "BATF3", 10090),
            (2098470, "BHLHE41", 10090),
            (2099183, "IL10RA", 10090),
            (2099315, "SMAD3", 10090),
            (2100108, "ZFP281", 10090),
            (2100220, "CCL5", 10090),
            (2100325, "CREB3L2", 10090),
            (2100419, "BATF", 10090),
            (2100648, "ERF", 10090),
            (2101330, "KLF9", 10090),
            (2102647, "ZFP691", 10090),
            (2102864, "JUN", 10090),
            (2102933, "KLF7", 10090),
            (2102968, "XBP1", 10090),
            (2103045, "FOXO1", 10090),
            (2103806, "JDP2", 10090),
            (2103842, "CREB1", 10090),
            (2104561, "JUNB", 10090),
            (2104603, "CEBPG", 10090),
            (2104650, "NFIL3", 10090),
            (2104785, "SP100", 10090),
            (2104843, "STAT1", 10090),
            (2104964, "KLF13", 10090),
            (2105219, "EGR1", 10090),
            (2105262, "CEBPB", 10090),
            (2105791, "NFKB2", 10090),
            (2106444, "RXRA", 10090),
            (2106500, "TFE3", 10090),
            (2106818, "ETV5", 10090),
            (2107042, "ETV6", 10090),
            (2107155, "NFE2L1", 10090),
            (2107486, "STAT2", 10090),
            (2107964, "CENPB", 10090),
            (2108666, "RELB", 10090),
            (2109370, "CEBPA", 10090),
            (2109530, "MAFB", 10090),
            (2110338, "SP3", 10090),
            (2110420, "REL", 10090),
            (2110976, "KLF4", 10090),
            (2111058, "BACH2", 10090),
            (2111212, "MAF", 10090),
            (2111287, "ATF4", 10090),
            (2111318, "NFIX", 10090),
            (2111533, "CCR5", 10090),
            (2112825, "IRF9", 10090),
            (2114069, "TGIF1", 10090),
            (2114274, "USF2", 10090)
        ]))

        protein_list = list(map(lambda p: randomize_case(p.name), proteins))
        results = fuzzy_search.search_protein_list(protein_list)

        self.assertEqual(len(protein_list), len(results))
        self.assertSequenceEqual(proteins, results)

    def test_search_pathway(self):

        for query in ["cytok", "Cytokine-cytokine", "cytokine interaction"]:
            self.assertIn(
                indexing.Pathway("path:mmu04060", "Cytokine-cytokine receptor interaction", context.SPECIES_ID),
                fuzzy_search.search_pathway(query, species_id=context.SPECIES_ID),
                query
            )

        for query in ["chemokine", "chemo signaling", "chemokine pathway"]:
            self.assertIn(
                indexing.Pathway("path:mmu04062", "Chemokine signaling pathway", context.SPECIES_ID),
                fuzzy_search.search_pathway(query, species_id=context.SPECIES_ID),
                query
            )

    def test_search_class(self):

        for klass in ["Immune diseases", "Immune system"]:
            self.assertIn(
                indexing.Class(klass),
                fuzzy_search.search_class("immun")
            )

        for query in ["meta", "metabolism"]:
            self.assertIn(
                indexing.Class("Metabolism"),
                fuzzy_search.search_class(query),
                query
            )


if __name__ == "__main__":
    print("Testing fuzzy search...")
    unittest.main()