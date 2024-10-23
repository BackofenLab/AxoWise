import re
from ast import literal_eval

import ollama


def make_prompt(message, proteins, funct_terms, abstract):
    """
    Create a prompt for the chatbot.
    Args:
        message: Input message from user.
        funct_terms: User selected functional terms to be included in the prompt.
        abstract: User selected abstracts to be included in the prompt.
    Returns:
        prompt: The prompt to be used for response generation.
    """
    functional_term_background = (
        f"Functional terms: {funct_terms} \n" if len(funct_terms) > 0 else ""
    )
    protein_background = f"Proteins: {proteins} \n" if len(proteins) > 0 else ""
    abstracts = f"Scientific Abstracts: {abstract} \n" if len(abstract) > 0 else ""
    functional_term_prompt = (
        "with the background of the provided functional terms, "
        if len(funct_terms) > 0
        else ""
    )
    protein_prompt = (
        f"with the background of the provided proteins, " if len(proteins) > 0 else ""
    )
    abstract_prompt = (
        f"use the information from the {len(abstract)} provided abstracts and state the pmids if used."
        if len(abstract) > 0
        else ""
    )

    final_prompt = f"{protein_background}{functional_term_background}{abstracts}{message}{protein_prompt}{functional_term_prompt}{abstract_prompt}"
    return final_prompt


def populate(data):
    pmids = []
    pmid_abstract = {}
    protein_list = []
    funct_terms_list = []
    for item in data:
        data_type = item["type"]
        entries = [item["data"]] if item["type"] != "subset" else item["data"]
        if data_type == "subset":
            pmids.extend([j["attributes"]["Name"] for j in entries])
            pmid_abstract.update(
                {
                    j["attributes"]["Name"]: j["attributes"]["Abstract"].replace(
                        "'", ""
                    )
                    for j in entries
                }
            )
        elif data_type == "protein":
            protein_list.extend([j["attributes"]["Name"] for j in entries])
        else:
            funct_terms_list.extend([j["name"] for j in entries])
    return pmids, pmid_abstract, protein_list, funct_terms_list


def chat(history, model="llama3.1"):
    """
    Generate a reply from the AI model, (chat history taken into consideration).

    Args:
        model: AI model to be used, defaults to llama3.1
        history: Chat history needed for ai memory, has format: {"role": <user, assistant or system>, "content": <message>}

    Returns:
        response["message"]: reply of the model
    """
    response = ollama.chat(model=model, messages=history, options={"temperature": 0.0})
    return response["message"]


def summarize(input_text, proteins):
    """
    Summarize abstracts obtained by Graph_RAG.

    Args:
        input_text: inputs to be summarized, format is list of lists
        proteins: proteins to be focused on when generating the summary

    Returns:
        flattened_response: List of the summarized abstracts
    """
    raw_response = [
        ollama.generate(
            "llama3.1",
            f"{i} summarize with a focus on {proteins} each one of the {len(i)} abstracts in 30 words into a list i.e format ['summary 1', .. , 'summary n'] dont say anything like here are the summaries or so, make sure it has the correct format for python",
        )["response"]
        for i in input_text
    ]
    cleaned_response = [
        literal_eval(re.sub(r"(?<![\[\],\s])'(?![\[\],])", "", i.replace("\n", "")))
        for i in raw_response
    ]
    flattened_response = [i for j in cleaned_response for i in j]
    return flattened_response
