import reader as rd
from uploader import first_setup, catlas_extention
from utils import print_update
from querier import run_queries
import os
import pandas as pd

os.environ["_DEFAULT_EXPERIMENT_PATH"] = "../source/experiment"
os.environ["_DEFAULT_STRING_PATH"] = "../source/string"
os.environ["_DEFAULT_FUNCTIONAL_PATH"] = "../source/functional"
os.environ["_DEFAULT_ENSEMBL_PATH"] = "../source/ensembl"
os.environ["_DEFAULT_CREDENTIALS_PATH"] = "../../config.yml"
os.environ["_DEV_MAX_REL"] = str(10000)
os.environ["_NEO4J_IMPORT_PATH"] = "/usr/local/bin/neo4j/import/"
os.environ["_FUNCTION_TIME_PATH"] = "../source/misc/function_times.tsv"

os.environ["_TIME_FUNCTIONS"] = str(False)
os.environ["_SILENT"] = str(False)
os.environ["_PRODUCTION"] = str(True)
os.environ["_UPDATE_NEO4J"] = str(False)


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


def read_catlas_files():
    data = rd.read(mode=4)
    return data


def upload_workflow():
    (
        tg_mean_count,
        tf_mean_count,
        de_values,
        or_nodes,
        or_mean_count,
        da_values,
        tf_tg_corr,
        or_tg_corr,
        motif,
        distance,
    ) = read_experiment_files()

    (complete, tf) = read_ensembl_files()

    (gene_gene_scores, genes_annotated) = read_string_files(complete=complete)

    (
        ft_nodes,
        ft_gene,
        ft_ft_overlap,
    ) = read_functional_files(complete=complete)

    # TODO: Distance (correct, not dummy), MOTIF
    (or_extended, catlas_or_context, catlas_correlation, catlas_celltype, distance_extended) = read_catlas_files()

    print_update(update_type="Done", text="Reading files", color="pink")

    # first_setup(
    #     gene_nodes=genes_annotated,
    #     tg_mean_count=tg_mean_count,
    #     tf_mean_count=tf_mean_count,
    #     or_nodes=or_extended,
    #     or_context_values=da_values,
    #     tg_context_values=de_values,
    #     tf_tg_corr=tf_tg_corr,
    #     or_tg_corr=or_tg_corr,
    #     motif=motif,
    #     distance=distance_extended,
    #     ft_nodes=ft_nodes,
    #     ft_gene=ft_gene,
    #     ft_ft_overlap=ft_ft_overlap,
    #     gene_gene_scores=gene_gene_scores,
    #     or_mean_count=or_mean_count,
    #     tf=tf,
    # )

    # catlas_extention(
    #     catlas_or_context=catlas_or_context, catlas_correlation=catlas_correlation, catlas_celltype=catlas_celltype
    # )


if __name__ == "__main__":
    upload_workflow()
    # run_queries()
