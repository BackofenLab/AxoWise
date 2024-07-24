import os
import re
import sys
from string import Template

import mygene
import requests

sys.path.append("..")

import util.data_util as util

# Predefined API endpoints
_organisms_endpoint = "http://rest.kegg.jp/list/organism"

# Template strings for constructing the API endpoints
_pathway_template = Template("http://rest.kegg.jp/list/pathway/${organism_id}")
_get_template = Template("http://rest.kegg.jp/get/${entries}${kgml}")
_map_id_template = Template(
    "https://string-db.org/api/${format}/get_string_ids?identifiers=${identifiers}&species=${species}&caller_identity=cgdb"
)
_map_id_template_no_species = Template(
    "https://string-db.org/api/${format}/get_string_ids?identifiers=${identifiers}&species=${species}&caller_identity=cgdb"
)


def version():
    """
    Check the latest build of KEGG

    Returns:
    Latest KEGG Version (str) in the format "%b %d"
    """
    try:
        # Assuming the URL and parameters are correctly set up to fetch the version
        url = "https://rest.kegg.jp/info/kegg"
        content = requests.get(url, timeout=5).text
        # Example regex, adjust based on actual content format
        match = re.search(r"Release \d+\.\d+\+/\d{2}-\d{2}, (\w{3} \d{2})", content)

        if match:
            release_number = match.group(1)
            return release_number  # Returns the matched date string in "%b %d" format
        else:
            raise ValueError(f"Could not find the release number of KEGG in\n{content}.")
    except requests.exceptions.Timeout:
        raise TimeoutError(f"The request to {url} timed out. Please try again later.")


def get_pathways(organism_id):
    endpoint = _pathway_template.substitute(organism_id=organism_id)
    pathways_file = util.get(endpoint)
    assert pathways_file is not None
    return pathways_file


def get_pathway_file(id, kgml=False):
    endpoint = _get_template.substitute(entries=id, kgml="/kgml" if kgml else "")
    pathway_file = util.get(endpoint)
    assert pathway_file is not None
    return pathway_file


def write_diseases(pathway_diseases, diseases_file, written_diseases):
    disease_ids, disease_names = zip(*pathway_diseases)
    for disease in pathway_diseases:
        if disease not in written_diseases:
            diseases_file.write("{}\t{}\n".format(*disease))
            written_diseases.add(disease)
    return disease_ids


def write_drugs(pathway_drugs, drugs_file, written_drugs):
    drug_ids, drug_names = zip(*pathway_drugs)
    for drug in pathway_drugs:
        if drug not in written_drugs:
            drugs_file.write("{}\t{}\n".format(*drug))
            written_drugs.add(drug)
    return drug_ids


def write_compounds(pathway_compounds, compounds_file, written_compounds):
    compound_ids, compound_names = zip(*pathway_compounds)
    for compound in pathway_compounds:
        if compound not in written_compounds:
            compounds_file.write("{}\t{}\n".format(*compound))
            written_compounds.add(compound)
    return compound_ids


def symbols_to_ensemble(symbols, species, specifier):
    """
    Convert a list of symbols to ensemble_ids

    Arguments:
    symbols: a list containing symbols to convert
    species: species which the symbols belong to
    specifier: specifies if user wants ensembl gene ids or protein ids

    Returns:
    ensemble_list: A list of ensemble_ids
    """
    mg = mygene.MyGeneInfo()
    ensembl_list = []
    results = mg.querymany(
        symbols, scopes="symbol", fields=f"ensembl.{specifier}", species=f"{species}"
    )
    for result in results:
        if "ensembl" in result:
            res = result["ensembl"]
            if isinstance(res, list):
                ensembl_id = res[0][f"{specifier}"]
            else:
                ensembl_id = res[f"{specifier}"]
            if isinstance(ensembl_id, list):
                for i in ensembl_id:
                    ensembl_list.append(i)
            else:
                ensembl_list.append(ensembl_id)
        else:
            print(f"{result['query']} not found")
    return ensembl_list


