import json
import time
import Api_key
import meilisearch


def add_data(client):
    """
    Uploads the given files to meilisearch

    Takes any number of json files and uploads them to meilisearch.
    Please make sure you follow the naming conventions. If you want to upload multiple files
    give them the same name with ascending number after the name - starting at 0

    Example: upload_to_db_0.json, upload_to_db_1.json, upload_to_db_2.json,....

    The upload speed depends on the size of your files, the program crashes without error if the
    size of one of your documents is bigger than the max payload limit set in meilisearch.
    Recommended size < 350MB

    WHEN UPLOADING ON SERVER:
    if you want to upload on the server and run this in the background, make sure to comment out
    all the inputs and set the value yourself.

    """

    number_files = int(input("How many files do you want to upload?: "))
    # number_files = 2
    if number_files > 1:
        print(
            "\nPlease make sure you files are named correct -"
            "Same name, ascending numbers at the end starting with 0:"
            "\ntest1.json, test2.json, test3.json ... \n"
        )
        input_file = str(
            input(
                "Please only give the name without .json ending and number \
                               \nlike this: 'test' for test0.json: "
            )
        )
        # input_file = "Pubmed"

        multiple_files = True
    elif number_files == 1:
        input_file = str(input("Please give the input file you would like to upload: "))
        multiple_files = False
    else:
        return
    # index = "pubmed_mouse_v1"
    index = str(input("What index do you want the data to be added to? "))
    print("Processing, this may take a while...")

    for x in range(number_files):  # going through all the files, loading one after another
        if multiple_files:
            filename = input_file + str(x) + ".json"
        else:
            filename = input_file

        with open(filename, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        print("Loading: ", filename)

        # sending the file to meilisearch
        task = client.index(index).add_documents(data)
        task_id = task.task_uid

        # wait until the documents are indexed
        while task.status == "enqueued" or task.status == "processing":
            time.sleep(10)  # we use sleep to avoid spamming the server with status requests
            task = client.get_task(task_id)

        if task.status == "failed":
            print("Failed to upload to meilisearch, check meilisearch console")
            return

        if x + 1 < number_files:
            print(f"{x+1} / {number_files} - {filename} uploaded successfully")
        else:
            print(f"Done - {filename} uploaded successfully")


def delete_index(client):
    """Deletes the given index"""
    index = str(input("What index do you want to delete? "))
    client.delete_index(index)


def main():
    """Uncomment function calls to either index new data to meilisearch or to delte an index"""

    # setup the client connection to the database using the master API key to identify us
    client = meilisearch.Client("http://localhost:7700", Api_key.ADMIN_API_KEY)

    add_data(client)

    # Uncomment this to delte an index
    # delete_index(client)


if __name__ == "__main__":
    main()
