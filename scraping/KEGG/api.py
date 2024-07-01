from string import Template

from .url import get

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


def organisms():
    organisms_file = get(_organisms_endpoint)
    assert organisms_file is not None
    return organisms_file


def pathways(organism_id):
    endpoint = _pathway_template.substitute(organism_id=organism_id)
    pathways_file = get(endpoint)
    assert pathways_file is not None
    return pathways_file


def pathway(pathway_id, kgml=False):
    endpoint = _get_template.substitute(
        entries=pathway_id, kgml="/kgml" if kgml else ""
    )
    pathway_file = get(endpoint)
    assert pathway_file is not None
    return pathway_file


def map_identifiers_to_STRING(identifiers, species=None, split=10):
    template = _map_id_template
    if species is None:
        template = _map_id_template_no_species

    if len(identifiers) > split:
        i = 0
        while True:
            identifiers_chunk = identifiers[i : i + split]
            endpoint = template.substitute(
                format="tsv", identifiers="%0d".join(identifiers_chunk), species=species
            )
            identifiers_file = get(endpoint)
            assert identifiers_file is not None
            yield identifiers_file, i
            if i + split >= len(identifiers):
                break
            else:
                i += split
    else:
        endpoint = template.substitute(
            format="tsv", identifiers="%0d".join(identifiers), species=species
        )
        identifiers_file = get(endpoint)
        assert identifiers_file is not None
        yield identifiers_file, 0
