import url

_api_endpoint = "https://www.uniprot.org/uniprot/"

def bool_to_uniprot_str(boolean):
    return ("yes" if boolean else "no")

def query(keyword, reviewed = True, format = "xml", compress = False):
    # Build a GET request arguments
    query_string = "{} AND reviewed:{}".format(
        keyword,
        bool_to_uniprot_str(reviewed)
    )

    get_params = dict(
        query = query_string,
        sort = "score",
        format = format,
        compress = bool_to_uniprot_str(compress),
        limit = 5
    )

    query_url = "{}?{}".format(
        _api_endpoint,
        url.url_encode(get_params, safe = ":")
    )
    
    # Get the XML file
    xml = url.get(query_url)
    return xml
