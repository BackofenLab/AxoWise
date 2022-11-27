from gprofiler import GProfiler


def functional_enrichment(identifiers, species_id = 'mmusculus'):
    """ Retrieves the functional enrichment for any set of input proteins.

    Arguments:
    - identifiers - protein identifiers as a list of strings (e.g. ["IL10", "IL10RA"])
    - species_id - NCBI taxon identifier (e.g. "mmusculus" or "hsapiens")

    Returns a single pandas.DataFrame.
    """
    gp = GProfiler(
    user_agent='PGDB_User', #optional user agent
    return_dataframe=True, #return pandas dataframe or plain python structures
    )

    return GProfiler.profile(gp, organism=species_id, query=identifiers, no_evidences=False)