"""
Author: Tillman Heisner
Email: theisner@posteo.de

This contains mutiple functions, which filter csvs for desired data.
The main writes them to new csvs
"""

import pandas as pd
#import sys
import os

def filter_for_rows(file1: pd.DataFrame, file2: pd.DataFrame, key1: str,
                     key2: str, match: bool) -> pd.DataFrame:
    """
    Takes 2 csv files, filters the rows of the second file in which 
    the value of a column are the same/not the same as in the first one 
    key1, key2: determines the columns on which to filter
    match: determines if u look for same vlaues or different values
    Output: pd.Dataframe
    """
    # specify the columns to use as the keys for filtering
    key_column_1 = key1
    key_column_2 = key2

    # set the columns to lower letters, to make the match case insensitive
    file1[key_column_1] = file1[key_column_1].str.lower()    
    file2[key_column_2] = file2[key_column_2].str.lower()
    
    # create a set of the values in the key column for df1
    df1_keys = set(file1[key_column_1])

    if match:
        # filter for the equal value
        df2_filtered = file2[file2[key_column_2].isin(df1_keys)]
    else: 
       # filter for the unequal value
        df2_filtered = file2[~file2[key_column_2].isin(df1_keys)]

    # return the filtered rows
    return(df2_filtered)

def delete_rows_having_value(file1: str, key_column: str, value) \
    -> pd.DataFrame:
    # read the csv
    df = pd.read_csv(file1)
    # Use boolean indexing to filter the rows where 
    # the value is not present in the key column 
    return(df[~df[key_column].str.contains(value)])


def filter_for_value_bigger(file: str, key: str, value: int):
    """
    This filters the given file on the key column for rows which have 
    a bigger value then the given one.
    """
    df = pd.read_csv(file, sep=' ')
    return(df[df[key] > int(value)])


if __name__ == '__main__':
    
    # Get current working directory
    current_dir = os.getcwd()
    # define the file names, which get used
    files = ['string_proteins.csv','exp_de_proteins.csv']
    # define the file names to which gets written
    target = ['string_proteins_filtered.csv','exp_de_proteins_filtered.csv',
              'duplicate_proteins.csv']
    # Construct the file paths
    path_to_string_proteins = os.path.join(current_dir, files[0])
    path_to_exp_de_proteins = os.path.join(current_dir, files[1])
    # filter for rows where prefered_name is not NA
    string_proteins_filtered_1 = delete_rows_having_value\
        (path_to_string_proteins, 'preferred_name', 'NA')
    # filter for rows where prefered_name does not start with ENSMUSG
    string_proteins_filtered_2 = delete_rows_having_value\
        (path_to_string_proteins, 'preferred_name', 'ENSMUSG')
    # filter for rows where prefered_name does not start with ENSEMBL
    exp_de_proteins_filtered = delete_rows_having_value\
        (path_to_exp_de_proteins, 'SYMBOL', 'ENSMUSG')
    # filter for proteins in exp_proteins which are present in string_proteins
    proteins_duplicates = filter_for_rows(string_proteins_filtered_2,
                                               exp_de_proteins_filtered,
                                               'preferred_name',
                                               'SYMBOL',True)
    # write the results to a csv
    string_proteins_filtered_2.to_csv(target[0], index= False, na_rep='NA') 
    exp_de_proteins_filtered.to_csv(target[1], index= False, na_rep='NA')
    proteins_duplicates.to_csv(target[2], index= False, na_rep='NA')


    