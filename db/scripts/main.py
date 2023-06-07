from pathlib import Path
import read

_DEFAULT_EXPERIMENT_PATH = Path("../source/experiment")
_DEFAULT_STRING_PATH = Path("../source/string")
_DEFAULT_FUNCTIONAL_PATH = Path("../source/functional")


def read_experiment_files(path=_DEFAULT_EXPERIMENT_PATH):
    data = read.parse_experiment(dir_path=path, reformat=True)
    return data

def read_string_files(path=_DEFAULT_STRING_PATH):
    data = read.read_string(dir_path=path)
    return data

def read_functional_files(path=_DEFAULT_FUNCTIONAL_PATH):
    data = read.read_functional(dir_path=path)
    return data

if __name__ == "__main__":
    read_experiment_files()
