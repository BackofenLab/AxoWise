"""
Author: Tillman Heisner
Email: theisner@posteo.de

This download files from the string database and converts them to csvs
"""
import requests
import gzip
import pandas as pd
import io

def download_gzip_files(url: str, data: str, seperator: str,target: str) -> None:
    #use the url given as an argument
    response = requests.get(url)
    # if request was sucesfull do this
    if response.status_code == 200:
        print('File downloaded successfully.')
    else:
        print('Failed to download file. Error code:', response.status_code)
    #open gzip to open the gz data downloaded previously
    with gzip.open(io.BytesIO(response.content), 'rb') as file:
        df = pd.read_csv(file, sep= seperator)
    df.to_csv(target, index= False, na_rep='NA') 
        
        

if __name__ == '__main__':
    tab = '\t' 
    space = ' '
    url = 'https://stringdb-static.org/download/protein.enrichment.terms.v11.5/10090.protein.enrichment.terms.v11.5.txt.gz'
    data = '10090.protein.enrichment.terms.v11.5.txt.gz'
    target = 'funtional_terms_to_proteins_edges.csv'
    download_gzip_files(url,data,tab,target)
    url2 = 'https://stringdb-static.org/download/protein.info.v11.5/10090.protein.info.v11.5.txt.gz'
    data2 = '10090.protein.info.v11.5.txt.gz'
    target2 = 'string_proteins.csv'
    download_gzip_files(url2,data2,tab,target2)
    url3 = 'https://stringdb-static.org/download/protein.links.v11.5/10090.protein.links.v11.5.txt.gz'
    data3 = '0090.protein.links.v11.5.txt.gz'
    target3 = 'string_proteins_edges.csv'
    download_gzip_files(url3,data3,space,target3)
