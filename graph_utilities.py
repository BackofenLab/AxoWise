import numpy as np
import pandas as pd
import networkx as nx


def adjust_graph(data):
    nodedf = pd.DataFrame(data['nodes'], columns=['x', 'y', 'id'])
    edgedf = pd.DataFrame(data['edges'], columns=['source', 'target', 'id'])
    return draw_network(edgedf, nodedf)


def draw_network(edges, nodedata):
    protein_g = nx.from_pandas_edgelist(edges, 'source', 'target', True, nx.Graph())
    nx.set_node_attributes(protein_g, nodedata.set_index('id').to_dict('index'))

    subgraphs = []
    components = nx.connected_components(protein_g)
    column_names = ['id', 'x', 'y']

    for component in components:
        coord = pd.DataFrame(np.array([(n, v['x'], v['y']) for n, v in protein_g.nodes(data=True) if n in component]),
                             columns=column_names)
        coord['x'] = pd.to_numeric(coord['x'])
        coord['y'] = pd.to_numeric(coord['y'])
        coord['id'] = pd.to_numeric(coord['id'])
        coord['subCentreX'] = coord['x'].sum()/len(coord)
        coord['subCentreY'] = coord['y'].sum()/len(coord)
        subgraphs.append(coord)

    return data_frame_op(pd.concat(subgraphs))


def data_frame_op(graphdata):

    graphdata['centreX'] = graphdata['subCentreX'].unique().sum() / graphdata['subCentreX'].nunique()
    graphdata['centreY'] = graphdata['subCentreY'].unique().sum() / graphdata['subCentreY'].nunique()
    graphdata['newCX'] = (graphdata['centreX'] + graphdata['subCentreX']) / 2
    graphdata['newCY'] = (graphdata['centreY'] + graphdata['subCentreY']) / 2

    graphdata['x'] = graphdata['x'] + (graphdata['newCX'] - graphdata['subCentreX'])
    graphdata['y'] = graphdata['y'] + (graphdata['newCY'] - graphdata['subCentreY'])

    return graphdata[['x', 'y', 'id']]
