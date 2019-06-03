"""
Functions for interacting with STRING's REST API.
"""

from io import StringIO
from string import Template

import pandas as pd

from url import get

_CALLER_IDENTITY = "pgdb"
_SEPARATOR = "%0d"

# =================================== Functional enrichment ===================================
# https://string-db.org/cgi/help.pl?subpage=api%23getting-functional-enrichment

functional_enrichment_template = Template("https://string-db.org/api/${format}/enrichment?identifiers=${identifiers}&species=${species}")

def functional_enrichment(identifiers, species_id):
    endpoint = functional_enrichment_template.substitute(
        format = "tsv",
        identifiers = _SEPARATOR.join(identifiers),
        species = species_id
    )

    enrichment_file = get(endpoint)
    if enrichment_file is None:
        return None

    df = pd.read_csv(StringIO(enrichment_file), sep="\t")

    return df
