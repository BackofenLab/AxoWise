import pandas as pd
import numpy as np
from neo4j import Driver
from upload.upload_experiment import create_correlation, create_context, create_motif
from utils import execute_query, print_update

__CATLAS__STUDY = {"name": "Catlas, Whole Mouse Brain", "source": "catlas.org/wholemousebrain/"}


def create_source(cell_info: pd.DataFrame, species: str, driver: Driver):
    print_update(update_type="Node Creation", text="Study, (Sub-/Subsub-)Celltype and Source", color="blue")
    _, nuclei_counts, celltype, subtype, subsubtype = (
        cell_info["region"],
        cell_info["nuclei_counts"],
        cell_info["celltype"],
        cell_info["subtype"],
        cell_info["sub-subtype"],
    )
    flag = True
    query = ""

    # Create Study
    query += f"""MERGE (s:Study {{name: "{__CATLAS__STUDY['name']}", source: "{__CATLAS__STUDY['source']}"}})"""

    # Create Cell Node (for Celltype)
    if celltype is not np.NaN:
        query += f""" MERGE (n1:Celltype:{species}{{name: "{celltype}"}})"""

    # Create Cell Node (for Subtype)
    if subtype is not np.NaN:
        query += f""" MERGE (n2:Subtype:{species}{{name: "{subtype}"}})"""
        query += f""" MERGE (n1)-[:IS]->(n2)"""
    else:
        query += f""" CREATE (n1)-[:HAS]->(o:Source:{species})<-[:HAS]-(s)"""
        flag = False

    # Create Cell Node (for Subsubtype)
    if flag:
        if subsubtype is not np.NaN:
            query += f""" MERGE (n3:Subtype:{species}{{name: "{subsubtype}"}})"""
            query += f""" MERGE (n2)-[:IS]->(n3)"""
            query += f""" CREATE (n3)-[:HAS]->(o:Source:{species})<-[:HAS]-(s)"""
        else:
            query += f""" CREATE (n2)-[:HAS]->(o:Source:{species})<-[:HAS]-(s)"""

    query += """ SET o.id = id(o)"""
    query += """ RETURN id(o) as id """

    result = execute_query(query=query, read=False, driver=driver)

    return result[0][0]


def extend_db_from_catlas(
    catlas_motifs: pd.DataFrame,
    catlas_or_context: pd.DataFrame,
    catlas_correlation: pd.DataFrame,
    catlas_celltype: pd.DataFrame,
    species: str,
    driver: Driver,
):
    for _, i in catlas_celltype.iterrows():
        print_update(update_type="Uploading", text=i["name"], color="pink")
        source = create_source(cell_info=i, driver=driver, species=species)

        or_context = catlas_or_context[catlas_or_context["cell_id"] == i["name"]].drop(columns=["cell_id"])
        create_context(
            context_type="Location", context=or_context, source=source, value_type=0, species=species, driver=driver
        )

        correlation = catlas_correlation[catlas_correlation["cell_id"] == i["name"]].drop(columns=["cell_id"])
        create_correlation(correlation=correlation, source=source, value_type=0, species=species, driver=driver)

        motif = catlas_motifs[catlas_motifs["cell_id"] == i["name"]].drop(columns=["cell_id"])
        create_motif(motif=motif, source=source, species=species, driver=driver)

    print_update(update_type="Done", text="Extending DB from Catlas Data", color="pink")
