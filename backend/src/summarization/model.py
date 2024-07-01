from concurrent.futures import ThreadPoolExecutor


def create_individual_summary(to_summarize, tokenizer, model):
    # Extract pmids and abstracts
    pmids = [i[1] for i in to_summarize]
    abstracts = [i[0] for i in to_summarize]

    def summarize(abstract):
        input_tokens = tokenizer(abstract, return_tensors="pt").to("cuda")
        prediction = model.generate(**input_tokens)
        section_summary = tokenizer.decode(prediction[0], skip_special_tokens=True)
        return section_summary

    # Initialize an empty list to store summaries
    summaries = []

    # Process each abstract independently
    with ThreadPoolExecutor() as executor:
        # Summarize each abstract in parallel
        results = executor.map(summarize, abstracts)
        summaries.extend(results)

    # Pair summaries with pmids
    result_with_pmids = [
        f"({summary}, {pmid})" for summary, pmid in zip(summaries, pmids)
    ]

    return result_with_pmids


def create_summary(summarize, tokenizer, model):
    # Lists to hold all summaries
    summaries = []
    final_summaries = []

    def summarize_section(section):
        inputs = tokenizer(section, return_tensors="pt").to("cuda")

        prediction = model.generate(**inputs, max_length=130)
        section_summary = tokenizer.batch_decode(prediction, skip_special_tokens=True)[
            0
        ]
        return section_summary

    def summarize_section_final(section):
        inputs = tokenizer(section, return_tensors="pt").to("cuda")

        prediction = model.generate(**inputs, max_length=160, min_length=160)
        section_summary = tokenizer.batch_decode(prediction, skip_special_tokens=True)[
            0
        ]
        return section_summary

    # Process each community independently
    with ThreadPoolExecutor() as executor:
        for community in summarize:
            # Summarize each section within the community in parallel
            summary_chunk = list(executor.map(summarize_section, community))
            summaries.append(
                summary_chunk
            )  # Append the list of summaries for this community

    # Concatenate abstract pairs to generate a final summary
    concatenate_pairs = lambda lst: [
        (
            (lst[i][:-1] + " " + lst[i + 1])
            if i == 0 and i + 1 < len(lst)
            else (lst[i] + lst[i + 1]) if i + 1 < len(lst) else lst[i]
        )
        for i in range(0, len(lst), 2)
    ]
    concatenated = [concatenate_pairs(i) for i in summaries]

    # Generate the final summary
    with ThreadPoolExecutor() as executor:
        for community in concatenated:
            # Summarize each section within the community in parallel
            summary_chunk = list(executor.map(summarize_section_final, community))
            final_summaries.append(
                summary_chunk
            )  # Append the list of summaries for this community

    # Post process summaries to assure correct sentences
    final_summaries = [
        [s[: s.rfind(".") + 1] for s in sublist if "." in s]
        for sublist in final_summaries
    ]
    return final_summaries
