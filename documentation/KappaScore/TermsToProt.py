import pandas as pd
import argparse
import sys
import csv
import kappa_score
import subset
from ast import literal_eval

def initParser():
    parser = argparse.ArgumentParser(description=
    "Formats the biological data and calculates kappa- and overlap-score")
    parser.add_argument('prot_terms_file', type=str,
        help='Pathway file: File with all pathways and their associated proteins')
    parser.add_argument('--proteins', type=str,
        dest='prot', help="File that contains all proteins of an organism")
    #parser.add_argument('--df', type=str,
    #    dest='df', help="dataframe with Kappa-Scores")
        
    
    return parser

# _______________Can be called as main__________________
if __name__ == '__main__':
    parser = initParser()    
    args = parser.parse_args()
    
    if args.prot_terms_file:
        # input file of user
        csv.field_size_limit(sys.maxsize)
        df = pd.read_csv(args.prot_terms_file, sep=',', engine='python' , quotechar='"')      
        df_prot = pd.read_csv(args.prot, sep='	', engine='python') 	# , quotechar='"')
        
        # Get proteins out of protein file"""
        
        lst = []
        
        for index, j in df.iterrows():
            dic = {}
            dic['term_id'] = j['external_id']
            dic['name'] = j['name']
            dic['category'] = j['category']
            dic['proteins'] = j['proteins']
            lst += [dic]
        proteins = df_prot['#string_protein_id'].tolist()

        df_kappa = kappa_score.getKappaScore(lst, proteins)
        
        df_overlap = subset.get_subsets(lst)
        
        lst_kappa = df_kappa["source"].tolist()
        lst_kappa += df_kappa["target"].tolist()
        set_kappa = set(lst_kappa)
        
        for i,j in df_overlap.iterrows():
            if (j["source"] not in set_kappa):
                print(j["source"])
                df_overlap.drop(i, inplace=True)
        for i,j in df_overlap.iterrows():
            if (j["target"] not in set_kappa):
                print(j["target"])
                df_overlap.drop(i, inplace=True)
            #if (j["target"] not in set_kappa):
            #    df_overlap.drop(i, inplace=True)
        
        df_overlap.to_csv("Overlap_Edges_test.csv", index = False, sep=',')

        
        
