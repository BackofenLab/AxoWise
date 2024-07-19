import threading

import ollama


def create_individual_summary(to_summarize):
    def get_response(prompt, final_summaries):
        response = ollama.generate(model="llama3", prompt=prompt[0])
        response = response["response"].split("\n")
        summary = response[-1] if len(response) <= 3 else "\n".join(response[2:-1])
        final_summaries.append((summary + " " + prompt[1]))

    prompts = [
        (
            f"Provide a summary of the following abstract in 50 or less words. The text is: {i[0]}",
            i[1],
        )
        for i in to_summarize
    ]

    threads = []
    result_with_pmids = []

    for prompt in prompts:
        thread = threading.Thread(target=get_response, args=(prompt, result_with_pmids))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    return result_with_pmids


def create_summary(summarize):
    def get_response(prompt, final_summaries):
        response = ollama.generate(model="llama3", prompt=prompt)
        response = response["response"].split("\n")
        summary = response[-1] if len(response) <= 3 else "\n".join(response[2:-1])
        final_summaries.append(summary)

    # List to hold all summaries
    final_summaries = []
    threads = []
    prompts = [
        f"Make a text that is 50 words or less with the most important information of the following text. The text is: {i[0] + i[1] if len(i) >= 2 else (i[0] if len(i) == 1 else '')}"
        for i in summarize
    ]

    for prompt in prompts:
        thread = threading.Thread(target=get_response, args=(prompt, final_summaries))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    return final_summaries
