from utils import start_driver, stop_driver
from query.query_functions import (
    get_tg_ensembl_by_symbol,
    get_or_by_da_under_contexts,
    get_or_by_distance_to_tg,
    get_or_by_motif_to_tf,
    get_tg_by_correlation_tfs,
    get_tg_by_de_under_contexts,
    get_tg_by_link_ft,
)


def run_queries():
    driver = start_driver()

    # Queries
    get_tg_ensembl_by_symbol(gene_list=[], driver=driver)
    get_or_by_da_under_contexts(contexts=[], subset=[], positive=True, threshold=0.5, driver=driver)
    get_or_by_distance_to_tg(subset=[], driver=driver)
    get_or_by_motif_to_tf(tf="", subset=[], driver=driver)
    get_tg_by_correlation_tfs(tf="", subset=[], positive=True, threshold=0.5, driver=driver)
    get_tg_by_de_under_contexts(contexts=[], subset=[], positive=True, driver=True)
    get_tg_by_link_ft(ft="", subset=[], driver=driver)

    stop_driver(driver=driver)
