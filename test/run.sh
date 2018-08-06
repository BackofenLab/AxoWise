#!/bin/bash

# Load the toy database
psql -U postgres -c "DROP DATABASE string;"
psql -U postgres -c "CREATE DATABASE string;"
psql -U postgres string < sql/dump.schema.psql
psql -U postgres string < sql/dump.test.psql

# Run the unit tests
export PYTHONPATH=$PYTHONPATH:$(pwd)
python test/test_sql_queries.py
