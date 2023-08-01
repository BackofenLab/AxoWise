import pandas as pd
import numpy as np
from neo4j import Driver
from upload.upload_experiment import create_correlation, create_context
from utils import execute_query

__CATLAS__STUDY = {"name": "Catlas, Whole Mouse Brain", "source": "catlas.org/wholemousebrain/"}


def create_source(cell_info: pd.DataFrame, driver: Driver):
    id = 0
    region, nuclei_counts, celltype, subtype, subsubtype = (
        cell_info["region"],
        cell_info["nuclei_counts"],
        cell_info["celltype"],
        cell_info["subtype"],
        cell_info["sub-subtype"],
    )
    query = ""

    # Create Study
    query += f"""MERGE (s:Study {{name: "{__CATLAS__STUDY['name']}", source: "{__CATLAS__STUDY['source']}"}})"""

    # Create Cell Node (for Celltype)
    if celltype is not np.NaN:
        query += f""" MERGE (n1:Celltype{{name: "{celltype}"}})"""

    # Create Cell Node (for Subtype)
    if subtype is not np.NaN:
        query += f""" MERGE (n2:Celltype{{name: "{subtype}"}})"""
        query += f""" MERGE (n1)-[:IS]->(n2)"""
    else:
        query += """ CREATE (n1)-[:HAS]->(o:Source)<-[:HAS]-(s)"""

    # Create Cell Node (for Subsubtype)
    if subsubtype is not np.NaN:
        query += f""" MERGE (n3:Celltype{{name: "{subsubtype}"}})"""
        query += f""" MERGE (n2)-[:IS]->(n3)"""
        query += """ CREATE (n3)-[:HAS]->(o:Source)<-[:HAS]-(s)"""
    else:
        query += """ CREATE (n2)-[:HAS]->(o:Source)<-[:HAS]-(s)"""

    query += """ SET o.id = id(o)"""
    query += """ RETURN id(o) as id """

    result = execute_query(query=query, read=False, driver=driver)

    return result[0][0]


def extend_db_from_catlas(
    catlas_or_context: pd.DataFrame, catlas_correlation: pd.DataFrame, catlas_celltype: pd.DataFrame, driver: Driver
):
    for _, i in catlas_celltype.iterrows():
        source = create_source(cell_info=i, driver=driver)

        or_context = catlas_or_context[catlas_or_context["cell_id"] == i["name"]].drop(columns=["cell_id"])
        create_context(context=or_context, source=source, value_type=0, driver=driver)

        correlation = catlas_correlation[catlas_correlation["cell_id"] == i["name"]].drop(columns=["cell_id"])
        create_correlation(correlation=correlation, source=source, value_type=0, driver=driver)
