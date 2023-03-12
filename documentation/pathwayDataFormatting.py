import pandas as pd
import argparse
import sys
import csv
import kappa_score
import subset
from ast import literal_eval

def initParser():
    parser = argparse.ArgumentParser(description=
    "Formats the biological pathway data")
    parser.add_argument('prot_terms_file', type=str,
        help='STRING file: File with all proteins and the pathways they are in')
    parser.add_argument('--o', type=str,
    	dest = 'organism', help='organism name (e.g. MusMusculus)')
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
        df = pd.read_csv(args.prot_terms_file, sep='	', engine='python' , quotechar='"')      
        
        # First: Extract only relevant databases out of all databases
        # use only GO, Reactome, WikiPathways databases
        
        df = df.loc[(df['category'] == 'Reactome Pathways') |
        (df['category'] == 'Biological Process (Gene Ontology)') |
        (df['category'] == 'Molecular Function (Gene Ontology)') |
        (df['category'] == 'Cellular Component (Gene Ontology)') |
        (df['category'] == 'WikiPathways')]
        
        # df.to_csv("TermsWithProteins.txt", index = False, sep=',')
        
        lst = []
        terms = df["term"].drop_duplicates().tolist()
        
        df_temp = pd.DataFrame()
        
        # term = df["description"].tolist()
        # nice way to drop duplicates from a list
        # mylist = list(dict.fromkeys(term))
        
        print("length terms: ", len(terms))
        
        
        # Second: Get all pathways with their associated proteins out
        # of the filtered dataframe 
        # Create new df with functional terms as id
        
        df_new = pd.DataFrame()
        
        category = ''
        description = ''
        myList = []
        
        prog = 0
        for i in terms:
            df_temp = df.loc[df['term'] == i]
            category = df_temp['category'].iat[0]
            description = df_temp['description'].iat[0]
            print('description: ', description)
            list_temp = []
            proteins = []
            for j, k in df_temp.iterrows():
                proteins += [k['#string_protein_id']]  
            list_temp = [i, description, category, proteins]
            myList += [list_temp]
            prog += 1
            print('Progress: ', prog)

        df_new = pd.DataFrame(myList, columns=['Term', 'Description', 'Category', 'Proteins'])            
        df_new.to_csv(args.organism + "TermsWithProteins.txt", index = False, sep=',')
