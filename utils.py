"""
Collection of useful functions.
"""

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

    if "\n" in buffer: # If it is a string, split by \n
        iterable = buffer.split("\n")
        for rstripped_line in rstrip_line_generator(iterable, skip_empty=True):
            yield rstripped_line
    else: # else assume it is a file handle
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
