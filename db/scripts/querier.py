import pandas as pd
from utils import start_driver, stop_driver
from query.query_functions import (
    query_1,
    query_2,
    query_3, 
    query_4, 
    query_5, 
    query_6,
    query_7, 
    query_8
)


def run_queries():
    driver = start_driver()

    open_regions = list(pd.read_csv("../source/processed/or_extended.csv")["id"])
    target_genes = list(pd.read_csv("../source/processed/tg.csv")["ENSEMBL"])
    transcription_factor = list(pd.read_csv("../source/processed/tf.csv")["ENSEMBL"])
    sources = list(pd.read_csv("../source/processed/sources.csv")["id"])
    celltypes = list(pd.read_csv("../source/processed/celltypes.csv")["name"])
    
    # Queries
    for i in range(1, len(transcription_factor), 100):
        tmp = transcription_factor[:i]
        query_1(i=i, list=tmp, threshold=0.5, driver=driver)
        query_2(i=i, list=tmp, threshold=0.5, driver=driver)

    for i in range(1, len(open_regions), 1000):
        tmp = open_regions[:i]
        query_3(i=i, list=open_regions, threshold=0.5, driver=driver)

    for i in range(1, len(sources)):
        tmp = sources[:i]
        query_4(i=i, list=sources, driver=driver)
        query_5(i=i, list=sources, driver=driver)

    for i in range(1, len(celltypes)):
        tmp = celltypes[:i]
        query_6(i=i, list=celltypes, driver=driver)

    for i in range(1, len(target_genes), 100):
        tmp = target_genes[:i]
        query_7(i=i, list=target_genes, threshold=0.5, driver=driver)
        query_8(i=i, list=target_genes, threshold=0.5, driver=driver)

    stop_driver(driver=driver)
