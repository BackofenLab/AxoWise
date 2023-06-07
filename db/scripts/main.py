from pathlib import Path
import read as rd
from upload import extend_db_from_experiment

_DEFAULT_EXPERIMENT_PATH = Path("../source/experiment")
_DEFAULT_STRING_PATH = Path("../source/string")
_DEFAULT_FUNCTIONAL_PATH = Path("../source/functional")


def read_experiment_files(path=_DEFAULT_EXPERIMENT_PATH):
    data = rd.parse_experiment(dir_path=path, reformat=True)
    return data


def read_string_files(path=_DEFAULT_STRING_PATH):
    data = rd.parse_string(dir_path=path)
    return data


def read_functional_files(path=_DEFAULT_FUNCTIONAL_PATH):
    data = rd.parse_functional(dir_path=path)
    return data

def read_functional_files(path=_DEFAULT_FUNCTIONAL_PATH):
    data = read.read_functional(dir_path=path)
    return data

if __name__ == "__main__":
    tg_nodes, tf_nodes, de_values, or_nodes, da_values, tf_tg_corr, tf_or_corr, motif = read_experiment_files()
    extend_db_from_experiment(tg_nodes=tg_nodes, tf_nodes=tf_nodes, or_nodes=or_nodes, da_values=da_values, de_values=de_values)
