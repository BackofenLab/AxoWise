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

    def test_search_protein_list(self):

        proteins = [
            ("SFPI1", 2093346, 10090),
            ("FOSB", 2093526, 10090),
            ("MLXIPL", 2093704, 10090),
            ("ELK3", 2093960, 10090),
            ("FLI1", 2094351, 10090),
            ("IL10", 2094384, 10090),
            ("IRF1", 2094594, 10090),
            ("NFIC", 2094875, 10090),
            ("SREBF1", 2094987, 10090),
            ("ID2", 2095028, 10090),
            ("HIF1A", 2095207, 10090),
            ("FOS", 2095256, 10090),
            ("MYC", 2095683, 10090),
            ("TEF", 2095696, 10090),
            ("RUNX1", 2095905, 10090),
            ("ATF1", 2095940, 10090),
            ("TFEB", 2096088, 10090),
            ("BACH1", 2096699, 10090),
            ("ATF3", 2097050, 10090),
            ("BATF3", 2097051, 10090),
            ("BHLHE41", 2098470, 10090),
            ("IL10RA", 2099183, 10090),
            ("SMAD3", 2099315, 10090),
            ("ZFP281", 2100108, 10090),
            ("CCL5", 2100220, 10090),
            ("CREB3L2", 2100325, 10090),
            ("BATF", 2100419, 10090),
            ("ERF", 2100648, 10090),
            ("KLF9", 2101330, 10090),
            ("ZFP691", 2102647, 10090),
            ("JUN", 2102864, 10090),
            ("KLF7",2102933, 10090),
            ("XBP1", 2102968, 10090),
            ("FOXO1", 2103045, 10090),
            ("JDP2", 2103806, 10090),
            ("CREB1", 2103842, 10090),
            ("JUNB", 2104561, 10090),
            ("CEBPG", 2104603, 10090),
            ("NFIL3", 2104650, 10090),
            ("SP100", 2104785, 10090),
            ("STAT1", 2104843, 10090),
            ("KLF13", 2104964, 10090),
            ("EGR1", 2105219, 10090),
            ("CEBPB", 2105262, 10090),
            ("NFKB2", 2105791, 10090),
            ("RXRA", 2106444, 10090),
            ("TFE3", 2106500, 10090),
            ("ETV5", 2106818, 10090),
            ("ETV6", 2107042, 10090),
            ("NFE2L1", 2107155, 10090),
            ("STAT2", 2107486, 10090),
            ("CENPB", 2107964, 10090),
            ("RELB", 2108666, 10090),
            ("CEBPA", 2109370, 10090),
            ("MAFB", 2109530, 10090),
            ("SP3", 2110338, 10090),
            ("REL", 2110420, 10090),
            ("KLF4", 2110976, 10090),
            ("BACH2", 2111058, 10090),
            ("MAF", 2111212, 10090),
            ("ATF4", 2111287, 10090),
            ("NFIX", 2111318, 10090),
            ("CCR5", 2111533, 10090),
            ("IRF9", 2112825, 10090),
            ("TGIF1", 2114069, 10090),
            ("USF2", 2114274, 10090)
        ]

        protein_list = list(map(lambda p: p[0], proteins))
        results = fuzzy_search.search_protein_list(protein_list)

        self.assertEqual(len(protein_list), len(results))
        self.assertSequenceEqual(proteins, results)

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