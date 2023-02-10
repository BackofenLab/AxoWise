import pandas as pd
import itertools
import time
from ast import literal_eval

def get_subsets(lst: list):
    list_df = []
    for j, k in itertools.combinations(lst, 2):
        prot_one = literal_eval(j['proteins'])
        prot_two = literal_eval(k['proteins'])
        set1 = frozenset(prot_one)
        set2 = frozenset(prot_two)
        intersection = set1.intersection(set2)
        min_set = min(len(set1), len(set2))
    	
        overlap_score = len(intersection) / min_set
        
        if (overlap_score >= 0.5):
            row = [j['name'], k['name'], overlap_score]
            # row = [j['term_id'], k['term_id'], kappa_score]
            list_df += [row]
    df = pd.DataFrame(list_df, columns=["source", "target", "score"])
    df = df.sort_values(by='score', ascending=False)
    
    return df
