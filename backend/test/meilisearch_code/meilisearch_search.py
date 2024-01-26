import meilisearch
import json
import pandas as pd


def search():
    """docstring"""
    # setup the client connection to the database using the master key to identify us
    client = meilisearch.Client(
        "http://localhost:7700", "f00df5d69e3bdb7739ae2349daef370db7902710ce741fbed03ab629450ed9f7"
    )

    user_input = str(input("What are you searching for: "))

    # remove - in the user input, workaround il-10 --> il10 to avoid results just containing the number 10 or just il
    # with il10 we still get il-10 as result, but with query il-10 we also get il-9, il-8,.....
    user_input = user_input.replace("-", "")
    input_words = user_input.split()

    # by using "" around every word we make sure it has to be in the query and the spelling has to be correct too, remove later
    query_input = ""
    for x in input_words:
        query_input += (
            " " + x + " "
        )  # weird behaviour, withous this the query doesnt work as expected ("il10 cancer stroke") != ("il10 stroke cancer")

    # set the result limit -- make sure max_variable is set to the same or higher
    result = client.index("pubmed_mouse_v4").search(
        query_input,
        {
            "limit": 1000,  # returns a maximum of 1000 results
            "matchingStrategy": "all",  # results have to match all words in their query or their synonyms (when not using "" around query word)
        },
    )

    with open("result.json", "w", encoding="utf-8") as outfile:
        json.dump(result, outfile, indent=2)
    print("Find results in result.json")


if __name__ == "__main__":
    search()
