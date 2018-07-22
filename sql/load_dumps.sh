#!/bin/bash

# Create the database
psql -c "CREATE DATABASE string;"

# Load the schema dumps
psql string < items_schema.v10.5.sql
psql string < network_schema.v10.5.sql
psql string < evidence_schema.v10.5.sql
