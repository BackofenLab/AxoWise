from string import Template
from url import get

# Predefined API endpoints
_organisms_endpoint = "http://rest.kegg.jp/list/organism"

# Template strings for constructing the API endpoints
_pathway_template = Template("http://rest.kegg.jp/list/pathway/${organism_id}")
_get_template = Template("http://rest.kegg.jp/get/${entries}${kgml}")
_map_id_template = Template("https://string-db.org/api/${format}/get_string_ids?identifiers=${identifiers}&caller_identity=cgdb")

def organisms():
    organisms_file = get(_organisms_endpoint)
    return organisms_file

def pathways(organism_id):
    endpoint = _pathway_template.substitute(organism_id = organism_id)
    pathways_file = get(endpoint)
    return pathways_file

def pathway(pathway_id, kgml = False):
    endpoint = _get_template.substitute(
        entries = pathway_id,
        kgml = "/kgml" if kgml else ""
    )
    pathway_file = get(endpoint)
    return pathway_file

def map_identifiers_to_STRING(identifiers):
    endpoint = _map_id_template.substitute(
        format = "tsv",
        identifiers = "%0d".join(identifiers)
    )
    identifiers_file = get(endpoint)
    return identifiers_file