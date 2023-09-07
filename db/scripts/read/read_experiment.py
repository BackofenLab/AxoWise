from utils import Reformatter, print_update
import pandas as pd
import os

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


def parse_experiment(
    symbol_ensembl_dict: pd.DataFrame, dir_path: str = os.getenv("_DEFAULT_EXPERIMENT_PATH"), reformat: bool = True
):
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
        5: motif_peaks_TF_no_peaks
        If some of the data is not present, the value will be None.
        """
        dataframes = [None] * 6
        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".tsv":
                df, index = _reformat_experiment_file(
                    df=pd.read_csv(file, sep="\t"), file_name=file_name.split("/")[-1], reformat=reformat
                )
                dataframes[index] = df
            elif file_extention == ".csv":
                df, index = _reformat_experiment_file(
                    df=pd.read_csv(file, sep=","), file_name=file_name.split("/")[-1], reformat=reformat
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
            filtered = df.filter(items=["id", context, context + "-padj", "summit"])
            out = pd.DataFrame(
                {
                    "id": filtered["id"],
                    "Context": context,
                    "Value": filtered[context],
                    "p": filtered[context + "-padj"],
                    "summit": filtered["summit"],
                }
            )
        return out

    def make_context_dataframes(context_list, df, protein):
        value_reformat = []
        for context in context_list:
            value_reformat.append(filter_df_by_context(context=context, df=df, protein=protein))

        values = pd.concat(value_reformat)
        return values

    def post_processing(exp: list[pd.DataFrame]):
        print_update(update_type="Post processing", text="Experiment files", color="red")
        # Filter Dataframes for relevant columns
        de = exp[1].filter(items=["ENSEMBL", "ENTREZID", "SYMBOL", "annot", "TF", "in_ATAC", "mean_count"])

        # Division into TG and TF nodes
        tg_nodes = de[de["TF"] == "no"]
        tg_nodes = tg_nodes.drop(columns=["TF"])
        tg_mean_count = tg_nodes.filter(items=["mean_count", "ENSEMBL"])

        tf_nodes = de[de["TF"] == "yes"]
        tf_nodes = tf_nodes.drop(columns=["TF"])
        tf_mean_count = tf_nodes.filter(items=["mean_count", "ENSEMBL"])

        # Filter for DE Values in specific contexts
        tmp_de = exp[1].filter(items=["ENSEMBL"] + DE_CONTEXT + [c + "-padj" for c in DE_CONTEXT])

        # Create DE DataFrame s.t. context is a column value
        de_values = make_context_dataframes(context_list=DE_CONTEXT, df=tmp_de, protein=True)

        # Filter for relevant values for OR nodes
        relevant_info = exp[0].filter(
            items=[
                "seqnames",
                "summit",
                "annotation",
                "feature",
                "nearest_ENSEMBL",
                "mean_count",
                "nearest_distanceToTSS",
                "nearest_index",
            ]
        )
        relevant_info["id"] = relevant_info["seqnames"] + "_" + relevant_info["summit"].astype(str)
        or_nodes = relevant_info.filter(items=["id", "annotation", "feature"])
        or_mean_count = relevant_info.filter(items=["mean_count", "id"])

        # Filter for Distance to transcription site
        distance = relevant_info.filter(items=["id", "nearest_distanceToTSS", "nearest_ENSEMBL"])
        distance = distance.rename(columns={"nearest_distanceToTSS": "Distance", "nearest_ENSEMBL": "ENSEMBL"}).dropna()

        # Filter for DA Values in specific contexts
        tmp_da = exp[0].filter(items=["seqnames", "summit"] + DA_CONTEXT + [c + "-padj" for c in DA_CONTEXT])
        tmp_da["id"] = tmp_da["seqnames"] + "_" + tmp_da["summit"].astype(str)
        tmp_da = tmp_da.drop(columns=["seqnames"])

        # Create DA DataFrame s.t. context is column value
        da_values = make_context_dataframes(context_list=DA_CONTEXT, df=tmp_da, protein=False)

        tf_tg_corr = exp[2].dropna()

        # Filter for relevant columns
        tmp_or_id = relevant_info.filter(items=["id", "nearest_index"])
        or_tg_corr = exp[3].filter(items=["ENSEMBL", "Correlation", "nearest_index", "p"])
        or_tg_corr = or_tg_corr.merge(tmp_or_id, left_on="nearest_index", right_on="nearest_index", how="left")
        or_tg_corr = or_tg_corr.drop(columns=["nearest_index"]).dropna()

        motif = (
            exp[4]
            .merge(tmp_or_id, left_on="peaks", right_on="nearest_index", how="left")
            .drop(columns=["peaks", "nearest_index"])
        )
        motif = (
            motif.merge(symbol_ensembl_dict, left_on="TF", right_on="SYMBOL", how="left")
            .drop(columns=["TF", "SYMBOL"])
            .dropna()
        )

        motif = (
            motif.merge(right=exp[5], left_on="motif_id", right_on="motif_id")
            .rename(columns={"id": "or_id", "motif_id": "id", "log_adj_pvalue": "p", "concentration": "Concentration"})
            .drop(columns=["TF", "number_of_peaks"])
        )

        return (
            tg_mean_count,
            tf_mean_count,
            de_values,
            or_nodes,
            or_mean_count,
            da_values,
            tf_tg_corr,
            or_tg_corr,
            motif,
            distance,
        )

    # Read and Rename columns of Experiment data
    exp = read_experiment()
    return post_processing(exp=exp)


def _reformat_experiment_file(df: pd.DataFrame, file_name: str, reformat: bool):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    # Filename and function pairs: same index <-> use function for file
    names = [
        "exp_DA",
        "exp_DE_filter",
        "correlation_pval_TF_target",
        "corr_peak_target",
        "TF_motif_peak",
        "motif_peaks_TF_no_peaks",
    ]
    functions = [_reformat_da, _reformat_de, _reformat_tf_tg, _reformat_or_tg, _reformat_motif, _reformat_motif_info]
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
    df = df.filter(items=["nearest_ENSEMBL_target", "ENSEMBL_TF", "korrelationskoeffizient", "p-Wert"])
    df = df.rename(
        columns={"nearest_ENSEMBL_target": "ENSEMBL_TG", "korrelationskoeffizient": "Correlation", "p-Wert": "p"}
    )
    return df


def _reformat_or_tg(df: pd.DataFrame):
    df = df.filter(items=["nearest_ENSEMBL_x", "nearest_index", "correlation_coefficient", "p-value"])
    df = df.rename(columns={"nearest_ENSEMBL_x": "ENSEMBL", "correlation_coefficient": "Correlation", "p-value": "p"})
    return df


def _reformat_motif(df: pd.DataFrame):
    df = df.rename(columns={"motif_consensus": "Consensus"})
    return df


def _reformat_motif_info(df: pd.DataFrame):
    return df
