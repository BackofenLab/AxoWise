from pathlib import Path
import read as rd
from upload import extend_db_from_experiment, first_setup

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


def read_experiment_files():
    data = rd.read(reformat=True, mode=0)
    return data


def read_string_files(complete: pd.DataFrame):
    data = rd.read(complete=complete, mode=1)
    return data


def read_ensembl_files():
    data = rd.read(mode=2)
    return data


def read_functional_files(complete: pd.DataFrame):
    data = rd.read(complete=complete, mode=3)
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

    print(len(de_values))
    print(len(da_values))
    print(len(tf_tg_corr))
    print(len(or_tg_corr))

    complete = read_ensembl_files()

    print(len(complete))

    (gene_gene_scores, genes_annotated) = read_string_files(complete=complete)
    print(len(gene_gene_scores))
    print(len(genes_annotated))

    (
        ft_nodes,
        ft_gene,
        ft_ft_overlap,
    ) = read_functional_files(complete=complete)

    print(len(ft_nodes))
    print(len(ft_gene))
    print(len(ft_ft_overlap))

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
