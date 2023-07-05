import pandas as pd
from utils import start_driver, stop_driver
from query.query_functions import (
    get_tg_ensembl_by_symbol,
    get_or_by_da_under_contexts,
    get_or_by_distance_to_tg,
    get_or_by_motif_to_tf,
    get_tg_by_correlation_tf,
    get_tg_by_de_under_contexts,
    get_tg_by_link_ft,
)


def run_queries():
    driver = start_driver()

    test_genes = list(pd.read_csv("../source/query_testing/genes.csv")["SYMBOL"])

    # Queries
    gene_subset = get_tg_ensembl_by_symbol(gene_list=test_genes, driver=driver)
    or_subset = [i[0] for i in get_or_by_distance_to_tg(subset=gene_subset, driver=driver)]
    get_or_by_da_under_contexts(
        contexts=["12h-0h", "24h-0h"], subset=or_subset, positive=True, threshold=0.5, driver=driver
    )
    get_or_by_motif_to_tf(tf="ENSMUSG00000052684", subset=or_subset, driver=driver)
    get_tg_by_correlation_tf(tf="ENSMUSG00000052684", subset=gene_subset, positive=True, threshold=0.5, driver=driver)
    get_tg_by_de_under_contexts(
        contexts=["6h-0h", "24h-0h"], subset=gene_subset, positive=True, threshold=0.5, driver=driver
    )
    get_tg_by_link_ft(ft="GO:0070851", subset=gene_subset, driver=driver)

    stop_driver(driver=driver)
