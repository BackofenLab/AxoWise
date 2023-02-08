#!/usr/bin/env python

"""
A script to calculate the pairwise overlap score of elemets in a specific
column of a DataFrame.
"""

__author__ = "Dilmurat Yusuf"

import itertools
import pandas as pd
import numpy as np
import time

start_time = time.time()

target_file = '../data/MusMusculusDATA/TermsWithProteins.csv.gz'
#t df = pd.DataFrame({'proteins': [[1, 2 , 'c'], [1, 2, 3, 4], [1, 0, 'a', 4, 5]], 'external_id': ['a','b','c']})
df = pd.read_csv(target_file, compression='gzip')
df['proteins'] = df['proteins'].apply(eval)
df = df[['external_id', 'proteins']]

#--- get the smaller set in a pairwise comparison
# calculate the sizes of each element
sizes = df['proteins'].apply(len).values
# list of pairwise comparison
paired_comp = [','.join(sorted((df['external_id'][tags[0]], df['external_id'][tags[1]]))) for tags in itertools.combinations(range(len(sizes)), 2)]
# pick the one with minimum size in a pairwise comparison
paired_min = [min(eles) for eles in itertools.combinations(sizes, 2)]
list_of_tuples = list(zip(paired_comp, paired_min))
df_min = pd.DataFrame(list_of_tuples, columns=['pair', 'min_len'])
del paired_comp, paired_min, list_of_tuples
#---

#--- get the size of intersection
# Convert to set
a = df['proteins'].apply(set).values
# Broadcast set intersection
new_df = pd.DataFrame(a[:, None] & a)
new_df.index = df['external_id'].values
new_df.columns = df['external_id'].values


# Extract the upper triangular elements
mask = np.triu(np.ones_like(new_df), k=1).astype(bool)
upper_triangular = new_df.where(mask)
del new_df
# Convert the extracted elements to long form
upper_triangular = upper_triangular.unstack().reset_index()
upper_triangular.columns = ["row", "col", "value"]
upper_triangular = upper_triangular[~upper_triangular["value"].isnull()]
upper_triangular['inters_len'] = upper_triangular['value'].apply(len)
upper_triangular['pair'] = [','.join(sorted(eles)) for eles in zip(upper_triangular.row, upper_triangular.col)]
#---

#---
# merge the two data sets
df_min_inters = pd.merge(df_min, upper_triangular[['pair', 'inters_len']],
                           on = "pair",
                           how = "outer")
del df_min, upper_triangular
df_min_inters["overlap_score"] = df_min_inters["inters_len"]/df_min_inters["min_len"]
df_min_inters = df_min_inters[['pair', 'overlap_score']]
df_min_inters.set_index(['pair']).apply(pd.Series.explode).reset_index()

# Split the values in the 'pair' column
df_exploded = df_min_inters['pair'].str.split(',', expand=True)

# Add a new column for each split result
df_exploded['ID_1st'] = df_exploded[0]
df_exploded['ID_2nd'] = df_exploded[1]

# Drop the original 'pair' column and the intermediate split result
df_min_inters = df_min_inters.drop('pair', axis=1)
df_exploded = df_exploded.drop([0, 1], axis=1)

# Join the exploded DataFrame with the original DataFrame
df_min_inters = df_exploded.join(df_min_inters)

df_min_inters.to_csv('../data/MusMusculusDATA/functional_terms_overlap.csv', index=False)
print('completed')
#---
# !less ../data/MusMusculusDATA/functional_terms_overlap.csv
print("--- %s seconds ---" % (time.time() - start_time))
