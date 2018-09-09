
import re
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

def parse_flat_file(pathway):
    name = None
    description = None
    classes = None
    diseases = None
    drugs = None
    genes = None
    compounds = None

    state = None
    for line in re.split("\n+", pathway):
        if not line.startswith(" "):
            state = None

        # List continuation
        if state == "DISEASE":
            disease_id, disease_name = line.strip().split("  ")
            diseases.append((disease_id, disease_name))
        elif state == "DRUG":
            drug_id, drug_name = line.strip().split("  ")
            drugs.append((drug_id, drug_name))
        elif state == "GENE":
            gene_id, gene_names = line.strip().split("  ")
            short_name, long_name = map(lambda string: string.strip(), gene_names.split(";"))
            long_name = long_name[: long_name.index("[") - 1]
            genes.append((gene_id, short_name, long_name))
        elif state == "COMPOUND":
            compound_id, compound_name = line.strip().split("  ")
            compounds.append((compound_id, compound_name))

        # One-line entries
        elif line.startswith("NAME"):
            name = line.lstrip("NAME").lstrip()
            name = name[ : name.index("-") - 1]
        elif line.startswith("DESCRIPTION"):
            description = line.lstrip("DESCRIPTION").lstrip()
        elif line.startswith("CLASS"):
            classes_str = line.lstrip("CLASS")
            classes = list(map(lambda string: string.strip(), classes_str.split(";")))

        # List start
        elif line.startswith("DISEASE"):
            state = "DISEASE"
            disease_id, disease_name = line.lstrip("DISEASE").strip().split("  ")
            diseases = [(disease_id, disease_name)]
        elif line.startswith("DRUG"):
            state = "DRUG"
            drug_id, drug_name = line.lstrip("DRUG").strip().split("  ")
            drugs = [(drug_id, drug_name)]
        elif line.startswith("GENE"):
            state = "GENE"
            gene_id, gene_names = line.lstrip("GENE").strip().split("  ")
            short_name, long_name = map(lambda string: string.strip(), gene_names.split(";"))
            long_name = long_name[: long_name.index("[") - 1]
            genes = [(gene_id, short_name, long_name)]
        elif line.startswith("COMPOUND"):
            state = "COMPOUND"
            compound_id, compound_name = line.lstrip("COMPOUND").strip().split("  ")
            compounds = [(compound_id, compound_name)]

    return name, description, classes, diseases, drugs, genes, compounds