from utils import print_update
import pandas as pd
import os
import json
from alive_progress import alive_bar


def parse_functional(dir_path: str = os.getenv("_DEFAULT_FUNCTIONAL_PATH")):
    """
    Parses Functional term files and reformats them to fit the structure needed for uploading.

    Source directory
    - Can be set with _DEFAULT_FUNCTIONAL_PATH

    Needed Files:
    - functional_terms_overlap_mus_musculus.csv
    - AllPathways_mouse.csv
    - functional_terms_overlap_homo_sapiens.csv
    - AllPathways_human.csv

    Return
    - ft_nodes_mouse (pandas DataFrame): Functional Term nodes for Mouse of form (Term, Name, Category, Proteins)
    - ft_gene_mouse (pandas DataFrame): Links between Functional Terms and Target Genes for Mouse of form (ENSEMBL, Term)
    - ft_protein_mouse (pandas DataFrame): Links between Functional Terms and Proteins for Mouse of form (ENSEMBL, Term)
    - ft_ft_overlap_mouse (pandas DataFrame): Overlap between Functional Terms for Mouse of form (source, target, Score)
    - ft_nodes_human (pandas DataFrame): Functional Term nodes for Human of form (Term, Name, Category, Proteins)
    - ft_gene_human (pandas DataFrame): Links between Functional Terms and Target Genes for Human of form (ENSEMBL, Term)
    - ft_protein_human (pandas DataFrame): Links between Functional Terms and Proteins for Human of form (ENSEMBL, Term)
    - ft_ft_overlap_human (pandas DataFrame): Overlap between Functional Terms for Human of form (source, target, Score)
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

    def post_processing(functional: list[pd.DataFrame], species: bool):
        """
        Mouse -> species = True,
        Human -> species = False,
        """

        if species:
            functional = functional[:2]
        else:
            functional = functional[2:]

        print_update(update_type="Post processing", text="Functional files", color="red")
        ft_nodes = functional[1].filter(items=["id", "name", "category", "proteins"])
        ft_nodes = ft_nodes.rename(
            columns={"id": "Term", "name": "Name", "category": "Category", "proteins": "Proteins"}
        )

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

        return (
            ft_nodes.drop_duplicates(),
            ft_gene.drop_duplicates(),
            ft_protein.drop_duplicates(),
            ft_ft_overlap.drop_duplicates(),
        )

    functional = read_functional()
    result = post_processing(functional=functional, species=True) + post_processing(
        functional=functional, species=False
    )
    return result


def _reformat_functional_term_file(df: pd.DataFrame, file_name: str):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    names = [
        "functional_terms_overlap_mus_musculus",
        "AllPathways_mouse",
        "functional_terms_overlap_homo_sapiens",
        "AllPathways_human",
    ]
    functions = [_reformat_ft_overlap, _reformat_terms_mouse, _reformat_ft_overlap_human, _reformat_terms_human]
    index = names.index(file_name)

    return functions[index](df=df), index


def _reformat_ft_overlap(df: pd.DataFrame):
    df = df.rename(columns={"score": "Score"})
    return df


def _reformat_ft_overlap_human(df: pd.DataFrame):
    df = df.rename(columns={"score": "Score"})
    return df


def _reformat_terms_mouse(df: pd.DataFrame):
    return df


def _reformat_terms_human(df: pd.DataFrame):
    return df
