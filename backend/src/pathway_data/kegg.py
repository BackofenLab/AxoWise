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
