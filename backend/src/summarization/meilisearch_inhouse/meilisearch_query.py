import json
import os

import meilisearch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
SEARCH_KEY = os.getenv("SEARCH_KEY")


def build_query(client, index, user_input, sort_by, limit=20000):
    """
    Function to search meilisearch, returns results.json file

    User/frontend supplies the query and index - hardcoded index atm

    Build 2 queries if one of the symbols has a full name

    """

    # Dict full name links symbols to their full names
    with open(
        "summarization/meilisearch_inhouse/Dict_full_name.json", "r", encoding="utf-8"
    ) as json_file:
        full_name = json.load(json_file)

    found_full_name = False
    symbol_query = ""
    full_name_query = ""

    user_input = user_input.split()

    for x in user_input:
        # check if the word x is an symbol / alias, if yes save full name in second query
        # if not just save the normal symbol to the query
        if x.lower() in full_name:
            full_name_query += ' "' + full_name[x.lower()] + '" '
            found_full_name = True

            # remove '-' in the input, workaround il-10 --> il10 to avoid results  containing only 10 or il
            # with il10 we still get il-10 as result, but with query il-10 we also get il-9, il-8,.....
            x = x.replace("-", "")
            x = x.replace(",", " ")
            symbol_query += " " + x + " "

        else:
            # remove '-' in the input, workaround il-10 --> il10 to avoid results  containing only 10 or il
            # with il10 we still get il-10 as result, but with query il-10 we also get il-9, il-8,.....
            x = x.replace("-", "")
            x = x.replace(",", " ")

            # weird behaviour, withous this the query doesnt work as expected
            # ("il10 cancer stroke") != ("il10 stroke cancer")
            symbol_query += " " + x + " "
            full_name_query += " " + x + " "

    result_symbol = search(client, index, symbol_query, sort_by, limit)

    if found_full_name:
        result_full_name = search(client, index, full_name_query, sort_by, limit)

        # add the results from full name to symbol results
        result_symbol["hits"].extend(result_full_name["hits"])
        result_symbol["processingTimeMs"] += result_full_name["processingTimeMs"]

    return result_symbol


def search(client, index, query, sort_by, limit):
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
            "limit": limit,  # returns a maximum of limit results - make sure limit < = max variable
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


def get_results(
    limit,
    query,
):
    """
    This function is just here until the connection to front end it established
    """
    # TODO:
    # This needs to be moved to the main function when connecting to the frontend
    client = meilisearch.Client("http://localhost:7700", SEARCH_KEY)
    index = "pubmed_mouse_v1"
    sort_by = ["Cited number:desc", "Published:desc"]
    return build_query(client, index, query, sort_by, limit)
