"""Module providing a function printing python version."""
import json
from ast import literal_eval
import time
import meilisearch
import pandas as pd

# TODO:
#  add remove synonyms function + return synonyms
#  split in reasonable big functions -- no pylint error
#  test how to use with variable files and indexes + adresses
#  add api key instead of using masterkey
#  maybe use input function (?)
#  add comment and docstrings + make sure all the variables + functions are named good


def main():
    """docstring"""
    input_file = str(input("Please give the input file: "))
    output_file = "processed_synonyms.json"
    failed_file = "failed_synonyms.json"
    error_file = "error_synonyms.json"

    client = meilisearch.Client("http://localhost:7700", "aSampleMasterKey")
    # index = str(input("Which index do you want to update? "))

    # upload = set_synonyms(input_file, output_file, failed_file)
    # if upload:
    #    upload_synonyms(output_file, client, index, error_file)

    # uncomment to activate the get synonyms function:
    get_synonyms_output = "synonyms_list.json"
    index = str(input("Which index do you want to get the synonyms from? "))
    get_synonyms(client, index, get_synonyms_output)


def set_synonyms(input_file, output_file, failed_file):
    """docstring"""

    cross_count = 0
    control_list = []
    failed_list = []
    synonyms_dict = {}

    print("Processing...")

    df = pd.read_csv(input_file)  # load csv file

    for x in range(len(df)):
        symbol = df.iloc[x, 0]
        aliases = df.iloc[x, 1]

        #  evaluating the input string format
        symbol = symbol.replace('"', "")
        aliases_list = literal_eval(aliases)
        aliases_list = literal_eval(aliases_list)

        # if we dont have an alias no need to add it to meilisearch
        # need to add len == 0 bc not all no aliases are labled correct, some are empty lists
        if len(aliases_list) == 0 or aliases_list[0] == "no alias":
            continue

        aliases_list.append(symbol)  # add symbol and all its aliases to one list
        synonyms_list = aliases_list

        # make sure all items are strings - some symbols have aliases in int format
        for index, term in enumerate(synonyms_list):
            if not isinstance(term, str):
                synonyms_list[index] = str(term)
                term = "'" + str(term) + "'"

            assert isinstance(synonyms_list[index], str), "One or multiple aliases could not be transformed to string"

        for _ in range(len(synonyms_list)):
            cross_count += 1  # count number of pairs created to determin amount of missing ones
            synonym = synonyms_list.pop(0)  # get the first item of the list

            if synonym in control_list:  # check if we have seen the item before
                failed_list.append(synonym)  # add to failed_list if it appeared before
            else:
                control_list.append(synonym)  #  add to list of seen items if seen for first time

            kopie = synonyms_list[:]
            synonyms_dict.update({synonym: kopie})
            synonyms_list.append(synonym)

    if len(synonyms_dict) != cross_count:
        print(
            f"Failed to process {cross_count - len(synonyms_dict)} items because they appear\
              more than once. Check {failed_file} to see the affected items"
        )
        with open(failed_file, "w", encoding="utf-8") as outfile:
            json.dump(failed_list, outfile, indent=2)

        answ = input("Do you want to continue with the succesful pairs?  [y/n]?")
        while answ not in ("n", "N", "no", "No", "y", "Y", "yes", "Yes"):
            answ = input("Do you want to continue with the succesful pairs?  [y/n]?")

        if answ in ("n", "N", "no", "No"):
            return False

    print(f"Synonyms are being saved to file: {output_file}")

    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(synonyms_dict, outfile, indent=2)

    return True


def upload_synonyms(output_file, client, index, error_file):
    """
    Upload synonyms to meilisearch

    Parameters:
        output_file = json file with synonym pairs
    client:
        client with an established connection to meilisearch
    index:
        Index the synonyms will be uploaded to
    error_file:
        File to save synonyms that havent been uploaded successfully

    Takes a json file of synonym pairs, uploades them to the corresponding index
    and checks if they have been uploaded successfully.

    """

    json_file = open(output_file, encoding="utf-8")
    synonym_file = json.load(json_file)
    task = client.index(index).update_synonyms(synonym_file)

    task_id = task.task_uid
    while task.status == "enqueued" or task.status == "processing":
        time.sleep(2)  #  use sleep to not spam the server with status requests
        task = client.get_task(task_id)
    if task.status == "failed":
        print("Failed to upload to meilisearch, check meilisearch console")
        return

    test_successful = True
    error_list = []

    uploaded_synonyms = client.index(index).get_synonyms()

    for x in synonym_file:
        if x not in uploaded_synonyms or synonym_file[x] != uploaded_synonyms[x]:
            print("X: ", x, "uploaded_synonyms[x]", uploaded_synonyms[x])
            print("synonym_file[x]", synonym_file[x], " vs ", uploaded_synonyms[x])
            test_successful = False
            error_list.append(str(x) + " : " + str(uploaded_synonyms))

    if test_successful:
        print("Synonyms have been uploaded to meilisearch successfully")
    else:
        print(
            "Error when uploading the synonyms, check which ones are missing \
              in: {error_file}"
        )
        with open(error_file, "w", encoding="utf-8") as outfile:
            json.dump(error_list, outfile, indent=2)


def get_synonyms(client, index, output_file):
    """
    docstring
    """
    synonyms = client.index(index).get_synonyms()
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(synonyms, outfile, indent=2)


if __name__ == "__main__":
    main()
