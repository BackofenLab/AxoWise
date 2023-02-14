"""
Author: Tillman Heisner
Email: theisner@posteo.de

This takes the files in the folder /original_data/string_data
and edits the in such a way that,
every string protein-id matches its prefered name.
"""

import pandas as pd
import os


def csvs_to_dataframe(proteins: str, rel_proteins: str,
                      funtional_term_edges: str):
    """
    Input: path to csv files
    Output: panda dataframes
    """
    # read the csvs and turn them into data frames
    df_proteins = pd.read_csv(proteins)
    df_rel_proteins = pd.read_csv(rel_proteins)
    df_funtional_term_edges = pd.read_csv(funtional_term_edges)
    return (df_proteins, df_rel_proteins, df_funtional_term_edges)


def filter_data_frames(proteins: pd.DataFrame,
                       funtional_term_edges: pd.DataFrame):
    """
    Input:
    proteins (contains all the columns of the orginal csv)
    func_terms_rel (contains all the columns and rows of the original csv)
    Output:
    filtered_proteins:
        only cotains the columns we want to select
        and renames one of them
    filtered_funtional_term_edges:
        filtered to contain only certain values of the column categories
    """
    # filter data frame proteins
    columns_to_select = ['#string_protein_id', 'SYMBOL']
    filtered_proteins = proteins[columns_to_select]
    # filter data frame funtional_term edges
    categories_to_select = ['Reactome Pathways',
                            'Biological Process (Gene Ontology)',
                            'Molecular Function (Gene Ontology)',
                            'Cellular Component (Gene Ontology)',
                            'WikiPathways']
    filtered_funtional_term_edges = funtional_term_edges.loc[
         (funtional_term_edges['category'].isin(categories_to_select))]
    # return the filtered dataframes
    return (filtered_proteins, filtered_funtional_term_edges)


def rel_string_proteins_with_symbol_name(proteins: pd.DataFrame, rel_proteins:
                                         pd.DataFrame) -> pd.DataFrame:
    """
    input:
    proteins (contains string-id and prefered name for the protein)
    rel_proteins (contains string ids and score of relationship)
    output: dataframe where the string-ids are matched with prefered gene name
    """
    # Set the key column for both DataFrames
    key_col1 = 'protein1'
    key_col2 = 'protein2'
    key_col3 = '#string_protein_id'
    # add prefered name for protein1
    merged_df1 = pd.merge(rel_proteins, proteins, left_on=key_col1,
                          right_on=key_col3)
    merged_df2 = pd.merge(merged_df1, proteins, left_on=key_col2,
                          right_on=key_col3)
    # select the columns that are wanted in the result
    result = merged_df2.drop(['#string_protein_id_x',
                              '#string_protein_id_y'], axis=1)
    # rename columns
    result = result.rename(columns={"SYMBOL_x":
                                    "protein1_SYMBOL",
                                    "SYMBOL_y":
                                    "protein2_SYMBOL"})
    return result


def rel_functional_term_with_symbol_name(proteins: pd.DataFrame,
                                         func_terms_rel: pd.DataFrame) \
                                            -> pd.DataFrame:
    """
    input:
    proteins (contains string-id and prefered name for the protein)
    func_terms_rel (contains string id,category,term ,description)
    output: dataframe where the string-ids are matched with prefered gene name
    """
    # Set the key column for both DataFrames
    key_col = '#string_protein_id'
    # add prefered name for protein1
    result = pd.merge(func_terms_rel, proteins, left_on=key_col,
                      right_on=key_col)
    return result


if __name__ == '__main__':
    # Get the path to the parent of the current directory
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    # get the path to the directories where the files are located
    source_dir1 = parent_dir + '/original_data/string_data/'
    source_dir2 = parent_dir + '/edited_data/'
    # define the path to the target diretory
    target_dir = source_dir2
    # define filename for the final csvs
    target_name1 = os.path.join(target_dir,
                                'rel_string_proteins_to_proteins.csv')
    target_name2 = os.path.join(target_dir, 'rel_string_funtional' +
                                '_terms_to_proteins.csv')
    # define the file names
    files = ['string_proteins_edges.csv',
             'funtional_terms_to_proteins_edges.csv',
             'string_proteins_filtered.csv']
    # Construct the file paths
    path_to_protein_rel = os.path.join(source_dir1, files[0])
    path_to_funtional_term_edges = os.path.join(source_dir1, files[1])
    path_to_proteins = os.path.join(source_dir2, files[2])
    # read csvs
    proteins, rel_proteins, funtional_term_edges = csvs_to_dataframe(
        path_to_proteins,
        path_to_protein_rel,
        path_to_funtional_term_edges)
    # filter data frames
    filtered_proteins, filtered_funtional_term_edges = filter_data_frames(
        proteins,
        funtional_term_edges)
    # match string ids by prefered name
    file1 = rel_string_proteins_with_symbol_name(filtered_proteins,
                                                 rel_proteins)
    file2 = rel_functional_term_with_symbol_name(filtered_proteins,
                                                 filtered_funtional_term_edges)
    # write data frames to csvs
    file1.to_csv(target_name1, index=False, na_rep='NA')
    file2.to_csv(target_name2, index=False, na_rep='NA')
    # edited string files written to
    print(f"Edited string files written to: {target_dir}")
