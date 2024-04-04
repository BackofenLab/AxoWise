from concurrent.futures import ThreadPoolExecutor


def create_summary(summarize, tokenizer, model):
    abstracts = [i[0] for i in summarize]
    pmids = [i[1] for i in summarize]

    def summarize_section(section):
        inputs = tokenizer(section, truncation=True, return_tensors="pt").to("cuda")
        num_tokens = inputs["input_ids"].shape[1]

        # Print the number of tokens
        prediction = model.generate(**inputs, num_beams=4, no_repeat_ngram_size=2, min_length=140)
        section_summary = tokenizer.batch_decode(prediction, skip_special_tokens=True)[0]
        return section_summary

    with ThreadPoolExecutor() as executor:
        # Map the function to the sections for parallel processing
        summaries = list(executor.map(summarize_section, abstracts))
    summaries = [i.replace("\n", "") for i in summaries]
    summaries = list(zip(summaries, pmids))
    # Step 4: Combine the individual summaries
    return summaries
