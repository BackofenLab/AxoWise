from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from concurrent.futures import ThreadPoolExecutor

tokenizer = AutoTokenizer.from_pretrained("lxyuan/distilbart-finetuned-summarization")  # abstractive very few words
model = AutoModelForSeq2SeqLM.from_pretrained("lxyuan/distilbart-finetuned-summarization")
model = model.to("cuda")


def build_model():
    tokenizer = AutoTokenizer.from_pretrained("lxyuan/distilbart-finetuned-summarization")  # abstractive very few words
    model = AutoModelForSeq2SeqLM.from_pretrained("lxyuan/distilbart-finetuned-summarization")
    model = model.to("cuda")
    return tokenizer, model


def summarize_section(section):
    inputs = tokenizer(section, truncation=True, return_tensors="pt").to("cuda")
    num_tokens = inputs["input_ids"].shape[1]

    # Print the number of tokens
    prediction = model.generate(**inputs, num_beams=4, early_stopping=True, length_penalty=0.8, no_repeat_ngram_size=2)
    section_summary = tokenizer.batch_decode(prediction, skip_special_tokens=True)[0]
    return section_summary


def create_summary(abstracts):
    with ThreadPoolExecutor() as executor:
        # Map the function to the sections for parallel processing
        summaries = list(executor.map(summarize_section, abstracts))

    # Step 4: Combine the individual summaries
    combined_summary = " ".join(summaries)
    return combined_summary
