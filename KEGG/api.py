from string import Template
from url import get

# Predefined API endpoints
_organisms_endpoint = "http://rest.kegg.jp/list/organism"

# Template strings for constructing the API endpoints
_pathway_template = Template("http://rest.kegg.jp/list/pathway/${organism_id}")
_get_template = Template("http://rest.kegg.jp/get/${entries}${kgml}")

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
