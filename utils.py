
def lines(file_path, encoding = "utf-8"):
    with open(file_path, "rt", encoding = encoding) as f:
        for line in f:
            yield line.rstrip("\n")

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
