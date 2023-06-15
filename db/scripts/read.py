from utils import Reformatter, time_function, print_update
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
    exp = time_function(read_experiment)

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
    de_values = time_function(
        make_context_dataframes, variables={"context_list": DE_CONTEXT, "df": tmp_de, "protein": True}
    )

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
    da_values = time_function(
        make_context_dataframes, variables={"context_list": DA_CONTEXT, "df": tmp_da, "protein": False}
    )

    tf_tg_corr = exp[2]

    # Filter for relevant columns
    or_tg_corr = exp[3].filter(items=["ENSEMBL", "Correlation", "nearest_index"])

    motif = exp[4]

    return tg_nodes, tf_nodes, de_values, or_nodes, da_values, tf_tg_corr, or_tg_corr, motif, distance


def parse_string(dir_path: str = _DEFAULT_STRING_PATH):
    """
    Reads STRING files and returns a Pandas dataframe
    [ protein.links.v11.5.tsv, protein.info.v11.5.tsv, string_SYMBOL_ENSEMBL.tsv ]
    """

    def read_string():
        dataframes = [None] * 3

        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".tsv":
                df, index = _reformat_string_file(df=pd.read_csv(file, sep="\t"), file_name=file_name.split("/")[-1])
            elif file_extention == ".txt":
                df, index = _reformat_string_file(df=pd.read_csv(file, sep=" "), file_name=file_name.split("/")[-1])
            dataframes[index] = df
        return dataframes

    string = time_function(read_string)

    gene_gene_scores = string[0].merge(string[2], left_on="protein1", right_on="Protein")
    gene_gene_scores = gene_gene_scores.filter(items=["ENSEMBL", "protein2", "Score"])
    gene_gene_scores = gene_gene_scores.rename(columns={"ENSEMBL": "ENSEMBL1"})
    gene_gene_scores = gene_gene_scores.merge(string[2], left_on="protein2", right_on="Protein")
    gene_gene_scores = gene_gene_scores.filter(items=["ENSEMBL1", "ENSEMBL", "Score"])
    gene_gene_scores = gene_gene_scores.rename(columns={"ENSEMBL": "ENSEMBL2"})

    protein_gene_dict = string[2]

    return gene_gene_scores, protein_gene_dict


def parse_functional(protein_gene_dict: pd.DataFrame, dir_path: str = _DEFAULT_FUNCTIONAL_PATH):
    """
    Reads Functional Terms files and returns a Pandas dataframe
    [ functional_terms_overlap.csv, KappaEdges.csv, TermsWithProteins.csv ]
    """

    def read_functional():
        dataframes = [None] * 3

        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".csv":
                df, index = _reformat_functional_term_file(
                    df=pd.read_csv(file, sep=","), file_name=file_name.split("/")[-1]
                )
            dataframes[index] = df
        return dataframes

    functional = time_function(read_functional)

    ft_nodes = functional[2].filter(items=["external_id", "name", "category"])
    ft_nodes = ft_nodes.rename(columns={"external_id": "Term"})

    ft_protein_df_list = []
    for _, i in functional[2].iterrows():
        tmp_df = pd.DataFrame()
        tmp_df["Protein"] = json.loads(i["proteins"].replace("'", '"'))
        tmp_df["Term"] = i["external_id"]
        ft_protein_df_list.append(tmp_df)
    ft_protein = pd.concat(ft_protein_df_list)

    ft_protein = ft_protein.merge(protein_gene_dict, left_on="Protein", right_on="Protein")

    ft_gene = ft_protein.filter(items=["Term", "ENSEMBL"])

    ft_ft_overlap = functional[0]

    return ft_nodes, ft_gene, ft_ft_overlap


def _reformat_experiment_file(df: pd.DataFrame, file_name: str, reformat: bool):
    print_update(update_type="Reformatting", text=file_name, color="orange")
    # print("Reformatting {} ...".format(file_name))

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
    print_update(update_type="Reformatting", text=file_name, color="orange")
    # print("Reformatting {} ...".format(file_name))

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
    df = df.filter(items=["#string_protein_id", "ENSEMBL"])
    df = df.rename(columns={"#string_protein_id": "Protein"})
    return df


def _reformat_functional_term_file(df: pd.DataFrame, file_name: str):
    print_update(update_type="Reformatting", text=file_name, color="orange")
    # print("Reformatting {} ...".format(file_name))

    names = ["functional_terms_overlap", "KappaEdges", "TermsWithProteins"]
    functions = [_reformat_ft_overlap, _reformat_kappa_edges, _reformat_terms_proteins]
    index = names.index(file_name)

    return functions[index](df=df), index


def _reformat_ft_overlap(df: pd.DataFrame):
    df = df.rename(columns={"score": "Score"})
    return df


def _reformat_terms_proteins(df: pd.DataFrame):
    return df


def _reformat_kappa_edges(df: pd.DataFrame):
    return df
