import unittest

from context import database, SQL

class TestSQLQueries(unittest.TestCase):

    def test_get_species_id(self):

        postgres_connection = database.connect_postgres("tests/credentials.test.json")
        species_id = SQL.get_species_id(postgres_connection, "mus musculus")
    
        self.assertEqual(species_id, 10090)

        postgres_connection.close()

    def test_get_proteins(self):
        postgres_connection = database.connect_postgres("tests/credentials.test.json")
        
        proteins = SQL.get_proteins(postgres_connection, species_id = 10090)

        entered_if_1 = False
        entered_if_2 = False
        num_proteins = 0
        for protein in proteins:
            num_proteins += 1
            if protein["preferred_name"].upper() == "ccl5".upper():
                entered_if_1 = True
                self.assertEqual(protein["id"], 2100220)
                self.assertEqual(protein["external_id"], "10090.ENSMUSP00000039600")
                self.assertEqual(
                    protein["annotation"],
                    "Chemokine (C-C motif) ligand 5; "
                    "Chemoattractant for blood monocytes, memory T-helper cells and eosinophils. Causes "
                    "the release of histamine from basophils and activates eosinophils. May activate "
                    "several chemokine receptors including CCR1, CCR3, CCR4 and CCR5. May also be an "
                    "agonist of the G protein-coupled receptor GPR75. Together with GPR75, may play a "
                    "role in neuron survival through activation of a downstream signaling pathway "
                    "involving the PI3, Akt and MAP kinases. By activating GPR75 may also play a role in "
                    "insulin secretion by islet cells"
                )
            elif protein["preferred_name"].upper() == "ccr5".upper():
                entered_if_2 = True
                self.assertEqual(protein["id"], 2111533)
                self.assertEqual(protein["external_id"], "10090.ENSMUSP00000107069")
                self.assertEqual(
                    protein["annotation"],
                    "Chemokine (C-C motif) receptor 5; Receptor for a number of inflammatory CC-chemokines "
                    "including MIP-1-alpha, MIP-1-beta and RANTES and subsequently transduces a signal "
                    "by increasing the intracellular calcium ion level. May play a role in the control of "
                    "granulocytic lineage proliferation or differentiation (By similarity)"
                )

        self.assertGreater(num_proteins, 0)
        self.assertTrue(entered_if_1 and entered_if_2)

        postgres_connection.close()

    def test_get_associations(self):

        postgres_connection = database.connect_postgres("tests/credentials.test.json")

        associations = SQL.get_associations(postgres_connection, species_id = 10090)

        num_associations = 0
        entered_if = False
        for association in associations:
            num_associations += 1
            if association["id1"] == 2100220 and association["id2"] == 2111533:
                entered_if = True
                self.assertEqual(association["combined_score"], 993)
                self.assertEqual(
                    association["evidence_scores"],
                    [
                        [6, 92],   # array_score
                        [7, 52],   # array_score_transferred
                        [9, 111],  # experimental_score_transferred
                        [10, 900], # database_score
                        [12, 906], # textmining_score
                        [13, 278]  # textmining_score_transferred
                    ]
                )

        self.assertGreater(num_associations, 0)
        self.assertTrue(entered_if)

        postgres_connection.close()

    # def test_get_actions(self):

    #     postgres_connection = database.connect_postgres("tests/credentials.test.json")

    #     actions = list(SQL.get_actions(postgres_connection, species_id = 10090))

    #     self.assertGreater(len(actions), 5)

    #     entered_if = False
    #     for ap in actions:
    #         if ap["id1"] == 2100220 and ap["id2"] == 2111533:
    #             entered_if = True
    #             if ap["mode"] == "activation":
    #                 self.assertEqual(ap["score"], 849)
    #             elif ap["mode"] == "binding":
    #                 self.assertEqual(ap["score"], 849)
    #             elif ap["mode"] == "catalysis":
    #                 self.assertEqual(ap["score"], 278)
    #             elif ap["mode"] == "ptmod":
    #                 self.assertEqual(ap["score"], 171)
    #             elif ap["mode"] == "reaction":
    #                 self.assertIn(ap["score"], (922, 278))

    #     self.assertTrue(entered_if)

    #     postgres_connection.close()

if __name__ == "__main__":
    print("Testing SQL queries...")
    unittest.main()
