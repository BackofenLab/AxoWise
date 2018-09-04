
import io
from Bio.KEGG.KGML import KGML_parser

def parse_KGML(pathway):
    gene_ids = set()
    pathway_stream = io.StringIO(pathway)
    pathway_object = KGML_parser.read(pathway_stream)

    for entry in pathway_object.genes:
        gene_ids.update(entry.name.split(" "))

    gene_ids = list(gene_ids)

    return pathway_object.title, gene_ids