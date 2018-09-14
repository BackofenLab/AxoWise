
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

    def last_index(string, substring):
        return len(string) - len(substring) - string[::-1].index(substring)
        
    def parse_disease_line(line):
        disease_id, disease_name = line.strip().split("  ")
        return disease_id, disease_name

    def parse_drug_line(line):
        drug_id, drug_name = line.strip().split("  ")
        return drug_id, drug_name

    def parse_gene_line(line):
        gene_id, gene_names = line.strip().split("  ")
        if ";" in gene_names: # Mutliple names
            names = list(map(lambda string: string.strip(), gene_names.split(";")))
            short_name, long_name = names[0], "; ".join(names[1:])
            if "[" in long_name:
                long_name = long_name[: long_name.index("[") - 1]
        else: # One name
            short_name = ""
            long_name = gene_names
            if "[" in long_name:
                long_name = long_name[: long_name.index("[") - 1]
        return gene_id, short_name, long_name

    def parse_compound_line(line):
        line = line.strip()
        if "  " in line:
            compound_id, compound_name = line.split("  ")
        else:
            compound_id = line
            compound_name = ""
        return compound_id, compound_name

    state = None
    for line in re.split("\n+", pathway):
        if not line.startswith(" "):
            state = None

        # List continuation
        if state == "DISEASE":
            diseases.append(parse_disease_line(line))
        elif state == "DRUG":
            drugs.append(parse_drug_line(line))
        elif state == "GENE":
            genes.append(parse_gene_line(line))
        elif state == "COMPOUND":
            compounds.append(parse_compound_line(line))

        # One-line entries
        elif line.startswith("NAME"):
            name = line.lstrip("NAME").lstrip()
            name = name[ : last_index(name, " - ")]
            assert name.strip() != ""
        elif line.startswith("DESCRIPTION"):
            description = line.lstrip("DESCRIPTION").lstrip()
        elif line.startswith("CLASS"):
            classes_str = line.lstrip("CLASS")
            classes = list(map(lambda string: string.strip(), classes_str.split(";")))

        # List start
        elif line.startswith("DISEASE"):
            state = "DISEASE"
            diseases = [parse_disease_line(line.lstrip("DISEASE"))]
        elif line.startswith("DRUG"):
            state = "DRUG"
            drugs = [parse_drug_line(line.lstrip("DRUG"))]
        elif line.startswith("GENE"):
            state = "GENE"
            genes = [parse_gene_line(line.lstrip("GENE"))]
        elif line.startswith("COMPOUND"):
            state = "COMPOUND"
            compounds = [parse_compound_line(line.lstrip("COMPOUND"))]

    return name, description, classes, diseases, drugs, genes, compounds