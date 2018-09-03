from string import Template
from url import get

# Predefined API endpoints
_organisms_endpoint = "http://rest.kegg.jp/list/organism"

# Template strings for constructing the API endpoints
_pathway_template = Template("http://rest.kegg.jp/list/pathway/${organism_id}")

def organisms():
    organisms_file = get(_organisms_endpoint)
    return organisms_file

def pathway(organism_id):
    endpoint = _pathway_template.substitute(organism_id = organism_id)
    pathway_file = get(endpoint)
    return pathway_file
