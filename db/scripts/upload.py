import pandas as pd
from utils import time_function, stop_driver, start_driver
from upload_base import setup_base_db
from upload_experiment import extend_db_from_experiment


@time_function
def first_setup(
    gene_nodes: pd.DataFrame,
    tg_mean_count: pd.DataFrame,
    tf_mean_count: pd.DataFrame,
    or_mean_count: pd.DataFrame,
    or_nodes: pd.DataFrame,
    de_values: pd.DataFrame,
    da_values: pd.DataFrame,
    tf_tg_corr: pd.DataFrame,
    or_tg_corr: pd.DataFrame,
    motif: pd.DataFrame,
    distance: pd.DataFrame,
    ft_nodes: pd.DataFrame,
    ft_ft_overlap: pd.DataFrame,
    ft_gene: pd.DataFrame,
    gene_gene_scores: pd.DataFrame,
    tf: pd.DataFrame,
):
    """
    Initial Setup with Base DB and Experiment data
    """
    driver = start_driver()

    setup_base_db(
        ft_nodes=ft_nodes,
        ft_ft_overlap=ft_ft_overlap,
        ft_gene=ft_gene,
        gene_gene_scores=gene_gene_scores,
        gene_nodes=gene_nodes,
        or_nodes=or_nodes,
        motif=motif,
        distance=distance,
        driver=driver,
        tf=tf,
    )

    extend_db_from_experiment(
        tg_mean_count=tg_mean_count,
        tf_mean_count=tf_mean_count,
        or_mean_count=or_mean_count,
        de_values=de_values,
        da_values=da_values,
        tf_tg_corr=tf_tg_corr,
        or_tg_corr=or_tg_corr,
        driver=driver,
    )

    utils.time_function(create_motif_edges, variables={"motif": motif, "driver": driver})

    utils.time_function(create_distance_edges, variables={"distance": distance, "driver": driver})

    utils.print_update(update_type="Done", text="Extending DB from Experimental Data", color="pink")
    return

