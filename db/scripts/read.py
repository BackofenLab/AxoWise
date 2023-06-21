import os
import pandas as pd
from utils import time_function
from read_experiment import parse_experiment
from read_string import parse_string
from read_ensembl import parse_ensembl
from read_functional import parse_functional


@time_function
def read(dir_path: str = None, reformat: bool = True, mode: int = -1, complete: pd.DataFrame = pd.DataFrame([])):
    if mode == 0:
        # Experiment
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_EXPERIMENT_PATH")
        result = parse_experiment(dir_path=dir_path, reformat=reformat)
    elif mode == 1:
        # STRING
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_STRING_PATH")
        result = parse_string(dir_path=dir_path, complete=complete)
    elif mode == 2:
        # ENSEMBL
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_ENSEMBL_PATH")
        result = parse_ensembl(dir_path=dir_path)
    elif mode == 3:
        # Functional
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_FUNCTIONAL_PATH")
        result = parse_functional(dir_path=dir_path, complete=complete)
    return result
