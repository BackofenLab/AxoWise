import reader as rd
from uploader import catlas_extention, base_setup, bulk_extention
from utils import print_update, time_function
from querier import run_queries
import os
import pandas as pd

os.environ["_DEFAULT_EXPERIMENT_PATH"] = "../source/experiment"
os.environ["_DEFAULT_STRING_PATH"] = "../source/string"
os.environ["_DEFAULT_FUNCTIONAL_PATH"] = "../source/functional"
os.environ["_DEFAULT_ENSEMBL_PATH"] = "../source/ensembl"
os.environ["_DEFAULT_CATLAS_PATH"] = "../source/catlas"
os.environ["_DEFAULT_CREDENTIALS_PATH"] = "../../config.yml"
os.environ["_DEV_MAX_REL"] = str(10000)
os.environ["_NEO4J_IMPORT_PATH"] = "/usr/local/bin/neo4j/import/"
os.environ["_FUNCTION_TIME_PATH"] = "../source/timing/function_times.tsv"

os.environ["_TIME_FUNCTIONS"] = str(False)
os.environ["_SILENT"] = str(False)
os.environ["_PRODUCTION"] = str(True)
os.environ["_ACCESS_NEO4J"] = str(True)


@time_function
def read_experiment_files(genes_annotated_mouse):
    data = rd.reading(genes_annotated_mouse=genes_annotated_mouse, mode=0)
    return data


@time_function
def read_string_files(
    complete_mouse: pd.DataFrame,
    proteins_mouse: pd.DataFrame,
    complete_human: pd.DataFrame,
    proteins_human: pd.DataFrame,
):
    data = rd.reading(
        complete_mouse=complete_mouse,
        proteins_mouse=proteins_mouse,
        complete_human=complete_human,
        proteins_human=proteins_human,
        mode=1,
    )
    return data


@time_function
def read_ensembl_files():
    data = rd.reading(mode=2)
    return data


@time_function
def read_functional_files():
    data = rd.reading(mode=3)
    return data


@time_function
def read_catlas_files(or_nodes: pd.DataFrame, distance: pd.DataFrame):
    data = rd.reading(or_nodes=or_nodes, distance=distance, mode=4)
    return data


@time_function
def upload_workflow():
    (
        complete_mouse,
        tf_mouse,
        proteins_mouse,
        gene_protein_link_mouse,
        complete_human,
        tf_human,
        proteins_human,
        gene_protein_link_human,
    ) = read_ensembl_files()

    (
        genes_annotated_mouse,
        proteins_annotated_mouse,
        protein_protein_scores_mouse,
        genes_annotated_human,
        proteins_annotated_human,
        protein_protein_scores_human,
    ) = read_string_files(
        complete_mouse=complete_mouse,
        proteins_mouse=proteins_mouse,
        complete_human=complete_human,
        proteins_human=proteins_human,
    )

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
    ) = read_experiment_files(genes_annotated_mouse=genes_annotated_mouse)

    (
        ft_nodes_mouse,
        ft_gene_mouse,
        ft_protein_mouse,
        ft_ft_overlap_mouse,
        ft_nodes_human,
        ft_gene_human,
        ft_protein_human,
        ft_ft_overlap_human,
    ) = read_functional_files()

    # TODO: Distance (correct, not dummy), MOTIF (correct, not dummy)
    (
        or_extended,
        catlas_or_context,
        catlas_correlation,
        catlas_celltype,
        distance_extended,
        catlas_motifs,
    ) = read_catlas_files(or_nodes=or_nodes, distance=distance)

    print_update(update_type="Done", text="Reading files", color="pink")

    base_setup(
        species="Homo_Sapiens",
        gene_nodes=genes_annotated_human,
        ft_nodes=ft_nodes_human,
        ft_gene=ft_gene_human,
        ft_ft_overlap=ft_ft_overlap_human,
        tf=tf_human,
        ft_protein=ft_protein_human,
        gene_protein_link=gene_protein_link_human,
        proteins_annotated=proteins_annotated_human,
        protein_protein_scores=protein_protein_scores_human,
    )

    base_setup(
        species="Mus_Musculus",
        gene_nodes=genes_annotated_mouse,
        or_nodes=or_extended,
        distance=distance_extended,
        ft_nodes=ft_nodes_mouse,
        ft_gene=ft_gene_mouse,
        ft_ft_overlap=ft_ft_overlap_mouse,
        tf=tf_mouse,
        ft_protein=ft_protein_mouse,
        gene_protein_link=gene_protein_link_mouse,
        proteins_annotated=proteins_annotated_mouse,
        protein_protein_scores=protein_protein_scores_mouse,
    )

    bulk_extention(
        species="Mus_Musculus",
        tg_mean_count=tg_mean_count,
        tf_mean_count=tf_mean_count,
        or_context_values=da_values,
        tg_context_values=de_values,
        tf_tg_corr=tf_tg_corr,
        or_tg_corr=or_tg_corr,
        motif=motif,
        or_mean_count=or_mean_count,
    )

    catlas_extention(
        species="Mus_Musculus",
        catlas_or_context=catlas_or_context,
        catlas_correlation=catlas_correlation,
        catlas_celltype=catlas_celltype,
        catlas_motifs=catlas_motifs,
    )


if __name__ == "__main__":
    # upload_workflow()
    # run_queries()
    pass
