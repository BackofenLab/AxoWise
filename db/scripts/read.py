from utils import Reformatter
import pandas as pd
import os
import json
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
    [ tg_nodes, tf_nodes, de_values, or_nodes, da_values, tf_tg_corr, tf_or_corr ]
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
                df, index = _reformat_experiment_file(
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
            filtered = df.filter(items=["nearest_index", context, context + "-padj"])
            out = pd.DataFrame(
                {
                    "nearest_index": filtered["nearest_index"],
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
        items=[
            "seqnames",
            "summit",
            "strand",
            "annotation",
            "feature",
            "in_RNAseq",
            "nearest_index",
            "nearest_distanceToTSS",
            "nearest_ENSEMBL",
            "mean_count",
        ]
    )

    # Filter for Distance to transcription site
    distance = exp[0].filter(items=["nearest_index", "nearest_distanceToTSS", "nearest_ENSEMBL"])
    distance = distance.rename(columns={"nearest_distanceToTSS": "Distance"})

    # Filter for DA Values in specific contexts
    tmp_da = exp[0].filter(items=["nearest_index", "mean_count"] + DA_CONTEXT + [c + "-padj" for c in DA_CONTEXT])

    # Create DA DataFrame s.t. context is column value
    da_values = make_context_dataframes(DA_CONTEXT, tmp_da, False)

    tf_tg_corr = exp[2]

    # Filter for relevant columns
    tg_or_corr = exp[3].filter(items=["ENSEMBL", "Correlation", "nearest_index"])

    motif = exp[4]

    return [tg_nodes, tf_nodes, de_values, or_nodes, da_values, tf_tg_corr, tg_or_corr, motif, distance]


def parse_string(dir_path: str = _DEFAULT_STRING_PATH):
    """
    Reads STRING files and returns a Pandas dataframe
    [ protein.links.v11.5.tsv, protein.info.v11.5.tsv, string_SYMBOL_ENSEMBL.tsv ]
    """

    string = [None] * 3

    for file in os.scandir(dir_path):
        file_name, file_extention = os.path.splitext(file)
        if file_extention == ".tsv":
            df, index = _reformat_string_file(df=pd.read_csv(file, sep="\t"), file_name=file_name.split("/")[-1])
        string[index] = df
    return string


def parse_functional(dir_path: str = _DEFAULT_FUNCTIONAL_PATH):
    """
    Reads Functional Terms files and returns a Pandas dataframe
    [ functional_terms_overlap.csv, KappaEdges.csv, TermsWithProteins.csv ]
    """

    functional = [None] * 3

    for file in os.scandir(dir_path):
        file_name, file_extention = os.path.splitext(file)
        if file_extention == ".csv":
            df, index = _reformat_functional_term_file(
                df=pd.read_csv(file, sep=","), file_name=file_name.split("/")[-1]
            )
        functional[index] = df

    return functional


def _reformat_experiment_file(df: pd.DataFrame, file_name: str, reformat: bool):
    # Filename and function pairs: same index <-> use function for file
    names = ["exp_DA", "exp_DE_filter", "TF_target_cor_", "peak_target_cor_", "TF_motif_peak"]
    functions = [_reformat_da, _reformat_de, _reformat_tf_tg, _reformat_or_tg, _reformat_motif]
    index = names.index(file_name)

    if not reformat:
        return df, index
    return functions[index](df=df), index


def _reformat_da(df: pd.DataFrame):
    reformatter = Reformatter("open_region_")

    rename_dict = dict([(old, reformatter.run(old, "tf")) for old in df.columns if "open_region_" in old])
    df = df.rename(columns=rename_dict)
    return df


def _reformat_de(df: pd.DataFrame):
    reformatter = Reformatter("")

    rename_dict = dict([(old, reformatter.run(old, "tf")) for old in df.columns if "wt" in old])
    df = df.rename(columns=rename_dict)
    return df


def _reformat_tf_tg(df: pd.DataFrame):
    df = df.rename(columns={"nearest_ENSEMBL": "ENSEMBL", "TF_target_cor": "Correlation"})
    return df


def _reformat_or_tg(df: pd.DataFrame):
    df = df.rename(columns={"nearest_ENSEMBL": "ENSEMBL", "peak_target_cor": "Correlation"})
    return df


def _reformat_motif(df: pd.DataFrame):
    df = df.rename(columns={"motif_consensus": "Motif"})
    return df


def _reformat_string_file(df: pd.DataFrame, file_name: str):
    names = ["protein.links.v11.5", "protein.info.v11.5", "string_SYMBOL_ENSEMBL"]
    functions = [_reformat_string_links, _reformat_string_info, _reformat_protein_gene_dict]
    index = names.index(file_name)

    return functions[index](df=df), index


def _reformat_string_links(df: pd.DataFrame):
    df = df.rename(columns={"combined_score": "Score"})
    return df


def _reformat_string_info(df: pd.DataFrame):
    df = df.rename(columns={"preferred_name": "SYMBOL", "string_protein_id": "ENSEMBL"})
    return df


def _reformat_protein_gene_dict(df: pd.DataFrame):
    # TODO
    return df


def _reformat_functional_term_file(df: pd.DataFrame, file_name: str):
    names = ["functional_terms_overlap", "KappaEdges", "TermsWithProteins"]
    functions = [_reformat_ft_overlap, _reformat_kappa_edges, _reformat_terms_proteins]
    index = names.index(file_name)

    return functions[index](df=df), index


def _reformat_ft_overlap(df: pd.DataFrame):
    return df


def _reformat_terms_proteins(df: pd.DataFrame):
    df_list = []
    for _, i in df.iterrows():
        tmp_df = pd.DataFrame()
        tmp_df["ENSEMBL"] = json.loads(i["proteins"].replace("'", '"'))
        tmp_df["Term"] = i["external_id"]
        df_list.append(tmp_df)
    new_df = pd.concat(df_list)
    return new_df


def _reformat_kappa_edges(df: pd.DataFrame):
    return df
