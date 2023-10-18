from utils import print_update
import pandas as pd
import os
import numpy as np


def parse_ensembl(dir_path: str = os.getenv("_DEFAULT_ENSEMBL_PATH")):
    """
    Parses ENSEMBL files and reformats them to fit the structure needed for uploading.

    Source directory
    Can be set with _DEFAULT_ENSEMBL_PATH

    Needed Files:
    - Mus_musculus.GRCm39.109.entrez.tsv
    - Mus_musculus.GRCm39.109.ena.tsv
    - Mus_musculus.GRCm39.109.refseq.tsv
    - Mus_musculus.GRCm39.109.uniprot.tsv
    - TFCheckpoint_download_180515.tsv
    - lost_correlations_symbols
    - Homo_sapiens.GRCh38.110.entrez.tsv
    - Homo_sapiens.GRCh38.110.ena.tsv
    - Homo_sapiens.GRCh38.110.refseq.tsv
    - Homo_sapiens.GRCh38.110.uniprot.tsv

    Return
    - complete_mouse (pandas Dataframe): Set of Genes for Mouse from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
    - tf_mouse (pandas Dataframe): List of Transcription factors for Mouse of form (ENSEMBL)
    - proteins_mouse (pandas Dataframe): Set of Proteins for Mouse from ENSEMBL of form (Protein)
    - gene_protein_link_mouse (pandas Dataframe): Links between genes and proteins for Mouse of form (ENSEMBL, Protein)
    - complete_human (pandas Dataframe): Set of Genes for Human from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
    - tf_human (pandas Dataframe): List of Transcription factors for Human of form (ENSEMBL)
    - proteins_human (pandas Dataframe): Set of Proteins for Human from ENSEMBL of form (Protein)
    - gene_protein_link_human (pandas Dataframe): Links between genes and proteins for Human of form (ENSEMBL, Protein)
    """

    def read_ensembl():
        dataframes = [None] * 10

        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".tsv":
                df, index = _reformat_ensembl_term_file(
                    df=pd.read_csv(file, sep="\t"), file_name=file_name.split("/")[-1]
                )
            dataframes[index] = df
        return dataframes

    def post_processing(ensembl: list[pd.DataFrame], species: bool):
        """
        Mouse -> species = True,
        Human -> species = False,
        """
        if species:
            ensembl = ensembl[:6]
            ensembl[4] = ensembl[4].drop(columns=["ENTREZID_human"]).rename(columns={"ENTREZID_mouse": "ENTREZID"})
        else:
            ensembl = ensembl[6:] + ensembl[4:6]
            ensembl[4] = ensembl[4].drop(columns=["ENTREZID_mouse"]).rename(columns={"ENTREZID_human": "ENTREZID"})

        print_update(
            update_type="Post processing",
            text="ENSEMBL files ({})".format("Mouse" if species else "Human"),
            color="red",
        )
        complete = pd.concat(ensembl[:4])
        complete = complete.drop(columns=["ENTREZID"])
        complete = complete.drop_duplicates(ignore_index=True)

        tmp_1 = complete[~complete["Protein"].isna()]
        tmp_2 = complete[complete["Protein"].isna()]

        proteins = complete[~complete["Protein"].isna()].drop_duplicates()["Protein"]
        gene_protein_link = complete[~complete["Protein"].isna() & ~complete["ENSEMBL"].isna()].drop_duplicates()
        gene_protein_link["Protein"] = (
            gene_protein_link["Protein"].apply(lambda x: x.removeprefix("10090."))
            if species
            else gene_protein_link["Protein"].apply(lambda x: x.removeprefix("9606."))
        )

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

        entrez["ENTREZID"] = entrez["ENTREZID"].astype(int)
        tf = (
            ensembl[4][ensembl[4]["ENTREZID"] != 0]
            .astype(int)
            .drop_duplicates(subset=["ENTREZID"], keep="first", ignore_index=True)
        )
        tf = tf.merge(entrez, left_on="ENTREZID", right_on="ENTREZID", how="left")
        tf = tf.drop(columns=["ENTREZID"])
        tf = tf.drop_duplicates(subset=["ENSEMBL"], keep="first", ignore_index=True)

        return (
            complete.drop_duplicates(),
            tf.drop_duplicates(),
            proteins.drop_duplicates(),
            gene_protein_link.drop_duplicates(),
        )

    ensembl = read_ensembl()
    result = post_processing(ensembl=ensembl, species=True) + post_processing(ensembl=ensembl, species=False)
    return result


def _reformat_ensembl_term_file(df: pd.DataFrame, file_name: str):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    names = [
        "Mus_musculus.GRCm39.109.entrez",
        "Mus_musculus.GRCm39.109.ena",
        "Mus_musculus.GRCm39.109.refseq",
        "Mus_musculus.GRCm39.109.uniprot",
        "TFCheckpoint_download_180515",
        "lost_correlations_symbols",
        "Homo_sapiens.GRCh38.110.entrez",
        "Homo_sapiens.GRCh38.110.ena",
        "Homo_sapiens.GRCh38.110.refseq",
        "Homo_sapiens.GRCh38.110.uniprot",
    ]
    functions = [
        _reformat_entrez,
        _reformat_ena,
        _reformat_refseq,
        _reformat_uniprot,
        _reformat_tf,
        _reformat_lost_symbols,
        _reformat_entrez_human,
        _reformat_ena_human,
        _reformat_refseq_human,
        _reformat_uniprot_human,
    ]
    index = names.index(file_name)

    return functions[index](df=df), index


def _reformat_ena(df: pd.DataFrame):
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "10090." + df["Protein"]
    df = df.replace("10090.-", np.nan)
    return df


def _reformat_ena_human(df: pd.DataFrame):
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "9606." + df["Protein"]
    df = df.replace("9606.-", np.nan)
    return df


def _reformat_entrez(df: pd.DataFrame):
    df = df.filter(items=["gene_stable_id", "protein_stable_id", "xref"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein", "xref": "ENTREZID"})
    df["Protein"] = "10090." + df["Protein"]
    df = df.replace("10090.-", np.nan)
    return df


def _reformat_entrez_human(df: pd.DataFrame):
    df = df.filter(items=["gene_stable_id", "protein_stable_id", "xref"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein", "xref": "ENTREZID"})
    df["Protein"] = "9606." + df["Protein"]
    df = df.replace("9606.-", np.nan)
    return df


def _reformat_refseq(df: pd.DataFrame):
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "10090." + df["Protein"]
    df = df.replace("10090.-", np.nan)
    return df


def _reformat_refseq_human(df: pd.DataFrame):
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "9606." + df["Protein"]
    df = df.replace("9606.-", np.nan)
    return df


def _reformat_uniprot(df: pd.DataFrame):
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "10090." + df["Protein"]
    df = df.replace("10090.-", np.nan)
    return df


def _reformat_uniprot_human(df: pd.DataFrame):
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "9606." + df["Protein"]
    df = df.replace("9606.-", np.nan)
    return df


def _reformat_tf(df: pd.DataFrame):
    df = df.filter(items=["entrez_mouse", "entrez_human"])
    df = df.rename(columns={"entrez_mouse": "ENTREZID_mouse", "entrez_human": "ENTREZID_human"})
    return df


def _reformat_lost_symbols(df: pd.DataFrame):
    return df
