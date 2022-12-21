import pandas as pd
import sys
# import os
"""
This is a 'script' to prepare a given data set into smaller datasets of nodes
and relationships.
Keep in mind this is using parameters of the given data. So it wont work if u 
dont feed it the right data.

it takes 2 csvs via sys.args as input files. Call it like this:

python3 script.py exp_DE.csv exp_DA.csv

author: Tillman Heisner <theisner2@gmail.com>
"""

def open_region(data):
    # read the data into panda frame
    df = pd.read_csv(data)
    # Remove all columns between column name "open_region_wt12h_wt0h" to
    # "open_region_wtRC12h_wt12h_padj"
    df = df.drop(df.loc[:, "open_region_wt12h_wt0h":
                        "open_region_wtRC12h_wt12h_padj"].columns, axis=1)
    df.to_csv('./OpenRegion.csv', index=False)


def protein(data):
    # read the data into panda frame
    df = pd.read_csv(data)
    # Remove all columns between column name  "wt6h_wt0h" to
    # "wtRC12h_wt6h_padj"
    df = df.drop(df.loc[:, "wt6h_wt0h":"wtRC12h_wt6h_padj"].columns, axis=1)
    df.to_csv('./Protein.csv', index=False)


def transcription_factor(data):
    # read the data into panda frame
    df = pd.read_csv(data)
    # Remove all columns between column name  "wt6h_wt0h" to
    # "wtRC12h_wt6h_padj"
    df = df.drop(df.loc[:, "wt6h_wt0h":"wtRC12h_wt6h_padj"].columns, axis=1)
    # filter for proteins, where protein is transcription factor
    df = df[df['TF'] != "no"]
    df.to_csv('./TranscriptionFactor.csv', index=False)


def rel_same_entity(data):
    # read the data into panda frame
    df = pd.read_csv(data)
    # filter for proteins, where protein is transcription factor
    df = df[df['TF'] != "no"]
    # only safe column symbol
    df = df[['SYMBOL']]
    df.to_csv('./rel_same_entity.csv', index=False)


def rel_nearest_distance(data):
    # read the data into panda frame
    df = pd.read_csv(data)
    # only safe column nearest_index and nearest_SYMBOL
    df = df[['nearest_index', 'nearest_SYMBOL']]
    df.to_csv('./rel_nearest_distance.csv', index=False)


