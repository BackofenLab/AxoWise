"""
Author: Tillman Heisner
Email: theisner@posteo.de

This contains mutiple functions, which filter csvs for desired data.
The main writes them to new csvs
"""

import pandas as pd
#import sys
import os

def filter_for_individual_rows(file1: str, file2: str, key1: str,key2: str)\
    -> pd.DataFrame:
    """
    Input: 2 csv files and the key on which to filter on
    Function: filter file2 for rows which are not present in file 1
    Output: pd.Dataframe
    """
    # read in the two csv files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # specify the columns to use as the keys for filtering
    key_column_1 = key1
    key_column_2 = key2

    # set the columns to lower letters, to make the match case insensitive
    df1[key_column_1] = df1[key_column_1].str.lower()    
    df2[key_column_2] = df2[key_column_2].str.lower()
    
    # create a set of the values in the key column for df1
    df1_keys = set(df1[key_column_1])

    # filter df2 for rows where the value in the key column 
    # is not in the df1_keys set
    df2_filtered = df2[~df2[key_column_2].isin(df1_keys)]

    # return the filtered rows
    return(df2_filtered)


def filter_for_same_rows(file1: str, file2: str, key1: str,key2: str)\
    -> pd.DataFrame:
    """
    Input: 2 csv files and the key on which to filter on
    Function: filter file2 for rows which are present in file 1
    Output: pd.Dataframe
    """
    # read in the two csv files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # specify the columns to use as the keys for filtering
    key_column_1 = key1
    key_column_2 = key2

    # set the columns to lower letters, to make the match case insensitive
    df1[key_column_1] = df1[key_column_1].str.lower()    
    df2[key_column_2] = df2[key_column_2].str.lower()
    
    # create a set of the values in the key column for df1
    df1_keys = set(df1[key_column_1])

    # filter df2 for rows where the value in the key column
    # is not in the df1_keys set
    df2_filtered = df2[df2[key_column_2].isin(df1_keys)]

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
    target = ['string_proteins_filtered.csv','exp_de_proteins_filtered.csv']
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
    # write the results to a csv
    string_proteins_filtered_2.to_csv(target[0], index= False, na_rep='NA') 
    exp_de_proteins_filtered.to_csv(target[1], index= False, na_rep='NA') 


    