
import time
import database
import argparse
import cypher_queries as Cypher

def time_query(neo4j_graph, query, *args):
    start = time.time()
    cursor = query(neo4j_graph, *args)
    num_rows = 0
    first_row = None
    for row in cursor:
        if first_row is None:
            first_row = row
        num_rows += 1
    end = time.time()
    elapsed_time = end - start
    return first_row, num_rows, elapsed_time 

def main():
    args_parser = argparse.ArgumentParser(
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )

    args_parser.add_argument(
        "--credentials",
        type = str,
        help = "Path to the credentials JSON file that will be used",
        default = "tests/credentials.test.json"
    )

    args = args_parser.parse_args()

    # Connect to the databases
    postgres_connection, neo4j_graph = database.connect(credentials_path = args.credentials)
    postgres_connection.close()

    print("[Protein-centric query]")
    first_row, num_rows, elapsed_time = time_query(neo4j_graph, Cypher.search_protein, "ccr5", "homo")
    print(f"{num_rows} row(s) returned in {elapsed_time:.4f} second(s)")

    print("[Protein list query]")
    first_row, num_rows, elapsed_time = time_query(neo4j_graph, Cypher.search_proteins, [
        "SFPI1",
        "FOSB",
        "MLXIPL",
        "ELK3",
        "FLI1",
        "IL10",
        "IRF1",
        "NFIC",
        "SREBF1",
        "ID2",
        "HIF1A",
        "FOS",
        "MYC",
        "TEF",
        "RUNX1",
        "ATF1",
        "TFEB",
        "BACH1",
        "ATF3",
        "BATF3",
        "BHLHE41",
        "IL10RA",
        "SMAD3",
        "ZFP281",
        "CCL5",
        "CREB3L2",
        "BATF",
        "ERF",
        "KLF9",
        "ZFP691",
        "JUN",
        "KLF7",
        "XBP1",
        "FOXO1",
        "JDP2",
        "CREB1",
        "JUNB",
        "CEBPG",
        "NFIL3",
        "SP100",
        "STAT1",
        "KLF13",
        "EGR1",
        "CEBPB",
        "NFKB2",
        "RXRA",
        "TFE3",
        "ETV5",
        "ETV6",
        "NFE2L1",
        "STAT2",
        "CENPB",
        "RELB",
        "CEBPA",
        "MAFB",
        "SP3",
        "REL",
        "KLF4",
        "BACH2",
        "MAF",
        "ATF4",
        "NFIX",
        "CCR5",
        "IRF9",
        "TGIF1",
        "USF2"
    ], 900)
    print(f"{num_rows} row(s) returned in {elapsed_time:.4f} second(s)")

    print("[Pathway-centric query]")
    first_row, num_rows, elapsed_time = time_query(neo4j_graph, Cypher.search_pathway, "Chemokine", "human")
    print(f"{num_rows} row(s) returned in {elapsed_time:.4f} second(s)")

    print("[Class-centric query]")
    first_row, num_rows, elapsed_time = time_query(neo4j_graph, Cypher.search_class, "Immune diseases")
    print(f"{num_rows} row(s) returned in {elapsed_time:.4f} second(s)")

if __name__ == "__main__":
    main()