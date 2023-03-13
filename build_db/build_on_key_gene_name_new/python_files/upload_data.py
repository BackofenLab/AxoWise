"""
Author: Tillman Heisner
Email: theisner@posteo.de

This connects to the local neo4j database. It expects that the files, which are
used for building the example database, with gene name as the primary key, to
be in this path "../final_data/".
"""

from py2neo import Graph
# from getpass import getpass
import pandas as pd
import os


def upload_relationships(data: str, comment: str, query: list,
                         path: str) -> None:
    """
    function: Upload relationships in batches of 1 million to a neo4j database
    input:
        - csv file with relationships between nodes
        - corresponding comment in regards to the query
        - pandas dataframe with the wanted queries
        - path to the import folder of neo4j

        This is for the future to give a console feedback on
        how many nodes got created
        if str(count_relation_ship_1) != '(No data)':
            console_return = 'Suceeded uploading:'
            console_return += str(count_relation_ship_1)[26:-1]
            console_return += ' of the first relationship'
            print(console_return)
        if str(count_relation_ship_2) != '(No data)':
            console_return = 'Suceeded uploading:'
            console_return += str(count_relation_ship_2)[26:-1]
            console_return += ' of the second relationship'
    """
    # read data csv file in chunks of 1 million rows
    chunks = pd.read_csv(data, chunksize=10**6, header=0)

    # comment of the query
    print(comment)

    # this creates the source node
    # if there is no source needed, it is just a placeholder query
    create_source = query[0]

    # the source node only gets created once so it runs here
    graph.run(create_source)

    # this matches the correlation nodes with the study and cell
    # and then creates the relationships between them
    # if there is no second relationship, it is just a place holder query
    create_rel_study_cell_source = query[4]

    # these relationships only get created once so it runs here
    graph.run(create_rel_study_cell_source)

    # this creates temporary nodes
    create_temp_nodes = query[1]

    # this matches the temporary nodes with the corresponding nodes
    # and then creates the first relationship
    create_rel_1 = query[2]

    # this matches the temporary nodes with the corresponding nodes
    # and then creates the second relationship
    # if there is no second relationship, it is just a place holder query
    create_rel_2 = query[3]

    # this deletes the temporary nodes again because we dont need them
    delete_temp_nodes = query[5]

    # iterate over the chunks and upload the data
    for chunk in chunks:
        # feedback for the user
        size_of_chunk = chunk.shape[0]
        print(f"Uploading {size_of_chunk} correlations")

        # write the chunks to csv file to a temporary file
        # in the neo4j import folder
        chunk.to_csv((path + "/temp.csv"), index=None)

        # run the actual queries
        try:
            graph.run(create_temp_nodes)
            graph.run(create_rel_1)
            graph.run(create_rel_2)
            graph.run(delete_temp_nodes)
            print("Query terminated sucessfull.")
        except Exception as e:
            print("Upload of the batch failed.")
            raise SystemExit(e)

        # delete the temporary csv file
        os.remove(path + "/temp.csv")
    return None


def upload_nodes(data: str, comment: str, query: str, path: str) -> None:
    """
    function: Upload nodes
    input:
        - csv file with relationships between nodes
        - corresponding comment in regards to the query
        - pandas dataframe with the wanted queries
        - path to the import folder of neo4j
    """
    # read data csv file in chunks of 1 million rows
    chunks = pd.read_csv(data, chunksize=10**6, header=0)

    # console feedback
    print(comment)

    # iterate over the chunks and upload the data
    for chunk in chunks:
        # feedback for the user
        size_of_chunk = chunk.shape[0]
        print(f"Uploading {size_of_chunk} entity nodes")

        # write the chunks to csv file to a temporary file
        # in the neo4j import folder
        chunk.to_csv((path + "/temp.csv"), index=None)

        # run the actual queries
        try:
            graph.run(query)
            print("Query terminated sucessfull.")
        except Exception as e:
            print("Upload failed.")
            raise SystemExit(e)

        # delete the temporary csv file
        os.remove(path + "/temp.csv")
    return (None)


def create_single_nodes(comment: str, query: str) -> None:
    """
    function: Create single nodes in the database
    input:
        - the corresponding comment in regards to the query
        - pandas dataframe with the wanted queries
    """
    # console feedback
    print(comment)

    # try to run the query
    try:
        graph.run(query)
        print("Query terminated sucessfull.")
    except Exception as e:
        print("Upload failed.")
        raise SystemExit(e)
    return (None)


