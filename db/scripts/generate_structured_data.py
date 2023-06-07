CELL_TYPE = "Microglia"
STUDY_SOURCE = "in-house"

def generate_context(values:list[str]) -> list[list]:
    return [[0, values[i], i] for i in range(values)]

def generate_tg(tg_data:list[list[str, list[tuple], float, dict]]):
    """
    tg_data = [identifier, context_values, mean_count, additional_info]
    """
    tg_list = list()
    for i, tg in tg_data:
        identifier, context_values, mean_count, additional_info = tg
        tg_list.append([0, identifier, context_values, mean_count, additional_info, i])
    return tg_list

def generate_tf(tf_data:list[list[str, list[tuple], dict]], source:int, context_values:tuple, additional_info:dict):
    """
    """
    tf_list = list()
    for i, tf in tf_data:
        identifier, context_values, additional_info = tf
        tf_list.append([0, identifier, context_values, additional_info, i])
    return tf_list

def generate_or(source:int, context_values:tuple, mean_count:float, additional_info:dict):
    pass

def generate_functional(category:str, fdr_rade:float, name:str, proteins:list):
    pass

def generate_correlation(source:int, tf_id:int, tg_id:int, correlation:float, p:float):
    pass

def generate_functional_association(tg_1:int, tg_2:int, score:float):
    pass

def generate_motif(or_id:int, tf_id:int, motif:str):
    pass

def generate_distance(or_id:int, tg_id:int, distance:int):
    pass

def generate_functional_overlap(ft_1:int, ft_2:int, score:int):
    pass

def generate_string_association(tg_1:int, tg_2:int, score:float):
    pass
