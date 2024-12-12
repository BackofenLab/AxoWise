import os
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from dotenv import load_dotenv
import neo4j
from summarization.article_graph import generate_embedding
from summarization.chat_bot import summarize
from queries import get_functional_term_proteins, cosine_similiarity, neo4j_vector_search, get_abstract
import ollama
from ReactAgent import ReActAgent

llm = Ollama(model="llama3.1")

def get_driver():
    load_dotenv()

    # set config
    NEO4J_HOST = os.getenv("NEO4J_HOST")
    NEO4J_PORT = os.getenv("NEO4J_PORT")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    # connect
    uri = f"bolt://{NEO4J_HOST}:{NEO4J_PORT}"
    driver = neo4j.GraphDatabase.driver(uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    return driver

def vector_search_abstracts(question: str, pmids: list, protein: list = None):
    """"Fetches protein abstracts, given a question. Not for functional terms. the first argument is the question, the second argument are the pmids to search through in format list of strings, 
    the third argument are proteins if mentioned in the question (can be an empty list if no protein is mentioned in the question)."""
    if protein is None:
        protein = []
    driver = get_driver()
    embedded_query = generate_embedding(query=question)
    if pmids:
        most_similiar = cosine_similiarity(driver=driver, pmids=pmids, embedding=embedded_query)
    else:
        most_similiar = neo4j_vector_search(driver=driver, embedding=embedded_query)
    abstracts = [f'PMID {i["PMID"]}: {i["abstract"]}' for i in most_similiar]
    abstracts_chunked = [abstracts[i:i + 3] for i in range(0, len(abstracts), 3)]
    abstracts = summarize(abstracts_chunked, protein)
    if len(abstracts) == 0:
        return "No abstracts found, maybe use another tool? The format for this tool is query:list, question:str, protein:list"
    return "\n".join(abstracts)

def fetch_proteins_from_functional_terms(funct_term:list):
    "Queries neo4j to retrieve proteins associated to functional terms. Never use this tool unless Functional term(s) are provided in the question."
    driver = get_driver()
    proteins = get_functional_term_proteins(driver, funct_term)
    proteins = [f'{i["name"]}: {i["symbols"]}'for i in proteins]
    driver.close()
    if len(proteins) == 0:
        return ["No proteins found, is your query maybe better suited for another tool?"]
    return "\n".join(proteins)

def summarize_abstracts(abstracts: list):
    """Summarizes information extracted from provided abstracts. If only PMIDS are provided call fetch_abstracts first. The format for this tool is abstracts:list"""
    prompt = f"{abstracts}. Summarize the information and keep all pmids"
    response = ollama.generate(prompt=prompt, model="llama3.1")["response"]
    return response

def fetch_and_summarize_abstracts(pmids: list):
    """Fetches abstracts from provided pmids and summarizes the information. The format for this tool is pmids:list. where the pmids are just the ids eg. ["12345678", "12345679"]
    not ["PMID 12345678", "PMID 12345679"]"""
    driver = get_driver()
    abstracts = get_abstract(driver=driver ,pmid=pmids,)
    abstracts = [f'PMID {i["PMID"]}: {i["abstract"]}' for i in abstracts]
    abstracts_chunked = [abstracts[i:i + 3] for i in range(0, len(abstracts), 3)]
    abstracts = summarize(abstracts_chunked)
    return abstracts

def setup():
    fetch_protein_abstracts = FunctionTool.from_defaults(fn=fetch_and_summarize_abstracts, return_direct=True)
    summarize_abstract_information = FunctionTool.from_defaults(fn=vector_search_abstracts, return_direct=True)
    summarizer = FunctionTool.from_defaults(fn=summarize_abstracts, return_direct=True)
    tools = [summarizer, fetch_protein_abstracts, summarize_abstract_information]
    agent = ReActAgent(tools=tools, llm=llm, timeout= 160)
    return agent

async def call_agent(query):
    agent = setup()
    response = await agent.run(input=query)
    return response["response"]