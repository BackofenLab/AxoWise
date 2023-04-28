"""
Functions for interacting with STRING's REST API.
"""

from io import StringIO
from string import Template

import pandas as pd

from url import get, post

_CALLER_IDENTITY = "pgdb"
_SEPARATOR = "%0d"

# =================================== Map identifiers ===================================
# https://string-db.org/cgi/help.pl?subpage=api%23mapping-identifiers

_MAP_IDS_TEMPLATE = Template("https://string-db.org/api/${format}/get_string_ids?identifiers=${identifiers}&species=${species}&caller_identity=${identity}&limit=${limit}")

def map_identifiers(identifiers, species_id, limit=1, split=350):
    """
    Before using other API methods it is always advantageous to map your identifiers to the ones STRING uses.
    For each input protein STRING places the best matching identifier in the first row, so the first line will
    usually be the correct one.

    Arguments:
    - identifiers - protein identifiers to be mapped
    - species_id - NCBI taxon identifier
    - limit - how many matches per identifier to return (default: 1)
    - split - how many identifiers to match in one request (default: 350)

    Yields one of more pandas.DataFrame chunks.
    """

    def map_chunk(chunk):
        endpoint = _MAP_IDS_TEMPLATE.substitute(
            format="tsv",
            identifiers=_SEPARATOR.join(chunk),
            species=species_id,
            limit=limit,
            identity = _CALLER_IDENTITY
        )
        identifiers_file = get(endpoint)
        assert identifiers_file is not None, "GET request did not return anything. Try using a smaller chunk size."

        df = pd.read_csv(StringIO(identifiers_file), sep="\t")
        return df

    if len(identifiers) > split:
        i = 0
        while True:
            identifiers_chunk = identifiers[i : i + split]
            df = map_chunk(identifiers_chunk)
            yield df
            if i + split >= len(identifiers):
                break
            else:
                i += split
    else:
        df = map_chunk(identifiers)
        yield df

# =================================== Functional enrichment ===================================
# https://string-db.org/cgi/help.pl?subpage=api%23getting-functional-enrichment

_ENRICHMENT_URL_TEMPLATE = Template("https://string-db.org/api/${format}/enrichment")
_ENRICHMENT_ARGS_TEMPLATE = Template("identifiers=${identifiers}&species=${species}&caller_identity=${identity}")

def functional_enrichment(identifiers, species_id):
    """
    Retrieves the functional enrichment for any set of input proteins.

    Arguments:
    - identifiers - protein identifiers (preferably mapped via STRING'S API before)
    - species_id - NCBI taxon identifier

    Returns a single pandas.DataFrame.
    """

    endpoint = _ENRICHMENT_URL_TEMPLATE.substitute(
        format="tsv"
    )

    data = _ENRICHMENT_ARGS_TEMPLATE.substitute(
        identifiers = _SEPARATOR.join(identifiers),
        species = species_id,
        identity = _CALLER_IDENTITY
    ).encode("utf-8")

    enrichment_file = post(endpoint, data)
    if enrichment_file is None:
        return None

    df = pd.read_csv(StringIO(enrichment_file), sep="\t")
    del df["ncbiTaxonId"], df["number_of_genes"], df["preferredNames"]

    return df
