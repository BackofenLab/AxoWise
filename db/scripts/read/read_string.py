from utils import print_update, remove_bidirectionality, retrieve_gene_id_by_symbol
import pandas as pd
import os


def parse_string(complete: pd.DataFrame, proteins: pd.DataFrame, dir_path: str = os.getenv("_DEFAULT_STRING_PATH")):
    """
    Reads STRING files and returns a Pandas dataframe
    [
      protein.links.v11.5.tsv,       protein.info.v11.5.tsv,
      string_SYMBOL_ENSEMBL.tsv,     difference.csv
      9606.protein.links.v11.5.tsv,  9606.protein.info.v11.5.tsv
    ]
    """

    def read_string():
        dataframes = [None] * 6

        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".tsv":
                df, index = _reformat_string_file(df=pd.read_csv(file, sep="\t"), file_name=file_name.split("/")[-1])
            elif file_extention == ".txt":
                df, index = _reformat_string_file(df=pd.read_csv(file, sep=" "), file_name=file_name.split("/")[-1])
            elif file_extention == ".csv":
                df, index = _reformat_string_file(df=pd.read_csv(file, sep=","), file_name=file_name.split("/")[-1])
            dataframes[index] = df
        return dataframes

    def adding_lost_connections(symbol_protein, protein_gene_dict, genes_annotated):
        for i in symbol_protein.iterrows():
            gene_ids = retrieve_gene_id_by_symbol(i[1]["SYMBOL"])
            insert = True
            if len(gene_ids) > 0:
                for g in gene_ids:
                    match_in_dict = protein_gene_dict[protein_gene_dict["ENSEMBL"] == g]
                    if len(match_in_dict) > 0:
                        insert = False
                        row = pd.DataFrame(
                            data=[[match_in_dict["ENSEMBL"].iloc[0], i[1]["Protein"]]], columns=["ENSEMBL", "Protein"]
                        )
                        protein_gene_dict = pd.concat([protein_gene_dict, row])
                if insert:
                    gene_info = list(i[1][1:])
                    gene_info.append(gene_ids[0])
                    row = pd.DataFrame(data=[gene_info], columns=["SYMBOL", "ENTREZID", "annotation", "ENSEMBL"])
                    genes_annotated = pd.concat([genes_annotated, row], ignore_index=True)
                    row = pd.DataFrame(data=[[gene_ids[0], i[1]["Protein"]]], columns=["ENSEMBL", "Protein"])
                    protein_gene_dict = pd.concat([protein_gene_dict, row])
            else:
                symbol = i[1]["SYMBOL"]
                if symbol.startswith("ENSMUSG"):
                    gene_info = list(i[1][1:])
                    gene_info.append(i[1]["SYMBOL"])
                    row = pd.DataFrame(data=[gene_info], columns=["SYMBOL", "ENTREZID", "annotation", "ENSEMBL"])
                    genes_annotated = pd.concat([genes_annotated, row], ignore_index=True)
                    row = pd.DataFrame(data=[[i[1]["SYMBOL"], i[1]["Protein"]]], columns=["ENSEMBL", "Protein"])
                    protein_gene_dict = pd.concat([protein_gene_dict, row])
                else:
                    with open("../source/misc/lost_proteins.csv", "a") as file:
                        file.write(symbol)
                        file.write("\n")
        return protein_gene_dict, genes_annotated

    def post_processing(string: list[pd.DataFrame]):
        print_update(update_type="Post processing", text="STRING files", color="red")
        genes_annotated = string[1].merge(complete, left_on="Protein", right_on="Protein", how="left")
        genes_annotated = genes_annotated.filter(items=["ENSEMBL", "SYMBOL", "annotation", "ENTREZID"])

        proteins_annotated = (
            proteins.merge(right=string[1], left_on="Protein", right_on="Protein", how="left")
            .drop_duplicates(subset=["Protein"], keep="first")
            .drop(columns=["ENSEMBL"])
        )
        proteins_annotated["Protein"] = proteins_annotated["Protein"].apply(lambda x: x.removeprefix("10090."))

        proteins_annotated = proteins_annotated.rename(columns={"Protein": "ENSEMBL"})

        # Drop duplicate annotations, keep first entry
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
        # genes_annotated.SYMBOL.fillna(genes_annotated.ENSEMBL, inplace=True)

        protein_gene_dict = complete.filter(items=["ENSEMBL", "Protein"])

        symbol_protein = string[3].merge(string[1], left_on="Protein", right_on="Protein")

        protein_gene_dict, genes_annotated = adding_lost_connections(
            symbol_protein=symbol_protein, protein_gene_dict=protein_gene_dict, genes_annotated=genes_annotated
        )

        protein_protein_scores = string[0].merge(proteins, left_on="protein1", right_on="Protein")
        protein_protein_scores = protein_protein_scores.filter(items=["Protein", "protein2", "Score"])
        protein_protein_scores = protein_protein_scores.rename(columns={"Protein": "Protein1"})

        protein_protein_scores = protein_protein_scores.merge(proteins, left_on="protein2", right_on="Protein")
        protein_protein_scores = protein_protein_scores.filter(items=["Protein1", "Protein", "Score"])
        protein_protein_scores = protein_protein_scores.rename(columns={"Protein": "Protein2"})

        protein_protein_scores = remove_bidirectionality(
            df=protein_protein_scores, columns=("Protein1", "Protein2"), additional=["Score"]
        )

        protein_protein_scores = protein_protein_scores.drop_duplicates()
        protein_protein_scores["Protein1"] = protein_protein_scores["Protein1"].apply(
            lambda x: x.removeprefix("10090.")
        )
        protein_protein_scores["Protein2"] = protein_protein_scores["Protein2"].apply(
            lambda x: x.removeprefix("10090.")
        )
        protein_protein_scores.rename(columns={"Protein1": "ENSEMBL1", "Protein2": "ENSEMBL2"})

        gene_gene_scores = string[0].merge(protein_gene_dict, left_on="protein1", right_on="Protein")
        gene_gene_scores = gene_gene_scores.filter(items=["ENSEMBL", "protein2", "Score"])
        gene_gene_scores = gene_gene_scores.rename(columns={"ENSEMBL": "ENSEMBL1"})

        gene_gene_scores = gene_gene_scores.merge(protein_gene_dict, left_on="protein2", right_on="Protein")
        gene_gene_scores = gene_gene_scores.filter(items=["ENSEMBL1", "ENSEMBL", "Score"])
        gene_gene_scores = gene_gene_scores.rename(columns={"ENSEMBL": "ENSEMBL2"})

        gene_gene_scores = remove_bidirectionality(
            df=gene_gene_scores, columns=("ENSEMBL1", "ENSEMBL2"), additional=["Score"]
        )

        gene_gene_scores = gene_gene_scores.drop_duplicates(keep="first")
        return gene_gene_scores, genes_annotated, proteins_annotated, protein_protein_scores

    string = read_string()
    return post_processing(string=string)


