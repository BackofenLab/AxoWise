import meilisearch
import json
import Api_key
import pandas as pd


def build_query():
    """
    Function to search meilisearch, returns results.json file

    User/frontend supplies the query and index - hardcoded index atm

    Build 2 queries if one of the symbols has a full name

    """

    # TODO:
    # Remove writing result to file
    # connect sort_by to frontend

    # setup the client connection to the database using an API key search only key
    client = meilisearch.Client("http://localhost:7700", Api_key.SEARCH_KEY)

    index = "pubmed_mouse_v5"
    sort_by = ["Cited number:desc", "Published:desc"]  # needs to be either asc or desc

    with open("Dict_full_name.json", "r", encoding="utf-8") as json_file:
        full_name = json.load(json_file)

    user_input = str(input("What are you searching for: "))

    # remove '-' in the input, workaround il-10 --> il10 to avoid results  containing only 10 or il
    # with il10 we still get il-10 as result, but with query il-10 we also get il-9, il-8,.....
    user_input = user_input.replace("-", "")
    user_input = user_input.replace(",", " ")
    input_words = user_input.split()
    symbol_query = ""
    full_name_query = ""

    found_full_name = False

    for x in input_words:
        # weird behaviour, withous this the query doesnt work as expected
        # ("il10 cancer stroke") != ("il10 stroke cancer")
        symbol_query += " " + x + " "

        # check if the word x is an symbol / alias, if yes save full name in second query
        # if not just save the normal symbol to the query
        if x.lower() in full_name:
            full_name_query += ' "' + full_name[x.lower()] + '" '
            found_full_name = True
        else:
            full_name_query += " " + x + " "

    result_symbol = search(client, index, symbol_query, sort_by)
    filename = "results/" + str(symbol_query) + ".json"
    save_results(result_symbol, filename)

    if found_full_name:
        result_full_name = search(client, index, full_name_query, sort_by)
        filename = "results/" + str(full_name_query) + ".json"
        save_results(result_full_name, filename)

        result_symbol["hits"].extend(result_full_name["hits"])
        result_symbol["processingTimeMs"] += result_full_name["processingTimeMs"]

        filename = "results/" + str(symbol_query) + "TOTAL.json"
        save_results(result_symbol, filename)


def search(client, index, query, sort_by):
    """
    Sends the query to meilisearch

    Parameters:
        client: established connection to meilisearch
        index: index to be searched
        query: Query to be searched
    """

    result = client.index(index).search(
        query,
        {
            "limit": 10000,  # returns a maximum of limit results - make sure limit < = max variable
            "matchingStrategy": "all",  # results have to match all words in query or their synonyms
            "sort": sort_by,
        },
    )

    return result


def save_results(data, filename):
    """
    Saves data to file
    """

    with open(filename, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=2)
    print(f"Find results in {filename}")


if __name__ == "__main__":
    build_query()
