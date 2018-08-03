import unittest
import database

import sql_queries as SQL

class TestSQLQueries(unittest.TestCase):

    def test_get_species_id(self):

        postgres_connection, _ = database.connect("test/credentials.test.json")
        species_id = SQL.get_species_id(postgres_connection, "Mus musculus")
    
        self.assertEqual(species_id, 10090)


if __name__ == "__main__":
    unittest.main()
