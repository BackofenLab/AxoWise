import os
import requests
import argparse
import pandas as pd
import kegg
import sys
import datetime
import mygene
import re

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


def get_url(species):
    """
    Gets the url for the Symbol file

    Arguments:
    species: the species which data we want to download
    string: whether to download from string or not
    """
    if species == "mouse":
        string_species = "mus+musculus"
    else:
        string_species = "homo+sapiens"
    url_string = f"https://string-db.org/cgi/download?sessionId=bthCAcyLVvFS&species_text={string_species}"
    url_bader = f"http://download.baderlab.org/EM_Genesets/current_release/{species.capitalize()}/symbol/"
    response_string = requests.get(url_string)
    response_bader = requests.get(url_bader)
    if response_bader.status_code == 404:
        print(f"The URL {url_bader} returned a 404 error")
        return 0
    pattern_proteins = r"(\S+\.protein\.info\.[\w.]+)"
    pattern_pathway = r"(\S+\.protein\.enrichment.terms\.[\w.]+)"
    match_proteins = re.findall(pattern_proteins, response_string.text)
    match_pathway = re.findall(pattern_pathway, response_string.text)
    result_protein = match_proteins[0].split("href=")[1].replace('"', "")
    result_pathway = match_pathway[0].split("href=")[1].replace('"', "")
    match = re.search(
        rf'{species.capitalize()}_GO_AllPathways_with_GO_iea_[A-Z][a-z]+_\d{{2}}_\d{{4}}_symbol\.gmt(?=">)',
        response_bader.text,
    )
    result = match.group()
    return [url_bader + result, result_protein, result_pathway]


def download_data(species):
    """
    Downloads the data from Baderlabs

    Arguments:
    species: the species which data we want to download
    """
    urls = get_url(species)
    url_bader = urls[0]
    string = [urls[1], urls[2]]
    if url_bader == 0:
        return 0
    # For string download
    response_protein = requests.get(string[0])
    response_pathway = requests.get(string[1])
    with open(f"data/proteins_string_{species}.txt.gz", "wb") as file:
        file.write(response_protein.content)
    with open(f"data/pathways_string_{species}.txt.gz", "wb") as file:
        file.write(response_pathway.content)
    response = requests.get(url_bader)
    # Handle 404 error (Case: database updated for human but mouse not yet available)
    if response.status_code == 404:
        print(f"The URL {url_bader} returned a 404 error")
        return 0
    if len(response.text) == 0:
        print("Empty gmt file, come back later")
        return 0
    with open(f"data/{species}_all_pathways.gmt", "wb") as file:
        file.write(response.content)
    return 1


def genes_to_proteins(genes, species):
    """
    Convert ensembl genes to all corresponding proteins

    Arguments:
    genes: list of ensemble_gene_ids
    species: species of interest

    returns:
    gene_mapping: a dict with the keys being gene_ids and values protein_ids
    """
    gene_mapping = {}
    m = mygene.MyGeneInfo()
    results = m.querymany(genes, fields="ensembl.protein", species=f"{species}")
    for result in results:
        if "ensembl" in result:
            res = result["ensembl"]
            old = result["query"]
            if isinstance(res, list):
                ensembl_id = res[0]["protein"]
            else:
                ensembl_id = res["protein"]
                ensembl_id = [ensembl_id] if isinstance(ensembl_id, str) else ensembl_id
            gene_mapping[old] = ensembl_id
    return gene_mapping


def format_string_data(species):
    """
    Format the data acquired from String to the correct format

    Argument:
    species: species of interest
    """
    df_proteins = pd.read_csv(f"data/proteins_string_{species}.txt.gz", compression="gzip", sep="\t")
    df_pathways = pd.read_csv(f"data/pathways_string_{species}.txt.gz", compression="gzip", sep="\t")
    df_pathways = df_pathways[df_pathways["category"] == "Reactome Pathways"]
    df_pathways = (
        df_pathways.groupby("term")
        .agg(
            {
                "#string_protein_id": list,  # convert string_protein_id to list
                "category": "first",  # keep the first category encountered
                "term": "first",
                "description": "first",  # keep the first description encountered
            }
        )
        .reset_index(drop=True)
    )
    protein_dict = df_proteins.set_index("#string_protein_id")["preferred_name"].to_dict()
    df_pathways["#string_protein_id"] = df_pathways["#string_protein_id"].apply(
        lambda ids: [protein_dict.get(id, id) for id in ids]
    )
    all_symbols = set()
    for symbol_list in df_pathways["#string_protein_id"]:
        all_symbols.update(symbol_list)
    unique_symbols_list = list(all_symbols)
    gene_mapping, genes_to_map = symbols_to_ensembl(unique_symbols_list, f"{species}", "gene")
    gene_lis = []
    for i in df_pathways["#string_protein_id"]:
        genes = []
        if i:
            for j in i:
                if j in gene_mapping:
                    g = gene_mapping[j]
                    if isinstance(g, list):
                        for k in g:
                            genes.append(k)
                    else:
                        genes.append(gene_mapping[j])
        gene_lis.append(genes)
    df_pathways["genes"] = gene_lis
    df_pathways = df_pathways.rename(columns={"term": "id", "#string_protein_id": "symbols", "description": "name"})
    df_pathways = df_pathways[["id", "name", "category", "symbols", "genes"]]
    df_pathways.to_csv(f"data/reactome_pathways_{species}.csv", index=False)
    df_proteins.to_csv(f"data/string_proteins_{species}.csv", index=False)
    return


