#!/bin/bash

# Create the database
psql -U postgres -c "CREATE DATABASE string;"

# Load the schema dumps
psql -U postgres string < dump.schema.psql
psql -U postgres string < dump.test.psql
