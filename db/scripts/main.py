import reader as rd
from uploader import catlas_extention, base_setup, bulk_extention
from utils import print_update, time_function
from querier import run_queries
import os
import pandas as pd

os.environ["_DEFAULT_EXPERIMENT_PATH"] = "../source/experiment"
os.environ["_DEFAULT_STRING_PATH"] = "../source/string"
os.environ["_DEFAULT_FUNCTIONAL_PATH"] = "../source/functional"
os.environ["_DEFAULT_ENSEMBL_PATH"] = "../source/ensembl"
os.environ["_DEFAULT_CATLAS_PATH"] = "../source/catlas"
os.environ["_DEFAULT_CREDENTIALS_PATH"] = "../../config.yml"
os.environ["_DEV_MAX_REL"] = str(10000)
os.environ["_NEO4J_IMPORT_PATH"] = "/usr/local/bin/neo4j/import/"
os.environ["_FUNCTION_TIME_PATH"] = "../source/timing/function_times.tsv"

os.environ["_TIME_FUNCTIONS"] = str(False)
os.environ["_SILENT"] = str(False)
os.environ["_PRODUCTION"] = str(True)
os.environ["_ACCESS_NEO4J"] = str(False)


@time_function
def read_experiment_files(genes_annotated_mouse):
    """
    Reads, reformats and returns data from the bulk sequencing experiment. Uses reading() with mode 0.

    Input:
    - genes_annotated_mouse (pandas Dataframe): Annotated Genes of form (ENSEMBL, ENTREZID, SYMBOL, annotation)

    Return:
    - tg_mean_count (pandas DataFrame): Target Gene Meancount values of form (mean_count, ENSEMBL)
    - tf_mean_count (pandas DataFrame): Transcription Factor Meancount values of form (mean_count, ENSEMBL)
    - de_values (pandas DataFrame): Differential Expression Values from Experiment of form (ENSEMBL, Context, Value, p)
    - or_nodes (pandas DataFrame): Open region nodes of form (id, annotation, feature)
    - or_mean_count (pandas DataFrame): Open Region Meancount values of form (id, mean_count)
    - da_values (pandas DataFrame): Differential Accesibility Values from Experiment of form (id, Context, Value, p, summit)
    - tf_tg_corr (pandas DataFrame): Correlation between TG and TF of form (ENSEMBL_TG, ENSEMBL_TF, Correlation, p)
    - or_tg_corr (pandas DataFrame): Correlation between TG and OR of form (ENSEMBL, Correlation, p, id)
    - motif (pandas DataFrame): Motif information of form (id, or_id,ENSEMBL, Consensus, p, number_of_peaks, Concentration)
    - distance (pandas DataFrame): Distance Information for Open Regions of form (id, Distance, ENSEMBL)
    """

    data = rd.reading(genes_annotated_mouse=genes_annotated_mouse, mode=0)
    return data


@time_function
def read_string_files(
    complete_mouse: pd.DataFrame,
    proteins_mouse: pd.DataFrame,
    complete_human: pd.DataFrame,
    proteins_human: pd.DataFrame,
):
    """
    Reads, reformats and returns data from STRING. Uses reading() with mode 1. Protein IDs must be have species prefix ("9606." for human, "10090." for mouse)

    Input
    - complete_mouse (pandas Dataframe): Set of Genes for Mouse from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
    - proteins_mouse (pandas Dataframe): Set of Proteins for Mouse from ENSEMBL of form (Protein)
    - complete_human (pandas Dataframe): Set of Genes for Humans from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
    - proteins_human (pandas Dataframe): Set of Proteins for Humans from ENSEMBL of form (Protein)

    Return
    - genes_annotated_mouse (pandas Dataframe): Target Gene nodes for Mouse of form (ENSEMBL, ENTREZID, SYMBOL, annotation)
    - proteins_annotated_mouse (pandas Dataframe): Protein nodes for Mouse of form (ENSEMBL, SYMBOL, protein_size, annotation)
    - protein_protein_scores_mouse (pandas Dataframe): Scores between Proteins (STRING) for Mouse of form (Protein1, Protein2, Score)
    - genes_annotated_human (pandas Dataframe): Target Gene nodes for Human of form (ENSEMBL, ENTREZID, SYMBOL, annotation)
    - proteins_annotated_human (pandas Dataframe): Protein nodes for Human of form (ENSEMBL, SYMBOL, protein_size, annotation)
    - protein_protein_scores_human (pandas Dataframe): Scores between Proteins (STRING) for Human of form (Protein1, Protein2, Score)
    """
    data = rd.reading(
        complete_mouse=complete_mouse,
        proteins_mouse=proteins_mouse,
        complete_human=complete_human,
        proteins_human=proteins_human,
        mode=1,
    )
    return data


