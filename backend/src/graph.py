import networkx as nx
import pandas as pd


def create_nodes_subgraph(dataframe: pd.DataFrame, subnodes):
    graphtype = nx.Graph()
    nodes_list = []
    graph = nx.from_pandas_edgelist(dataframe, "source", "target", create_using=graphtype)
    main_component = max(nx.connected_components(graph), key=len)
    for i in main_component:
        loc_sub = subnodes.loc[subnodes["external_id"] == i]
        dict_sub = loc_sub.to_dict("records")
        nodes_list.append(dict_sub[0])
    new_df = pd.DataFrame(nodes_list)
    return new_df
