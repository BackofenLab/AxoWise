import os
import requests
import argparse
import pandas as pd
import csv
import kegg
import sys
import datetime
import mygene

sys.path.append("..")
import util.data_util as util


def parse_cli_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "species_name",
        type=str,
        help="Species name (e.g. Homo sapiens / human)",
    )

    return parser.parse_args()


def download_data(species):
    """
    Downloads the data from Baderlabs

    Arguments:
    species: the species which data we want to download
    """

    if species.lower() == "mouse":
        url = "http://download.baderlab.org/EM_Genesets/current_release/Mouse/symbol/Mouse_GO_AllPathways_with_GO_iea_July_03_2023_symbol.gmt"

    elif species.lower() == "human":
        url = "http://download.baderlab.org/EM_Genesets/current_release/Human/symbol/Human_GO_AllPathways_with_GO_iea_July_03_2023_symbol.gmt"

    else:
        return "Invalid species."

    response = requests.get(url)
    with open(f"data/{species}_all_pathways.gmt", "wb") as file:
        file.write(response.content)
    return 1


def read_data(file_name):
    """
    Reads the data from the specified file and returns it as a DataFrame.

    Arguments:
    file_name: the name of the file to read
    """
    with open(file_name, "r") as file:
        reader = csv.reader(file, delimiter="\t")
        data = []
        for row in reader:
            name = row[0].split("%")
            source = name[1]
            id = name[2]
            descr = row[1]
            proteins = ",".join(row[2:])
            data.append([id, descr, source, proteins])
        df = pd.DataFrame(data, columns=["id", "name", "category", "proteins"])
    return df


def read_kegg_data(specifier):
    """
    Reads the KEGG data and returns it as a DataFrame.

    Arguments:
    specifier: the species specifier (e.g. 'mmu' or 'human')
    """
    kegg_df = pd.read_csv(
        f"data/kegg_pathways.{specifier}.tsv",
        delimiter="\t",
        usecols=["id", "name", "genes_external_ids"],
    )
    kegg_df.insert(loc=2, column="category", value="KEGG")
    kegg_df = kegg_df.rename(columns={"genes_external_ids": "proteins"})
    return kegg_df


def symbols_to_ensembl(symbols, species):
    """
    Maps Symbols to Ensemble_Gene_id

    Arguments:
    symbols: list of symbols to be mapped
    species: species that the symbols belong to, eg: "mouse"

    returns:
    mapping: a dictionary of symbols where their key is the ensembleT_id
    """
    mapping = {}
    mg = mygene.MyGeneInfo()
    results = mg.querymany(symbols, scopes="symbol", fields="ensembl.gene", species=f"{species}")
    for result in results:
        if "ensembl" in result:
            res = result["ensembl"]
            old = result["query"]
            if isinstance(res, list):
                ensembl_id = res[0]["gene"]
            else:
                ensembl_id = res["gene"]
            mapping[old] = ensembl_id
        else:
            print(f"{result['query']} not found")
    return mapping


def data_formatting(species, folder):
    """
    Formats the data to our specifications

    Arguments:
    species: the species which data we want to format
    """
    file_name = os.path.join(folder, f"{species.lower()}_all_pathways.gmt")

    # Read the data from Baderlabs
    df = read_data(file_name)

    # Read the KEGG data
    kegg_df = read_kegg_data(species.lower())

    merged_df = pd.concat([df, kegg_df], ignore_index=True)
    merged_df = merged_df.drop_duplicates(subset=["name", "category"])
    merged_df.to_csv(f"data/AllPathways_{species}.csv")


def download_necessary(filepath):
    """
    Check if new releases are available

    Arguments:
    filepath: filepath of the text file that contains last used release

    Returns:
    Tuple of (bool, bool, string) which correspond to whether KEGG and/or Baderlabs
    respectively have a new release and lastly a string of the versions of both.
    """
    update_kegg = False
    update_geneset = False
    response = requests.get("http://download.baderlab.org/EM_Genesets/")
    kegg_release = f"kegg: {kegg.version()}"
    # get the content of the webpage as a string
    webpage_content = response.text
    geneset_file = f"bader: {util.get_latest_release_date_bader(webpage_content).strftime('%Y-%m-%d')}"
    with open(filepath, "a+") as file:
        file.seek(0)
        content = file.read()
        if len(content) == 0:
            update_geneset = True
            update_kegg = True
        else:
            old_version_geneset = util.search_line(filepath, r"bader: (.*)")
            old_version_kegg = util.search_line(filepath, r"kegg: (.*)")
            if not old_version_geneset or datetime.datetime.strptime(
                old_version_geneset, "%Y-%m-%d"
            ) < util.get_latest_release_date_bader(webpage_content):
                update_geneset = True
            if not old_version_kegg or datetime.datetime.strptime(
                old_version_kegg, "%b %d"
            ) < datetime.datetime.strptime(kegg.version(), "%b %d"):
                update_kegg = True

    return (update_kegg, update_geneset, geneset_file, kegg_release)


def main():
    # Directory for saving the data
    folder = "data"
    os.makedirs(folder, exist_ok=True)

    # Set correct url and pattern
    gene_pattern = r"bader: (.*)"
    kegg_pattern = r"kegg: (.*)"
    filepath = os.path.join(folder, f"release_versions.txt")

    kegg_update, geneset_update, geneset_name, kegg_version = download_necessary(filepath)
    if geneset_update:
        # Download the data from Baderlabs
        print("Downloading Pathway data for mouse")
        download_data("mouse")
        print("Geneset download succesfull for mouse")
        # print("Downloading Pathway data for human") uncomment once human will be included
        # download_data("human") uncomment once human will be included
        # print("Geneset download succesfull for human") uncomment once human will be included
        util.update_line(filepath, gene_pattern, geneset_name)
    if kegg_update:
        # Download the KEGG data
        print("Downloading KEGG data for mouse")
        kegg.scrapping(folder, "mouse")
        print("KEGG download succesfull for mouse")
        # kegg.scrapping(folder, "human") uncomment once human will be included
        # print("KEGG download succesfull for human") uncomment once human will be included
        util.update_line(filepath, kegg_pattern, kegg_version)
    if kegg_update or geneset_update:
        print("Formatting mouse data...")
        data_formatting("mouse", folder)
        print("Formating mouse data succesfull")
        # print("Formatting human data...") uncomment once human will be included
        # data_formatting("human", folder) uncomment once human will be included
        # print("Formating human data succesfull") uncomment once human will be included


if __name__ == "__main__":
    main()
