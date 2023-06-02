from utils import Reformatter
import pandas as pd
import os


def read_experiment(dir_path: str, reformat: bool = True):
    """
    Reads Experiment Files from a given path and returns a list of Pandas dataframes,
    where indices are as follows:
    0: DA values
    1: DE values
    2: TF_target_cor
    3: peak_target_cor
    4: TF_motif_peak
    If some of the data is not present, the value will be None.
    """
    dataframes = [None] * 5
    for file in os.scandir(dir_path):
        df, index = read_file(file_path=file, reformat=reformat)
        if df is not None and index is not None:
            dataframes[index] = df
    return dataframes


def read_file(file_path: os.DirEntry, reformat: bool):
    file_name, file_extention = os.path.splitext(file_path)
    if file_extention == ".tsv":
        df, index = _reformat_file(
            df=pd.read_csv(file_path, sep="\t"), file_name=file_name.split("/")[-1], reformat=reformat
        )
        return df, index
    else:
        return None, None


def _reformat_file(df: pd.DataFrame, file_name: str, reformat: bool):
    # Filename and function pairs: same index <-> use function for file
    names = ["exp_DA", "exp_DE_filter", "TF_target_cor_", "peak_target_cor_", "TF_motif_peak"]
    functions = [_reformat_DA, _reformat_DE, _reformat_TF_TG, _reformat_OR_TG, _reformat_Motif]
    index = names.index(file_name)

    if not reformat:
        return df, index
    return functions[index](df=df), index


def _reformat_DA(df: pd.DataFrame):
    reformatter = Reformatter("open_region_")

    rename_dict = dict([(old, reformatter.run(old, "tf")) for old in df.columns if "open_region_" in old])
    df = df.rename(columns=rename_dict)
    return df


def _reformat_DE(df: pd.DataFrame):
    reformatter = Reformatter("")

    rename_dict = dict([(old, reformatter.run(old, "tf")) for old in df.columns if "wt" in old])
    df = df.rename(columns=rename_dict)
    return df


def _reformat_TF_TG(df: pd.DataFrame):
    return df


def _reformat_OR_TG(df: pd.DataFrame):
    return df


def _reformat_Motif(df: pd.DataFrame):
    return df