def _reformat_string_file(df: pd.DataFrame, file_name: str):
    print_update(update_type="Reformatting", text=file_name, color="orange")

    names = [
        "protein.links.v11.5",
        "protein.info.v11.5",
        "string_SYMBOL_ENSEMBL",
        "difference",
        "9606.protein.links.v11.5",
        "9606.protein.info.v11.5",
    ]
    functions = [
        _reformat_string_links,
        _reformat_string_info,
        _reformat_protein_gene_dict,
        _reformat_difference,
        _reformat_string_links_human,
        _reformat_string_info_human,
    ]
    index = names.index(file_name)

    return functions[index](df=df), index


def _reformat_string_links(df: pd.DataFrame):
    df = df.rename(columns={"combined_score": "Score"})
    return df


def _reformat_string_links_human(df: pd.DataFrame):
    df = df.rename(columns={"combined_score": "Score"})
    return df


def _reformat_string_info(df: pd.DataFrame):
    df = df.rename(columns={"preferred_name": "SYMBOL", "#string_protein_id": "Protein"})
    return df


def _reformat_string_info_human(df: pd.DataFrame):
    df = df.rename(columns={"preferred_name": "SYMBOL", "#string_protein_id": "Protein"})
    return df


def _reformat_protein_gene_dict(df: pd.DataFrame):
    df = df.filter(items=["#string_protein_id", "ENSEMBL", "annotation", "ENTREZID", "preferred_name"])
    df = df.rename(columns={"#string_protein_id": "Protein", "annotation": "annot", "preferred_name": "SYMBOL"})
    return df


def _reformat_difference(df: pd.DataFrame):
    return df
