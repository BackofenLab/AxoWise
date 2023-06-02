from pathlib import Path
import read

_DEFAULT_EXPERIMENT_PATH = Path("../source/experiment")


def read_experiment_files(path_to_experiment=_DEFAULT_EXPERIMENT_PATH):
    data = read.read_experiment(dir_path=path_to_experiment, reformat=True)
    return data


if __name__ == "__main__":
    read_experiment_files()
