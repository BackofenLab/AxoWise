import unittest

import database
import cypher_queries as Cypher

class TestCypherQueries(unittest.TestCase):

    def test_get_protein_subgraph(self):

        postgres_connection, neo4j_graph = database.connect("test/credentials.test.json")
        postgres_connection.close()

        subgraph = Cypher.get_protein_subgraph(neo4j_graph, "Ccr5")

        for entry in subgraph:
            # self.assertEqual(entry["protein"]["preferred_name"], "Ccr5")
            association = entry["association"]
            action = entry["action"]
            if entry["other"]["preferred_name"] == "Ccl5":
                self.assertEqual(association["coexpression"], 92)
                self.assertEqual(association["database"], 900)
                self.assertEqual(association["textmining"], 906)
                self.assertEqual(association["combined"], 993)
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


if __name__ == "__main__":
    unittest.main()
