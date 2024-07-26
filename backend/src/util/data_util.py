"""
Collection of useful functions.
"""

import datetime
import functools
import os
import re
import time
from urllib.parse import urlparse
from urllib.request import urlopen


def parse_flat_file(pathway):
    name = None
    description = None
    classes = None
    diseases = None
    drugs = None
    genes = None
    compounds = None

    def last_index(string, substring):
        return len(string) - len(substring) - string[::-1].index(substring)

    def parse_disease_line(line):
        disease_id, disease_name = line.strip().split("  ")
        return disease_id, disease_name

    def parse_drug_line(line):
        drug_id, drug_name = line.strip().split("  ")
        return drug_id, drug_name

    def parse_gene_line(line):
        parts = line.strip().split("  ")
        if len(parts) >= 2:
            gene_id, gene_names = parts
        else:
            return
        if ";" in gene_names:  # Mutliple names
            names = list(map(lambda string: string.strip(), gene_names.split(";")))
            short_name, long_name = names[0], "; ".join(names[1:])
            if "[" in long_name:
                long_name = long_name[: long_name.index("[") - 1]
        else:  # One name
            short_name = ""
            long_name = gene_names
            if "[" in long_name:
                long_name = long_name[: long_name.index("[") - 1]
        return gene_id, short_name, long_name

    def parse_compound_line(line):
        line = line.strip()
        if "  " in line:
            compound_id, compound_name = line.split("  ")
        else:
            compound_id = line
            compound_name = ""
        return compound_id, compound_name

    state = None
    for line in re.split("\n+", pathway):
        if not line.startswith(" "):
            state = None

        # List continuation
        if state == "DISEASE":
            diseases.append(parse_disease_line(line))
        elif state == "DRUG":
            drugs.append(parse_drug_line(line))
        elif state == "GENE":
            genes.append(parse_gene_line(line))
        elif state == "COMPOUND":
            compounds.append(parse_compound_line(line))

        # One-line entries
        elif line.startswith("NAME"):
            name = line.lstrip("NAME").lstrip()
            name = name[: last_index(name, " - ")]
            if name.strip() == "":
                raise ValueError("Name cannot be an empty string")
        elif line.startswith("DESCRIPTION"):
            description = line.lstrip("DESCRIPTION").lstrip()
        elif line.startswith("CLASS"):
            classes_str = line.lstrip("CLASS")
            classes = list(map(lambda string: string.strip(), classes_str.split(";")))

        # List start
        elif line.startswith("DISEASE"):
            state = "DISEASE"
            diseases = [parse_disease_line(line.lstrip("DISEASE"))]
        elif line.startswith("DRUG"):
            state = "DRUG"
            drugs = [parse_drug_line(line.lstrip("DRUG"))]
        elif line.startswith("GENE"):
            state = "GENE"
            genes = [parse_gene_line(line.lstrip("GENE"))]
        elif line.startswith("COMPOUND"):
            state = "COMPOUND"
            compounds = [parse_compound_line(line.lstrip("COMPOUND"))]

    return name, description, classes, diseases, drugs, genes, compounds


def get(url, timeout=10, wait=1):
    if type(wait) is int and wait > 0:
        time.sleep(wait)

    parsed_url = urlparse(url)
    if parsed_url.scheme not in ["http", "https"]:
        raise ValueError("URL scheme must be http or https")

    try:
        return (
            urlopen(url, timeout=timeout)  # nosec
            .read()
            .decode(encoding="utf-8", errors="ignore")
        )
    except:
        return None


def rstrip_line_generator(iterable, skip_empty=False):
    """
    Generator which iterates over lines provided by the
    file handle but strips '\n' from the right of each
    line.
    """

    for line in iterable:
        new_line = line.rstrip("\n")
        if skip_empty and new_line != "":
            yield new_line


def lines(buffer, encoding="utf-8"):
    """
    Generator which iterates over text lines in the
    buffer. The buffer can either be a string or a file
    handle.
    """

    if "\n" in buffer:  # If it is a string, split by \n
        iterable = buffer.split("\n")
        for rstripped_line in rstrip_line_generator(iterable, skip_empty=True):
            yield rstripped_line
    else:  # else assume it is a file handle
        with open(buffer, "rt", encoding=encoding) as iterable:
            for rstripped_line in rstrip_line_generator(iterable, skip_empty=True):
                yield rstripped_line


def read_table(file_path, types, delimiter=",", header=False):
    """
    Read a text file as a table (e.g. TSV if delimiter set to '\t')
    and automatically converts the cells to the specified types.

    'types' should be an iterable containing data type constructors
    and its length should be the same as the number of expected columns.
    """

    types = tuple(types)
    expected_cols = len(types)
    for line in lines(file_path):
        if header:
            header = False
            continue

        cols = line.split(delimiter)
        try:
            true_cols = [t(c) for (t, c) in zip(types, cols)]
            if len(true_cols) == expected_cols:
                yield tuple(true_cols)
        except ValueError:
            pass


def pair_generator(elements):
    """
    Generate pairs of elements from a list of elements.
    """

    n = len(elements)
    for i in range(n):
        for j in range(i + 1, n):
            yield elements[i], elements[j]


def batches(generator, batch_size):
    """
    Generate batches of data from the given generator.
    """

    batch = []
    for item in generator:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    yield batch


def concat(list_of_lists):
    """
    Concatenate lists from the list ('list_of_lists')
    into a single list.
    """

    for list in list_of_lists:
        for item in list:
            yield item


def exit_on(*exceptions, print_msg=False, default=None):
    """
    Decorator that catches the specified exceptions.
    """

    def decorate(f):
        @functools.wraps(f)
        def _f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except exceptions as e:
                if print_msg:
                    print(e)
                elif KeyboardInterrupt in exceptions:
                    print()
                return default

        return _f

    return decorate


def throttle(wait=1):
    """
    Decorator that ensures `wait` second(s) pass between each
    call of the decorated function.
    """

    # Time of the last call
    last_call = 0

    def decorate(f):
        @functools.wraps(f)
        def _f(*args, **kwargs):
            nonlocal last_call

            elapsed = time.time() - last_call
            if elapsed < wait:
                time.sleep(wait - elapsed)

            retval = f(*args, **kwargs)
            last_call = time.time()
            return retval

        return _f

    return decorate


def update_line(file_path, pattern, new_line):
    """
    Find pattern in text file and overwrite

    Arguments:
    file_path: path of file
    pattern: an re pattern
    new_line: line that should replace the old line
    """
    lines = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
    with open(file_path, "w") as f:
        found = False
        for line in lines:
            if re.search(pattern, line):
                f.write(new_line + "\n")
                found = True
            else:
                f.write(line)
        if not found:
            f.write(new_line + "\n")


def search_line(file_path, pattern):
    """
    Search text file for a re pattern

    Arguments:
    file_path: path of file
    pattern: an re pattern
    """
    lines = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
    with open(file_path, "w") as f:
        found = None
        for line in lines:
            match = re.search(pattern, line)
            if match:
                f.write(line)
                found = match.group(1)
            else:
                f.write(line)
    return found


def get_latest_release_date_bader(text):
    # Use a regular expression to search for lines that contain a date in the format "Month_Day_Year"
    matches = re.findall(r"(\w+)_(\d{2})_(\d{4})/", text)
    if not matches:
        return None
    # Convert the matches to datetime objects
    dates = [
        datetime.datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
        for month, day, year in matches
    ]
    # Find the maximum (most recent) date
    latest_date = max(dates)
    # Format the latest date as a string and return it
    return latest_date
