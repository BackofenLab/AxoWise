import unittest
import database

import sql_queries as SQL

class TestSQLQueries(unittest.TestCase):

    def test_get_species_id(self):

        postgres_connection, _ = database.connect("test/credentials.test.json")
        species_id = SQL.get_species_id(postgres_connection, "Mus musculus")
    
        assert species_id == 10090

        query, params = SQL.QueryBuilder.species_id_query("Mus musculus")
        connect.return_value.cursor.return_value.execute.assert_called_once_with(query, params)

if __name__ == "__main__":
    unittest.main()
