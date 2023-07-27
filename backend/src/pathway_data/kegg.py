import re
from string import Template

import sys
import os
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
    Latest KEGG Version (float)
    """
    content = requests.get("https://rest.kegg.jp/info/kegg").text
    match = re.search(r"Release \d+\.\d+\+/\d{2}-\d{2}, (\w{3} \d{2})", content)
    release_number = match.group(1)
    return release_number


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


def map_identifiers_to_STRING(identifiers, species=None, split=70):
    template = _map_id_template
    if species is None:
        template = _map_id_template_no_species

    if len(identifiers) > split:
        i = 0
        while True:
            identifiers_chunk = identifiers[i : i + split]
            endpoint = template.substitute(format="tsv", identifiers="%0d".join(identifiers_chunk), species=species)
            identifiers_file = util.get(endpoint)
            assert identifiers_file is not None
            yield identifiers_file, i
            if i + split >= len(identifiers):
                break
            else:
                i += split
    else:
        endpoint = template.substitute(format="tsv", identifiers="%0d".join(identifiers), species=species)
        identifiers_file = util.get(endpoint)
        assert identifiers_file is not None
        yield identifiers_file, 0


def map_genes(pathway_genes, ncbi_id, kegg_id):
    gene_ids, gene_short_names, gene_long_names = zip(*pathway_genes)
    gene_ids = list(map(lambda gene_id: "{}:{}".format(kegg_id, gene_id), list(gene_ids)))
    print("\tGenes:", len(gene_ids))

    # Map KEGG gene identifiers to STRING external identifiers
    kegg2external = dict()
    for mapped_identifiers, idx_offset in map_identifiers_to_STRING(gene_ids, ncbi_id):
        for idx, external_id, species_id, species_name, preferred_name, annotation in util.read_table(
            mapped_identifiers, (int, str, int, str, str, str), delimiter="\t"
        ):
            gene_id = gene_ids[idx + idx_offset]
            if gene_id in kegg2external:
                print("\tMapping for {} not unique!".format(gene_id))
            else:
                kegg2external[gene_id] = external_id

    num_not_mapped = len(gene_ids) - len(kegg2external)
    if num_not_mapped > 0:
        print("\t{} gene(s) could not be mapped to STRING external ID!".format(num_not_mapped))

    return kegg2external
