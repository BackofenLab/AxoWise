from scipy.stats import fisher_exact
from scipy.stats import hypergeom
import scipy.special
import decimal
import sys
import csv
from ast import literal_eval
import pandas as pd
import cypher_queries as Cypher
from cypher_queries import *
import time

def functional_enrichment(in_proteins, species_id):
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
    bg_proteins = NUM_PROTEINS
    num_in_prot = len(in_proteins)

    # TODO: Improve runtime?
    
    #pandas DataFrames for nodes and edges
    csv.field_size_limit(sys.maxsize)

    df_terms = pd.read_csv('/tmp/'+repr(TERM_FILE)+'.csv', sep=',', engine='python', quotechar='"')
    terms = df_terms.to_dict('records')
    for i in terms:
        i['proteins'] = literal_eval(i['proteins'])
    # os.remove('/tmp/'+repr(TERM_FILE)+'.csv')

    t_setup = time.time()
    print("Time Spent (setup_enrichment): ", t_setup - t_begin)


    in_proteins = frozenset(in_proteins)

    # set significance level to 0.05
    ALPHA = 0.05
    # calculate p_value for all terms

    for i, val in enumerate(terms):
        curr_set = frozenset(val['proteins'])

        # get the protein length of term
        num_term_prot = len(curr_set)

        # Get intersection of proteins
        prots_term = list(in_proteins.intersection(curr_set))
        num_inter = len(prots_term)

        if (num_inter == 0):
            # Condition reduces runtime by 60%, needs to be tested carefully!
            # Check if enriched terms with and without that condition are 
            # more or less the same
            p_value = 0.05 
        else:
            p_value = hypergeom.pmf(num_inter, bg_proteins, num_term_prot,
            num_in_prot)    # decimal.Decimal()

            #p_value = hypergeo_testing(num_inter, bg_proteins, num_term_prot,
            #    num_in_prot)
        temp_dic = val
        temp_dic['proteins'] = prots_term
        temp_dic['p_value'] = p_value
        terms[i] = temp_dic

    # calculate Benjamini-Hochberg FDR

    tot_tests = len(terms)
    terms = sorted(terms, key=lambda item: item['p_value'], reverse=True)

    t_pvalue = time.time()
    print("Time Spent (pvalue_enrichment): ", t_pvalue - t_setup)
    
    # adjust p_values
    rank_lst = []
    for ind, prop in enumerate(terms):
        rank = tot_tests-ind
        p_adj = prop['p_value']*(tot_tests/rank)        # decimal.Decimal()
        rank_lst += [p_adj]

    rank_lst_fil = []
    for i in range(len(rank_lst) - 1):
        if rank_lst[i] < rank_lst[i+1]:
                rank_lst[i+1] = rank_lst[i]
        if (rank_lst[i] < ALPHA):
            term_temp = terms[i]
            term_temp["fdr_rate"] = rank_lst[i]
            rank_lst_fil += [term_temp]
            if (i == (len(rank_lst) - 2)):
                term_temp = terms[i+1]
                term_temp["fdr_rate"] = rank_lst[i+1]
                rank_lst_fil += [term_temp]

    # df = pd.DataFrame(rank_lst_fil)
    # df.to_csv("inhouse_enrichment2.csv", header=True, index=False)

    t_cypher = time.time()
    print("Time Spent (fdr_enrichment): ", t_cypher - t_pvalue)

    return rank_lst_fil
    

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
    term_one = decimal.Decimal(scipy.special.binom(term_proteins, intersec))
    # in case term_two will give error: change .binom to comb(exact=True)
    term_two = decimal.Decimal(scipy.special.comb(
        total_proteins-term_proteins, in_proteins-intersec, exact=True))
    term_three = decimal.Decimal(scipy.special.comb(total_proteins, in_proteins, exact=True))
    p_value = (term_one * term_two)/term_three
    # p_value = float(p_value)
    return p_value
