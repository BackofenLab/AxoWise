from utils import print_update
import pandas as pd
import os
import json
from alive_progress import alive_bar


def parse_functional(dir_path: str = os.getenv("_DEFAULT_FUNCTIONAL_PATH")):
    """
    Reads Functional Terms files and returns a Pandas dataframe
    [ functional_terms_overlap_mus_musculus.csv, AllPathways_mouse.csv, AllPathways_human.csv, functional_terms_overlap_homo_sapiens.csv]
    """

    def read_functional():
        dataframes = [None] * 4

        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_name.split("/")[-1].startswith("."):
                continue
            if file_extention == ".csv":
                df, index = _reformat_functional_term_file(
                    df=pd.read_csv(file, sep=","), file_name=file_name.split("/")[-1]
                )
            dataframes[index] = df
        return dataframes

    def post_processing(functional: list[pd.DataFrame]):
        print_update(update_type="Post processing", text="Functional files", color="red")
        ft_nodes = functional[1].filter(items=["id", "name", "category"])
        ft_nodes = ft_nodes.rename(columns={"id": "Term", "name": "Name", "category": "Category"})

        ft_protein_df_list = []
        ft_gene_df_list = []

        with alive_bar(len(functional[1])) as bar:
            for _, i in functional[1].iterrows():
                tmp_df_protein = pd.DataFrame()
                tmp_df_gene = pd.DataFrame()

                tmp_df_gene["ENSEMBL"] = json.loads(i["genes"].replace("'", '"'))
                tmp_df_gene["Term"] = i["id"]

                tmp_df_protein["ENSEMBL"] = json.loads(i["proteins"].replace("'", '"'))
                tmp_df_protein["Term"] = i["id"]

                ft_protein_df_list.append(tmp_df_protein)
                ft_gene_df_list.append(tmp_df_gene)
                bar()

        ft_protein = pd.concat(ft_protein_df_list).drop_duplicates()
        ft_gene = pd.concat(ft_gene_df_list).drop_duplicates()

        ft_ft_overlap = functional[0]

        return ft_nodes, ft_gene, ft_protein, ft_ft_overlap

    functional = read_functional()
    return post_processing(functional=functional)


def _reformat_functional_term_file(df: pd.DataFrame, file_name: str):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    names = ["functional_terms_overlap_mus_musculus", "AllPathways_mouse", "AllPathways_human", "functional_terms_overlap_homo_sapiens"]
    functions = [_reformat_ft_overlap, _reformat_terms_mouse, _reformat_terms_human, _reformat_ft_overlap_human]
    index = names.index(file_name)

    return functions[index](df=df), index


def _reformat_ft_overlap(df: pd.DataFrame):
    df = df.rename(columns={"score": "Score"})
    return df


def _reformat_ft_overlap_human(df: pd.DataFrame):
    df = df.rename(columns={"score": "Score"})
    return df


def _reformat_terms_mouse(df: pd.DataFrame):
    df = df.drop(columns=["Unnamed: 0"])
    return df


def _reformat_terms_human(df: pd.DataFrame):
    df = df.drop(columns=["Unnamed: 0"])
    return df
