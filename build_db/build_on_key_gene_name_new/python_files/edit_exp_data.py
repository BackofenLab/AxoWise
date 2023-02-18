"""
This takes the files exp_DE.csv and exp_DA.csv and
splits them into smaller csvs.
author: Tillman Heisner <theisner2@gmail.com>
"""

import pandas as pd
import os


def open_region(data: str, target_dir: str):
    # read the data into panda frame
    df = pd.read_csv(data, sep='\t')
    # Remove all columns between column name "open_region_wt12h_wt0h" to
    # "open_region_wtRC12h_wt12h_padj"
    df = df.drop(df.loc[:, "open_region_wt12h_wt0h":
                        "open_region_wtRC12h_wt12h_padj"].columns, axis=1)
    df.to_csv(target_dir + '/OpenRegion.csv', index=False)


def protein(data: str, target_dir: str):
    # read the data into panda frame
    df = pd.read_csv(data)
    # Remove all columns between column name  "wt6h_wt0h" to
    # "wtRC12h_wt6h_padj"
    df = df.drop(df.loc[:, "wt6h_wt0h":"wtRC12h_wt6h_padj"].columns, axis=1)
    df.to_csv(target_dir + '/exp_de_proteins.csv', index=False, na_rep='NA')


def transcription_factor(data: str, target_dir: str):
    # read the data into panda frame
    df = pd.read_csv(data)
    # Remove all columns between column name  "wt6h_wt0h" to
    # "wtRC12h_wt6h_padj"
    df = df.drop(df.loc[:, "wt6h_wt0h":"wtRC12h_wt6h_padj"].columns, axis=1)
    # filter for proteins, where protein is transcription factor
    df = df[df['TF'] != "no"]
    df.to_csv(target_dir + '/TranscriptionFactor.csv', index=False)


def rel_nearest_distance(data: str, target_dir: str):
    # read the data into panda frame
    df = pd.read_csv(data, sep='\t')
    # only safe column nearest_index and nearest_SYMBOL
    df = df[['nearest_index', 'nearest_SYMBOL']]
    df.to_csv(target_dir + '/rel_nearest_distance.csv', index=False)


def rel_de(data: str, target_dir: str):
    # read the data into panda frame
    df = pd.read_csv(data)
    # only safe column SYMBOL and the corresponding DE time
    df1 = df[['SYMBOL', 'wt6h_wt0h']]
    df1 = df1.assign(Study='1', Celltype='Microglia')
    df1.to_csv(target_dir + '/rel_protein_wt6h_wt0h.csv', index=False)
    # see line 68
    df2 = df[['SYMBOL', 'wt24h_wt0h']]
    df2 = df2.assign(Study='1', Celltype='Microglia')
    df2.to_csv(target_dir + '/rel_protein_wt24h_wt0h.csv', index=False)
    # see line 68
    df3 = df[['SYMBOL', 'wt336h_wt0h']]
    df3 = df3.assign(Study='1', Celltype='Microglia')
    df3.to_csv(target_dir + '/rel_protein_wt336h_wt0h.csv', index=False)
    # see line 68
    df4 = df[['SYMBOL', 'wtRC12h_wt0h']]
    df4 = df4.assign(Study='1', Celltype='Microglia')
    df4.to_csv(target_dir + '/rel_protein_wtRC12h_wt0h.csv', index=False)
    # see line 68
    df5 = df[['SYMBOL', 'wtRC12h_wt6h']]
    df5 = df5.assign(Study='1', Celltype='Microglia')
    df5.to_csv(target_dir + '/rel_protein_wtRC12h_wt6h.csv', index=False)
    # see line 68
    df6 = df[['SYMBOL', 'wt6h_wt0h_padj']]
    df6 = df6.assign(Study='1', Celltype='Microglia')
    df6.to_csv(target_dir + '/rel_protein_wt6h_wt0h_padj.csv', index=False)
    # see line 68
    df7 = df[['SYMBOL', 'wt24h_wt0h_padj']]
    df7 = df7.assign(Study='1', Celltype='Microglia')
    df7.to_csv(target_dir + '/rel_protein_wt24h_wt0h_padj.csv', index=False)
    # see line 68
    df8 = df[['SYMBOL', 'wt336h_wt0h_padj']]
    df8 = df8.assign(Study='1', Celltype='Microglia')
    df8.to_csv(target_dir + '/rel_protein_wtRC336h_wt0h_padj.csv', index=False)
    # see line 68
    df9 = df[['SYMBOL', 'wtRC12h_wt0h_padj']]
    df9 = df9.assign(Study='1', Celltype='Microglia')
    df9.to_csv(target_dir + '/rel_protein_wtRC12h_wt0h_padj.csv', index=False)
    # see line 68
    df10 = df[['SYMBOL', 'wtRC12h_wt6h_padj']]
    df10 = df10.assign(Study='1', Celltype='Microglia')
    df10.to_csv(target_dir + '/rel_protein_wtRC12h_wt6h_padj.csv', index=False)


