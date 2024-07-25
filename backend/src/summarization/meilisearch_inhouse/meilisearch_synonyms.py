"""Module providing a function printing python version."""

import json
import os
import time
from ast import literal_eval

import meilisearch
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


output_file = "processed_synonyms.json"
failed_file = "failed_synonyms.json"
error_file = "error_synonyms.json"
full_name_dict_file = "Dict_full_name.json"


def main():
    """main"""

    client = meilisearch.Client("http://localhost:7700", ADMIN_API_KEY)

    input_file = str(input("Please give the input file: "))
    upload = set_synonyms(input_file)
    if upload:
        index = str(input("Which index do you want to update? "))
        upload_synonyms(client, index, output_file)

    # uncomment to activate the get synonyms function:
    # index = str(input("Which index do you want to get the synonyms from? "))
    # get_synonyms(client, index)

    # uncomment to activate the reset synonyms function:
    # index = str(input("Which index do you want to reset the synonyms from? "))
    # reset_synonyms(client, index)


def set_synonyms(input_file):
    """
    Takes an input file in csv style and creates synonym-pairs and symbole-full_name
    connection

    Parameters:
        input_file:
            Csv file with these columns [symbol, alias, full_name, ensembl ID]
    """

    cross_count = 0  # count all pairs that have been created
    control_list = []  # saves all symbols seen already
    failed_list = []  # saves all symbols seen more than once
    synonyms_dict = {}  # saves the synonym pairs
    full_name_dict = {}  #  saves the symbol - full name pairs

    print("Processing...")

    df = pd.read_csv(input_file)

    for x in range(len(df)):
        symbol = df.iloc[x, 0]
        aliases = df.iloc[x, 1]
        full_name = df.iloc[x, 2]
        ensembl_id = df.iloc[x, 3]

        #  evaluating the input string format
        symbol = symbol.replace('"', "")
        synonyms_list = literal_eval(aliases)
        synonyms_list = literal_eval(synonyms_list)
        full_name = full_name.replace('"', "")
        ensembl_id = ensembl_id.replace('"', "")

        # checking if the symbol is available:
        if symbol.lower() == "no symbol":
            continue

        # add symbol all its aliases and ensemble ID to one list
        synonyms_list.append(symbol)
        synonyms_list.append(ensembl_id)

        # saving the combination of symbol and full name that are available
        if full_name.lower() != "not available":
            full_name_dict = add_full_name(full_name, synonyms_list, full_name_dict)

        # need to add len == 0 bc not all no aliases are labled correct, some are empty lists
        if not synonyms_list or synonyms_list == ["no alias"]:
            continue
        else:
            # Remove "no alias" from the list if it exists, keep all other terms
            synonyms_list = [
                synonym for synonym in synonyms_list if synonym != "no alias"
            ]

        # synonyms_list = aliases_list

        # make sure all items are strings - some symbols have aliases in int format
        for index, term in enumerate(synonyms_list):
            if not isinstance(term, str):
                synonyms_list[index] = str(term)
                term = "'" + str(term) + "'"

            if not isinstance(synonyms_list[index], str):
                raise TypeError(
                    "One or multiple aliases could not be transformed to string"
                )

        for _ in range(len(synonyms_list)):
            cross_count += (
                1  # count number of pairs created to determin amount of missing ones
            )
            synonym = synonyms_list.pop(0)

            # check if we have seen the item before
            if synonym in control_list:
                failed_list.append(synonym)  # add to failed_list if it appeared before
            else:
                control_list.append(
                    synonym
                )  #  add to list of seen items if seen for first time

            copie = synonyms_list[:]
            synonyms_dict.update({synonym: copie})
            synonyms_list.append(synonym)

    save_to_file(full_name_dict, full_name_dict_file)
    return check_synonyms(synonyms_dict, cross_count, failed_list)


