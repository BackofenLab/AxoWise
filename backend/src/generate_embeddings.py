import pandas as pd
from langchain_ollama import OllamaEmbeddings

# Assuming you have OllamaEmbeddings properly configured
embedder = OllamaEmbeddings(model="llama3.1")

# Step 1: Read the CSV into a DataFrame
df = pd.read_csv("/mnt/workspace/for_graph_RAG/PMID_abstracts.csv")

# Step 2: Define the chunk size (100,000 rows per CSV file)
chunk_size = 1000000
total_rows = len(df)

# Step 3: Loop through the DataFrame in chunks of 100,000 rows
for i in range(0, total_rows, chunk_size):
    # Get the chunk of data
    df_chunk = df[i:i + chunk_size].copy()
    
    # Step 4: Generate embeddings for each abstract in the chunk
    df_chunk['embeddings'] = df_chunk['abstract'].apply(lambda x: embedder.embed_query(x))
    
    # Step 5: Save each chunk as a separate CSV file
    chunk_file_name = f"genes_abstract_with_embeddings_part_{i//chunk_size + 1}.csv"
    df_chunk.to_csv(chunk_file_name, index=False)
    
    print(f"Saved {chunk_file_name} with {len(df_chunk)} rows.")

print("Splitting and embedding generation completed.")
