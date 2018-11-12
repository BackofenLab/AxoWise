import unittest

import database
import sql_queries as SQL

class TestSQLQueries(unittest.TestCase):

    def test_get_species_id(self):

        postgres_connection, _ = database.connect("test/credentials.test.json")
        species_id = SQL.get_species_id(postgres_connection, "homo sapiens")
    
        self.assertEqual(species_id, 9606)

        postgres_connection.close()

    def test_get_proteins(self):
        postgres_connection, _ = database.connect("test/credentials.test.json")
        
        proteins = SQL.get_proteins(postgres_connection, species_id = 9606)

        entered_if_1 = False
        entered_if_2 = False
        num_proteins = 0
        for protein in proteins:
            num_proteins += 1
            if protein["preferred_name"].upper() == "ccl5".upper():
                entered_if_1 = True
                self.assertEqual(protein["id"], 1847396)
                self.assertEqual(protein["external_id"], "9606.ENSP00000293272")
                self.assertEqual(
                    protein["annotation"],
                    "Chemokine (C-C motif) ligand 5; Chemoattractant for blood monocytes, memory T-helper cells "
                    "and eosinophils. Causes the release of histamine from basophils and activates eosinophils. "
                    "May activate several chemokine receptors including CCR1, CCR3, CCR4 and CCR5. One of the major "
                    "HIV-suppressive factors produced by CD8+ T-cells. Recombinant RANTES protein induces a dose-dependent "
                    "inhibition of different strains of HIV-1, HIV-2, and simian immunodeficiency virus (SIV). The "
                    "processed form RANTES(3-68) acts as a natural chemotaxis inhibitor and is a more potent inhibitor of "
                    "HIV-1- infection.  [...]"
                )
            elif protein["preferred_name"].upper() == "ccr5".upper():
                entered_if_2 = True
                self.assertEqual(protein["id"], 1847342)
                self.assertEqual(protein["external_id"], "9606.ENSP00000292303")
                self.assertEqual(
                    protein["annotation"],
                    "Chemokine (C-C motif) receptor 5 (gene/pseudogene); Receptor for a number of inflammatory "
                    "CC-chemokines including MIP-1-alpha, MIP-1-beta and RANTES and subsequently transduces a "
                    "signal by increasing the intracellular calcium ion level. May play a role in the control "
                    "of granulocytic lineage proliferation or differentiation. Acts as a coreceptor (CD4 being "
                    "the primary receptor) for HIV-1 R5 isolates"
                )

        self.assertGreater(num_proteins, 0)
        self.assertTrue(entered_if_1 and entered_if_2)

        postgres_connection.close()

    def test_get_associations(self):

        postgres_connection, _ = database.connect("test/credentials.test.json")

        associations = SQL.get_associations(postgres_connection, species_id = 9606)

        num_associations = 0
        entered_if = False
        for association in associations:
            num_associations += 1
            if association["id1"] == 1847342 and association["id2"] == 1847396:
                entered_if = True
                self.assertEqual(association["combined_score"], 997)
                self.assertEqual(
                    association["evidence_scores"],
                    [
                        [6, 152],   # array_score
                        [7, 43],   # array_score_transferred
                        [8, 360],  # experimental_score_transferred
                        [10, 900], # database_score
                        [12, 962], # textmining_score
                        [13, 127]  # textmining_score_transferred
                    ]
                )

        self.assertGreater(num_associations, 0)
        self.assertTrue(entered_if)

        postgres_connection.close()

    # def test_get_actions(self):

    #     postgres_connection, _ = database.connect("test/credentials.test.json")

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
