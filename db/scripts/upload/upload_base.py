from utils import time_function, print_update, save_df_to_csv, get_values_reformat
from .upload_functions import create_nodes, create_relationship, update_nodes
import pandas as pd
from neo4j import Driver


@time_function
def create_gene_nodes(nodes: pd.DataFrame, driver: Driver):
    """
    Creates Gene Nodes based on ENSEMBL Data (with annotations from STRING)

    Variables:
        nodes -> Dataframe with Node info (ENSEMBL, ENTREZID, SYMBOL, annotation)
    """
    print_update(update_type="Node Creation", text="Genes from ENSEMBL", color="blue")
    save_df_to_csv(file_name="genes.csv", df=nodes, override_prod=True)
    create_nodes(
        source_file="genes.csv",
        type_="TG",
        id="ENSEMBL",
        values=["ENTREZID", "ENSEMBL", "SYMBOL", "annotation"],
        reformat_values=[("ENTREZID", "toInteger")],
        driver=driver,
        merge=False,
    )


@time_function
def create_tf_label(tf: pd.DataFrame, driver: Driver):
    print_update(update_type="Node Update", text="Transcription Factor", color="orange")

    save_df_to_csv(file_name="tf.csv", df=tf, override_prod=True)
    update_nodes(
        source_file="tf.csv",
        type_="TG",
        id="ENSEMBL",
        values=[],
        reformat_values=[],
        additional_label="TF",
        driver=driver,
    )


@time_function
def create_or_nodes(nodes: pd.DataFrame, driver: Driver):
    """
    Creates Open Region Nodes with <Chomosome>_<summit> as id
    """
    print_update(update_type="Node Creation", text="Open Region", color="blue")

    save_df_to_csv(file_name="or.csv", df=nodes, override_prod=True)
    create_nodes(
        source_file="or.csv",
        type_="OR",
        id="id",
        values=["id", "annotation", "feature"],
        reformat_values=[],
        merge=False,
        driver=driver,
    )


@time_function
def create_motif_edges(motif: pd.DataFrame, driver: Driver):
    """
    Creates MOTIF edges between TF and OR
    """
    print_update(update_type="Edge Creation", text="MOTIF", color="cyan")

    values, reformat = get_values_reformat(df=motif, match=["ENSEMBL", "id"])
    save_df_to_csv(file_name="motif.csv", df=motif)
    create_relationship(
        source_file="motif.csv",
        type_="MOTIF",
        between=(("ENSEMBL", "ENSEMBL"), ("id", "id")),
        node_types=("TF", "OR"),
        values=values,
        reformat_values=reformat,
        merge=False,
        driver=driver,
    )


@time_function
def create_distance_edges(distance: pd.DataFrame, driver: Driver):
    """
    Creates DISTANCE edges between OR and TG
    """
    print_update(update_type="Edge Creation", text="DISTANCE", color="cyan")

    values, reformat = get_values_reformat(df=distance, match=["id", "ENSEMBL"])
    save_df_to_csv(file_name="distance.csv", df=distance)
    create_relationship(
        source_file="distance.csv",
        type_="DISTANCE",
        between=(("id", "id"), ("ENSEMBL", "ENSEMBL")),
        node_types=("OR", "TG"),
        values=values,
        reformat_values=reformat,
        merge=False,
        driver=driver,
    )


@time_function
def create_string(gene_gene_scores: pd.DataFrame, driver: Driver):
    """
    Creates STRING edges between TG and TG with STRING Association Score
    """
    print_update(update_type="Edge Creation", text="STRING", color="cyan")

    values, reformat = get_values_reformat(df=gene_gene_scores, match=["ENSEMBL1", "ENSEMBL2"])
    save_df_to_csv(file_name="string_scores.csv", df=gene_gene_scores)
    create_relationship(
        source_file="string_scores.csv",
        type_="STRING",
        between=(("ENSEMBL", "ENSEMBL1"), ("ENSEMBL", "ENSEMBL2")),
        node_types=("TG", "TG"),
        values=values,
        reformat_values=reformat,
        merge=False,
        driver=driver,
    )

    return


@time_function
def create_functional(
    ft_nodes: pd.DataFrame,
    ft_ft_overlap: pd.DataFrame,
    ft_gene: pd.DataFrame,
    driver: Driver,
):
    """
    Creates Functional Term nodes, OVERLAP egdes between FT and FT, and LINK edges between TG and FT
    """
    # print_update(update_type="Node Creation", text="Functional Term", color="blue")
    #
    # TODO: Change "Terms" to "FT" and "external_id" to "Term"
    # save_df_to_csv(file_name="ft_nodes.csv", df=ft_nodes, override_prod=True)
    # create_nodes(
    #     source_file="ft_nodes.csv",
    #     type_="FT",
    #     id="Term",
    #     values=["Term", "Name", "Category"],
    #     reformat_values=[],
    #     merge=False,
    #     driver=driver,
    # )

    print_update(update_type="Edge Creation", text="OVERLAP", color="cyan")

    values, reformat = get_values_reformat(df=ft_ft_overlap, match=["source", "target"])
    save_df_to_csv(file_name="ft_overlap.csv", df=ft_ft_overlap)
    create_relationship(
        source_file="ft_overlap.csv",
        type_="OVERLAP",
        between=(("external_id", "source"), ("external_id", "target")),
        node_types=("FT", "FT"),
        values=values,
        reformat_values=reformat,
        merge=False,
        driver=driver,
    )

    print_update(update_type="Edge Creation", text="LINK (Gene -> Functional Term)", color="cyan")

    values, reformat = get_values_reformat(df=ft_gene, match=["ENSEMBL", "Term"])
    save_df_to_csv(file_name="ft_gene.csv", df=ft_gene)
    create_relationship(
        source_file="ft_gene.csv",
        type_="LINK",
        between=(("ENSEMBL", "ENSEMBL"), ("external_id", "Term")),
        node_types=("TG", "FT"),
        values=values,
        reformat_values=reformat,
        merge=False,
        driver=driver,
    )

    return


@time_function
def setup_base_db(
    ft_nodes: pd.DataFrame,
    ft_ft_overlap: pd.DataFrame,
    ft_gene: pd.DataFrame,
    gene_gene_scores: pd.DataFrame,
    gene_nodes: pd.DataFrame,
    or_nodes: pd.DataFrame,
    motif: pd.DataFrame,
    distance: pd.DataFrame,
    tf: pd.DataFrame,
    driver: Driver,
):
    """
    Sets up Base DB with Functional Terms, ENSEMBL Genes and STRING Associations
    """
    create_gene_nodes(nodes=gene_nodes, driver=driver)
    create_tf_label(tf=tf, driver=driver)
    create_or_nodes(nodes=or_nodes, driver=driver)
    create_string(gene_gene_scores=gene_gene_scores, driver=driver)

    create_motif_edges(motif=motif, driver=driver)
    create_distance_edges(distance=distance, driver=driver)

    create_functional(
        ft_nodes=ft_nodes,
        ft_ft_overlap=ft_ft_overlap,
        ft_gene=ft_gene,
        driver=driver,
    )

    print_update(update_type="Done", text="Setting up Base DB", color="pink")
    return