def scrapping(path, species):
    """
    Scraps relevant data from KEGG

    Arguments:
    path: the directory in which the data will be stored
    species: the species of interest for scrapping
    """
    kegg_id = "mmu" if species == "mouse" else "hsa"

    # Diseases, drugs & compounds
    diseases_file = open(
        os.path.join(path, "kegg_diseases.{}.tsv".format(species)),
        mode="w",
        encoding="utf-8",
    )
    drugs_file = open(
        os.path.join(path, "kegg_drugs.{}.tsv".format(species)),
        mode="w",
        encoding="utf-8",
    )
    compounds_file = open(
        os.path.join(path, "kegg_compounds.{}.tsv".format(species)),
        mode="w",
        encoding="utf-8",
    )

    written_diseases = set()
    written_drugs = set()
    written_compounds = set()

    # Pathways
    pathways_file = open(
        os.path.join(path, "kegg_pathways.{}.tsv".format(species)),
        mode="w",
        encoding="utf-8",
    )

    # Write headers
    diseases_file.write("\t".join(["id", "name"]) + "\n")
    drugs_file.write("\t".join(["id", "name"]) + "\n")
    compounds_file.write("\t".join(["id", "name"]) + "\n")
    pathways_file.write(
        "\t".join(
            [
                "id",
                "name",
                "description",
                "classes",
                "symbols",
                "genes_external_ids",
                "diseases_ids",
                "drugs_ids",
                "compounds_ids",
            ]
        )
        + "\n"
    )

    pathways = get_pathways(kegg_id)

    # Get the pathway
    pathway_table = list(util.read_table(pathways, (str, str), "\t"))
    for idx, (pathway_id, pathway_name) in enumerate(pathway_table):
        pathway = get_pathway_file(pathway_id, kgml=False)

        # Parse the KEGG pathway flat file
        pathway_parsed = util.parse_flat_file(pathway)
        pathway_title = pathway_parsed[0]
        pathway_description = pathway_parsed[1]
        pathway_classes = pathway_parsed[2]
        pathway_diseases = pathway_parsed[3]
        pathway_drugs = pathway_parsed[4]
        pathway_genes = pathway_parsed[5]
        pathway_compounds = pathway_parsed[6]

        print("[{} / {}]".format(idx + 1, len(pathway_table)), pathway_title)

        # Description
        has_description = pathway_description is not None

        # Classes
        has_classes = pathway_classes is not None

        # Genes and proteins
        has_genes = pathway_genes is not None
        if has_genes:
            pathway_gene_symbols = []
            for i in pathway_genes:
                if i:
                    pathway_gene_symbols.append(i[1])
            kegg2external_genes = symbols_to_ensemble(
                pathway_gene_symbols, species, "gene"
            )
        # Diseases
        has_diseases = pathway_diseases is not None
        if has_diseases:
            disease_ids = write_diseases(
                pathway_diseases, diseases_file, written_diseases
            )

        # Drugs
        has_drugs = pathway_drugs is not None
        if has_drugs:
            drug_ids = write_drugs(pathway_drugs, drugs_file, written_drugs)

        # Compounds
        has_compounds = pathway_compounds is not None
        if has_compounds:
            compound_ids = write_compounds(
                pathway_compounds, compounds_file, written_compounds
            )

        # Save the pathway
        description_column = pathway_description if has_description else ""
        symbol_column = pathway_gene_symbols if has_genes else ""
        genes_column = kegg2external_genes if has_genes else ""
        classes_column = ",".join(pathway_classes) if has_classes else ""
        diseases_column = ",".join(disease_ids) if has_diseases else ""
        drugs_column = ",".join(drug_ids) if has_drugs else ""
        compounds_column = ",".join(compound_ids) if has_compounds else ""
        pathways_file.write(
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                pathway_id,
                pathway_title,
                description_column,
                classes_column,
                symbol_column,
                genes_column,
                diseases_column,
                drugs_column,
                compounds_column,
            )
        )
    pathways_file.close()
    diseases_file.close()
    drugs_file.close()
    compounds_file.close()
