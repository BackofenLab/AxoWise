import pandas as pd
import itertools
import time

def getKappaScore(enrichedList: list, proteins: list):
    """ Calculates the kappa-score between all functional enriched terms
    
    Arguments:
        enrichedList(lst): List with the functional enriched terms and their associated proteins
    Returns:
        dataframe with source, target, Kappa-score"""
    # timer
    t_start = time.time()

    # create pandas dataframe
    df = pd.DataFrame()

    
    terms = []
    # TODO Filter for terms, for 100 terms we already calculate (100*99)/2 edges
    # Only use functional terms from GO, KEGG, Reactome, WikiPathways
    for i in enrichedList:
        if (i["category"] == "KEGG"): # or i["category"] == "RCTM" or i["category"] == "WikiPathways"):  # or i["category"] == "Function" or
        # i["category"] == "Component" or i["category"] == "Process"
            terms += [i]

    # take the top 100 fdr values

    terms = sorted(terms, key= lambda x:x["p_value"])[:100]
    # print(terms)
    # print(len(terms))

    for j, k in itertools.combinations(terms, 2):   # binomial coef.len(terms) over 2
        a = 0   # number of proteins that are in term A and in term B
        b = 0   # number of proteins that are in term A and not in term B
        c = 0   # number of proteins that are not in term A and in term B
        d = len(proteins)   # " " that are not in term A and not in term B
        for i in proteins:
            if (i not in j["proteins"] and i not in k["proteins"]):
                continue
            elif (i in j["proteins"] and i not in k["proteins"]):
                b += 1
                d -= 1
            elif (i not in j["proteins"] and i in k["proteins"]):
                c += 1
                d -= 1
            else:
                a += 1
                d -= 1
        
        p_zero = (a+d)/(a+b+c+d)
        marginal_a = ((a+b)*(a+c))/(a+b+c+d)
        marginal_b = ((c+d)*(b+d))/(a+b+c+d)
        p_c = (marginal_a+marginal_b)/(a+b+c+d)
        kappa_score = (p_zero - p_c)/(1 - p_c)              # value between -1 and 1
        if (kappa_score < 0.4):                             # threshold
            continue
        if (df.empty):
            df = pd.DataFrame([[j["name"],k["name"], kappa_score]], columns=["Source", "Target", "Kappa-Score"])
        else:
            # drop_duplicates?
            df_new = pd.DataFrame([[j["name"],k["name"], kappa_score]], columns=["Source", "Target", "Kappa-Score"])
            df = pd.concat([df, df_new])
            
    # sort depending on kappa-score
    df = df.sort_values(by='Kappa-Score', ascending=False)
    df.to_csv("Kappa_Score.csv", index = False, sep=',')
    t_end = time.time()
    print("Time Spent (Kappa-Score):", t_end-t_start)
    return terms