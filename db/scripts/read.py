from utils import Reformatter, time_function, print_update
import pandas as pd
import os
import json

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


@time_function
def parse_experiment(dir_path: str = os.getenv("_DEFAULT_EXPERIMENT_PATH"), reformat: bool = True):
    """
    Parses experiment files and returns list of Pandas DataFrames s.t.
    [ tg_nodes, tf_nodes, de_values, or_nodes, da_values, tf_tg_corr, tf_or_corr ]
    """

    @time_function
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

    @time_function
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

    @time_function
    def make_context_dataframes(context_list, df, protein):
        value_reformat = []
        for context in context_list:
            value_reformat.append(filter_df_by_context(context=context, df=df, protein=protein))

        values = pd.concat(value_reformat)
        return values

    @time_function
    def post_processing(exp: list[pd.DataFrame]):
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
        de_values = make_context_dataframes(context_list=DE_CONTEXT, df=tmp_de, protein=True)

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
        da_values = make_context_dataframes(context_list=DA_CONTEXT, df=tmp_da, protein=False)

        tf_tg_corr = exp[2]

        # Filter for relevant columns
        or_tg_corr = exp[3].filter(items=["ENSEMBL", "Correlation", "nearest_index"])

        motif = exp[4]

        return tg_nodes, tf_nodes, de_values, or_nodes, da_values, tf_tg_corr, or_tg_corr, motif, distance

    # Read and Rename columns of Experiment data
    exp = read_experiment()
    return post_processing(exp=exp)


@time_function
def parse_string(temporary_protein_gene_dict: pd.DataFrame, dir_path: str = os.getenv("_DEFAULT_STRING_PATH")):
    """
    Reads STRING files and returns a Pandas dataframe
    [ protein.links.v11.5.tsv, protein.info.v11.5.tsv, string_SYMBOL_ENSEMBL.tsv ]
    """

    @time_function
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

    @time_function
    def post_processing(string: list[pd.DataFrame]):
        string_gene_nodes = string[1].merge(temporary_protein_gene_dict, left_on="Protein", right_on="Protein")

        string_gene_nodes = string_gene_nodes.filter(items=["ENSEMBL", "SYMBOL", "annotation"])
        string_gene_nodes = string_gene_nodes.dropna(subset=["ENSEMBL"])

        protein_gene_dict = string[2]
        protein_gene_dict = protein_gene_dict.filter(items=["ENSEMBL", "Protein"])
        protein_gene_dict = protein_gene_dict.dropna()
        protein_gene_dict = pd.concat([temporary_protein_gene_dict, protein_gene_dict]).drop_duplicates(
            ignore_index=True
        )

        gene_gene_scores = string[0].merge(protein_gene_dict, left_on="protein1", right_on="Protein")
        gene_gene_scores = gene_gene_scores.filter(items=["ENSEMBL", "protein2", "Score"])
        gene_gene_scores = gene_gene_scores.rename(columns={"ENSEMBL": "ENSEMBL1"})
        gene_gene_scores = gene_gene_scores.merge(protein_gene_dict, left_on="protein2", right_on="Protein")
        gene_gene_scores = gene_gene_scores.filter(items=["ENSEMBL1", "ENSEMBL", "Score"])
        gene_gene_scores = gene_gene_scores.rename(columns={"ENSEMBL": "ENSEMBL2"})

        return gene_gene_scores, protein_gene_dict, string_gene_nodes

    string = read_string()
    return post_processing(string=string)


@time_function
def parse_functional(protein_gene_dict: pd.DataFrame, dir_path: str = os.getenv("_DEFAULT_FUNCTIONAL_PATH")):
    """
    Reads Functional Terms files and returns a Pandas dataframe
    [ functional_terms_overlap.csv, TermsWithProteins.csv ]
    """

    @time_function
    def read_functional():
        dataframes = [None] * 2

        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".csv":
                df, index = _reformat_functional_term_file(
                    df=pd.read_csv(file, sep=","), file_name=file_name.split("/")[-1]
                )
            dataframes[index] = df
        return dataframes

    @time_function
    def post_processing(functional: list[pd.DataFrame]):
        ft_nodes = functional[1].filter(items=["external_id", "name", "category"])
        ft_nodes = ft_nodes.rename(columns={"external_id": "Term"})

        ft_protein_df_list = []
        for _, i in functional[1].iterrows():
            tmp_df = pd.DataFrame()
            tmp_df["Protein"] = json.loads(i["proteins"].replace("'", '"'))
            tmp_df["Term"] = i["external_id"]
            ft_protein_df_list.append(tmp_df)
        ft_protein = pd.concat(ft_protein_df_list)

        ft_protein = ft_protein.merge(protein_gene_dict, left_on="Protein", right_on="Protein")

        ft_gene = ft_protein.filter(items=["Term", "ENSEMBL"])

        ft_ft_overlap = functional[0]

        return ft_nodes, ft_gene, ft_ft_overlap

    functional = read_functional()
    return post_processing(functional=functional)


