from ast import literal_eval
import time
from igraph import Graph
import leidenalg as la
import summarization.meilisearch_inhouse.meilisearch_query as query
from summarization.model import create_summary


def citations_pagerank(graph):
    """
    Return a list of pagerank scores.

    Arguments:
    graph: an igraph graph
    """

    pagerank = graph.pagerank()
    return pagerank


def create_cluster_pagerank_mapping(pagerank, communities):
    """
    Calculates the pagerank score of each cluster by summing up the pagerank
    of each individual node in that cluster (community)

    returns: mapping of cluster:pagerank_value
    """
    mapping = {}
    for num, i in enumerate(communities):
        pagerank_score = 0
        for j in list(i):
            pagerank_score += pagerank[j]
        mapping[str(num)] = pagerank_score
    return mapping


def communities_sorted_by_pagerank(pagerank_dict):
    """
    Return the keys of the top k performing communities based on their pagerank (sorted)
    """
    top_k_communities = sorted(pagerank_dict.items(), key=lambda x: x[1], reverse=True)
    return [int(i[0]) for i in top_k_communities]


def create_citations_graph(limit, search_query, tokenizer, model):
    """
    Return a tuple of(networkit_graph, node_mapping)

    Arguments:
    limit: The limit of returned hits from meilisearch
    query: User query that wants to be summarized
    """

    begin = time.time()

    # Call Meilisearch to retrieve results
    file = query.get_results(limit, search_query)
    print(f"Meilisearch: {time.time() - begin}")

    # Initialize an empty directed graph
    graph = Graph(directed=True)
    abstracts = {}

    # Initialize mappings and variables
    node_mapping = {}
    pmids = set()
    integer_id = 0
    hits = file["hits"]
    node_names = []
    edges = []
    nodes = []

    # Process hits and add nodes to the graph, also add abstracts to mapping
    for hit in hits:
        pmid = str(hit["PubMed ID"])
        if pmid not in pmids:
            year = hit["Published"]
            abstract = hit["Abstract"]
            title = hit["Title"]
            citations = hit["Cited number"]
            abstracts[pmid] = {"abstract": abstract, "year": year, "cited_by": citations}
            pmids.add(pmid)
            node_mapping[pmid] = integer_id
            integer_id += 1
            node_names.append(pmid)
            nodes.append(
                {"external_id": str(pmid), "abstract": abstract, "year": year, "cited_by": citations, "title": title}
            )

    # Add edges to the graph
    for hit in hits:
        pmid = str(hit["PubMed ID"])
        cited_by = literal_eval(hit["Cited by"])
        target = node_mapping[pmid]
        for source in cited_by:
            if str(source) in node_mapping:
                if node_mapping[str(source)] != target:
                    edges.append((node_mapping[str(source)], target))
    graph.add_vertices(node_names)
    graph.add_edges(edges)
    print(f"Graph creation: {time.time()-begin}s")

    # Pagerank calculations
    begin = time.time()
    pagerank = citations_pagerank(graph)
    node_pagerank_mapping = {str(i): j for i, j in enumerate(pagerank)}
    print(f"pagerank: {time.time()-begin}s")

    # Community calculations
    begin = time.time()
    communities = la.find_partition(graph, la.ModularityVertexPartition)
    print(f"community creation: {time.time()-begin}")

    # Top community and node detection
    begin = time.time()
    cluster_pagerank = create_cluster_pagerank_mapping(pagerank, communities)
    best_communities = communities_sorted_by_pagerank(cluster_pagerank)
    best_communities = best_communities[:5]
    begin = time.time()
    top_nodes = []
    for i in best_communities:
        community = communities[i]
        top1 = None
        top2 = None
        for i in community:
            pagerank_i = node_pagerank_mapping[str(i)]
            if top1 is None or pagerank_i > node_pagerank_mapping[str(top1)]:
                top2 = top1
                top1 = i
            elif top2 is None or pagerank_i > node_pagerank_mapping[str(top2)]:
                top2 = i
        if top2 is not None:
            top_nodes.append([top1, top2])
        else:
            top_nodes.append(top1)
    summarized_dict = {}
    to_summarize = []
    check_edges = set()
    for i in top_nodes:
        if isinstance(i, list):
            name = str(graph.vs(i[0])["name"][0])
            node = str(i[0])
        else:
            name = str(graph.vs(i)["name"][0])
            node = str(i)
        to_summarize.append((abstracts[name]["abstract"], name))
        check_edges.add(name)
        summarized_dict[name] = {
            "external_id": name,
            "pagerank": node_pagerank_mapping[node],
            "year": abstracts[name]["year"],
            "cited_by": abstracts[name]["cited_by"],
        }

    edge_list = []
    edge_mapping = dict((v, k) for k, v in node_mapping.items())
    for source, target in edges:
        edge_list.append({"source": edge_mapping[source], "target": edge_mapping[target], "score": 1})
    """summary_time = time.time()
    summary = create_summary(to_summarize, tokenizer, model)
    for i in summary:
        summarized_dict[i[1]]["summary"] = i[0]
    print(f"summarization: {time.time()-summary_time}")"""
    return edge_list, nodes
