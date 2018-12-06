import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Test database is for a mouse (Mus musculus)
SPECIES_ID = 10090

# Databases
import database

# Cypher queries
import cypher_queries as Cypher

# SQL queries
import sql_queries as SQL

# KEGG data
import KEGG.parse as parse

# Fuzzy search
import indexing, fuzzy_search

