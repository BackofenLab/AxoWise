import unittest

import database
import cypher_queries as Cypher

class TestCypherQueries(unittest.TestCase):

    def test_get_protein_subgraph(self):

        postgres_connection, neo4j_graph = database.connect("test/credentials.test.json")
        postgres_connection.close()

        subgraph = Cypher.get_protein_subgraph(neo4j_graph, "Ccr5")

        for entry in subgraph:
            self.assertEqual(entry["protein"]["preferred_name"], "Ccr5")
            association = entry["association"]

            if entry["other"] is not None:
                self.assertIn(entry["other"]["preferred_name"], ["Ccl5", "Ccr5", "Il10ra"])
                
                if entry["other"]["preferred_name"] == "Ccl5":
                    self.assertEqual(association["coexpression"], 92)
                    self.assertEqual(association["database"], 900)
                    self.assertEqual(association["textmining"], 906)
                    self.assertEqual(association["combined"], 993)

                    if entry["action"] is not None:
                        self.assertIn(entry["action"]["mode"], [
                            "ptmod",
                            "reaction",
                            "binding",
                            "catalysis",
                            "activation"
                        ])
                        action = entry["action"]

                        if action["mode"] == "binding":
                            self.assertEqual(action["score"], 849)
                        elif action["mode"] == "ptmod":
                            self.assertEqual(action["score"], 171)
                        elif action["mode"] == "catalysis":
                            self.assertEqual(action["score"], 278)
                        elif action["mode"] == "reaction":
                            self.assertEqual(action["score"], 278)
                        elif action["mode"] == "activation":
                            self.assertEqual(action["score"], 849)

                    elif entry["other"]["preferred_name"] == "Il10ra":
                        self.assertEqual(association["coexpression"], 246) 
                        self.assertEqual(association["textmining"], 318)
                        self.assertEqual(association["combined"], 469)

            if entry["pathway"] is not None:
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

                self.assertIsNone(entry["drug"])
                self.assertIsNone(entry["disease"])

                if entry["compound"] is not None:
                    self.assertIn(entry["compound"]["name"], [
                        "L-Homocysteine",
                        "Potassium cation",
                        "Nitric oxide",
                        "Defensin alpha-1",
                        "Defensin alpha-2",
                        "Defensin alpha-3",
                        "Defensin alpha-4",
                        "Defensin alpha-5",
                        "Defensin beta-1",
                        "Defensin beta-2",
                        "Defensin beta-3",
                        "Defensin beta-4",
                        "Hydrogen peroxide",
                        "Corticosterone",
                        "L-Arginine",
                        "Bradykinin",
                        "H+",
                        "Vitamin D3",
                        "Parathyroid hormone",
                        "Lipopolysaccharide",
                        "1-Phosphatidyl-D-myo-inositol",
                        "Calcidiol",
                        "Calcitriol",
                        "Sphingosine 1-phosphate",
                        "Trehalose-6,6'-dibehenate",
                        "Trehalose dimycolate",
                        "Lipomannan",
                        "Triacylated phosphatidyl-myo-inositol pentamannoside",
                        "Triacylated phosphatidyl-myo-inositol hexamannoside",
                        "Triacylated phosphatidyl-myo-inositol dimannoside",
                        "Tetraacylated phosphatidyl-myo-inositol dimannoside",
                        "Tetraacylated phosphatidyl-myo-inositol hexamannoside",
                        "Tetraacylated phosphatidyl-myo-inositol pentamannoside",
                        "Lipoarabinomannan",
                        "Mannose-capped lipoarabinomannan",
                        "Calcium cation",
                        "Diacylglycerol",
                        "3',5'-Cyclic AMP",
                        "D-myo-Inositol 1,4,5-trisphosphate",
                        "Phosphatidylinositol-3,4,5-trisphosphate",
                        "GDP",
                        "GTP",
                        "1-Phosphatidyl-1D-myo-inositol 3-phosphate",
                        "1-Phosphatidyl-D-myo-inositol 4,5-bisphosphate",
                        "1-Phosphatidyl-1D-myo-inositol 3,5-bisphosphate",
                        "Lipoxin A4",
                        "Prostaglandin E2",
                        "Cyclic GMP-AMP",
                        "Phosphatidylethanolamine",
                        "ATP"
                    ])

if __name__ == "__main__":
    print("Testing Cypher queries...")
    unittest.main()