def rel_da(data: str, target_dir: str):
    # read the data into panda frame
    df = pd.read_csv(data, sep='\t')
    # only safe column SYMBOL and the corresponding DA time
    df1 = df[['nearest_index', 'open_region_wt12h_wt0h']]
    df1 = df1.assign(Study='1', Celltype='Microglia')
    df1.to_csv(target_dir + '/rel_or_wt12h_wt0h.csv', index=False)
    # see line 113
    df2 = df[['nearest_index', 'open_region_wt24h_wt0h']]
    df2 = df2.assign(Study='1', Celltype='Microglia')
    df2.to_csv(target_dir + '/rel_or_wt24h_wt0h.csv', index=False)
    # see line 113
    df3 = df[['nearest_index', 'open_region_wt336h_wt0h']]
    df3 = df3.assign(Study='1', Celltype='Microglia')
    df3.to_csv(target_dir + '/rel_or_wt336h_wt0h.csv', index=False)
    # see line 113
    df4 = df[['nearest_index', 'open_region_wtRC12h_wt0h']]
    df4 = df4.assign(Study='1', Celltype='Microglia')
    df4.to_csv(target_dir + '/rel_or_wtRC12h_wt0h.csv', index=False)
    # see line 113
    df5 = df[['nearest_index', 'open_region_wtRC12h_wt12h']]
    df5 = df5.assign(Study='1', Celltype='Microglia')
    df5.to_csv(target_dir + '/rel_or_wtRC12h_wt12h.csv', index=False)
    # see line 113
    df6 = df[['nearest_index', 'open_region_wt12h_wt0h_padj']]
    df6 = df6.assign(Study='1', Celltype='Microglia')
    df6.to_csv(target_dir + '/rel_or_wt12h_wt0h_padj.csv', index=False)
    # see line 113
    df7 = df[['nearest_index', 'open_region_wt24h_wt0h_padj']]
    df7 = df7.assign(Study='1', Celltype='Microglia')
    df7.to_csv(target_dir + '/rel_or_wt24h_wt0h_padj.csv', index=False)
    # see line 113
    df8 = df[['nearest_index', 'open_region_wt336h_wt0h_padj']]
    df8 = df8.assign(Study='1', Celltype='Microglia')
    df8.to_csv(target_dir + '/rel_or_wtRC336h_wt0h_padj.csv', index=False)
    # see line 113
    df9 = df[['nearest_index', 'open_region_wtRC12h_wt0h_padj']]
    df9 = df9.assign(Study='1', Celltype='Microglia')
    df9.to_csv(target_dir + '/rel_or_wtRC12h_wt0h_padj.csv', index=False)
    # see line 113
    df10 = df[['nearest_index', 'open_region_wtRC12h_wt12h_padj']]
    df10 = df10.assign(Study='1', Celltype='Microglia')
    df10.to_csv(target_dir + '/rel_or_wtRC12h_wt12h_padj.csv', index=False)


if __name__ == "__main__":
    # Get the path to the parent of the current directory
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    # get the path to the directory where the files are located
    original_data_dir = parent_dir + '/original_data/exp_data/'
    # define the path to the target diretory
    edited_data_dir = parent_dir + '/edited_data/'
    exp_DA = original_data_dir + 'exp_DA.csv'
    exp_DE = edited_data_dir + 'exp_de_proteins_filtered.csv'
    # run the functions
    # protein(exp_DE, edited_data_dir)
    transcription_factor(exp_DE, edited_data_dir)
    rel_de(exp_DE, edited_data_dir)
    rel_nearest_distance(exp_DA, edited_data_dir)
    open_region(exp_DA, edited_data_dir)
    rel_da(exp_DA, edited_data_dir)
    output = "Edited differential expression files written to: "
    print(output + edited_data_dir)
