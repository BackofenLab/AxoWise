import re

import ollama


def make_prompt(message="", proteins=None, funct_terms=None, abstract=None):
    """
    Create a prompt for the chatbot.
    Args:
        message: Input message from user.
        funct_terms: User selected functional terms to be included in the prompt.
        abstract: User selected abstracts to be included in the prompt.

    Returns:
        prompt: The prompt to be used for response generation.
    """
    functional_term_background = f"Functional terms: {funct_terms} \n" if funct_terms else ""
    protein_background = f"Proteins: {proteins} \n" if proteins else ""
    abstracts = f"Scientific Abstracts: {abstract} \n" if abstract else ""
    functional_term_prompt = "with the background of the provided functional terms, " if funct_terms else ""
    protein_prompt = "using only the provided proteins stating a synonym if used." if proteins else ""
    abstract_prompt = (
        f"use the information from the {len(abstract)} provided abstracts and state the pmids if used."
        if abstract
        else ""
    )

    final_prompt = f"{protein_background}{functional_term_background}{abstracts}{message} {functional_term_prompt}{abstract_prompt}{protein_prompt}"
    return final_prompt


def populate(data):
    pmids = []
    pmid_abstract = {}
    protein_list = []
    funct_terms_list = []
    for item in data:
        data_mode = item["mode"]
        data_type = item["type"]
        entries = [item["data"]] if item["type"] != "subset" else item["data"]
        if data_mode == "citation":
            pmids.extend([j["attributes"]["Name"] for j in entries])
            pmid_abstract.update(
                {j["attributes"]["Name"]: j["attributes"]["Abstract"].replace("'", "") for j in entries}
            )
        elif data_mode == "protein":
            if data_type == "term":
                funct_terms_list.extend([j["name"] for j in entries])
            else:
                protein_list.extend([j["attributes"]["Name"] for j in entries])
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


def clean_abstracts(input_list):
    """
    Clean raw summarized text from AI model to get a single list, rather than batches of summarized text
    """
    # Initialize a list to store cleaned abstracts
    cleaned_abstracts = []

    # Iterate over each string in the input list
    for string in input_list:
        # Remove unwanted characters such as brackets and newline characters
        cleaned_text = re.sub(r"[\[\]\n']", "", string)
        # Split each cleaned string by ', ' to get individual abstracts
        individual_abstracts = cleaned_text.split(", ")
        # Extend the cleaned_abstracts list with the current individual abstracts
        cleaned_abstracts.extend(individual_abstracts)

    return cleaned_abstracts


def summarize(input_text, proteins, model="llama3.1"):
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
            model,
            f"""{i} create a summary of each one of the {len(i)} abstracts in 30 words into a list i.e format ['summary 1', .. , 'summary n']
                dont say anything like here are the summaries or so, make sure it has the correct format for python and make sure to keep any
                information regarding {proteins}
            """,
        )["response"]
        for i in input_text
    ]
    cleaned_response = clean_abstracts(raw_response)
    return cleaned_response
