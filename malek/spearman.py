from numpy import histogram
from IPython.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
import pandas as pd
import sys
import csv
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

csv.field_size_limit(sys.maxsize)

# initialize the two dataframes to compare
df_opt = pd.read_csv("multi_10k.csv")
df_in = pd.read_csv("10k_old.csv")
'''
# filter for relevant categories in STRING
df_STRING = df_STRING.loc[(df_STRING['#category'] == 'Reactome') |
        (df_STRING['#category'] == 'GO Process') |
        (df_STRING['#category'] == 'GO Function') |
        (df_STRING['#category'] == 'GO Component') |
        (df_STRING['#category'] == 'WikiPathways') |
        (df_STRING['#category'] == 'KEGG')]'''

# id comparison
B = df_opt['id']
A = df_in['id']

# merge into one df
df_str_in = pd.merge(df_opt, df_in, left_on=['id'], right_on = ['id'], how='inner')


A = df_str_in['fdr_rate_x'].tolist()

B = df_str_in['fdr_rate_y'].tolist()

df = pd.DataFrame({'Old Enrichment': A,
                   'Multiprocess Enrichment': B})

corr = df.corr(method = 'spearman')

sns.heatmap(corr, annot = True)

plt.show()
