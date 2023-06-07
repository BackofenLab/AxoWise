from utils import Reformatter
import pandas as pd
import os
from main import _DEFAULT_EXPERIMENT_PATH, _DEFAULT_FUNCTIONAL_PATH, _DEFAULT_STRING_PATH

DE_CONTEXT = ['6h-0h', '24h-0h', '336h-0h', 'RC12h-0h', 'RC12h-6h', '6h-0h-padj', '24h-0h-padj', '336h-0h-padj', 'RC12h-0h-padj', 'RC12h-6h-padj']
DA_CONTEXT = ['12h-0h', '24h-0h', '336h-0h', 'RC12h-0h', 'RC12h-12h', '12h-0h-padj', '24h-0h-padj', '336h-0h-padj', 'RC12h-0h-padj', 'RC12h-12h-padj']

def parse_experiment(dir_path:str = _DEFAULT_EXPERIMENT_PATH, reformat: bool = True):
    def read_experiment():
        """
        Reads Experiment Files from a given path and returns a list of Pandas dataframes,
        where indices are as follows:
        0: DA values
        1: DE values
        2: TF_target_cor
        3: peak_target_cor
        4: TF_motif_peak
        If some of the data is not present, the value will be None.
        """
        dataframes = [None] * 5
        for file in os.scandir(dir_path):
            file_name, file_extention = os.path.splitext(file)
            if file_extention == ".tsv":
                df, index = _reformat_file(
                    df=pd.read_csv(file, sep="\t"), file_name=file_name.split("/")[-1], reformat=reformat
                )
                dataframes[index] = df
        return dataframes
    
    def filter_df_by_context(context:str, df:pd.DataFrame, protein:bool):
        if protein:
            filtered = df.filter(items=['ENSEMBL', context])
            out = pd.DataFrame({'ENSEMBL': filtered['ENSEMBL'], 'Context': context, 'Value': filtered[context]})
        else:
            filtered = df.filter(items=['SYMBOL', context])
            out = pd.DataFrame({'SYMBOL': filtered['SYMBOL'], 'Context': context, 'Value': filtered[context]})
        return out
    
    exp = read_experiment()
    de = exp[1].filter(items=['ENSEMBL', 'ENTREZID', 'SYMBOL', 'annot', 'TF', 'in_ATAC'])
    
    # TODO: gives Loc not DataFrame
    tg_nodes = de.loc(de['TF'].str == "no")
    tf_nodes = de.loc(de['TF'].str == "yes")
    tmp_de = exp[1].filter(items=['ENSEMBL'] + DE_CONTEXT)

    de_reformat = []
    for context in DE_CONTEXT:
        de_reformat.append(filter_df_by_context(context=context, df=tmp_de, protein=True))
    
    de_values = pd.concat(de_reformat)

    or_nodes = exp[0].filter(items=['SYMBOL', 'seqnames', 'summit', 'strand', 'annotation', 'feature', 'in_RNAseq'])
    tmp_da = exp[0].filter(items=['SYMBOL', 'mean_count'] + DA_CONTEXT)
    
    da_reformat = []
    for context in DA_CONTEXT:
        da_reformat.append(filter_df_by_context(context=context, df=tmp_da, protein=False))
    
    da_values = pd.concat(da_reformat)

    tf_tg_corr = exp[2]

    tf_or_corr = exp[3].filter(items=["ENSEMBL", "Correlation", "SYMBOL"])
    
    print(tg_nodes)
    print(tf_nodes)
    print(de_values)
    print(or_nodes)
    print(da_values)
    print(tf_tg_corr)
    print(tf_or_corr)


def read_string(dir_path:str = _DEFAULT_STRING_PATH):
    """
    Reads STRING files and returns a Pandas dataframe
    """
    for file in os.scandir(dir_path):
        df = pd.read_csv(file, sep=" ")
    # TODO: for more files in string dir, extend...
    return df

def read_functional(dir_path:str = _DEFAULT_FUNCTIONAL_PATH):
    for file in os.scandir(dir_path):
        df = pd.read_csv(file, sep=",")
    # TODO: for more files in functional dir, extend...
    return df


def _reformat_file(df: pd.DataFrame, file_name: str, reformat: bool):
    # Filename and function pairs: same index <-> use function for file
    names = ["exp_DA", "exp_DE_filter", "TF_target_cor_", "peak_target_cor_", "TF_motif_peak"]
    functions = [_reformat_DA, _reformat_DE, _reformat_TF_TG, _reformat_OR_TG, _reformat_Motif]
    index = names.index(file_name)

    if not reformat:
        return df, index
    return functions[index](df=df), index


def _reformat_DA(df: pd.DataFrame):
    reformatter = Reformatter("open_region_")

    rename_dict = dict([(old, reformatter.run(old, "tf")) for old in df.columns if "open_region_" in old])
    df = df.rename(columns=rename_dict)
    return df


def _reformat_DE(df: pd.DataFrame):
    reformatter = Reformatter("")

    rename_dict = dict([(old, reformatter.run(old, "tf")) for old in df.columns if "wt" in old])
    df = df.rename(columns=rename_dict)
    return df


def _reformat_TF_TG(df: pd.DataFrame):
    df = df.rename(columns={'nearest_ENSEMBL': 'ENSEMBL', 'TF_target_cor': 'Correlation'})
    return df


def _reformat_OR_TG(df: pd.DataFrame):
    df = df.rename(columns={'nearest_ENSEMBL': 'ENSEMBL', 'peak_target_cor': 'Correlation'})
    return df


def _reformat_Motif(df: pd.DataFrame):
    return df
