
def rstrip_line_generator(iterable, skip_empty = False):
    for line in iterable:
        new_line = line.rstrip("\n")
        if skip_empty and new_line != "":	
            yield new_line

def lines(file_path, encoding = "utf-8"):
    with open(file_path, "rt", encoding = encoding) as f:
        for rstripped_line in rstrip_line_generator(f):
            yield rstripped_line

def read_table(file_path, types, delimiter = ","):
    expected_cols = len(types)
    for line in lines(file_path):
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

