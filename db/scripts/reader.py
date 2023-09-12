import os
import pandas as pd
from utils import time_function, check_for_files
from read.read_experiment import parse_experiment
from read.read_string import parse_string
from read.read_ensembl import parse_ensembl
from read.read_functional import parse_functional
from read.read_catlas import parse_catlas


def read(
    dir_path: str = None,
    reformat: bool = True,
    mode: int = -1,
    complete_mouse: pd.DataFrame = pd.DataFrame([]),
    proteins_mouse: pd.DataFrame = pd.DataFrame([]),
    complete_human: pd.DataFrame = pd.DataFrame([]),
    proteins_human: pd.DataFrame = pd.DataFrame([]),
    or_nodes: pd.DataFrame = pd.DataFrame([]),
    distance: pd.DataFrame = pd.DataFrame([]),
    genes_annotated_mouse: pd.DataFrame = pd.DataFrame([]),
):
    if mode == 0:
        # Experiment
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_EXPERIMENT_PATH")

        if check_for_files(mode=mode):
            symbol_ensembl_dict = genes_annotated_mouse.filter(items=["ENSEMBL", "SYMBOL"])
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
            ) = parse_experiment(symbol_ensembl_dict=symbol_ensembl_dict, dir_path=dir_path, reformat=reformat)

            tg_mean_count.to_csv("../source/processed/tg_mean_count.csv", index=False)
            tf_mean_count.to_csv("../source/processed/tf_mean_count.csv", index=False)
            de_values.to_csv("../source/processed/de_values.csv", index=False)
            or_nodes.to_csv("../source/processed/or_nodes.csv", index=False)
            or_mean_count.to_csv("../source/processed/or_mean_count.csv", index=False)
            da_values.to_csv("../source/processed/da_values.csv", index=False)
            tf_tg_corr.to_csv("../source/processed/tf_tg_corr.csv", index=False)
            or_tg_corr.to_csv("../source/processed/or_tg_corr.csv", index=False)
            motif.to_csv("../source/processed/motif.csv", index=False)
            distance.to_csv("../source/processed/distance.csv", index=False)
        else:
            tg_mean_count = pd.read_csv("../source/processed/tg_mean_count.csv")
            tf_mean_count = pd.read_csv("../source/processed/tf_mean_count.csv")
            de_values = pd.read_csv("../source/processed/de_values.csv")
            or_nodes = pd.read_csv("../source/processed/or_nodes.csv")
            or_mean_count = pd.read_csv("../source/processed/or_mean_count.csv")
            da_values = pd.read_csv("../source/processed/da_values.csv")
            tf_tg_corr = pd.read_csv("../source/processed/tf_tg_corr.csv")
            or_tg_corr = pd.read_csv("../source/processed/or_tg_corr.csv")
            motif = pd.read_csv("../source/processed/motif.csv")
            distance = pd.read_csv("../source/processed/distance.csv")

        result = (
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

    elif mode == 1:
        # STRING
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_STRING_PATH")

        if check_for_files(mode=mode):
            (
                gene_gene_scores_mouse,
                genes_annotated_mouse,
                proteins_annotated_mouse,
                protein_protein_scores_mouse,
                gene_gene_scores_human,
                genes_annotated_human,
                proteins_annotated_human,
                protein_protein_scores_human,
            ) = parse_string(
                dir_path=dir_path,
                complete_mouse=complete_mouse,
                proteins_mouse=proteins_mouse,
                complete_human=complete_human,
                proteins_human=proteins_human,
            )

            gene_gene_scores_mouse.to_csv("../source/processed/gene_gene_scores_mouse.csv", index=False)
            genes_annotated_mouse.to_csv("../source/processed/genes_annotated_mouse.csv", index=False)
            protein_protein_scores_mouse.to_csv("../source/processed/protein_protein_scores_mouse.csv", index=False)
            proteins_annotated_mouse.to_csv("../source/processed/proteins_annotated_mouse.csv", index=False)
            gene_gene_scores_human.to_csv("../source/processed/gene_gene_scores_human.csv", index=False)
            genes_annotated_human.to_csv("../source/processed/genes_annotated_human.csv", index=False)
            protein_protein_scores_human.to_csv("../source/processed/protein_protein_scores_human.csv", index=False)
            proteins_annotated_human.to_csv("../source/processed/proteins_annotated_human.csv", index=False)

        else:
            gene_gene_scores_mouse = pd.read_csv("../source/processed/gene_gene_scores_mouse.csv")
            genes_annotated_mouse = pd.read_csv("../source/processed/genes_annotated_mouse.csv")
            proteins_annotated_mouse = pd.read_csv("../source/processed/proteins_annotated_mouse.csv")
            protein_protein_scores_mouse = pd.read_csv("../source/processed/protein_protein_scores_mouse.csv")
            gene_gene_scores_human = pd.read_csv("../source/processed/gene_gene_scores_human.csv")
            genes_annotated_human = pd.read_csv("../source/processed/genes_annotated_human.csv")
            proteins_annotated_human = pd.read_csv("../source/processed/proteins_annotated_human.csv")
            protein_protein_scores_human = pd.read_csv("../source/processed/protein_protein_scores_human.csv")

        result = (
            gene_gene_scores_mouse,
            genes_annotated_mouse,
            proteins_annotated_mouse,
            protein_protein_scores_mouse,
            gene_gene_scores_human,
            genes_annotated_human,
            proteins_annotated_human,
            protein_protein_scores_human,
        )

    elif mode == 2:
        # ENSEMBL
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_ENSEMBL_PATH")

        if check_for_files(mode=mode):
            (
                complete_mouse,
                tf_mouse,
                proteins_mouse,
                gene_protein_link_mouse,
                complete_human,
                tf_human,
                proteins_human,
                gene_protein_link_human,
            ) = parse_ensembl(dir_path=dir_path)

            complete_mouse.to_csv("../source/processed/complete_mouse.csv", index=False)
            tf_mouse.to_csv("../source/processed/tf_mouse.csv", index=False)
            proteins_mouse.to_csv("../source/processed/proteins_mouse.csv", index=False)
            gene_protein_link_mouse.to_csv("../source/processed/gene_protein_link_mouse.csv", index=False)
            complete_human.to_csv("../source/processed/complete_human.csv", index=False)
            tf_human.to_csv("../source/processed/tf_human.csv", index=False)
            proteins_human.to_csv("../source/processed/proteins_human.csv", index=False)
            gene_protein_link_human.to_csv("../source/processed/gene_protein_link_human.csv", index=False)
        else:
            complete_mouse = pd.read_csv("../source/processed/complete_mouse.csv")
            tf_mouse = pd.read_csv("../source/processed/tf_mouse.csv")
            proteins_mouse = pd.read_csv("../source/processed/proteins_mouse.csv")
            gene_protein_link_mouse = pd.read_csv("../source/processed/gene_protein_link_mouse.csv")
            complete_human = pd.read_csv("../source/processed/complete_human.csv")
            tf_human = pd.read_csv("../source/processed/tf_human.csv")
            proteins_human = pd.read_csv("../source/processed/proteins_human.csv")
            gene_protein_link_human = pd.read_csv("../source/processed/gene_protein_link_human.csv")

        result = (
            complete_mouse,
            tf_mouse,
            proteins_mouse,
            gene_protein_link_mouse,
            complete_human,
            tf_human,
            proteins_human,
            gene_protein_link_human,
        )

    elif mode == 3:
        # Functional
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_FUNCTIONAL_PATH")

        if check_for_files(mode=mode):
            (
                ft_nodes_mouse,
                ft_gene_mouse,
                ft_protein_mouse,
                ft_ft_overlap_mouse,
                ft_nodes_human,
                ft_gene_human,
                ft_protein_human,
                ft_ft_overlap_human,
            ) = parse_functional(dir_path=dir_path)

            ft_nodes_mouse.to_csv("../source/processed/ft_nodes_mouse.csv", index=False)
            ft_gene_mouse.to_csv("../source/processed/ft_gene_mouse.csv", index=False)
            ft_protein_mouse.to_csv("../source/processed/ft_protein_mouse.csv", index=False)
            ft_ft_overlap_mouse.to_csv("../source/processed/ft_ft_overlap_mouse.csv", index=False)
            ft_nodes_human.to_csv("../source/processed/ft_nodes_human.csv", index=False)
            ft_gene_human.to_csv("../source/processed/ft_gene_human.csv", index=False)
            ft_protein_human.to_csv("../source/processed/ft_protein_human.csv", index=False)
            ft_ft_overlap_human.to_csv("../source/processed/ft_ft_overlap_human.csv", index=False)
        else:
            ft_nodes_mouse = pd.read_csv("../source/processed/ft_nodes_mouse.csv")
            ft_gene_mouse = pd.read_csv("../source/processed/ft_gene_mouse.csv")
            ft_protein_mouse = pd.read_csv("../source/processed/ft_protein_mouse.csv")
            ft_ft_overlap_mouse = pd.read_csv("../source/processed/ft_ft_overlap_mouse.csv")
            ft_nodes_human = pd.read_csv("../source/processed/ft_nodes_human.csv")
            ft_gene_human = pd.read_csv("../source/processed/ft_gene_human.csv")
            ft_protein_human = pd.read_csv("../source/processed/ft_protein_human.csv")
            ft_ft_overlap_human = pd.read_csv("../source/processed/ft_ft_overlap_human.csv")

        result = (
            ft_nodes_mouse,
            ft_gene_mouse,
            ft_protein_mouse,
            ft_ft_overlap_mouse,
            ft_nodes_human,
            ft_gene_human,
            ft_protein_human,
            ft_ft_overlap_human,
        )

    elif mode == 4:
        # Catlas

        if check_for_files(mode=mode):
            (
                or_extended,
                catlas_or_context,
                catlas_correlation,
                catlas_celltype,
                distance_extended,
                catlas_motifs,
            ) = parse_catlas(or_nodes=or_nodes, distance=distance)

            or_extended.to_csv("../source/processed/or_extended.csv", index=False)
            catlas_or_context.to_csv("../source/processed/catlas_or_context.csv", index=False)
            catlas_correlation.to_csv("../source/processed/catlas_correlation.csv", index=False)
            catlas_celltype.to_csv("../source/processed/catlas_celltype.csv", index=False)
            distance_extended.to_csv("../source/processed/distance_extended.csv", index=False)
            catlas_motifs.to_csv("../source/processed/catlas_motifs.csv", index=False)
        else:
            or_extended = pd.read_csv("../source/processed/or_extended.csv")
            catlas_or_context = pd.read_csv("../source/processed/catlas_or_context.csv")
            catlas_correlation = pd.read_csv("../source/processed/catlas_correlation.csv")
            catlas_celltype = pd.read_csv("../source/processed/catlas_celltype.csv")
            distance_extended = pd.read_csv("../source/processed/distance_extended.csv")
            catlas_motifs = pd.read_csv("../source/processed/catlas_motifs.csv")

        result = (
            or_extended,
            catlas_or_context,
            catlas_correlation,
            catlas_celltype,
            distance_extended,
            catlas_motifs,
        )

    return result
