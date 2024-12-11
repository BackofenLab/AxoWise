import matplotlib.pyplot as plt
from collections import Counter
import os
import pandas as pd


def data():

    dic = {'bioactmat':'Bioactive Materials',
           '/s13024':'Mole. Neurodegeneration',
           '/s12943':'Mole. Cancer',
           'j.cmet':'Cell Metabolism',
           '/s41590':'Nat. Immunology',
           '/s41587':'Nat. Biotech.',
           '/nbt':'Nat. Biotech.',
           'j.stem':'Cell Stem Cell',
           'j.chom':'Cell Host & Microbe',
           '/s41556':'Nat. Cell Bio.',
           'j.ccell':'Cancer Cell',
           'gutjnl':'Gut',
           'neuonc':'Neuro-Oncology',
           'j.immuni':'Immunity',
           'j.gastro':'Gastroenterology',
           'CIRCULATIONAHA':'Circulation',
           '/s13045':'J. Hematology & Oncology',
           'annrheumdis':'A. Rheumatic Diseases',
           'S1473':'L. Infectious Diseases',
           '/s41392':'Signal Trans. TT',
           '/nar/':'Nucleic Acids R.',
           'scitranslmed':'Sci. Trans. Medicine',
           '/S1470':'Lancet Oncology',
           '/nsr/':'National Sci. Review',
           'j.jhep':'J. of Hepatology',
           '/s40779':'Military Medical R.',
           '/S2666':'Lancet Microbe',
           '/s41551':'Nat. Biomed. Eng.',
           '/s41423':'Cellular & Mole. Imm.',
           'nmeth':'Nat. Methods',
           '/s43018':'Nat. Cancer',
           '/s42255':'Nat. Metabolism',
           '/s41593':'Nat. Neuroscience',
           '/s41588':'Nat. Genetics',
           '/s41591':'Nat. Medicine',
           '/s41564':'Nat. Microbio.',
           '/s41565':'Nat. Nanotech.',
           'sciimmunol':'Sci. Imm.',
           '/science.':'Science',
           'j.cell':'Cell',
           '/s41586':'Nature',
           'j.scib':'Sci. Bulletin',
           '.CD-':'Cancer Discovery',
           '/s41422':'Cell Research',
           '/cr.':'Cell Research'}

    doi_files = [f for f in os.listdir('.') if f.startswith('_') and f.endswith('.txt') if 'no_data' not in f if 'error_list' not in f]
    
    no_data_files = [f for f in os.listdir('.') if f.startswith('_') and f.endswith('_no_data.txt')]
    
    return (dic, doi_files, no_data_files)

def count_total_nodata(doi_files, no_data_files, total_c, no_data_c, j_dict):
    
    for iteration in doi_files:
        with open(iteration, "r") as f:
            for line in f:
                line = line.strip()  # Remove whitespace/newlines
                for j_name, full_name in j_dict.items():
                    if j_name in line:
                        total_c[full_name] += 1
    
    for iteration in no_data_files:
        if '_Nature Microbiology_Nature Nanotechnology_Science Immunology_no_data.txt' in iteration:
            continue
        with open(iteration, "r") as f:
            for line in f:
                line = line.strip()  # Remove whitespace/newlines
                for j_name, full_name in j_dict.items():
                    if j_name in line:
                        no_data_c[full_name] += 1

    return(total_c, no_data_c)

def calc_data_found(total_c, no_data_c, dic):
    new_dic = {}
    for item in dic.values():
        # print(item)
        data_found = total_c[item] - no_data_c[item]
        new_dic[item] = {'data_found': data_found,
                         'no_data': no_data_c[item]}
    
    return new_dic

def plot_data(counter_dict):

    df_data = []
    for journal, counts in counter_dict.items():
        df_data.append({
            'Journal': journal,
            'Data found': counts['data_found'],
            'No data found': counts['no_data']
        })
    
    df = pd.DataFrame(df_data)
    
    df['Total'] = df['Data found'] + df['No data found']
    df = df.sort_values('Total', ascending=True)
    
    plt.figure(figsize=(12, 16))
    
    bar_plot = df.plot(
        x='Journal',
        y=['Data found', 'No data found'],
        kind='barh',
        stacked=True,
        color=['#2ecc71', '#e74c3c'],
        figsize=(12, 16)
    )
    
    plt.title('Data Availability in Scientific Publications by Journal', pad=20, fontsize=14)
    plt.xlabel('Number of Publications', fontsize=12)
    plt.ylabel('Journal', fontsize=12)
    
    plt.legend(title='Publication Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    for i in bar_plot.containers:
        bar_plot.bar_label(i, label_type='center')
    
    plt.tight_layout()
    
    plt.savefig('journal_data_distribution.png', bbox_inches='tight', dpi=300)
    plt.close()



if __name__ == "__main__":
    """ Generalize the code """

    total_c = Counter()
    no_data_c = Counter()
    j_dict, doi_files, no_data_files = data()
    
    total_counter, no_data_counter = count_total_nodata(doi_files, no_data_files, total_c, no_data_c, j_dict)

    counter_dict = calc_data_found(total_counter, no_data_counter, j_dict)

    plot_data(counter_dict)