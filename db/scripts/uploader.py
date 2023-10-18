import pandas as pd
from utils import time_function, stop_driver, start_driver
from upload.upload_base import setup_base_db
from upload.upload_experiment import extend_db_from_experiment
from upload.upload_catlas import extend_db_from_catlas


@time_function
def base_setup(
    species: str,
    gene_nodes: pd.DataFrame,
    ft_nodes: pd.DataFrame,
    ft_ft_overlap: pd.DataFrame,
    ft_gene: pd.DataFrame,
    tf: pd.DataFrame,
    ft_protein: pd.DataFrame,
    gene_protein_link: pd.DataFrame,
    proteins_annotated: pd.DataFrame,
    protein_protein_scores: pd.DataFrame,
    or_nodes: pd.DataFrame | None = None,
    distance: pd.DataFrame | None = None,
):
    """
    This Function Sets up the base network (Protein, Gene nodes, TF labels, Protein-Gene Links, STRING associations, Functional Terms, Overlap, TG-FT und Protein-FT links, Distance between OR and TG). Uses start_driver(), stop_driver(), setup_base_db()

    Input
    - species (String): Representing Species (i.e. "Mus_Musculus", "Homo_Sapiens")
    - gene_nodes (pandas DataFrame): Target Gene nodes of form (ENSEMBL, ENTREZID, SYMBOL, annotation)
    - ft_nodes (pandas DataFrame): Functional Term nodes of form (Term, Name, Category, Proteins)
    - ft_ft_overlap (pandas DataFrame): Overlap between Functional Terms of form (source, target, Score)
    - ft_gene (pandas DataFrame): Links between Functional Terms and Target Genes of form (ENSEMBL, Term)
    - tf (pandas DataFrame): List of Transcription factors (subset of TGs, must be still included in gene_nodes) of form (ENSEMBL)
    - ft_protein (pandas DataFrame): Links between Functional Terms and Proteins of form (ENSEMBL, Term)
    - gene_protein_link (pandas Dataframe): Links between genes and proteins of form (ENSEMBL, Protein)
    - proteins_annotated (pandas DataFrame): Protein nodes of form (ENSEMBL, SYMBOL, protein_size, annotation)
    - protein_protein_scores (pandas DataFrame): Scores between Proteins (STRING) of form (Protein1, Protein2, Score)
    - or_nodes (pandas DataFrame): Open chromatin region nodes of form (id, annotation, feature)
    - distance (pandas DataFrame): Distance between OR and TG of form (id, Distance, ENSEMBL, Dummy)
    """
    driver = start_driver()

    setup_base_db(
        ft_nodes=ft_nodes,
        ft_ft_overlap=ft_ft_overlap,
        ft_gene=ft_gene,
        ft_protein=ft_protein,
        gene_nodes=gene_nodes,
        or_nodes=or_nodes,
        distance=distance,
        tf=tf,
        gene_protein_link=gene_protein_link,
        proteins=proteins_annotated,
        protein_protein_scores=protein_protein_scores,
        species=species,
        driver=driver,
    )

    stop_driver(driver=driver)


@time_function
def bulk_extention(
    species: str,
    tg_mean_count: pd.DataFrame,
    tf_mean_count: pd.DataFrame,
    or_mean_count: pd.DataFrame,
    tg_context_values: pd.DataFrame,
    or_context_values: pd.DataFrame,
    tf_tg_corr: pd.DataFrame,
    or_tg_corr: pd.DataFrame,
    motif: pd.DataFrame,
):
    """
    Extends Database with Data from bulk sequencing experiment. Uses start_driver(), stop_driver(), extend_db_from_experiment()

    Input
    - species (String): Representing Species (i.e. "Mus_Musculus", "Homo_Sapiens")
    - tg_mean_count (pandas DataFrame): Target Gene Meancount values of form (mean_count, ENSEMBL)
    - tf_mean_count (pandas DataFrame): Transcription Factor Meancount values of form (mean_count, ENSEMBL)
    - or_mean_count (pandas DataFrame): Open Region Meancount values of form (id, mean_count)
    - tf_tg_corr (pandas DataFrame): Correlation between TG and TF of form (ENSEMBL_TG, ENSEMBL_TF, Correlation, p)
    - or_tg_corr (pandas DataFrame): Correlation between TG and OR of form (ENSEMBL, Correlation, p, id)
    - motif (pandas DataFrame): Motif information of form (id, or_id,ENSEMBL, Consensus, p, number_of_peaks, Concentration)
    - tg_context_values (pandas DataFrame): Differential Expression Values from Experiment of form (ENSEMBL, Context, Value, p)
    - or_context_values (pandas DataFrame): Differential Accesibility Values from Experiment of form (id, Context, Value, p, summit)
    """
    driver = start_driver()

    extend_db_from_experiment(
        tg_mean_count=tg_mean_count,
        tf_mean_count=tf_mean_count,
        or_mean_count=or_mean_count,
        tg_context_values=tg_context_values,
        or_context_values=or_context_values,
        tf_tg_corr=tf_tg_corr,
        or_tg_corr=or_tg_corr,
        motif=motif,
        species=species,
        driver=driver,
    )

    stop_driver(driver=driver)


@time_function
def catlas_extention(
    species: str,
    catlas_or_context: pd.DataFrame,
    catlas_correlation: pd.DataFrame,
    catlas_celltype: pd.DataFrame,
    catlas_motifs: pd.DataFrame,
):
    """
    Extends Database with Data from Catlas Whole Mouse Brain experiment. Uses start_driver(), stop_driver(), extend_db_from_catlas()

    Input
    - species (String): Representing Species (i.e. "Mus_Musculus", "Homo_Sapiens")
    - catlas_or_context (pandas DataFrame): Open Region Context Information in form (Context, id, cell_id)
    - catlas_correlation (pandas DataFrame): OR-TG Correlation of form (id, ENSEMBL, Correlation, cell_id)
    - catlas_celltype (pandas DataFrame): Celltype and Subtype info of form (name, region, nuclei_counts, celltype, subtype, sub-subtype)
    - catlas_motifs (pandas DataFrame): Motif information of form (id, or_id, ENSEMBL, Consensus, p, number_of_peaks, Concentration, cell_id)
    """
    driver = start_driver()

    extend_db_from_catlas(
        catlas_or_context=catlas_or_context,
        catlas_correlation=catlas_correlation,
        catlas_celltype=catlas_celltype,
        catlas_motifs=catlas_motifs,
        species=species,
        driver=driver,
    )

    stop_driver(driver=driver)
