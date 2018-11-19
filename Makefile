
env:
	conda env create -f conda_env.yml

test:
	# Load the toy database
	psql -U postgres -c "DROP DATABASE string;"
	psql -U postgres -c "CREATE DATABASE string;"
	psql -U postgres string < sql/dump.schema.psql
	psql -U postgres string < sql/dump.test.psql

	# Run the unit tests
	python tests/test_kegg.py
	python tests/test_sql_queries.py
	python translate_db.py --credentials tests/credentials.test.json --species_name "Mus musculus"
	python tests/test_cypher_queries.py
