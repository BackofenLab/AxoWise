import unittest

import context
from context import database, Cypher, fuzzy_search

class TestCypherQueries(unittest.TestCase):

    def test_get_protein_subgraph(self):

        neo4j_graph = database.connect_neo4j(context.CREDENTIALS_FILE_PATH)

        protein_id = fuzzy_search.search_protein("ccr5", context.SPECIES_ID)[0].id

        result = list(Cypher.get_protein_subgraph(neo4j_graph, protein_id))

        has_ccl5_other = False
        has_il10ra_other = False

        self.assertEqual(len(result), 1)
        data = result[0]

        protein = data["protein"]
        self.assertEqual(protein["name"], "CCR5")

        associations = data["associations"]
        for association in associations:
            combined_score = association["combined_score"]
            other = association["other"]

            if other["name"] == "CCL5":
                has_ccl5_other = True
                # self.assertEqual(association["coexpression"], 92)
                # self.assertEqual(association["database"], 900)
                # self.assertEqual(association["textmining"], 906)
                self.assertEqual(combined_score, 993)

            elif other["name"] == "IL10RA":
                has_il10ra_other = True
                #self.assertEqual(association["coexpression"], 246)
                #self.assertEqual(association["textmining"], 318)
                self.assertEqual(combined_score, 469)

        pathways = data["pathways"]
        for pathway in pathways:
            self.assertIn(pathway["name"], [
                "Toll-like receptor signaling pathway",
                "NOD-like receptor signaling pathway",
                "Cytosolic DNA-sensing pathway",
                "TNF signaling pathway",
                "Prion diseases",
                "Chagas disease (American trypanosomiasis)",
                "Influenza A",
                "Herpes simplex infection",
                "Rheumatoid arthritis",
                "JAK-STAT signaling pathway",
                "Tuberculosis",
                "Epstein-Barr virus infection",
                "Cytokine-cytokine receptor interaction",
                "Chemokine signaling pathway",
                "Endocytosis",
                "Toxoplasmosis",
                "Human cytomegalovirus infection",
                "Kaposi sarcoma-associated herpesvirus infection",
                "Human immunodeficiency virus 1 infection",
                "Viral carcinogenesis"
            ])

        self.assertTrue(has_ccl5_other)
        self.assertTrue(has_il10ra_other)

    def test_get_pathway_subgraph(self):
        neo4j_graph = database.connect_neo4j(context.CREDENTIALS_FILE_PATH)

        pathway_name, pathway_id, species_id = fuzzy_search.search_pathway("chemo signaling path", species_id=context.SPECIES_ID)[0]

        result = Cypher.get_pathway_subgraph(neo4j_graph, pathway_id)

        for entry in result:
            self.assertEqual(entry["pathway"]["name"], "Chemokine signaling pathway")
            self.assertEqual(
                entry["pathway"]["description"],
                "Inflammatory immune response requires the recruitment of leukocytes to the site "
                "of inflammation upon foreign insult. Chemokines are small chemoattractant peptides "
                "that provide directional cues for the cell trafficking and thus are vital for "
                "protective host response. In addition, chemokines regulate plethora of biological "
                "processes of hematopoietic cells to lead cellular activation, differentiation and "
                "survival."
            )
            self.assertEqual(entry["pathway"]["id"], "path:mmu04062")
            self.assertEqual(sorted(map(lambda c: c["name"], entry["classes"])), ["Immune system", "Organismal Systems"])
            self.assertEqual(len(entry["proteins"]), 180)

    def test_get_class_subgraph(self):
        neo4j_graph = database.connect_neo4j(context.CREDENTIALS_FILE_PATH)

        class_name = fuzzy_search.search_class("Immun sstem")[0].name

        result = Cypher.get_class_subgraph(neo4j_graph, class_name)

        num_entries = 0
        for entry in result:
            num_entries += 1
            class_name = entry["class"]["name"]
            self.assertEqual(class_name, "Immune system")
            num_pathways = len(entry["pathways"])
            self.assertEqual(num_pathways, 20)

        self.assertEqual(num_entries, 1)

if __name__ == "__main__":
    print("Testing Cypher queries...")
    unittest.main()
