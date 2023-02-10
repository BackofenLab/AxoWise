import pandas as pd
import argparse
import sys
import csv
import kappa_score
import subset
from ast import literal_eval

def initParser():
    parser = argparse.ArgumentParser(description="Converts protein ids into protein names")
    
    # metavar: alternative name for input when using help
    # nargs: number of arguments
    parser.add_argument('prot_terms_file', type=str,
        help='STRING_organism-file, needed for conversion from protein-term file to term-proteins file')
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
        # df_kapp = pd.read_csv(args.df, sep=',', engine='python') 	# , quotechar='"')
        
        # NOTE: AT each step (first, second,...) the updated dataframe is used,
        # all steps work as single program
        
        # First: Extract only relevant databases out of all databases
        # use only GO, Reactome, WikiPathways databases
        
        """df = df.loc[(df['category'] == 'Reactome Pathways') |
        (df['category'] == 'Biological Process (Gene Ontology)') |
        (df['category'] == 'Molecular Function (Gene Ontology)') |
        (df['category'] == 'Cellular Component (Gene Ontology)') |
        (df['category'] == 'WikiPathways')]"""
        
        # df.to_csv("TermsWithProteins.txt", index = False, sep=',')
        
        """ lst = []
        terms = df["term"].drop_duplicates().tolist()
        
        df_temp = pd.DataFrame()
        
        # term = df["description"].tolist()
        # nice way to drop duplicates from a list
        # mylist = list(dict.fromkeys(term))
        
        print("length: ", len(terms))
        
        
        # Second: Get all functional terms with their associated proteins out
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
        df_new.to_csv("TermsWithProteins.txt", index = False, sep=',')"""
        
        # Third: Convert Dataframe into list of dictionaries for KappaScore calculation
        # Get proteins out of protein file"""
        
        lst = []
        
        for index, j in df.iterrows():
            dic = {}
            dic['term_id'] = j['external_id']
            dic['name'] = j['name']
            dic['category'] = j['category']
            dic['proteins'] = j['proteins']
            lst += [dic]
        # print(lst)
        proteins = df_prot['#string_protein_id'].tolist()

        # print("Proteins: ", proteins)
        # print(len(proteins))
        
        # print("List: ", lst)
        df_kappa = kappa_score.getKappaScore(lst, proteins)# , df_kapp)
        
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
        
        df_overlap.to_csv("Kappa_Edges_test_overlap.csv", index = False, sep=',')

        
        
