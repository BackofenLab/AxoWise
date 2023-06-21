from utils import print_update
import pandas as pd
import os
import numpy as np


def parse_ensembl(dir_path: str = os.getenv("_DEFAULT_ENSEMBL_PATH")):
    """
    Reads ENSEMBL files and returns a Pandas dataframe
    [ Mus_musculus.GRCm39.109.ena.tsv,    Mus_musculus.GRCm39.109.entrez.tsv,
      Mus_musculus.GRCm39.109.refseq.tsv, Mus_musculus.GRCm39.109.uniprot.tsv ]

    """

    def read_ensembl():
        dataframes = [None] * 4

        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".tsv":
                df, index = _reformat_ensembl_term_file(
                    df=pd.read_csv(file, sep="\t"), file_name=file_name.split("/")[-1]
                )
            dataframes[index] = df
        return dataframes

    def post_processing(ensembl: list[pd.DataFrame]):
        complete = pd.concat(ensembl)
        complete = complete.drop(columns=["ENTREZID"])
        complete = complete.drop_duplicates(ignore_index=True)

        tmp_1 = complete[~complete["Protein"].isna()]
        tmp_2 = complete[complete["Protein"].isna()]

        # Remove rows where ENSEMBL has at least one associated Protein in other row, but where its Protein value is NaN
        complete = pd.concat(
            [tmp_2[~tmp_2["ENSEMBL"].isin(set(tmp_2["ENSEMBL"]).difference(tmp_1["ENSEMBL"]))], tmp_1],
            ignore_index=True,
        )

        # get entrez ids and merge them into the complete df
        # drop duplicate ENSEMBL IDs, keep first ENTREZ Gene ID
        entrez = (
            ensembl[0]
            .filter(items=["ENSEMBL", "ENTREZID"])
            .drop_duplicates(subset=["ENSEMBL"], keep="first", ignore_index=True)
        )

        complete = complete.merge(entrez, left_on="ENSEMBL", right_on="ENSEMBL", how="left")
        return complete

    ensembl = read_ensembl()
    return post_processing(ensembl=ensembl)


def _reformat_ensembl_term_file(df: pd.DataFrame, file_name: str):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    names = [
        "Mus_musculus.GRCm39.109.entrez",
        "Mus_musculus.GRCm39.109.ena",
        "Mus_musculus.GRCm39.109.refseq",
        "Mus_musculus.GRCm39.109.uniprot",
    ]
    functions = [_reformat_entrez, _reformat_ena, _reformat_refseq, _reformat_uniprot]
    index = names.index(file_name)

    return functions[index](df=df), index


def _reformat_ena(df: pd.DataFrame):
    # TODO
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "10090." + df["Protein"]
    df = df.replace("10090.-", np.nan)
    return df


def _reformat_entrez(df: pd.DataFrame):
    # TODO
    df = df.filter(items=["gene_stable_id", "protein_stable_id", "xref"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein", "xref": "ENTREZID"})
    df["Protein"] = "10090." + df["Protein"]
    df = df.replace("10090.-", np.nan)
    return df


def _reformat_refseq(df: pd.DataFrame):
    # TODO
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "10090." + df["Protein"]
    df = df.replace("10090.-", np.nan)
    return df


def _reformat_uniprot(df: pd.DataFrame):
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "10090." + df["Protein"]
    df = df.replace("10090.-", np.nan)
    return df
