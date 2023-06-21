from utils import time_function, print_update
import pandas as pd
import os


@time_function
def parse_string(complete: pd.DataFrame, dir_path: str = os.getenv("_DEFAULT_STRING_PATH")):
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
        genes_annotated = string[1].merge(complete, left_on="Protein", right_on="Protein", how="left")
        genes_annotated = genes_annotated.filter(items=["ENSEMBL", "SYMBOL", "annotation", "ENTREZID"])

        # Drop duplicate annotations, keep last entry
        genes_annotated = genes_annotated.drop_duplicates(subset=["ENSEMBL"], keep="first", ignore_index=True)
        genes_annotated = genes_annotated.dropna(subset=["ENSEMBL"])

        complete_unannot = complete.filter(items=["ENSEMBL", "ENTREZID"])
        complete_unannot = complete.drop_duplicates(subset=["ENSEMBL"], keep="first", ignore_index=True)

        # Concat unannot and annotated, where there is
        genes_annotated = pd.concat(
            [
                complete_unannot[
                    ~complete_unannot["ENSEMBL"].isin(
                        set(complete_unannot["ENSEMBL"]).intersection(genes_annotated["ENSEMBL"])
                    )
                ],
                genes_annotated,
            ],
            ignore_index=True,
        ).drop(columns=["Protein"])

        protein_gene_dict = complete.filter(items=["ENSEMBL", "Protein"])
        protein_gene_dict = protein_gene_dict.drop_duplicates(ignore_index=True)

        gene_gene_scores = string[0].merge(protein_gene_dict, left_on="protein1", right_on="Protein")
        gene_gene_scores = gene_gene_scores.filter(items=["ENSEMBL", "protein2", "Score"])
        gene_gene_scores = gene_gene_scores.rename(columns={"ENSEMBL": "ENSEMBL1"})
        gene_gene_scores = gene_gene_scores.merge(protein_gene_dict, left_on="protein2", right_on="Protein")
        gene_gene_scores = gene_gene_scores.filter(items=["ENSEMBL1", "ENSEMBL", "Score"])
        gene_gene_scores = gene_gene_scores.rename(columns={"ENSEMBL": "ENSEMBL2"})

        return gene_gene_scores, genes_annotated

    string = read_string()
    return post_processing(string=string)


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
