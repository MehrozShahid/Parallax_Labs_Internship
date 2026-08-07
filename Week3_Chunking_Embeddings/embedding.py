import os
import time

import pandas as pd
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):

    embeddings = []
    embedding_logs = []

    for index, chunk in enumerate(chunks):

        start_time = time.time()

        embedding = model.encode(chunk)

        end_time = time.time()

        embedding_time = end_time - start_time

        embeddings.append(embedding)

        embedding_logs.append(
            {
                "chunk_id": index + 1,
                "chunk_length": len(chunk),
                "embedding_time": embedding_time
            }
        )

    return embeddings, embedding_logs


def save_embedding_logs(logs):

    os.makedirs("logs", exist_ok=True)

    df = pd.DataFrame(logs)

    df.to_csv(
        "logs/embedding_log.csv",
        index=False
    )

    total_time = df["embedding_time"].sum()

    print("\nEmbedding Report")
    print(f"Total Chunks: {len(df)}")
    print(f"Total Indexing Time: {total_time:.4f} seconds")