def check_synonyms(synonyms_dict, cross_count, failed_list):
    """
    Function that checks if any synonym pairs could not be created or
    a symbol exist more than once.
    Gives option to upload synonyms or return after check

     Parameters:
        synonyms dict:  holds all synonym pairs created
        cross count:  count of how many pairs we are supposed to have
        failed_list:  List of symbols that appeared more than once

    Returns:
        outputfile with the saved synonym pairs
        failed_file with the list of symbols causing trouble
    """

    print(f"Synonyms are being saved to file: {output_file}")
    try:
        save_to_file(synonyms_dict, output_file)
    except TypeError:
        print("Failed to save the Synonyms")
        return False

    if len(synonyms_dict) != cross_count:
        print(
            f"Failed to process {cross_count - len(synonyms_dict)} items because they appear\
              more than once. Check {failed_file} to see the affected items"
        )
        save_to_file(failed_list, failed_file)

        answ = input("Do you want to continue with the succesful pairs?  [y/n]?")
        while answ not in ("n", "N", "no", "No", "y", "Y", "yes", "Yes"):
            answ = input("Do you want to continue with the succesful pairs?  [y/n]?")

        if answ in ("n", "N", "no", "No"):
            return False

    else:
        answ = input("Do you want to upload the synonyms?  [y/n]?")
        while answ not in ("n", "N", "no", "No", "y", "Y", "yes", "Yes"):
            answ = input("Do you want to upload the synonyms?  [y/n]?")

        if answ in ("n", "N", "no", "No"):
            return False

    return True


def save_to_file(data, filename):
    """
    Saves data in json format to a file

    Parameters:
        data: The data to be save
        filename: Name of the file you want to save to

    """
    with open(filename, "w", encoding="utf-8") as outfile:
        json_object = json.dumps(data, indent=4)
        outfile.write(json_object)


def add_full_name(full_name, synonyms_list, full_name_dict):
    """
    Takes a full name and a list of aliases and adds them to the symbol -> full_name dict

    Parameters:
        full_name : a full name of a protein
        synonyms_list : a list the corresponding symbol and all its aliases + ensembl ID
        full_name_dict : A dict holding all translations from synonym to full_name

    returns the full_name_dict

    """
    for synonym in synonyms_list:
        full_name_dict[synonym.lower()] = full_name.lower()
    return full_name_dict


def upload_synonyms(client, index, input_file=output_file):
    """
    Upload synonyms to meilisearch

    Parameters:
        input_file = json file with synonym pairs
        client: client with an established connection to meilisearch
        index: Index the synonyms will be uploaded to

    """

    json_file = open(input_file, encoding="utf-8")
    synonym_file = json.load(json_file)
    task = client.index(index).update_synonyms(synonym_file)

    task_id = task.task_uid
    while task.status == "enqueued" or task.status == "processing":
        time.sleep(2)  #  use sleep to not spam the server with status requests
        task = client.get_task(task_id)
    if task.status == "failed":
        print("Failed to upload to meilisearch, check meilisearch console")
        return

    check_synonyms_upload(client, index, synonym_file)


def check_synonyms_upload(client, index, synonym_file):
    """
    Function to check that all synonyms have been uploaded correctly

    Parameters:
        client: client with an established connection to meilisearch
        index:  Index the synonyms have been uploaded to
        synonym_file:  File that holds all the synonyms are supposed to be uploaded
    """

    test_successful = True
    error_list = []

    # get the synonyms that have been uploaded
    uploaded_synonyms = client.index(index).get_synonyms()

    # compare uploaded synonyms to the one supposed to be uploaded
    for x in synonym_file:
        if x not in uploaded_synonyms or synonym_file[x] != uploaded_synonyms[x]:
            print("X: ", x, "uploaded_synonyms[x]", uploaded_synonyms[x])
            print("synonym_file[x]", synonym_file[x], " vs ", uploaded_synonyms[x])
            test_successful = False
            error_list.append(str(x) + " : " + str(uploaded_synonyms))

    if test_successful:
        print("Synonyms have been successfully uploaded to meilisearch")
    else:
        with open(error_file, "w", encoding="utf-8") as outfile:
            json.dump(error_list, outfile, indent=2)

        print(
            "Error when uploading the synonyms, check which ones are missing \
              in:",
            error_file,
        )


def get_synonyms(client, index):
    """
    Gets the synonyms of a certain index and saves them to the output file

    Parameters:
        client:  client with an established connection to meilisearch
        index:  Index the synonyms will be retrieved from

    """
    synonyms = client.index(index).get_synonyms()
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(synonyms, outfile, indent=2)
    print("Synonyms have been saved to: ", output_file)


def reset_synonyms(client, index):
    """
    resets the synonyms of a given index
    """
    client.index(index).reset_synonyms()


if __name__ == "__main__":
    main()
