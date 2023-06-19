import read as rd
from upload import first_setup
import os
from utils import get_consistent_entries
import pandas as pd

os.environ["_DEFAULT_EXPERIMENT_PATH"] = "../source/experiment"
os.environ["_DEFAULT_STRING_PATH"] = "../source/string"
os.environ["_DEFAULT_FUNCTIONAL_PATH"] = "../source/functional"
os.environ["_DEFAULT_ENSEMBL_PATH"] = "../source/ensembl"
os.environ["_DEFAULT_CREDENTIALS_PATH"] = "../../config.yml"
os.environ["_DEV_MAX_REL"] = str(10000)
os.environ["_NEO4J_IMPORT_PATH"] = "/usr/local/bin/neo4j/import/"
os.environ["_FUNCTION_TIME_PATH"] = "./function_times.csv"

os.environ["_TIME_FUNCTIONS"] = str(True)
os.environ["_SILENT"] = str(False)
os.environ["_PRODUCTION"] = str(False)


def read_experiment_files(path=os.getenv("_DEFAULT_EXPERIMENT_PATH")):
    data = rd.parse_experiment(dir_path=path, reformat=True)
    return data


def read_string_files(temporary_protein_gene_dict, path=os.getenv("_DEFAULT_STRING_PATH")):
    data = rd.parse_string(temporary_protein_gene_dict=temporary_protein_gene_dict, dir_path=path)
    return data


def read_functional_files(protein_gene_dict: pd.DataFrame, path=os.getenv("_DEFAULT_FUNCTIONAL_PATH")):
    data = rd.parse_functional(protein_gene_dict=protein_gene_dict, dir_path=path)
    return data


def read_ensembl_files(path=os.getenv("_DEFAULT_ENSEMBL_PATH")):
    data = rd.parse_ensembl(dir_path=path)
    return data


if __name__ == "__main__":
    (
        tg_nodes,
        tf_nodes,
        de_values,
        or_nodes,
        da_values,
        tf_tg_corr,
        or_tg_corr,
        motif,
        distance,
    ) = read_experiment_files()

    (complete_genes, temporary_protein_gene_dict) = read_ensembl_files()

    (gene_gene_scores, protein_gene_dict, string_gene_nodes) = read_string_files(
        temporary_protein_gene_dict=temporary_protein_gene_dict
    )

    (
        ft_nodes,
        ft_gene,
        ft_ft_overlap,
    ) = read_functional_files(protein_gene_dict=protein_gene_dict)

    string_gene_nodes = get_consistent_entries(comparing_genes=string_gene_nodes, ensembl_genes=complete_genes, mode=0)
    tg_nodes = get_consistent_entries(comparing_genes=tg_nodes, ensembl_genes=complete_genes, mode=1)
    tf_nodes = get_consistent_entries(comparing_genes=tf_nodes, ensembl_genes=complete_genes, mode=1)

    # first_setup(
    #     tg_nodes=tg_nodes,
    #     tf_nodes=tf_nodes,
    #     or_nodes=or_nodes,
    #     da_values=da_values,
    #     de_values=de_values,
    #     tf_tg_corr=tf_tg_corr,
    #     or_tg_corr=or_tg_corr,
    #     motif=motif,
    #     distance=distance,
    #     ft_nodes=ft_nodes,
    #     ft_gene=ft_gene,
    #     ft_ft_overlap=ft_ft_overlap,
    #     gene_gene_scores=gene_gene_scores,
    #     string_gene_nodes=string_gene_nodes,
    # )