def rel_de(data):
    # read the data into panda frame
    df = pd.read_csv(data)
    # only safe column SYMBOL and the corresponding DE time
    df1 = df[['SYMBOL', 'wt6h_wt0h']]
    df1 = df1.assign(Study='1', Celltype='Microglia')
    df1.to_csv('./rel_protein_wt6h_wt0h.csv', index=False)
    # only safe column SYMBOL and the corresponding DE time
    df2 = df[['SYMBOL', 'wt24h_wt0h']]
    df2 = df2.assign(Study='1', Celltype='Microglia')
    df2.to_csv('./rel_protein_wt24h_wt0h.csv', index=False)
    # only safe column SYMBOL and the corresponding DE time
    df3 = df[['SYMBOL', 'wt336h_wt0h']]
    df3 = df3.assign(Study='1', Celltype='Microglia')
    df3.to_csv('./rel_protein_wt336h_wt0h', index=False)
    # only safe column SYMBOL and the corresponding DE time
    df4 = df[['SYMBOL', 'wtRC12h_wt0h']]
    df4 = df4.assign(Study='1', Celltype='Microglia')
    df4.to_csv('./rel_protein_wtRC12h_wt0h.csv', index=False)
    # only safe column SYMBOL and the corresponding DE time
    df5 = df[['SYMBOL', 'wtRC12h_wt6h']]
    df5 = df5.assign(Study='1', Celltype='Microglia')
    df5.to_csv('./rel_protein_wtRC12h_wt6h.csv', index=False)
    # only safe column SYMBOL and the corresponding DE time
    df6 = df[['SYMBOL', 'wt6h_wt0h_padj']]
    df6 = df6.assign(Study='1', Celltype='Microglia')
    df6.to_csv('./rel_protein_wt6h_wt0h_padj.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df7 = df[['SYMBOL', 'wt24h_wt0h_padj']]
    df7 = df7.assign(Study='1', Celltype='Microglia')
    df7.to_csv('./rel_protein_wt24h_wt0h_padj.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df8 = df[['SYMBOL', 'wt336h_wt0h_padj']]
    df8 = df8.assign(Study='1', Celltype='Microglia')
    df8.to_csv('./rel_protein_wtRC336h_wt0h_padj.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df9 = df[['SYMBOL', 'wtRC12h_wt0h_padj']]
    df9 = df9.assign(Study='1', Celltype='Microglia')
    df9.to_csv('./rel_protein_wtRC12h_wt0h_padj.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df10 = df[['SYMBOL', 'wtRC12h_wt6h_padj']]
    df10 = df10.assign(Study='1', Celltype='Microglia')
    df10.to_csv('./rel_protein_wtRC12h_wt6h_padj.csv', index=False)


def rel_da(data):
    # read the data into panda frame
    df = pd.read_csv(data)
    # only safe column SYMBOL and the corresponding DA time
    df1 = df[['nearest_index', 'open_region_wt12h_wt0h']]
    df1 = df1.assign(Study='1', Celltype='Microglia')
    df1.to_csv('./rel_or_wt12h_wt0h.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df2 = df[['nearest_index', 'open_region_wt24h_wt0h']]
    df2 = df2.assign(Study='1', Celltype='Microglia')
    df2.to_csv('./rel_or_wt24h_wt0h.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df3 = df[['nearest_index', 'open_region_wt336h_wt0h']]
    df3 = df3.assign(Study='1', Celltype='Microglia')
    df3.to_csv('./rel_or_wt336h_wt0h', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df4 = df[['nearest_index', 'open_region_wtRC12h_wt0h']]
    df4 = df4.assign(Study='1', Celltype='Microglia')
    df4.to_csv('./rel_or_wtRC12h_wt0h.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df5 = df[['nearest_index', 'open_region_wtRC12h_wt12h']]
    df5 = df5.assign(Study='1', Celltype='Microglia')
    df5.to_csv('./rel_or_wtRC12h_wt12h.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df6 = df[['nearest_index', 'open_region_wt12h_wt0h_padj']]
    df6 = df6.assign(Study='1', Celltype='Microglia')
    df6.to_csv('./rel_or_wt12h_wt0h_padj.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df7 = df[['nearest_index', 'open_region_wt24h_wt0h_padj']]
    df7 = df7.assign(Study='1', Celltype='Microglia')
    df7.to_csv('./rel_or_wt24h_wt0h_padj.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df8 = df[['nearest_index', 'open_region_wt336h_wt0h_padj']]
    df8 = df8.assign(Study='1', Celltype='Microglia')
    df8.to_csv('./rel_or_wtRC336h_wt0h_padj.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df9 = df[['nearest_index', 'open_region_wtRC12h_wt0h_padj']]
    df9 = df9.assign(Study='1', Celltype='Microglia')
    df9.to_csv('./rel_or_wtRC12h_wt0h_padj.csv', index=False)
    # only safe column SYMBOL and the corresponding DA time
    df10 = df[['nearest_index', 'open_region_wtRC12h_wt12h_padj']]
    df10 = df10.assign(Study='1', Celltype='Microglia')
    df10.to_csv('./rel_or_wtRC12h_wt12h_padj.csv', index=False)


if __name__ == "__main__":
    exp_DE = sys.argv[1]
    exp_DA = sys.argv[2]
    protein(exp_DE)
    transcription_factor(exp_DE)
    rel_same_entity(exp_DE)
    rel_de(exp_DE)
    rel_nearest_distance(exp_DA)
    open_region(exp_DA)
    rel_da(exp_DA)