@time_function
def read_ensembl_files():
    """
    Reads, reformats and returns data from ENSEMBL. Uses reading() with mode 2.

    Return
    - complete_mouse (pandas Dataframe): Set of Genes for Mouse from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
    - tf_mouse (pandas Dataframe): List of Transcription factors for Mouse of form (ENSEMBL)
    - proteins_mouse (pandas Dataframe): Set of Proteins for Mouse from ENSEMBL of form (Protein)
    - gene_protein_link_mouse (pandas Dataframe): Links between genes and proteins for Mouse of form (ENSEMBL, Protein)
    - complete_human (pandas Dataframe): Set of Genes for Human from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
    - tf_human (pandas Dataframe): List of Transcription factors for Human of form (ENSEMBL)
    - proteins_human (pandas Dataframe): Set of Proteins for Human from ENSEMBL of form (Protein)
    - gene_protein_link_human (pandas Dataframe): Links between genes and proteins for Human of form (ENSEMBL, Protein)
    """
    data = rd.reading(mode=2)
    return data


@time_function
def read_functional_files():
    """
    Reads, reformats and returns data from Functional Term files. Uses reading() with mode 3.

    Return
    - ft_nodes_mouse (pandas DataFrame): Functional Term nodes for Mouse of form (Term, Name, Category, Proteins)
    - ft_gene_mouse (pandas DataFrame): Links between Functional Terms and Target Genes for Mouse of form (ENSEMBL, Term)
    - ft_protein_mouse (pandas DataFrame): Links between Functional Terms and Proteins for Mouse of form (ENSEMBL, Term)
    - ft_ft_overlap_mouse (pandas DataFrame): Overlap between Functional Terms for Mouse of form (source, target, Score)
    - ft_nodes_human (pandas DataFrame): Functional Term nodes for Human of form (Term, Name, Category, Proteins)
    - ft_gene_human (pandas DataFrame): Links between Functional Terms and Target Genes for Human of form (ENSEMBL, Term)
    - ft_protein_human (pandas DataFrame): Links between Functional Terms and Proteins for Human of form (ENSEMBL, Term)
    - ft_ft_overlap_human (pandas DataFrame): Overlap between Functional Terms for Human of form (source, target, Score)
    """
    data = rd.reading(mode=3)
    return data


@time_function
def read_catlas_files(or_nodes: pd.DataFrame, distance: pd.DataFrame):
    """
    Reads, reformats and returns data from Catlas Whole Mouse Brain dataset. Uses reading() with mode 4.

    Input
    - or_nodes (pandas DataFrame): Existing Open region nodes of form (id, annotation, feature)
    - distance (pandas DataFrame): Existing Distance edges of form (id, Distance, ENSEMBL)

    Return
    - or_extended (pandas DataFrame): Extended Open region nodes of form (id, annotation, feature)
    - catlas_or_context (pandas DataFrame): Open Region Context Information in form (Context, id, cell_id)
    - catlas_correlation (pandas DataFrame): OR-TG Correlation of form (id, ENSEMBL, Correlation, cell_id)
    - catlas_celltype (pandas DataFrame): Celltype and Subtype info of form (name, region, nuclei_counts, celltype, subtype, sub-subtype)
    - distance_extended (pandas DataFrame): Extended Distance edges of form (id, Distance, ENSEMBL)
    - catlas_motifs (pandas DataFrame): Motif information of form (id, or_id, ENSEMBL, Consensus, p, number_of_peaks, Concentration, cell_id)
    """
    data = rd.reading(or_nodes=or_nodes, distance=distance, mode=4)
    return data


