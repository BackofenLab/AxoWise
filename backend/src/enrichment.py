import csv
import json
import multiprocessing
import sys
import time
from functools import lru_cache
from typing import Any

import mpmath
import neo4j
import pandas as pd

import cypher_queries as Cypher


def calc_proteins_pval(curr, alpha, in_pr, bg_proteins, num_in_prot):
    # Lists are read as strings, evaluate to lists using JSON.
    # alternative is using eval() which is slower
    prot_list = curr.replace("'", '"')
    prot_list = json.loads(prot_list)

    # get the protein length of term
    num_term_prot = len(prot_list)

    # Get intersection of proteins
    prots_term = list(set(prot_list) & in_pr)
    num_inter = len(prots_term)

    if num_inter == 0:
        # Condition reduces runtime by 60%, needs to be tested carefully!
        # Check if enriched terms with and without that condition are
        # more or less the same
        p_value = alpha
    else:
        p_value = hypergeo_testing(num_inter, bg_proteins, num_term_prot, num_in_prot)

    return (p_value, prots_term)


@lru_cache(maxsize=None)
def hypergeo_testing(intersec, total_proteins, term_proteins, in_proteins):
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
    term_one = mpmath.binomial(term_proteins, intersec)
    term_two = mpmath.binomial(total_proteins - term_proteins, in_proteins - intersec)
    term_three = mpmath.binomial(total_proteins, in_proteins)

    # Calculate final p_value
    p_value = (term_one * term_two) / term_three
    return float(p_value)


def functional_enrichment(driver: neo4j.Driver, in_proteins, species_id: Any):
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

    # Begin a timer to time
    t_begin = time.time()

    # Get number of all proteins in the organism (from Cypher)
    bg_proteins = Cypher.get_number_of_proteins(driver)
    num_in_prot = len(in_proteins)
    prots = set(in_proteins)
    # pandas DataFrames for nodes and edges
    csv.field_size_limit(sys.maxsize)

    # Read Terms and put into Dataframe
    df_terms = pd.DataFrame(Cypher.get_enrichment_terms(driver))
    tot_tests = len(df_terms)

    t_setup = time.time()
    print("Time Spent (setup_enrichment): ", t_setup - t_begin)

    # set significance level to 0.05
    alpha = 0.05

    # calculate p_value for all terms
    new_prots = []
    new_p = []
    arguments = [(value, alpha, prots, bg_proteins, num_in_prot) for value in df_terms["proteins"]]
    with multiprocessing.Pool() as pool:
        # Apply the function to each input value in parallel and collect the results
        for a, b in pool.starmap(calc_proteins_pval, arguments):
            new_p.append(a)
            new_prots.append(b)

    # Update Dataframe and sort by p_value (descending)
    df_terms["proteins"] = new_prots
    df_terms["p_value"] = new_p
    df_terms.sort_values(by="p_value", ascending=False, inplace=True)
    df_terms = df_terms.reset_index(drop=True)
    t_pvalue = time.time()
    print("Time Spent (pvalue_enrichment): ", t_pvalue - t_setup)

    # calculate Benjamini-Hochberg FDR
    rank_lst = []
    prev = 0
    # Loop over p_value column in Dataframe
    for i, val in enumerate(df_terms["p_value"]):
        rank = tot_tests - i
        p_adj = val * (tot_tests / rank)
        # Ensure FDR rates are non-increasing
        if prev < p_adj and i != 0:
            p_adj = prev
        prev = p_adj
        rank_lst += [p_adj]

    # Update Dataframe
    df_terms["fdr_rate"] = rank_lst

    # Remove all entries where FDR >= 0.05
    df_terms = df_terms[df_terms["fdr_rate"] < alpha]
    df_terms = df_terms.reset_index(drop=True)

    t_cypher = time.time()
    print("Time Spent (fdr_enrichment): ", t_cypher - t_pvalue)
    return df_terms
