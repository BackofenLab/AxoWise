from pathlib import Path
import read as rd
import utils
from upload import first_setup

_DEFAULT_EXPERIMENT_PATH = Path("../source/experiment")
_DEFAULT_STRING_PATH = Path("../source/string")
_DEFAULT_FUNCTIONAL_PATH = Path("../source/functional")
_DEFAULT_CELLTYPE_INFO = {"Name": "Microglia"}
_DEFAULT_STUDY_INFO = {"Source": "in-house"}
_DEFAULT_CREDENTIALS_PATH = Path(__file__).parent / Path("../../config.yml")
_DEV_MAX_REL = 10000
_NEO4J_IMPORT_PATH = "/usr/local/bin/neo4j/import/"
_FUNCTION_TIME_PATH = Path(__file__).parent / Path("./function_times.csv")

_PRODUCTION = False


def read_experiment_files(path=_DEFAULT_EXPERIMENT_PATH):
    data = rd.parse_experiment(dir_path=path, reformat=True)
    return data


def read_string_files(path=_DEFAULT_STRING_PATH):
    data = rd.parse_string(dir_path=path)
    return data


def read_functional_files(protein_gene_dict, path=_DEFAULT_FUNCTIONAL_PATH):
    data = rd.parse_functional(protein_gene_dict=protein_gene_dict, dir_path=path)
    return data


if __name__ == "__main__":
    (
        tg_nodes,
        tf_nodes,
        de_values,
        or_nodes,
        da_values,
        tf_tg_corr,
        or_tg_corr,
        motif,
        distance,
    ) = utils.time_function(read_experiment_files)

    (gene_gene_scores, protein_gene_dict, string_gene_nodes) = utils.time_function(read_string_files)

    (
        ft_nodes,
        ft_gene,
        ft_ft_overlap,
    ) = utils.time_function(read_functional_files, variables={"protein_gene_dict": protein_gene_dict})

    first_setup(
        tg_nodes=tg_nodes,
        tf_nodes=tf_nodes,
        or_nodes=or_nodes,
        da_values=da_values,
        de_values=de_values,
        tf_tg_corr=tf_tg_corr,
        or_tg_corr=or_tg_corr,
        motif=motif,
        distance=distance,
        ft_nodes=ft_nodes,
        ft_gene=ft_gene,
        ft_ft_overlap=ft_ft_overlap,
        gene_gene_scores=gene_gene_scores,
        string_gene_nodes=string_gene_nodes,
    )