def read_data(species, file_name):
    """
    Reads the data from the specified file.

    Arguments:
    species: species of interest
    file_name: the name of the file to read
    """
    symbol = []
    unique_symbols = set()
    data = []
    with open(file_name, "r") as f:
        for line in f:
            fields = line.strip().split("\t")
            name = fields[0].split("%")
            if len(name) >= 2:
                source = name[1]
                ids = name[2]
                descr = fields[1]
                symbols = fields[2:]
                # Exclude lines where source starts with "REACTOME"
                if not source.startswith("REACTOME"):
                    data.append([ids, descr, source, symbols])
                    symbol.append(symbols)
                    unique_symbols.update(symbols)
            else:
                pass

    unique_symbols = list(unique_symbols)
    gene_mapping, genes_to_map = symbols_to_ensembl(unique_symbols, f"{species}", "gene")
    prots = genes_to_proteins(genes_to_map, species)
    pd.DataFrame(list(prots.items()), columns=["genes", "proteins"]).to_csv(f"data/mapped_genes_proteins_{species}.csv")
    gene_lis = []
    for i in symbol:
        genes = []
        prots = []
        if i:
            for j in i:
                if j in gene_mapping:
                    g = gene_mapping[j]
                    if isinstance(g, list):
                        for k in g:
                            genes.append(k)
                    else:
                        genes.append(gene_mapping[j])

        gene_lis.append(genes)

    df = pd.DataFrame(data, columns=["id", "name", "category", "symbols"])
    df["genes"] = gene_lis
    df.to_csv(f"data/bader_{species}.csv.gz", compression="gzip", index=False)
    return


def read_kegg_data(specifier):
    """
    Reads the KEGG data and returns it as a DataFrame.

    Arguments:
    specifier: the species specifier (e.g. 'mmu' or 'human')
    """
    kegg_df = pd.read_csv(
        f"data/kegg_pathways.{specifier}.tsv",
        delimiter="\t",
        usecols=["id", "name", "symbols", "genes_external_ids"],
    )
    kegg_df.insert(loc=2, column="category", value="KEGG")
    kegg_df = kegg_df.rename(columns={"genes_external_ids": "genes"})
    return kegg_df


def symbols_to_ensembl(symbols, species, specifier):
    """
    Maps Symbols to Ensemble_Gene_id

    Arguments:
    symbols: list of symbols to be mapped
    species: species that the symbols belong to, eg: "mouse"
    specifier: specifies if user wants ensembl gene ids or protein ids

    returns:
    mapping: a dictionary of symbols where their key is the ensembleT_id
    """
    mapping = {}
    gene_lis = []
    mg = mygene.MyGeneInfo()
    results = mg.querymany(symbols, scopes="symbol", fields=f"ensembl.{specifier}", species=f"{species}")
    for result in results:
        if "ensembl" in result:
            res = result["ensembl"]
            old = result["query"]
            if isinstance(res, list):
                ensembl_id = res[0][f"{specifier}"]
            else:
                ensembl_id = res[f"{specifier}"]
            mapping[old] = ensembl_id
            gene_lis.append(ensembl_id)
        else:
            print(f"{result['query']} not found")
    return mapping, gene_lis


def data_formatting(species, folder):
    """
    Formats the data to our specifications

    Arguments:
    species: the species which data we want to format
    """
    file_name = os.path.join(folder, f"{species.lower()}_all_pathways.gmt")

    # Read the data from Baderlabs
    read_data(species, file_name)
    df = pd.read_csv(f"data/bader_{species}.csv.gz", compression="gzip")
    # Read the KEGG data
    kegg_df = read_kegg_data(species.lower())
    reactome = pd.read_csv(f"data/reactome_pathways_{species}.csv")
    merged_df = pd.concat([df, kegg_df, reactome], ignore_index=True)
    merged_df = merged_df.drop_duplicates(subset=["name", "category"])
    merged_df = merged_df.loc[merged_df["genes"].str.len() > 2]
    merged_df["id"] = merged_df.apply(lambda row: f"{row['id']}~{row['category']}", axis=1)
    merged_df = merged_df.reset_index(drop=True)
    merged_df.to_csv(f"data/AllPathways_{species}.csv.gz", compression="gzip", index=False)


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
        if download_data("mouse") == 0:
            print("Mouse file not available on the server yet")
            return
        download_data("mouse")
        format_string_data("mouse")
        print("Pathway download succesfull for mouse")
        print("Downloading Pathway data for human")
        if download_data("human") == 0:
            print("Human file not available on the server yet")
            return
        download_data("human")
        format_string_data("human")
        print("Pathway download succesfull for human")
        util.update_line(filepath, gene_pattern, geneset_name)
    if kegg_update:
        # Download the KEGG data
        print("Downloading KEGG data for mouse")
        kegg.scrapping(folder, "mouse")
        print("KEGG download succesfull for mouse")
        print("Downloading KEGG data for human")
        kegg.scrapping(folder, "human")
        print("KEGG download succesfull for human")
        util.update_line(filepath, kegg_pattern, kegg_version)
    if kegg_update or geneset_update:
        print("Formatting mouse data...")
        data_formatting("mouse", folder)
        print("Formating mouse data succesfull")
        print("Formatting human data...")
        data_formatting("human", folder)
        print("Formating human data succesfull")


if __name__ == "__main__":
    main()