@time_function
def parse_ensembl(dir_path: str = os.getenv("_DEFAULT_ENSEMBL_PATH")):
    """
    Reads ENSEMBL files and returns a Pandas dataframe
    [ Mus_musculus.GRCm39.109.ena.tsv, Mus_musculus.GRCm39.109.entrez.tsv, Mus_musculus.GRCm39.109.refseq.tsv, Mus_musculus.GRCm39.109.uniprot.tsv ]
    """

    @time_function
    def read_ensembl():
        dataframes = [None] * 4

        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".tsv":
                df, index = _reformat_ensembl_term_file(
                    df=pd.read_csv(file, sep="\t"), file_name=file_name.split("/")[-1]
                )
            dataframes[index] = df
        return dataframes

    @time_function
    def post_processing(ensembl: list[pd.DataFrame]):
        complete = pd.concat(ensembl)
        complete = complete.drop_duplicates(ignore_index=True)
        complete_genes = complete.filter(items=["ENSEMBL"]).drop_duplicates(ignore_index=True)
        temporary_protein_gene_dict = complete[~complete["Protein"].isin(["10090.-"])]
        temporary_protein_gene_dict = temporary_protein_gene_dict.dropna()
        return complete_genes, temporary_protein_gene_dict

    ensembl = read_ensembl()
    return post_processing(ensembl=ensembl)


@time_function
def _reformat_experiment_file(df: pd.DataFrame, file_name: str, reformat: bool):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    # Filename and function pairs: same index <-> use function for file
    names = ["exp_DA", "exp_DE_filter", "TF_target_cor_", "peak_target_cor_", "TF_motif_peak"]
    functions = [_reformat_da, _reformat_de, _reformat_tf_tg, _reformat_or_tg, _reformat_motif]
    index = names.index(file_name)

    if not reformat:
        return df, index
    return functions[index](df=df), index


@time_function
def _reformat_da(df: pd.DataFrame):
    reformatter = Reformatter("open_region_")

    rename_dict = dict([(old, reformatter.run(old, "tf")) for old in df.columns if "open_region_" in old])
    df = df.rename(columns=rename_dict)
    return df


@time_function
def _reformat_de(df: pd.DataFrame):
    reformatter = Reformatter("")

    rename_dict = dict([(old, reformatter.run(old, "tf")) for old in df.columns if "wt" in old])
    df = df.rename(columns=rename_dict)
    return df


@time_function
def _reformat_tf_tg(df: pd.DataFrame):
    df = df.rename(columns={"nearest_ENSEMBL": "ENSEMBL", "TF_target_cor": "Correlation"})
    return df


@time_function
def _reformat_or_tg(df: pd.DataFrame):
    df = df.rename(columns={"nearest_ENSEMBL": "ENSEMBL", "peak_target_cor": "Correlation"})
    return df


@time_function
def _reformat_motif(df: pd.DataFrame):
    df = df.rename(columns={"motif_consensus": "Motif"})
    return df


@time_function
def _reformat_string_file(df: pd.DataFrame, file_name: str):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    names = ["protein.links.v11.5", "protein.info.v11.5", "string_SYMBOL_ENSEMBL"]
    functions = [_reformat_string_links, _reformat_string_info, _reformat_protein_gene_dict]
    index = names.index(file_name)

    return functions[index](df=df), index


@time_function
def _reformat_string_links(df: pd.DataFrame):
    df = df.rename(columns={"combined_score": "Score"})
    return df


@time_function
def _reformat_string_info(df: pd.DataFrame):
    df = df.rename(columns={"preferred_name": "SYMBOL", "#string_protein_id": "Protein"})
    return df


@time_function
def _reformat_protein_gene_dict(df: pd.DataFrame):
    df = df.filter(items=["#string_protein_id", "ENSEMBL", "annotation", "ENTREZID", "preferred_name"])
    df = df.rename(columns={"#string_protein_id": "Protein", "annotation": "annot", "preferred_name": "SYMBOL"})
    return df


@time_function
def _reformat_functional_term_file(df: pd.DataFrame, file_name: str):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    names = ["functional_terms_overlap", "TermsWithProteins"]
    functions = [_reformat_ft_overlap, _reformat_terms_proteins]
    index = names.index(file_name)

    return functions[index](df=df), index


@time_function
def _reformat_ft_overlap(df: pd.DataFrame):
    df = df.rename(columns={"score": "Score"})
    return df


@time_function
def _reformat_terms_proteins(df: pd.DataFrame):
    return df


@time_function
def _reformat_ensembl_term_file(df: pd.DataFrame, file_name: str):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    names = [
        "Mus_musculus.GRCm39.109.ena",
        "Mus_musculus.GRCm39.109.entrez",
        "Mus_musculus.GRCm39.109.refseq",
        "Mus_musculus.GRCm39.109.uniprot",
    ]
    functions = [_reformat_ena, _reformat_entrez, _reformat_refseq, _reformat_uniprot]
    index = names.index(file_name)

    return functions[index](df=df), index


@time_function
def _reformat_ena(df: pd.DataFrame):
    # TODO
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "10090." + df["Protein"]
    return df


@time_function
def _reformat_entrez(df: pd.DataFrame):
    # TODO
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "10090." + df["Protein"]
    return df


@time_function
def _reformat_refseq(df: pd.DataFrame):
    # TODO
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "10090." + df["Protein"]
    return df


@time_function
def _reformat_uniprot(df: pd.DataFrame):
    # TODO
    df = df.filter(items=["gene_stable_id", "protein_stable_id"])
    df = df.rename(columns={"gene_stable_id": "ENSEMBL", "protein_stable_id": "Protein"})
    df["Protein"] = "10090." + df["Protein"]
    return df
