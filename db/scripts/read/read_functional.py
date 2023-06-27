from utils import print_update
import pandas as pd
import os
import json


def parse_functional(complete: pd.DataFrame, dir_path: str = os.getenv("_DEFAULT_FUNCTIONAL_PATH")):
    """
    Reads Functional Terms files and returns a Pandas dataframe
    [ functional_terms_overlap.csv, TermsWithProteins.csv ]
    """

    def read_functional():
        dataframes = [None] * 2

        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".csv":
                df, index = _reformat_functional_term_file(
                    df=pd.read_csv(file, sep=","), file_name=file_name.split("/")[-1]
                )
            dataframes[index] = df
        return dataframes

    def post_processing(functional: list[pd.DataFrame]):
        print_update(update_type="Post processing", text="Functional files", color="red")
        ft_nodes = functional[1].filter(items=["external_id", "name", "category"])
        ft_nodes = ft_nodes.rename(columns={"external_id": "Term", "name": "Name", "category": "Category"})

        ft_protein_df_list = []
        for _, i in functional[1].iterrows():
            tmp_df = pd.DataFrame()
            tmp_df["Protein"] = json.loads(i["proteins"].replace("'", '"'))
            tmp_df["Term"] = i["external_id"]
            ft_protein_df_list.append(tmp_df)
        ft_protein = pd.concat(ft_protein_df_list)

        ft_protein = ft_protein.merge(complete, left_on="Protein", right_on="Protein")

        ft_gene = ft_protein.filter(items=["Term", "ENSEMBL"]).drop_duplicates(ignore_index=True)

        ft_ft_overlap = functional[0]

        return ft_nodes, ft_gene, ft_ft_overlap

    functional = read_functional()
    return post_processing(functional=functional)


def _reformat_functional_term_file(df: pd.DataFrame, file_name: str):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    names = ["functional_terms_overlap", "TermsWithProteins"]
    functions = [_reformat_ft_overlap, _reformat_terms_proteins]
    index = names.index(file_name)

    return functions[index](df=df), index


def _reformat_ft_overlap(df: pd.DataFrame):
    df = df.rename(columns={"score": "Score"})
    return df


def _reformat_terms_proteins(df: pd.DataFrame):
    return df
