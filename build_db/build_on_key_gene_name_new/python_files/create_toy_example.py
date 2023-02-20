"""
This creates the data for the toy example. It uses all 
the data which is stored in the edited_folder, the data is also specfied in
the corresponding lists.
"""

import pandas as pd
if __name__ == '__main__':
    number_rows = 10
    entities = ["TranscriptionFactor.csv", "OpenRegion.csv",
                "string_proteins_filtered.csv",
                "proteins_unique_to_exp_data.csv",
                "KappaTerms.csv"]
    relationships = ["rel_or_wt12h_wt0h.csv",
                     "rel_or_wt336h_wt0h.csv",
                     "rel_or_wtRC12h_wt12h_padj.csv",
                     "rel_or_wt12h_wt0h_padj.csv",
                     "rel_or_wtRC12h_wt0h.csv",
                     "rel_or_wtRC336h_wt0h_padj.csv",
                     "rel_or_wt24h_wt0h.csv",
                     "rel_or_wtRC12h_wt0h_padj.csv",
                     "rel_or_wt24h_wt0h_padj.csv",
                     "rel_or_wtRC12h_wt12h.csv",
                     "rel_protein_wt6h_wt0h.csv",
                     "rel_protein_wtRC12h_wt6h.csv",
                     "rel_protein_wt24h_wt0h.csv",
                     "rel_protein_wt6h_wt0h_padj.csv",
                     "rel_protein_wtRC12h_wt6h_padj.csv",
                     "rel_protein_wt336h_wt0h.csv",
                     "rel_protein_wtRC12h_wt0h_padj.csv",
                     "rel_protein_wt24h_wt0h_padj.csv",
                     "rel_protein_wtRC12h_wt0h.csv",
                     "rel_protein_wtRC336h_wt0h_padj.csv",
                     "TF_target_cor_.csv",
                     "peak_target_cor_.csv",
                     "TF_motif_peak.csv",
                     "rel_string_funtional_terms_to_proteins.csv",
                     "OverlapEdges.csv",
                     "rel_string_proteins_to_proteins.csv"]

    OR = pd.DataFrame({'name': []})

    # time relationships OR
    for i in range(10):
        df = pd.read_csv(("../edited_data/" + relationships[i]),
                         nrows=number_rows)
        df.to_csv(("../final_data/" + relationships[i]), index=None)
    df.rename(columns={"nearest_index": "name"}, inplace=True)
    OR = pd.concat([OR, df[~df['name'].isin(OR['name'])]], ignore_index=True)

    # peak_target_cor.csv
    df = pd.read_csv(("../edited_data/" + relationships[21]),
                     nrows=number_rows, sep='\t')
    df.to_csv(("../final_data/" + relationships[21]), index=None)
    df.rename(columns={'nearest_index': 'name'}, inplace=True)
    OR = pd.concat([OR, df[~df['name'].isin(OR['name'])]], ignore_index=True)

    # TF_motif_peak.csv
    df = pd.read_csv(("../edited_data/" + relationships[22]),
                     nrows=number_rows, sep='\t')
    df.to_csv(("../final_data/" + relationships[22]), index=None)
    df.rename(columns={'peaks': 'name'}, inplace=True)
    OR = pd.concat([OR, df[~df['name'].isin(OR['name'])]], ignore_index=True)

    Proteins = pd.DataFrame({'SYMBOL': []})

    # time relationships Protein
    for i in range(10, 20):
        df = pd.read_csv(("../edited_data/" + relationships[i]),
                         nrows=number_rows)
        df.to_csv(("../final_data/" + relationships[i]), index=None)
    Proteins = pd.concat([Proteins, df[~df['SYMBOL'].isin(Proteins['SYMBOL'])]], ignore_index=True)

    # TF_target_cor.csv
    df = pd.read_csv(("../edited_data/" + relationships[20]),
                     nrows=number_rows, sep='\t')
    df.to_csv(("../final_data/" + relationships[20]), index=None)

    Proteins = pd.concat([Proteins, df[~df['SYMBOL'].isin(Proteins['SYMBOL'])]], ignore_index=True)
    # rel_string_functional_terms_to_proteins.csv
    df = pd.read_csv(("../edited_data/" + relationships[23]),
                     nrows=number_rows)
    df.to_csv(("../final_data/" + relationships[23]), index=None)
    df.rename(columns={'preferred_name': 'SYMBOL'}, inplace=True)
    Proteins = pd.concat([Proteins, df[~df['SYMBOL'].isin(Proteins['SYMBOL'])]], ignore_index=True)

    # peak_target_cor.csv
    df = pd.read_csv(("../edited_data/" + relationships[21]),
                     nrows=number_rows, sep='\t')
    df.rename(columns={'SYMBOL': 'SYMBOL'}, inplace=True)
    Proteins = pd.concat([Proteins, df[~df['SYMBOL'].isin(Proteins['SYMBOL'])]], ignore_index=True)

    # rel_string_proteins_to_proteins.csv
    df = pd.read_csv(("../edited_data/" + relationships[25]),
                     nrows=number_rows)
    df.to_csv(("../final_data/" + relationships[25]), index=None)
    df.rename(columns={'protein1_SYMBOL': 'SYMBOL'}, inplace=True)
    Proteins = pd.concat([Proteins, df[~df['SYMBOL'].isin(Proteins['SYMBOL'])]], ignore_index=True)

    # rel_string_proteins_to_proteins.csv
    df = pd.read_csv(("../edited_data/" + relationships[25]),
                     nrows=number_rows)
    df.to_csv(("../final_data/" + relationships[25]), index=None)
    df.rename(columns={'protein2_SYMBOL': 'SYMBOL'}, inplace=True)
    Proteins = pd.concat([Proteins, df[~df['SYMBOL'].isin(Proteins['SYMBOL'])]], ignore_index=True)

    FunctionalTerms = pd.DataFrame({'term': []})

    # rel_string_functional_terms_to_proteins.csv
    df = pd.read_csv(("../edited_data/" + relationships[23]),
                     nrows=number_rows)
    df.to_csv(("../final_data/" + relationships[23]), index=None)
    FunctionalTerms = pd.concat([FunctionalTerms, df[~df['term'].isin(FunctionalTerms['term'])]],
                            ignore_index=True)

    # "KappaEdges.csv"
    df = pd.read_csv(("../edited_data/" + relationships[24]),
                     nrows=number_rows)
    df.to_csv(("../final_data/" + relationships[24]), index=None)
    df.rename(columns={'source': 'term'}, inplace=True)
    FunctionalTerms = pd.concat([FunctionalTerms, df[~df['term'].isin(FunctionalTerms['term'])]],
                            ignore_index=True)

    # "KappaEdges.csv"
    df = pd.read_csv(("../edited_data/" + relationships[24]),
                     nrows=number_rows)
    df.to_csv(("../final_data/" + relationships[24]), index=None)
    df.rename(columns={'target': 'term'}, inplace=True)
    FunctionalTerms = pd.concat([FunctionalTerms, df[~df['term'].isin(FunctionalTerms['term'])]],
                            ignore_index=True)

    TranscriptionFactors = pd.DataFrame({'TF': []})

    # TF_target_cor.csv
    df = pd.read_csv(("../edited_data/" + relationships[20]),
                     nrows=number_rows, sep='\t')
    TranscriptionFactors = pd.concat([TranscriptionFactors, 
                                  df[~df['TF'].isin(TranscriptionFactors['TF'])]], 
                                 ignore_index=True)

    # TF_motif_peak.csv
    df = pd.read_csv(("../edited_data/" + relationships[22]),
                     nrows=number_rows, sep='\t')
    TranscriptionFactors = pd.concat([TranscriptionFactors, 
                                  df[~df['TF'].isin(TranscriptionFactors['TF'])]], 
                                 ignore_index=True)

    # TranscriptionFactor.csv
    df1 = pd.read_csv(("../edited_data/" + entities[0]))
    df1 = df1[df1['SYMBOL'].isin(TranscriptionFactors['TF'])]
    df1.to_csv(("../final_data/" + entities[0]), index=None)
    # OpenRegion.csv
    df2 = pd.read_csv(("../edited_data/" + entities[1]))
    df2 = df2[df2['nearest_index'].isin(OR['name'])]
    df2.to_csv(("../final_data/" + entities[1]), index=None)
    # "string_proteins_filtered.csv"
    df3 = pd.read_csv(("../edited_data/" + entities[2]))
    df3 = df3[df3['SYMBOL'].isin(Proteins['SYMBOL'])]
    df3.to_csv(("../final_data/" + entities[2]), index=None)
    # "proteins_unique_to_exp_data.csv"
    df4 = pd.read_csv(("../edited_data/" + entities[3]))
    df4 = df4[df4['SYMBOL'].isin(Proteins['SYMBOL'])]
    df4.to_csv(("../final_data/" + entities[3]), index=None)
    # "KappaTerms.csv"
    df5 = pd.read_csv(("../edited_data/" + entities[4]))
    df5 = df5[df5['external_id'].isin(FunctionalTerms['term'])]
    df5.to_csv(("../final_data/" + entities[4]), index=None)
