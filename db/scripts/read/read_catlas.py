import pandas as pd
import numpy as np
import urllib


def parse_catlas(or_nodes: pd.DataFrame):
    catlas_celltype = pd.read_csv("../source/catlas/cell_infos.csv")
    or_ids = pd.read_csv("../source/catlas/ccre_id_dict.csv")
    tmp_or = or_ids.filter("id")
    tmp_or["annotation"] = np.NaN
    tmp_or["feature"] = np.NaN
    or_extended = pd.concat([or_nodes, tmp_or], ignore_index=True)
    or_extended = or_extended.drop_duplicates()

    catlas_or_context = pd.DataFrame(columns=["summit", "id", "cell_id"])

    for name in catlas_celltype["name"]:
        urllib.request.urlretrieve(
            f"http://catlas.org/catlas_downloads/wholemousebrain/cCREs/{name}", f"../source/catlas/ccre/{name}"
        )
        df_ccre = pd.read_csv(f"../source/catlas/ccre/{name}", sep="\t", header=None)
        df_ccre.columns = ["chrom", "chromStart", "chromEnd", "name"]
        df_ccre["summit"] = round(df_ccre["chromStart"] + ((df_ccre["chromEnd"] - df_ccre["chromStart"]) / 2))
        df_ccre = df_ccre.merge(or_ids, how="left", left_on="name", right_on="name").filter(items=["summit", "id"])
        df_ccre["cell_id"] = name
        catlas_or_context = pd.concat([catlas_or_context, df_ccre], ignore_index=True)

    catlas_correlation = pd.read_csv("../source/catlas/cell_specific_correlation.csv", sep="\t")
    catlas_correlation = catlas_correlation.merge(or_ids, how="left", left_on="cCRE", right_on="name")
    catlas_correlation = catlas_correlation.filter(["id", "ENSEMBL", "Correlation", "Cell"])

    print(catlas_correlation)
    print(catlas_or_context)
    print(or_extended)
    print(catlas_celltype)

    return or_extended, catlas_or_context, catlas_correlation, catlas_celltype
