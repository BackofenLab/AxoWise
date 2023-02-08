import pandas as pd
import itertools
import time
from ast import literal_eval

def getKappaScore(enrichedList: list, proteins: list): # , df_kapp):
    """ Calculates the kappa-score between all functional enriched terms
    
    Arguments:
        enrichedList(list): List with the functional enriched terms and their associated proteins
        proteins(list): list of all proteins of the organism
        df_kapp(dataframe): pandas dataframe with saved kappa_scores to be concatenated with new ones
    Returns:
        dataframe with source, target, score"""
    # timer
    t_start = time.time()

    # create pandas dataframe
    df = pd.DataFrame()
    
    list_df = []
    comb_terms = []
    num_prots = len(proteins)
    n = len(enrichedList) - 1
    length = (len(enrichedList) * n)/ 2 	# len(itertools.combinations(enrichedList, 2))
    length_one = 0
    length_two = 0
    progress = 0
    mod = 0
    
    list_div = []
    counter = 0
                
    a = 0			# number of proteins that are in term A and in term B
    b = 0			# number of proteins that are in term A and not in term B
    c = 0			# number of proteins that are not in term A and in term B
    d = 0			# " " that are not in term A and not in term B
    
    # print(enrichedList)
                
    for j, k in itertools.combinations(enrichedList, 2):   # binomial coef.len(terms) over 2
        row = []
        mod += 1
        
        # list get converted into string when loading from csv
        # use literal_eval to convert them back
        prot_one = literal_eval(j['proteins'])
        prot_two = literal_eval(k['proteins'])
        length_one = len(prot_one)
        length_two = len(prot_two)
        
        a = len(list(set(prot_one) & set(prot_two)))			
        b = length_one - a			
        c = length_two - a			
        d = num_prots - a - b - c
        
        if (mod % n == 0):
            n -= 1
            counter += 1
            mod = 0
            print("\n New term")
            print(counter)
        # Check save
        if (counter == 2000):
            df = pd.DataFrame(list_df, columns=["Source", "Target", "Score"])
            df.to_csv("Kappa_Score_Two.csv", index = False, sep=',')
        p_zero = (a+d)/(a+b+c+d)
        marginal_a = ((a+b)*(a+c))/(a+b+c+d)
        marginal_b = ((c+d)*(b+d))/(a+b+c+d)
        p_c = (marginal_a + marginal_b)/(a+b+c+d)
        # Should not happen with complete protein set
        if (p_c == 1):
            continue
        kappa_score = (p_zero - p_c)/(1 - p_c)              # value between -1 and 1
        if (kappa_score < 0.4):                             # threshold
            progress += 1
            continue
        #dic_a = {'id':j["term_id"], 'name':j['description'], 'category':j['category'], 'proteins':j['proteins']}
        #dic_b = {'id':k["term_id"], 'name':k['description'], 'category':k['category'], 'proteins':k['proteins']}
        row = [j['term_id'], k['term_id'], kappa_score]
        list_df += [row]
        progress += 1
        print("\n Progress: (" + str(progress) + "/" + str(length) + ")")
        if ((len(list_df) % 1000) == 0):
            df = pd.DataFrame(list_df, columns=["source", "target", "score"])
            df.to_csv("Kappa_Edges_KEGG.csv", index = False, sep=',')
        
    df = pd.DataFrame(list_df, columns=["source", "target", "score"])
    # df = pd.concat([df_kapp, df])
    if (len(enrichedList) != 0):
        # sort depending on kappa-score
        df = df.sort_values(by='score', ascending=False)
    df.to_csv("Kappa_Edges_KEGG.csv", index = False, sep=',')
    t_end = time.time()
    print("Time Spent (Kappa-Score):", t_end-t_start)
    return df