if __name__ == '__main__':
    # establish the connection to the neo4j database
    # port = input("Neo4j DB Port: ")
    # user = input("Neo4j DB Username: ")
    # pswd = getpass()

    port = "7687"
    user = "neo4j"
    pswd = "pgdb"

    # make the graph global so the functions can access it
    global graph

    # path to the neo4j import directory
    neo4j_import_dir = "/var/lib/neo4j/import"

    # Make sure the database is started first, otherwise attempt to
    # connect will fail
    try:
        graph = Graph('bolt://localhost:'+port, auth=(user, pswd))
        print('SUCCESS: Connected to the Neo4j Database.')
    except Exception as e:
        print('ERROR: Could not connect to the Neo4j Database. \
            See console for details.')
        raise SystemExit(e)
    path_to_import_dir = "/var/lib/neo4j/import"

    # the query for the cell and study
    query_cell_study = pd.read_csv("query_study_cell.csv", header=None)

    # upload the nodes
    for index, row in query_cell_study.iloc[:].iterrows():
        if (index % 2 == 0):
            comment = row[0]
        else:
            query = row[0]
            create_single_nodes(comment, query)

    # the biological entities
    entities = ["TranscriptionFactor.csv", "OpenRegion.csv",
                "string_proteins_filtered.csv",
                "proteins_unique_to_exp_data.csv",
                "KappaTerms.csv"]

    # the query for the biological entities
    query_entities = pd.read_csv("queries_biological_entities.csv",
                                 header=None)

    # upload the biological entites
    for index, row in query_entities.iloc[:].iterrows():
        if (index % 2 == 0):
            comment = row[0]
            file = entities[int(index/2)]
        else:
            query = row[0]
            upload_nodes("../final_data/" + file, comment, query,
                         neo4j_import_dir)

    # the relationships, it is important that they are in the order in
    # which they are in the query file
    relationships = ["rel_or_wt12h_wt0h.csv",
                     "rel_or_wt336h_wt0h.csv",
                     "rel_or_wtRC12h_wt12h_padj.csv",
                     "rel_or_wt12h_wt0h_padj.csv",
                     "rel_or_wtRC12h_wt0h.csv",
                     "rel_or_wtRC336h_wt0h_padj.csv",
                     "rel_or_wt24h_wt0h.csv",
                     "rel_or_wtRC12h_wt0h_padj.csv",
                     "rel_or_wt24h_wt0h_padj.csv",
                     "rel_or_wtRC12h_wt12h.csv",
                     "rel_protein_wt6h_wt0h.csv",
                     "rel_protein_wtRC12h_wt6h.csv",
                     "rel_protein_wt24h_wt0h.csv",
                     "rel_protein_wt6h_wt0h_padj.csv",
                     "rel_protein_wtRC12h_wt6h_padj.csv",
                     "rel_protein_wt336h_wt0h.csv",
                     "rel_protein_wtRC12h_wt0h_padj.csv",
                     "rel_protein_wt24h_wt0h_padj.csv",
                     "rel_protein_wtRC12h_wt0h.csv",
                     "rel_protein_wtRC336h_wt0h_padj.csv",
                     "TF_target_cor_.csv",
                     "peak_target_cor_.csv",
                     "TF_motif_peak.csv",
                     "rel_nearest_distance.csv",
                     "rel_string_funtional_terms_to_proteins.csv",
                     "OverlapEdges.csv",
                     "rel_string_proteins_to_proteins.csv",
                     "rel_mean_count.csv"]

    # the query for the relationships
    query_relationships = pd.read_csv("queries_correlation.csv", header=None)

    # the list containing the queries
    query = []

    # upload the relationships
    for index, row in query_relationships.iloc[:].iterrows():
        if (index % 7 == 0):
            comment = row[0]
            file = relationships[int(index/7)]
        elif (index % 7 == 1):
            query.append(row[0])
        elif (index % 7 == 2):
            query.append(row[0])
        elif (index % 7 == 3):
            query.append(row[0])
        elif (index % 7 == 4):
            query.append(row[0])
        elif (index % 7 == 5):
            query.append(row[0])
        else:
            query.append(row[0])
            upload_relationships("../final_data/" + file, comment,
                                 query, neo4j_import_dir)
            query = []