@time_function
def upload_workflow():
    """
    The Workflow is as follows:
    1. The files are read using read_experiment_files(), read_string_files(), read_ensembl_files(), read_functional_files(), read_catlas_files() and bring them into the appropriate format.
    2. The data is uploaded using base_setup(), bulk_extention() und catlas_extention().
    """
    (
        complete_mouse,
        tf_mouse,
        proteins_mouse,
        gene_protein_link_mouse,
        complete_human,
        tf_human,
        proteins_human,
        gene_protein_link_human,
    ) = read_ensembl_files()

    (
        genes_annotated_mouse,
        proteins_annotated_mouse,
        protein_protein_scores_mouse,
        genes_annotated_human,
        proteins_annotated_human,
        protein_protein_scores_human,
    ) = read_string_files(
        complete_mouse=complete_mouse,
        proteins_mouse=proteins_mouse,
        complete_human=complete_human,
        proteins_human=proteins_human,
    )

    (
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
    ) = read_experiment_files(genes_annotated_mouse=genes_annotated_mouse)

    (
        ft_nodes_mouse,
        ft_gene_mouse,
        ft_protein_mouse,
        ft_ft_overlap_mouse,
        ft_nodes_human,
        ft_gene_human,
        ft_protein_human,
        ft_ft_overlap_human,
    ) = read_functional_files()

    # TODO: Distance (correct, not dummy), MOTIF (correct, not dummy)
    (
        or_extended,
        catlas_or_context,
        catlas_correlation,
        catlas_celltype,
        distance_extended,
        catlas_motifs,
    ) = read_catlas_files(or_nodes=or_nodes, distance=distance)

    print_update(update_type="Done", text="Reading files", color="pink")

    base_setup(
        species="Homo_Sapiens",
        gene_nodes=genes_annotated_human,
        ft_nodes=ft_nodes_human,
        ft_gene=ft_gene_human,
        ft_ft_overlap=ft_ft_overlap_human,
        tf=tf_human,
        ft_protein=ft_protein_human,
        gene_protein_link=gene_protein_link_human,
        proteins_annotated=proteins_annotated_human,
        protein_protein_scores=protein_protein_scores_human,
    )

    base_setup(
        species="Mus_Musculus",
        gene_nodes=genes_annotated_mouse,
        or_nodes=or_extended,
        distance=distance_extended,
        ft_nodes=ft_nodes_mouse,
        ft_gene=ft_gene_mouse,
        ft_ft_overlap=ft_ft_overlap_mouse,
        tf=tf_mouse,
        ft_protein=ft_protein_mouse,
        gene_protein_link=gene_protein_link_mouse,
        proteins_annotated=proteins_annotated_mouse,
        protein_protein_scores=protein_protein_scores_mouse,
    )

    bulk_extention(
        species="Mus_Musculus",
        tg_mean_count=tg_mean_count,
        tf_mean_count=tf_mean_count,
        or_context_values=da_values,
        tg_context_values=de_values,
        tf_tg_corr=tf_tg_corr,
        or_tg_corr=or_tg_corr,
        motif=motif,
        or_mean_count=or_mean_count,
    )

    catlas_extention(
        species="Mus_Musculus",
        catlas_or_context=catlas_or_context,
        catlas_correlation=catlas_correlation,
        catlas_celltype=catlas_celltype,
        catlas_motifs=catlas_motifs,
    )


if __name__ == "__main__":
    upload_workflow()
    # run_queries()
    pass
