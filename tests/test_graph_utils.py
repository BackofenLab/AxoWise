import graph_utilities
import json
import pandas as pd
import pytest
import numpy as np


sample_nodedf = pd.DataFrame({'x': pd.Series([-0.062410, 1.092847], dtype='float'),
                   'y': pd.Series([0.285142, -4.993033], dtype='float'),
                   'id': pd.Series([2093704, 2094987 ], dtype='int')})
sample_edgedf = pd.DataFrame({'source': pd.Series([2093704], dtype='int'),
                              'target': pd.Series([2094987], dtype='int'),
                              'id': pd.Series([0], dtype='int')})
sample_cluster = pd.DataFrame([[2093704, -0.062410,  0.285142,    0.515218,   -2.353946],
                               [2094987,  1.092847, -4.993033,    0.515218,   -2.353946]],
                              columns=['id', 'x', 'y','subCentreX', 'subCentreY'])
sample_points = pd.DataFrame({'x': pd.Series([-0.062410, 1.092847], dtype='float'),
                              'y': pd.Series([0.285142, -4.993033], dtype='float'),
                              'id': pd.Series([2093704, 2094987 ], dtype='int')})

@pytest.fixture
def data():
    with open('sample.json') as f:
        data = json.load(f)
    return data



def test_graphdf_create(data):
    edges, nodes = graph_utilities.create_graphdf(data)
    nodes['id'] = nodes['id'].astype(np.int64)
    np.testing.assert_allclose(sample_nodedf, nodes,rtol=1e-4, err_msg="Error in creating dataframes from json")

def test_generate_clusters():
    clusters = graph_utilities.generate_clusters(sample_edgedf, sample_nodedf)
    np.testing.assert_allclose(sample_cluster, clusters, rtol=1e-4, err_msg="Error in generating clusters")


def test_adjust_points():
    new_coord = graph_utilities.adjust_points(sample_cluster)
    np.testing.assert_allclose(sample_points, new_coord, rtol=1e-4, err_msg="Error in adjusting points")


if __name__ == '__main__':
    test_graphdf_create(data)
    test_generate_clusters()
    test_adjust_points()
    print(f"Testing complete")
