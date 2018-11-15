import unittest

import database
import cypher_queries as Cypher

class TestCypherQueries(unittest.TestCase):

    def test_search_protein(self):

        postgres_connection, neo4j_graph = database.connect("test/credentials.test.json")
        postgres_connection.close()

        result = Cypher.search_protein(neo4j_graph, "ccr5")

        num_entries = 0
        has_pathway = False
        has_ccl5_other = False
        has_il10ra_other = False
        for entry in result:
            num_entries += 1
            self.assertEqual(entry["protein"]["name"], "CCR5")
            association = entry["association"]

            if entry["other"] is not None:
                
                if entry["other"]["name"] == "CCL5":
                    has_ccl5_other = True
                    self.assertEqual(association["coexpression"], 92)
                    self.assertEqual(association["database"], 900)
                    self.assertEqual(association["textmining"], 906)
                    self.assertEqual(association["combined"], 993)

                    # if entry["action"] is not None:
                    #     self.assertIn(entry["action"]["mode"], [
                    #         "ptmod",
                    #         "reaction",
                    #         "binding",
                    #         "catalysis",
                    #         "activation"
                    #     ])
                    #     action = entry["action"]

                    #     if action["mode"] == "binding":
                    #         self.assertEqual(action["score"], 849)
                    #     elif action["mode"] == "ptmod":
                    #         self.assertEqual(action["score"], 171)
                    #     elif action["mode"] == "catalysis":
                    #         self.assertEqual(action["score"], 278)
                    #     elif action["mode"] == "reaction":
                    #         self.assertEqual(action["score"], 278)
                    #     elif action["mode"] == "activation":
                    #         self.assertEqual(action["score"], 849)

                elif entry["other"]["name"] == "IL10RA":
                    has_il10ra_other = True
                    self.assertEqual(association["coexpression"], 246) 
                    self.assertEqual(association["textmining"], 318)
                    self.assertEqual(association["combined"], 469)

            if entry["pathway"] is not None:
                has_pathway = True
                self.assertIn(entry["pathway"]["name"], [
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

        self.assertGreater(num_entries, 0)
        self.assertTrue(has_ccl5_other)
        self.assertTrue(has_il10ra_other)
        self.assertTrue(has_pathway)

    def test_search_pathway(self):
        postgres_connection, neo4j_graph = database.connect("test/credentials.test.json")
        postgres_connection.close()

        result = Cypher.search_pathway(neo4j_graph, "chemokine")

        num_entries = 0
        for entry in result:
            num_entries += 1

        self.assertEqual(num_entries, 1)


if __name__ == "__main__":
    print("Testing Cypher queries...")
    unittest.main()
