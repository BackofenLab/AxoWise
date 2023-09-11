import csv
import json
import multiprocessing
import sys
from functools import lru_cache
from typing import Any

import mpmath
import neo4j
import pandas as pd

import queries
from util.stopwatch import Stopwatch


def calc_genes_pval(curr, alpha, in_gene, bg_genes, num_in_genes):
    # Lists are read as strings, evaluate to lists using JSON.
    # alternative is using eval() which is slower
    gene_list = curr.replace("'", '"')
    gene_list = json.loads(gene_list)

    # get the protein length of term
    num_term_prot = len(gene_list)

    # Get intersection of proteins
    gene_term = list(set(gene_list) & in_gene)
    num_inter = len(gene_term)

    if num_inter == 0:
        # Condition reduces runtime by 60%, needs to be tested carefully!
        # Check if enriched terms with and without that condition are
        # more or less the same
        p_value = alpha
    else:
        p_value = hypergeo_testing(num_inter, bg_genes, num_term_prot, num_in_genes)

    return (p_value, gene_term)


@lru_cache(maxsize=None)
def hypergeo_testing(intersec, total_genes, term_genes, in_genes):
    """Perfoms hypergeometric testing and returns a p_value
    Args:
        intersec(int): number of intersections between input and
            term proteins
        total_proteins(int): number of total proteins of organism
        term_proteins(int): number of proteins for a specific term
        in_proteins(int): number of input proteins given by the user
    Return:
        p-value(float): p-value of hypergeometric testing"""
    # Set the decimal precision
    mpmath.mp.dps = 64

    # Do the relevant calculations for the hypergeometric testing
    term_one = mpmath.binomial(term_genes, intersec)
    term_two = mpmath.binomial(total_genes - term_genes, in_genes - intersec)
    term_three = mpmath.binomial(total_genes, in_genes)

    # Calculate final p_value
    p_value = (term_one * term_two) / term_three
    return float(p_value)


def functional_enrichment(driver: neo4j.Driver, in_genes, species_id: Any):
    """inhouse functional enrichment - performs gene set enrichment analysis
    for a given set of proteins. Calculates p-value and Benjamini-Hochberg FDR
    for every functional term
    Args:
        in_proteins(list): list with input proteins
        species_id(int): Right now not used; default organism is mus musculus
    Return:
        rank_lst_fil(list): A list of dictionaries, where each dictionary the
            properties of a term: external_id, name, category, proteins,
            p-value, fdr-rate
    """
    stopwatch = Stopwatch()

    # Get number of all proteins in the organism (from Cypher)
    bg_proteins = queries.get_number_of_genes(driver, species_id)
    num_in_gene = len(in_genes)
    genes = set(in_genes)
    # pandas DataFrames for nodes and edges
    csv.field_size_limit(sys.maxsize)

    # Read Terms and put into Dataframe
    tot_tests = len(df_terms)

    stopwatch.round("setup_enrichment")

    # set significance level to 0.05
    alpha = 0.05

    # calculate p_value for all terms
    new_genes = []
    new_p = []
    arguments = [(value, alpha, genes, bg_proteins, num_in_gene) for value in df_terms["symbols"]]

    with multiprocessing.Pool() as pool:
        # Apply the function to each input value in parallel and collect the results
        for a, b in pool.starmap(calc_genes_pval, arguments):
            new_p.append(a)
            new_genes.append(b)

    # Update Dataframe and sort by p_value (descending)
    df_terms["symbols"] = new_genes
    df_terms["p_value"] = new_p
    df_terms.sort_values(by="p_value", ascending=False, inplace=True)
    df_terms = df_terms.reset_index(drop=True)
    stopwatch.round("pvalue_enrichment")

    # calculate Benjamini-Hochberg FDR
    p_vals = []
    rank_lst = []
    # Set cutoff value for p_value and fdr_rate
    cutoff = 1e-318
    prev = 0
    # Loop over p_value column in Dataframe
    for i, val in enumerate(df_terms["p_value"]):
        rank = tot_tests - i
        p_adj = val * (tot_tests / rank)
        # Ensure FDR rates are non-increasing
        if prev < p_adj and i != 0:
            p_adj = prev
        prev = p_adj
        val, p_adj = (cutoff, cutoff) if val <= cutoff or p_adj <= cutoff else (val, p_adj)
        p_vals += [val]
        rank_lst += [p_adj]
    # Update Dataframe
    df_terms["fdr_rate"] = rank_lst
    df_terms["p_value"] = p_vals
    # Remove all entries where FDR >= 0.05
    df_terms = df_terms[df_terms["fdr_rate"] < alpha]
    df_terms = df_terms.reset_index(drop=True)

    stopwatch.round("fdr_enrichment")
    stopwatch.total("functional_enrichment")
    return df_terms
