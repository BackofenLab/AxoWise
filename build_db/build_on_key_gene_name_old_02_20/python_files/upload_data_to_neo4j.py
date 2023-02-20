"""
Author: Tillman Heisner
Email: theisner@posteo.de

This connects to the local neo4j database. It expects that the files, which are
used for building the example database, with gene name as the primary key, to 
be in the import folder of the neo4j home directory.
"""
from py2neo import Graph
from getpass import getpass
import pandas as pd

port = input("Neo4j DB Port: ")
user = input("Neo4j DB Username: ")
pswd = getpass()

# Make sure the database is started first, otherwise attempt to 
# connect will fail
try:
    graph = Graph('bolt://localhost:'+port, auth=(user, pswd))
    print('SUCCESS: Connected to the Neo4j Database.')
except Exception as e:
    print('ERROR: Could not connect to the Neo4j Database. \
          See console for details.')
    raise SystemExit(e)
queries_1 = pd.read_csv("queries_proteins_tf_or_and_cor.csv",header=None)

# iterate over the csv file, print the comments and run the queries
for index, row in queries_1.iterrows():
    # comments are at index = [0, 2, 4, ...]
    if (index % 2 == 0):
        print(row[0])
    # queries are at index = [1, 3, 5, ...]
    else:
        query = row[0]
        try:
            graph.run(query)
            print("Query terminated sucessfull.")
        except Exception as e:
            print("Upload failed.")
            raise SystemExit(e)

queries_2 = pd.read_csv("queries_exp_time_data.csv",header=None)
# print the first row
print(queries_2.iloc[0][0])
# the queries come after first row
for i, row in queries_2.iloc[1:].iterrows():
    query = row[0]
    try:
        graph.run(query)
        print("Query terminated sucessfull.")
    except Exception as e:
        print("Upload failed.")
        raise SystemExit(e)

