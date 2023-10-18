from utils import time_function, print_update, save_df_to_csv, get_values_reformat
from .upload_functions import create_nodes, create_relationship, update_nodes
import pandas as pd
from neo4j import Driver


@time_function
def create_gene_nodes(nodes: pd.DataFrame, species: str, driver: Driver):
    """
    Creates Gene Nodes based on ENSEMBL Data (with annotations from STRING). Uses create_nodes(), get_values_reformat(), save_df_to_csv()

    Input
    - nodes (pandas Dataframe): Node info of form (ENSEMBL, ENTREZID, SYMBOL, annotation)
    - species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
    - driver (neo4j Driver): Started Neo4j driver (can be done with start_driver())
    """
    print_update(update_type="Node Creation", text="Genes from ENSEMBL", color="blue")

    values, reformat = get_values_reformat(df=nodes, match=["ENSEMBL"])
    save_df_to_csv(file_name="genes.csv", df=nodes, override_prod=True)
    create_nodes(
        source_file="genes.csv",
        type_="TG",
        id="ENSEMBL",
        values=values,
        reformat_values=reformat,
        driver=driver,
        merge=False,
        species=species,
    )


@time_function
def create_protein_nodes(nodes: pd.DataFrame, species: str, driver: Driver):
    """
    Creates Protein Nodes based on ENSEMBL Data (with annotations from STRING). Uses create_nodes(), get_values_reformat(), save_df_to_csv()

    Input
    - nodes (pandas Dataframe): Protein info of form (ENSEMBL, SYMBOL, protein_size, annotation)
    - species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
    - driver (neo4j Driver): Started Neo4j driver (can be done with start_driver())
    """
    print_update(update_type="Node Creation", text="Proteins from ENSEMBL", color="blue")

    values, reformat = get_values_reformat(df=nodes, match=["ENSEMBL"])
    save_df_to_csv(file_name="proteins.csv", df=nodes, override_prod=True)
    create_nodes(
        source_file="proteins.csv",
        type_="Protein",
        id="ENSEMBL",
        values=values,
        reformat_values=reformat,
        merge=False,
        species=species,
        driver=driver,
    )


@time_function
def create_gene_protein_edges(links: pd.DataFrame, species: str, driver: Driver):  # TODO
    """
    Creates PRODUCT edges between TG and Protein nodes. Uses create_relationship(), get_values_reformat(), save_df_to_csv()

    Input
    - links (pandas DataFrame): Links between Genes and Proteins as given from ENSEMBL of form (ENSEMBL, Protein)
    - species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
    - driver (neo4j Driver): Started Neo4j driver (can be done with start_driver())
    """
    print_update(update_type="Edge Creation", text="PRODUCT", color="cyan")

    values, reformat = get_values_reformat(df=links, match=["ENSEMBL", "Protein"])
    save_df_to_csv(file_name="protein_gene_links.csv", df=links)
    create_relationship(
        source_file="protein_gene_links.csv",
        type_="PRODUCT",
        between=(("ENSEMBL", "ENSEMBL"), ("ENSEMBL", "Protein")),
        node_types=("TG", "Protein"),
        values=values,
        reformat_values=reformat,
        merge=False,
        species=species,
        driver=driver,
    )


@time_function
def create_tf_label(tf: pd.DataFrame, species: str, driver: Driver):
    """
    Sets TF label to TG nodes Uses update_nodes(), get_values_reformat(), save_df_to_csv()

    Input
    - tf (pandas DataFrame): List of Transcription Factors of form (ENSEMBL)
    - species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
    - driver (neo4j Driver): Started Neo4j driver (can be done with start_driver())
    """
    print_update(update_type="Node Update", text="Transcription Factor", color="orange")

    values, reformat = get_values_reformat(df=tf, match=["ENSEMBL"])
    save_df_to_csv(file_name="tf.csv", df=tf, override_prod=True)
    update_nodes(
        source_file="tf.csv",
        type_="TG",
        id="ENSEMBL",
        values=values,
        reformat_values=reformat,
        additional_label="TF",
        species=species,
        driver=driver,
    )


@time_function
def create_or_nodes(nodes: pd.DataFrame, species: str, driver: Driver):
    """
    Creates OR nodes from Dataframe. Uses create_nodes(), get_values_reformat(), save_df_to_csv()

    Input
    - nodes (pandas DataFrame): List of Open regions to be added of form (id, annotation, feature)
    - species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
    - driver (neo4j Driver): Started Neo4j driver (can be done with start_driver())
    """
    print_update(update_type="Node Creation", text="Open Region", color="blue")

    values, reformat = get_values_reformat(df=nodes, match=["id"])
    save_df_to_csv(file_name="or.csv", df=nodes, override_prod=True)
    create_nodes(
        source_file="or.csv",
        type_="OR",
        id="id",
        values=values,
        reformat_values=reformat,
        merge=False,
        species=species,
        driver=driver,
    )


