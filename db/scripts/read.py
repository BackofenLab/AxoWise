from utils import Reformatter
import pandas as pd
import os
from main import _DEFAULT_EXPERIMENT_PATH, _DEFAULT_FUNCTIONAL_PATH, _DEFAULT_STRING_PATH

DE_CONTEXT = [
    "6h-0h",
    "24h-0h",
    "336h-0h",
    "RC12h-0h",
    "RC12h-6h",
]
DA_CONTEXT = [
    "12h-0h",
    "24h-0h",
    "336h-0h",
    "RC12h-0h",
    "RC12h-12h",
]


def parse_experiment(dir_path: str = _DEFAULT_EXPERIMENT_PATH, reformat: bool = True):
    """
    Parses experiment files and returns list of Pandas DataFrames s.t.
    [tg_nodes, tf_nodes, de_values, or_nodes, da_values, tf_tg_corr, tf_or_corr]
    """

    def read_experiment():
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
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".tsv":
                df, index = _reformat_file(
                    df=pd.read_csv(file, sep="\t"), file_name=file_name.split("/")[-1], reformat=reformat
                )
                dataframes[index] = df
        return dataframes

    def filter_df_by_context(context: str, df: pd.DataFrame, protein: bool):
        if protein:
            filtered = df.filter(items=["ENSEMBL", context, context + "-padj"])
            out = pd.DataFrame(
                {
                    "ENSEMBL": filtered["ENSEMBL"],
                    "Context": context,
                    "Value": filtered[context],
                    "p": filtered[context + "-padj"],
                }
            )
        else:
            filtered = df.filter(items=["SYMBOL", context, context + "-padj"])
            out = pd.DataFrame(
                {
                    "SYMBOL": filtered["SYMBOL"],
                    "Context": context,
                    "Value": filtered[context],
                    "p": filtered[context + "-padj"],
                }
            )
        return out

    def make_context_dataframes(context_list, df, protein):
        value_reformat = []
        for context in context_list:
            value_reformat.append(filter_df_by_context(context=context, df=df, protein=protein))

        values = pd.concat(value_reformat)
        return values

    # Read and Rename columns of Experiment data
    exp = read_experiment()

    # Filter Dataframes for relevant columns
    de = exp[1].filter(items=["ENSEMBL", "ENTREZID", "SYMBOL", "annot", "TF", "in_ATAC", "mean_count"])

    # Division into TG and TF nodes
    tg_nodes = de[de["TF"] == "no"]
    tg_nodes = tg_nodes.drop(columns=["TF"])

    tf_nodes = de[de["TF"] == "yes"]
    tf_nodes = tf_nodes.drop(columns=["TF"])

    # Filter for DE Values in specific contexts
    tmp_de = exp[1].filter(items=["ENSEMBL"] + DE_CONTEXT + [c + "-padj" for c in DE_CONTEXT])

    # Create DE DataFrame s.t. context is a column value
    de_values = make_context_dataframes(DE_CONTEXT, tmp_de, True)

    # Filter for relevant values for OR nodes
    or_nodes = exp[0].filter(
        items=["SYMBOL", "seqnames", "summit", "strand", "annotation", "feature", "in_RNAseq", "nearest_index"]
    )

    # Filter for DA Values in specific contexts
    tmp_da = exp[0].filter(items=["SYMBOL", "mean_count"] + DA_CONTEXT + [c + "-padj" for c in DA_CONTEXT])

    # Create DA DataFrame s.t. context is column value
    da_values = make_context_dataframes(DA_CONTEXT, tmp_da, False)

    tf_tg_corr = exp[2]

    # Filter for relevant columns
    tf_or_corr = exp[3].filter(items=["ENSEMBL", "Correlation", "SYMBOL"])

    motif = exp[4]

    return [tg_nodes, tf_nodes, de_values, or_nodes, da_values, tf_tg_corr, tf_or_corr, motif]


def parse_string(dir_path: str = _DEFAULT_STRING_PATH):
    """
    Reads STRING files and returns a Pandas dataframe
    """
    for file in os.scandir(dir_path):
        df = pd.read_csv(file, sep=" ")
    # TODO: for more files in string dir, extend...
    return df


def parse_functional(dir_path: str = _DEFAULT_FUNCTIONAL_PATH):
    for file in os.scandir(dir_path):
        df = pd.read_csv(file, sep=",")
    # TODO: for more files in functional dir, extend...
    return df


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
    df = df.rename(columns={"nearest_ENSEMBL": "ENSEMBL", "TF_target_cor": "Correlation"})
    return df


def _reformat_OR_TG(df: pd.DataFrame):
    df = df.rename(columns={"nearest_ENSEMBL": "ENSEMBL", "peak_target_cor": "Correlation"})
    return df


def _reformat_Motif(df: pd.DataFrame):
    return df
