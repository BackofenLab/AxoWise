import time

import pandas as pd
from langchain_ollama import OllamaEmbeddings

# Assuming you have OllamaEmbeddings properly configured
embedder = OllamaEmbeddings(model="llama3.1")

# Step 1: Read the CSV into a DataFrame
df = pd.read_csv("/mnt/workspace/for_graph_RAG/PMID_abstracts.csv")

# Step 2: Define the chunk size (100,000 rows per CSV file)
chunk_size = 50000
total_rows = len(df)

# Step 3: Loop through the DataFrame in chunks of 100,000 rows
for i in range(0, total_rows, chunk_size):
    time_begin = time.time()
    # Get the chunk of data
    df_chunk = df[i : i + chunk_size].copy()

    print(f"Started generating embeddings of chunk {i // chunk_size + 1}")

    # Initialize list to store embeddings for the whole chunk
    embeddings = []

    # Process the chunk in batches of 100 rows
    for j in range(0, len(df_chunk), 100):
        sub_chunk = df_chunk["abstract"].iloc[j : j + 100].tolist()

        # Generate embeddings for the current sub-chunk
        sub_embeddings = embedder.embed_documents(sub_chunk)

        # Append the sub_embeddings to the main embeddings list
        embeddings.extend(sub_embeddings)

    # Add the embeddings to the dataframe
    df_chunk["embeddings"] = embeddings

    # Save each chunk as a separate CSV file
    chunk_file_name = f"genes_abstract_with_embeddings_part_{i // chunk_size + 1}.gz"
    df_chunk.to_csv(chunk_file_name, index=False)

    print(f"Saved {chunk_file_name} with {len(df_chunk)} rows in {time.time() - time_begin}s.")

print("Splitting and embedding generation completed.")
