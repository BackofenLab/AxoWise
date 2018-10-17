
def rstrip_line_generator(iterable, skip_empty = False):
    for line in iterable:
        new_line = line.rstrip("\n")
        if skip_empty and new_line != "":	
            yield new_line

def lines(buffer, encoding = "utf-8"):
    if "\n" in buffer: # If it is a string, split by \n
        iterable = buffer.split("\n")
        for rstripped_line in rstrip_line_generator(iterable, skip_empty = True):
                yield rstripped_line
    else: # else assume it is a file handle
        with open(buffer, "rt", encoding = encoding) as iterable:
            for rstripped_line in rstrip_line_generator(iterable, skip_empty = True):
                yield rstripped_line

def read_table(file_path, types, delimiter = ",", header = False):
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
    n = len(elements)
    for i in range(n):
        for j in range(i + 1, n):
            yield elements[i], elements[j]

def batches(generator, batch_size):
    batch = []
    for item in generator:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    yield batch

def concat(list_of_lists):
    for list in list_of_lists:
        for item in list:
            yield item