@time_function
def create_distance_edges(distance: pd.DataFrame, species: str, driver: Driver):
    """
    Creates DISTANCE edges between OR and TG. Uses create_relationship(), get_values_reformat(), save_df_to_csv()

    Input
    - distance (pandas DataFrame): Distance information of form (id, Distance, ENSEMBL, Dummy)
    - species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
    - driver (neo4j Driver): Started Neo4j driver (can be done with start_driver())
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
        species=species,
        driver=driver,
    )


@time_function
def create_string(protein_protein_scores: pd.DataFrame, species: str, driver: Driver):
    """
    Creates STRING edges from STRING association scores. Uses create_relationship(), get_values_reformat(), save_df_to_csv()

    Input
    - protein_protein_scores (pandas DataFrame): Edge information of form (Protein1, Protein2, Score)
    - species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
    - driver (neo4j Driver): Started Neo4j driver (can be done with start_driver())
    """
    print_update(update_type="Edge Creation", text="STRING", color="cyan")

    values, reformat = get_values_reformat(df=protein_protein_scores, match=["Protein1", "Protein2"])
    save_df_to_csv(file_name="string_scores.csv", df=protein_protein_scores)
    create_relationship(
        source_file="string_scores.csv",
        type_="STRING",
        between=(("ENSEMBL", "Protein1"), ("ENSEMBL", "Protein2")),
        node_types=("Protein", "Protein"),
        values=values,
        reformat_values=reformat,
        merge=False,
        species=species,
        driver=driver,
    )

    return


@time_function
def create_functional(
    ft_nodes: pd.DataFrame,
    ft_ft_overlap: pd.DataFrame,
    ft_gene: pd.DataFrame,
    ft_protein: pd.DataFrame,
    species: str,
    driver: Driver,
):
    """
    Creates functional term nodes, OVERLAP edges, and LINKs to TG and Protein nodes. Uses create_nodes(), create_relationship(), get_values_reformat(), save_df_to_csv()

    Input
    - ft_nodes (pandas DataFrame): Functional Term nodes of form (Term, Name, Category, Proteins)
    - ft_ft_overlap (pandas DataFrame): Overlap edges of form (source, target, Score)
    - ft_gene (pandas DataFrame): FT-Gene edges of form (ENSEMBL, Term)
    - ft_protein (pandas DataFrame): FT-Protein edges of form (ENSEMBL, Term)
    - species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
    - driver (neo4j Driver): Started Neo4j driver (can be done with start_driver())
    """
    print_update(update_type="Node Creation", text="Functional Term", color="blue")

    values, reformat = get_values_reformat(df=ft_nodes, match=["Term"])
    save_df_to_csv(file_name="ft_nodes.csv", df=ft_nodes, override_prod=True)
    create_nodes(
        source_file="ft_nodes.csv",
        type_="FT",
        id="Term",
        values=values,
        reformat_values=reformat,
        merge=False,
        species=species,
        driver=driver,
    )

    print_update(update_type="Edge Creation", text="OVERLAP", color="cyan")

    values, reformat = get_values_reformat(df=ft_ft_overlap, match=["source", "target"])
    save_df_to_csv(file_name="ft_overlap.csv", df=ft_ft_overlap)
    create_relationship(
        source_file="ft_overlap.csv",
        type_="OVERLAP",
        between=(("Term", "source"), ("Term", "target")),
        node_types=("FT", "FT"),
        values=values,
        reformat_values=reformat,
        merge=False,
        species=species,
        driver=driver,
    )

    print_update(update_type="Edge Creation", text="LINK (Gene -> Functional Term)", color="cyan")

    values, reformat = get_values_reformat(df=ft_gene, match=["ENSEMBL", "Term"])
    save_df_to_csv(file_name="ft_gene.csv", df=ft_gene)
    create_relationship(
        source_file="ft_gene.csv",
        type_="LINK",
        between=(("ENSEMBL", "ENSEMBL"), ("Term", "Term")),
        node_types=("TG", "FT"),
        values=values,
        reformat_values=reformat,
        merge=False,
        species=species,
        driver=driver,
    )

    print_update(update_type="Edge Creation", text="LINK (Protein -> Functional Term)", color="cyan")

    values, reformat = get_values_reformat(df=ft_protein, match=["ENSEMBL", "Term"])
    save_df_to_csv(file_name="ft_protein.csv", df=ft_protein)
    create_relationship(
        source_file="ft_protein.csv",
        type_="LINK",
        between=(("ENSEMBL", "ENSEMBL"), ("Term", "Term")),
        node_types=("Protein", "FT"),
        values=values,
        reformat_values=reformat,
        merge=False,
        species=species,
        driver=driver,
    )

    return


@time_function
def setup_base_db(
    ft_nodes: pd.DataFrame,
    ft_ft_overlap: pd.DataFrame,
    ft_gene: pd.DataFrame,
    ft_protein: pd.DataFrame,
    protein_protein_scores: pd.DataFrame,
    gene_nodes: pd.DataFrame,
    or_nodes: pd.DataFrame | None,
    distance: pd.DataFrame | None,
    tf: pd.DataFrame,
    proteins: pd.DataFrame,
    gene_protein_link: pd.DataFrame,
    species: str,
    driver: Driver,
):
    """
    Sets up the database without experiments. Uses create_gene_nodes(), create_protein_nodes(), create_gene_protein_edges(), create_tf_label(), create_or_nodes(), create_distance_edges(), create_string(), create_functional()
    """
    create_gene_nodes(nodes=gene_nodes, species=species, driver=driver)
    create_tf_label(tf=tf, species=species, driver=driver)
    if or_nodes is not None:
        create_or_nodes(nodes=or_nodes, species=species, driver=driver)
    create_protein_nodes(nodes=proteins, species=species, driver=driver)
    create_gene_protein_edges(links=gene_protein_link, species=species, driver=driver)

    create_string(protein_protein_scores=protein_protein_scores, species=species, driver=driver)

    if distance is not None:
        create_distance_edges(distance=distance, species=species, driver=driver)

    create_functional(
        ft_nodes=ft_nodes,
        ft_ft_overlap=ft_ft_overlap,
        ft_gene=ft_gene,
        ft_protein=ft_protein,
        species=species,
        driver=driver,
    )

    print_update(update_type="Done", text=f"Setting up Base DB ({' '.join(species.split('_'))})", color="pink")
    return
