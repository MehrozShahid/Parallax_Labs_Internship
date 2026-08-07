import pandas as pd

from chunking import split_text
from embedding import (
    generate_embeddings,
    save_embedding_logs
)

# Load cleaned dataset from Week 2
df = pd.read_csv(
    r"../Week2_Data_Cleaning_Preprocessing/dataset/cleaned_train.csv"
)

all_chunks = []

# Split each document into smaller chunks
for text in df["clean_text"]:

    chunks = split_text(text)

    all_chunks.extend(chunks)

print(f"Total chunks created: {len(all_chunks)}")

# Generate embeddings for all chunks
embeddings, embedding_logs = generate_embeddings(
    all_chunks
)

# Save embedding log
save_embedding_logs(
    embedding_logs
)

print("\nWeek 3 completed successfully.")