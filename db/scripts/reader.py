import os
import pandas as pd
from utils import time_function, check_for_files
from read.read_experiment import parse_experiment
from read.read_string import parse_string
from read.read_ensembl import parse_ensembl
from read.read_functional import parse_functional


@time_function
def read(dir_path: str = None, reformat: bool = True, mode: int = -1, complete: pd.DataFrame = pd.DataFrame([])):
    if mode == 0:
        # Experiment
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_EXPERIMENT_PATH")

        if check_for_files(mode=mode):
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
            ) = parse_experiment(dir_path=dir_path, reformat=reformat)

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
            (gene_gene_scores, genes_annotated) = parse_string(dir_path=dir_path, complete=complete)

            gene_gene_scores.to_csv("../source/processed/gene_gene_scores.csv", index=False)
            genes_annotated.to_csv("../source/processed/genes_annotated.csv", index=False)
        else:
            gene_gene_scores = pd.read_csv("../source/processed/gene_gene_scores.csv")
            genes_annotated = pd.read_csv("../source/processed/genes_annotated.csv")

        result = (gene_gene_scores, genes_annotated)
    elif mode == 2:
        # ENSEMBL
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_ENSEMBL_PATH")

        if check_for_files(mode=mode):
            (complete, tf) = parse_ensembl(dir_path=dir_path)

            complete.to_csv("../source/processed/complete.csv", index=False)
            tf.to_csv("../source/processed/tf.csv", index=False)
        else:
            complete = pd.read_csv("../source/processed/complete.csv")
            tf = pd.read_csv("../source/processed/tf.csv")

        result = (complete, tf)

    elif mode == 3:
        # Functional
        if dir_path == None:
            dir_path = os.getenv("_DEFAULT_FUNCTIONAL_PATH")

        if check_for_files(mode=mode):
            (
                ft_nodes,
                ft_gene,
                ft_ft_overlap,
            ) = parse_functional(dir_path=dir_path, complete=complete)

            ft_nodes.to_csv("../source/processed/ft_nodes.csv", index=False)
            ft_gene.to_csv("../source/processed/ft_gene.csv", index=False)
            ft_ft_overlap.to_csv("../source/processed/ft_ft_overlap.csv", index=False)
        else:
            ft_nodes = pd.read_csv("../source/processed/ft_nodes.csv")
            ft_gene = pd.read_csv("../source/processed/ft_gene.csv")
            ft_ft_overlap = pd.read_csv("../source/processed/ft_ft_overlap.csv")

        result = (
            ft_nodes,
            ft_gene,
            ft_ft_overlap,
        )

    return result
