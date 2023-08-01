import pandas as pd
import numpy as np
import urllib


def parse_catlas(or_nodes: pd.DataFrame, distance: pd.DataFrame):
    catlas_celltype = pd.read_csv("../source/catlas/cell_infos.csv")
    or_ids = pd.read_csv("../source/catlas/ccre_id_dict.csv")
    tmp_or = or_ids.filter(items=["id"])
    tmp_or["annotation"] = np.NaN
    tmp_or["feature"] = np.NaN

    or_extended = pd.concat([or_nodes, tmp_or], ignore_index=True)
    or_extended = or_extended.drop_duplicates(["id"])

    catlas_or_context = pd.DataFrame(columns=["summit", "id", "cell_id"])

    for name in catlas_celltype["name"]:
        df_ccre = pd.read_csv(f"../source/catlas/ccre/{name}.bed", sep="\t", header=None)
        df_ccre.columns = ["chrom", "chromStart", "chromEnd", "name"]
        df_ccre["summit"] = round(df_ccre["chromStart"] + ((df_ccre["chromEnd"] - df_ccre["chromStart"]) / 2))
        df_ccre["summit"] = df_ccre["summit"].astype(int)
        df_ccre = df_ccre.merge(or_ids, how="left", left_on="name", right_on="name").filter(items=["summit", "id"])
        df_ccre["cell_id"] = name
        catlas_or_context = pd.concat([catlas_or_context, df_ccre], ignore_index=True)

    catlas_or_context = catlas_or_context.merge(catlas_celltype, left_on="cell_id", right_on="name", how="left")
    catlas_or_context = catlas_or_context.rename(columns={"region": "Context"}).filter(items=["Context", "id", "cell_id", "summit"])

    catlas_correlation = pd.read_csv("../source/catlas/cell_specific_correlation.csv", sep="\t")
    catlas_correlation = catlas_correlation.merge(or_ids, how="left", left_on="cCRE", right_on="name")
    catlas_correlation = catlas_correlation.filter(["id", "ENSEMBL", "Correlation", "Cell"]).rename(columns={"Cell": "cell_id"})

    catlas_distance = pd.read_csv("../source/catlas/gene_ccre_distance.csv").merge(or_ids, left_on="cCRE", right_on="name", how="left").filter(items=["id", "Distance", "ENSEMBL"]).dropna()
    
    distance_extended = pd.concat([distance, catlas_distance], ignore_index=True).drop_duplicates(subset=["id", "ENSEMBL"], keep="first")
    return or_extended, catlas_or_context, catlas_correlation, catlas_celltype, distance_extended
