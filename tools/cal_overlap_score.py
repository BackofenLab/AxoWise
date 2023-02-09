#!/usr/bin/env python

"""
A script to calculate the score of pairwise protein overlap between
functional terms
"""

__author__ = "Dilmurat Yusuf"

import itertools
import pandas as pd
import numpy as np
import multiprocessing
import gzip
import time

def cal_overlap_score(id1, id2, set1, set2, size1, size2):
    """
    calculate the overlap between two lists measured by
    the fraction of smaller list that corresponds to
    the size of overlap
    """

    # calculate the size of intersection
    intersection_size = len(set1 & set2)

    # the sizes are pre-calculated
    # so when performing pairwise comparison of a long list
    # len() won't be repeated over the same list
    min_set = min(size1, size2)

    return id1, id2, intersection_size / min_set

def cal_overlap_score_worker(args):
    """
    for multiprocessing
    """

    i, j = args
    score = cal_overlap_score(df.loc[i].external_id,
                              df.loc[j].external_id,
                              df.loc[i].proteins,
                              df.loc[j].proteins,
                              df.loc[i].sizes,
                              df.loc[j].sizes)

    # an abitratry threshold, assuming > 50% should indicate
    # a strong relation
    if score[2] < 0.5:
        return None
    else:
        return f"{score[0]},{score[1]},{score[2]}\n"

start_time = time.time()

target_file = '../data/MusMusculusDATA/TermsWithProteins.csv.gz'
df = pd.read_csv(target_file, compression='gzip')
df['proteins'] = df['proteins'].apply(eval).apply(set)
df = df[['external_id', 'proteins']]
#t df = df.head(200)
#t df = pd.DataFrame({'proteins': [{1, 2 , 'c'}, {1, 2, 3, 'd'}, {1, 2, 3, 'a', 'b'}, {'bla'}], 'external_id': ['a','b','c', 'd']})

# calculate the sizes of each element
# this will be used later when calcualted overlap score
df["sizes"] = [len(ele) for ele in df['proteins']]

score_file = "../data/MusMusculusDATA/functional_terms_overlap.csv.gz"
start_time = time.time()
with gzip.open(score_file, "wb") as f:
    pool = multiprocessing.Pool()
    results = pool.map(cal_overlap_score_worker, itertools.combinations(range(len(df)), 2))
    results = [ele for ele in results if ele != None]
    f.write("".join(results).encode())
print(f'completed overlap calculation and saved in {score_file}')

time_cost = (time.time() - start_time)/3600
time_file = "../data/MusMusculusDATA/functional_terms_overlap_time_cost.txt"
with open(time_file, "w") as f:
    f.write(f'time cost: {time_cost} hours\n')
print(f'time cost at {time_file}')
