""" docstring """
import json
import pandas as pd


def csv_to_json():
    """
    Transforms one csv file into (multiple) json files

    Make sure the csv file comes in the right format and that the allocation of attributes
    matches the code and your file.
    For more information on the expected formate check the
    meilisearch documentation.

    Make sure the output files are not bigger than meilisearch max_payload!
    """

    input_file = str(input("Please give the input file: "))
    filesize = int(input("How many abstracts should be saved in one file? (recommended ~ 100k): "))
    print(f"Loading {input_file} ...")
    df = pd.read_csv(input_file, on_bad_lines="warn")

    listofdata = []
    y = 0  # used to create different filenames

    print(f"Processing a total of {len(df)} abstracts...")

    for x in range(len(df)):  # going through every line in our file
        if (x % filesize == 0) and (x != 0):  # split into several output files
            filename = f"Pubmed{y}.json"
            with open(filename, "w", encoding="utf-8") as outfile:
                json_object = json.dumps(listofdata, indent=4)
                outfile.write(json_object)

            y += 1
            print(f"{y} / {len(df) // filesize + 1}...")  # print status
            listofdata = []

        # retriving attributes from file, make sure they are json compatible
        pubmed_id = str(df.iloc[x, 0])
        title = df.iloc[x, 1]
        abstract = df.iloc[x, 2]
        cited_by = df.iloc[x, 3]
        published_year = str(df.iloc[x, 4])

        dictionary = {
            "PubMed ID": pubmed_id,
            "Title": title,
            "Abstract": abstract,
            "Cited by": cited_by,
            "Published": published_year,
        }

        listofdata.append(dictionary)

    # save the last last data into the last file
    filename = f"Pubmed{y}.json"
    with open(filename, "w", encoding="utf-8") as outfile:
        json_object = json.dumps(listofdata, indent=4)
        outfile.write(json_object)

    print("Done")


if __name__ == "__main__":
    csv_to_json()
