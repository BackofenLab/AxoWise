import pandas as pd
from utils import start_driver, stop_driver
from query.query_functions import query_1, query_2, query_3, query_4, query_5, query_6, query_7, query_8, query_9
import random


def run_queries():
    """
    Runs queries from query/query_functions.py. Uses start_driver(), stop_driver().
    """
    driver = start_driver()

    proteins = list(pd.read_csv("../source/processed/proteins_annotated_mouse.csv")["ENSEMBL"])
    open_regions = list(pd.read_csv("../source/processed/or_extended.csv")["id"])
    target_genes = list(pd.read_csv("../source/processed/tg.csv")["ENSEMBL"])
    transcription_factor = list(pd.read_csv("../source/processed/tf.csv")["ENSEMBL"])
    sources = list(pd.read_csv("../source/processed/sources.csv")["id"])
    celltypes = list(pd.read_csv("../source/processed/celltypes.csv")["name"])

    # Queries
    # for i in range(1, len(transcription_factor) + 100, 100):
    #     random.shuffle(transcription_factor)
    #     index = i if i < len(transcription_factor) else len(transcription_factor)
    #     tmp = transcription_factor[:index]

    #     query_1(i=index, list=tmp, threshold=0.5, driver=driver)
    #     query_2(i=index, list=tmp, threshold=0.5, driver=driver)

    # for i in range(1, len(open_regions) + 1000, 1000):
    #     random.shuffle(open_regions)
    #     index = i if i < len(open_regions) else len(open_regions)
    #     tmp = open_regions[:index]

    #     query_3(i=index, list=tmp, threshold=0.5, driver=driver)

    # for i in range(1, len(sources) + 10, 10):
    #     random.shuffle(sources)
    #     index = i if i < len(sources) else len(sources)
    #     tmp = sources[:index]

    #     query_4(i=index, list=tmp, driver=driver)
    #     query_5(i=index, list=tmp, driver=driver)

    # for i in range(1, len(celltypes) + 1):
    #     index = i if i < len(celltypes) else len(celltypes)
    #     tmp = celltypes[index]

    #     query_6(i=celltypes[index], list=tmp, driver=driver)

    # for i in range(1, len(target_genes) + 100, 100):
    #     random.shuffle(target_genes)
    #     index = i if i < len(target_genes) else len(target_genes)
    #     tmp = target_genes[:index]
    #     print(index)

    #     query_7(i=index, list=tmp, threshold=0.5, driver=driver)
    #     query_8(i=index, list=tmp, threshold=0.5, driver=driver)

    for i in range(1, len(proteins) + 100, 100):
        random.shuffle(proteins)
        index = i if i < len(proteins) else len(proteins)
        tmp = proteins[:index]
        query_9(i=index, list=tmp, threshold=600, driver=driver)

    stop_driver(driver=driver)
