import json
from ast import literal_eval
import pandas as pd


def csv_to_json():
    """
    Transforms one csv file into (multiple) json files

    Make sure the csv file comes in the right format and that the allocation of attributes
    matches the code and your file.
    For more information on the expected formate check the
    meilisearch documentation.

    Make sure the output files are not bigger than meilisearch max_payload or adjust max_payload!
    """

    input_file = str(input("Please give the input file: "))
    filesize = int(input("How many abstracts should be saved in one file? (recommended ~ 3.000.000): "))
    print(f"Loading {input_file} in blocks")

    block_size = 3000000
    start_line = 1  # Assuming the first line is a header
    y = 0  # used to create different filenames

    line_count = 0  # counts all lines to display progress -- comment out if file is too big
    with open(input_file, "r", encoding="utf-8", errors="ignore") as file:
        for _ in file:
            line_count += 1

    while True:  # runs until the loaded block is empty --> end of file
        df = read_csv_in_blocks(input_file, start_line, block_size)
        if df.empty:
            break

        start_line += block_size  # increase the start_line by the block size for the next block
        listofdata = []

        print(f"Processing a total of {len(df)} abstracts in this block")

        for x in range(len(df)):  # going through every line in our block
            if (x % filesize == 0) and (x != 0):  # split into several output files
                filename = f"Pubmed{y}.json"
                with open(filename, "w", encoding="utf-8") as outfile:
                    json_object = json.dumps(listofdata, indent=4)
                    outfile.write(json_object)

                y += 1
                print(f"{y} / { line_count // filesize + 1}...")  # print status
                listofdata = []

            # retriving attributes from file, make sure that they are oriented the right way
            try:
                pubmed_id = str(df.iloc[x, 0])
                title = df.iloc[x, 1]
                abstract = df.iloc[x, 2]
                cited_by = df.iloc[x, 3]
                cited_number = int(len(literal_eval(cited_by)))
                published_year = int(df.iloc[x, 4])

            except ValueError:  # if a value is not json compatible
                continue
            try:
                if len(abstract) < 2:
                    continue
            except TypeError:  # if abstract is NaN or not available
                continue

            dictionary = {
                "PubMed ID": pubmed_id,
                "Title": title,
                "Abstract": abstract,
                "Cited by": cited_by,
                "Cited number": cited_number,
                "Published": published_year,
            }

            listofdata.append(dictionary)

        # save the last last data from our block into a file
        filename = f"Pubmed{y}.json"
        with open(filename, "w", encoding="utf-8") as outfile:
            json_object = json.dumps(listofdata, indent=4)
            outfile.write(json_object)

        y += 1
        print(f"{y} / { line_count// filesize + 1}...")  # print status
        listofdata = []

    print("Done")


def read_csv_in_blocks(file_path, start_line, block_size):
    """
    Reads a block of lines from a CSV file using pandas.

    Parameters:
    - file_path: The path to the CSV file.
    - start_line: The line number to start reading from (1-based indexing; note that header is considered as the first line if present).
    - block_size: The number of lines to read in the block.

    Returns:
    A pandas DataFrame containing the lines read from start_line for block_size lines.
    """
    # If the file has a header, adjust skiprows accordingly
    skiprows = range(1, start_line) if start_line > 1 else None

    # Use pandas read_csv with skiprows and nrows
    df = pd.read_csv(file_path, skiprows=skiprows, nrows=block_size, on_bad_lines="warn")
    return df


if __name__ == "__main__":
    csv_to_json()
