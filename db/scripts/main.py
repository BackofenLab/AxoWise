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

os.environ["_TIME_FUNCTIONS"] = str(False)
os.environ["_SILENT"] = str(False)
os.environ["_PRODUCTION"] = str(False)


def read_experiment_files():
    data = rd.read(reformat=True, mode=0)
    return data


def read_string_files(complete: pd.DataFrame):
    data = rd.read(complete=complete, mode=1)
    return data


def read_ensembl_files():
    data = rd.read(mode=2)
    return data


def read_functional_files(complete: pd.DataFrame):
    data = rd.read(complete=complete, mode=3)
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

    print(len(de_values))
    print(len(da_values))
    print(len(tf_tg_corr))
    print(len(or_tg_corr))

    complete = read_ensembl_files()

    print(len(complete))

    (gene_gene_scores, genes_annotated) = read_string_files(complete=complete)
    print(len(gene_gene_scores))
    print(len(genes_annotated))

    (
        ft_nodes,
        ft_gene,
        ft_ft_overlap,
    ) = read_functional_files(complete=complete)

    print(len(ft_nodes))
    print(len(ft_gene))
    print(len(ft_ft_overlap))

    tg_nodes = get_consistent_entries(comparing_genes=tg_nodes, complete=complete, mode=1)
    tf_nodes = get_consistent_entries(comparing_genes=tf_nodes, complete=complete, mode=1)

    # TODO Filter DE, DA, Correlation on consistent entries

    # first_setup(
    #     gene_nodes=complete,
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
    # )
