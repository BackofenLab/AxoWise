import pandas as pd
from utils import time_function, stop_driver, start_driver
from upload.upload_base import setup_base_db
from upload.upload_experiment import extend_db_from_experiment
from upload.upload_catlas import extend_db_from_catlas


@time_function
def base_setup(
    species: str,
    gene_nodes: pd.DataFrame,
    ft_nodes: pd.DataFrame,
    ft_ft_overlap: pd.DataFrame,
    ft_gene: pd.DataFrame,
    tf: pd.DataFrame,
    ft_protein: pd.DataFrame,
    gene_protein_link: pd.DataFrame,
    proteins_annotated: pd.DataFrame,
    protein_protein_scores: pd.DataFrame,
    or_nodes: pd.DataFrame | None = None,
    distance: pd.DataFrame | None = None,
):
    driver = start_driver()

    setup_base_db(
        ft_nodes=ft_nodes,
        ft_ft_overlap=ft_ft_overlap,
        ft_gene=ft_gene,
        ft_protein=ft_protein,
        gene_nodes=gene_nodes,
        or_nodes=or_nodes,
        distance=distance,
        tf=tf,
        gene_protein_link=gene_protein_link,
        proteins=proteins_annotated,
        protein_protein_scores=protein_protein_scores,
        species=species,
        driver=driver,
    )

    stop_driver(driver=driver)


@time_function
def bulk_extention(
    species: str,
    tg_mean_count: pd.DataFrame,
    tf_mean_count: pd.DataFrame,
    or_mean_count: pd.DataFrame,
    tg_context_values: pd.DataFrame,
    or_context_values: pd.DataFrame,
    tf_tg_corr: pd.DataFrame,
    or_tg_corr: pd.DataFrame,
    motif: pd.DataFrame,
):
    driver = start_driver()

    extend_db_from_experiment(
        tg_mean_count=tg_mean_count,
        tf_mean_count=tf_mean_count,
        or_mean_count=or_mean_count,
        tg_context_values=tg_context_values,
        or_context_values=or_context_values,
        tf_tg_corr=tf_tg_corr,
        or_tg_corr=or_tg_corr,
        motif=motif,
        species=species,
        driver=driver,
    )

    stop_driver(driver=driver)


@time_function
def catlas_extention(
    species: str,
    catlas_or_context: pd.DataFrame,
    catlas_correlation: pd.DataFrame,
    catlas_celltype: pd.DataFrame,
    catlas_motifs: pd.DataFrame,
):
    driver = start_driver()

    extend_db_from_catlas(
        catlas_or_context=catlas_or_context,
        catlas_correlation=catlas_correlation,
        catlas_celltype=catlas_celltype,
        catlas_motifs=catlas_motifs,
        species=species,
        driver=driver,
    )

    stop_driver(driver=driver)
