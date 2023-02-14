"""
Author: Tillman Heisner
Email: theisner@posteo.de

This download files from the string database and converts them to csvs
"""
import requests
import gzip
import pandas as pd
import io
import os


def download_gzip_files(url: str, data: str, seperator: str) -> pd.DataFrame:
    # use the url given as an argument
    response = requests.get(url)
    # if request was sucesfull do this
    if response.status_code == 200:
        print('File downloaded successfully.')
    else:
        print('Failed to download file. Error code:', response.status_code)
    # open gzip to open the gz data downloaded previously
    with gzip.open(io.BytesIO(response.content), 'rb') as file:
        df = pd.read_csv(file, sep=seperator)
    return df


if __name__ == '__main__':
    # different delimiters used in the gzip files
    tab = '\t'
    space = ' '
    # Define the directory we want to write the files in
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    target_dir = parent_dir + '/original_data/string_data/'
    # download the files and write them to target directory
    url = 'https://stringdb-static.org/download/protein.enrichment.terms.'
    url = url + 'v11.5/10090.protein.enrichment.terms.v11.5.txt.gz'
    data = '10090.protein.enrichment.terms.v11.5.txt.gz'
    file_name = 'funtional_terms_to_proteins_edges.csv'
    funtional_terms_to_proteins_edges = download_gzip_files(url, data, tab)
    funtional_terms_to_proteins_edges.to_csv(target_dir + file_name,
                                             index=False, na_rep='NA')
    # see line 38
    url2 = 'https://stringdb-static.org/download/protein.info.v11.5/'
    url2 = url2 + '10090.protein.info.v11.5.txt.gz'
    data2 = '10090.protein.info.v11.5.txt.gz'
    file_name_2 = 'string_proteins.csv'
    string_proteins = download_gzip_files(url2, data2, tab)
    string_proteins.to_csv(target_dir + file_name_2,
                           index=False, na_rep='NA')
    # see line 38
    url3 = 'https://stringdb-static.org/download/protein.links.v11.5/'
    url3 = url3 + '10090.protein.links.v11.5.txt.gz'
    data3 = '0090.protein.links.v11.5.txt.gz'
    file_name_3 = 'string_proteins_edges.csv'
    string_proteins_edges = download_gzip_files(url3, data3, space)
    string_proteins_edges.to_csv(target_dir + file_name_3,
                                 index=False, na_rep='NA')
    print(f"Downloaded string files to: {target_dir}")
