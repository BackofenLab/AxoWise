import time
from ast import literal_eval

import leidenalg as la
import numpy as np
from igraph import Graph
from langchain_ollama.embeddings import OllamaEmbeddings
from queries import get_abstracts
from summarization.chat_bot import summarize
from util.stopwatch import Stopwatch


def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


def generate_embedding(query):
    embedder = OllamaEmbeddings(model="llama3.1")
    embeddings = embedder.embed_query(query)
    return embeddings


def top_n_similar_vectors(input_vector, vectors, n):
    """Find the top n most similar vectors to the input_vector."""
    similarities = []

    for vector in vectors:
        similiars = cosine_similarity(input_vector, vector["abstractEmbedding"])
        similarities.append((vector["PMID"], similiars))

    # Sort by similarity score in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Get the top n similar vectors
    top_n = similarities[:n]
    top_n = [i[0] for i in top_n]
    return top_n


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


def create_citations_graph(driver, species, search_query):
    """
    Return a tuple of(networkit_graph, node_mapping)

    Arguments:
    limit: The limit of returned hits from meilisearch
    query: User query that wants to be summarized
    """

    begin = time.time()

    # Call neo4j to retrieve results
    results = get_abstracts(driver, species, search_query)
    print(f"Neo4j for abstracts: {time.time() - begin}")
    # Initialize an empty directed graph
    graph = Graph(directed=True)
    abstracts = {}

    # Initialize mappings and variables
    node_mapping = {}
    pmids = set()
    integer_id = 0
    node_names = []
    edges = []
    nodes = []

    # Process hits and add nodes to the graph, also add abstracts to mapping
    for hit in results:
        pmid = str(hit["PMID"])
        if pmid not in pmids:
            year = hit["published"]
            abstract = hit["abstract"]
            title = hit["title"]
            citations = hit["times_cited"]
            abstracts[pmid] = {
                "abstract": abstract,
                "year": year,
                "cited_by": citations,
            }
            pmids.add(pmid)
            node_mapping[pmid] = integer_id
            integer_id += 1
            node_names.append(pmid)
            nodes.append(
                {
                    "external_id": str(pmid),
                    "abstract": abstract,
                    "year": year,
                    "cited_by": citations,
                    "title": title,
                }
            )

    # Add edges to the graph
    for hit in results:
        pmid = str(hit["PMID"])
        cited_by = literal_eval(hit["citations"])
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
        top_nodes.append(
            sorted(
                [
                    (abstracts[str(graph.vs(i)["name"][0])]["abstract"])
                    for i in community
                ],
                key=lambda x: x[1],
                reverse=True,
            )[:2]
        )
    edge_list = []
    edge_mapping = dict((v, k) for k, v in node_mapping.items())
    for source, target in edges:
        edge_list.append(
            {"source": edge_mapping[source], "target": edge_mapping[target], "score": 1}
        )
    return edge_list, nodes


def get_most_relevant_abstracts(message, pmids_embeddings, pmid_abstract, protein_list):
    """
    Using vector search, obtain abstracts most similiar to the input message. These abstracts are summarized to
    then be returned for further processing.

    Args:
        message: user input
        pmids_embeddings: dictionary of format {pmid: embedding} of all abstracts to be searched with vector search
        pmid_abstract: dictionary of format {pmid: abstract}
        protein_list: list of proteins to be taken into account in summarization of abstracts
    Returns:
        abstracts: Abstracts obtained from vector search in format list of dictionaries
                    (each dictionary is format: {Abstract <abstract_i> with PMID <pmid>: summarized abstract})
        top_n_similiar: pmids of the most similiar abstracts
    """
    stopwatch = Stopwatch()
    embedded_query = generate_embedding(str(message))
    stopwatch.round("Embedding query")
    top_n_similiar = top_n_similar_vectors(embedded_query, pmids_embeddings, 6)
    stopwatch.round("Vector search")
    unsummarized = [
        [pmid_abstract[i] for i in top_n_similiar[j : j + 3]]
        for j in range(0, len(top_n_similiar), 3)
    ]
    summarized = summarize(unsummarized, protein_list)
    stopwatch.round("Summarize in batches")
    abstracts = [
        f"Abstract {num+1} with PMID {i}: {summarized[num]}"
        for num, i in enumerate(top_n_similiar)
    ]
    return abstracts, top_n_similiar
