import meilisearch
import json
import pandas as pd

# TODO:
# discuss how we can modify the search in such a way that we know where one word ends and the next one starts
# for example lung cancer, do we want results that only have "lung cancer" or do we also accept terms having
# cancer and lung in it, but possibly not related


def search():
    """
    Function to search meilisearch, returns results.json file

    User/frontend supplies the query and index - hardcoded index atm

    Returning a json file with hits (only up to limit)

    """
    # setup the client connection to the database using an API key search only key
    client = meilisearch.Client(
        "http://localhost:7700", "f00df5d69e3bdb7739ae2349daef370db7902710ce741fbed03ab629450ed9f7"
    )

    user_input = str(input("What are you searching for: "))

    # remove '-' in the input, workaround il-10 --> il10 to avoid results  containing only 10 or il
    # with il10 we still get il-10 as result, but with query il-10 we also get il-9, il-8,.....
    user_input = user_input.replace("-", "")
    input_words = user_input.split()
    query_input = ""
    for x in input_words:
        query_input += " " + x + " "  # weird behaviour, withous this the query doesnt work as expected
        # ("il10 cancer stroke") != ("il10 stroke cancer")

    result = client.index("pubmed_mouse_v4").search(
        query_input,
        {
            "limit": 1000,  # returns a maximum of 1000 results - make sure limit < = max variable
            "matchingStrategy": "all",  # results have to match all words in query or their synonyms
        },
    )

    with open("result.json", "w", encoding="utf-8") as outfile:
        json.dump(result, outfile, indent=2)
    print("Find results in result.json")


if __name__ == "__main__":
    search()
