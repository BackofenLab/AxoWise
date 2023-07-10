import networkit as nk
import pandas as pd


def nk_graph(nodes, edges):
    """
    Return a tuple of(networkit_graph, node_mapping)

    Arguments:
    nodes: nodes to be added to the graph, in our case a pd dataframe.
    edges: edges to be added to the graph, also a pd dataframe.
    """

    # Create an empty graph
    graph = nk.Graph()

    # Create a mapping between string node IDs and integer node IDs
    node_mapping = {}
    integer_id = 0
    for node_id in nodes["external_id"]:
        graph.addNode()
        node_mapping[node_id] = integer_id
        integer_id += 1
    # Add edges to the graph using integer node IDs
    for edge in edges[["source", "target"]].itertuples(index=False):
        source = node_mapping[edge.source]
        target = node_mapping[edge.target]
        graph.addEdge(source, target)
    return graph, node_mapping


def create_nodes_subgraph(graph, nodes):
    """
    Returns Dataframe of isolated nodes

    Arguments:
    graph: a networkit graph.
    subnodes: dataframe of the nodes
    """

    nodes_list = []
    main_component = nk.components.ConnectedComponents(graph).run()
    g = main_component.extractLargestConnectedComponent(graph)
    for i in g.iterNodes():
        nodes_list.append(nodes.iloc[i])
    new_df = pd.DataFrame(nodes_list)
    return new_df


def betweenness(graph):
    """
    Return a list of betweenness scores through networkit.

    Arguments:
    graph: a networkit graph
    """

    scores = nk.centrality.Betweenness(graph).run().scores()
    return scores


def pagerank(graph):
    """
    Return a list of pagerank scores through networkit.

    Arguments:
    graph: a networkit graph
    """

    scores = nk.centrality.PageRank(graph).run().scores()
    return scores


def eigenvector_centrality(graph):
    """
    Return a list of Eigenvector centrality scores through networkit.

    Arguments:
    graph: a networkit graph
    """

    scores = nk.centrality.EigenvectorCentrality(graph).run().scores()
    return scores
