import os
import shutil
import time

import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


# CONFIGURATION
DATASET_PATH = "dataset/cleaned_train.csv"

MODEL_NAME = "all-MiniLM-L6-v2"

# Chunk sizes to experiment with
CHUNK_SIZES = [250, 500, 750, 1000]

# Separate folder for chunk-size experiments
EXPERIMENT_PATH = "./chunk_experiments"

# Column containing the news article text
TEXT_COLUMN = "Description"


# LOAD DATASET
print("=" * 60)
print("CHUNK SIZE EXPERIMENT")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully.")
print("Dataset shape:", df.shape)

print("\nAvailable columns:")
print(df.columns.tolist())


# CHECK TEXT COLUMN
if TEXT_COLUMN not in df.columns:
    raise ValueError(
        f"\nColumn '{TEXT_COLUMN}' was not found.\n"
        f"Available columns: {df.columns.tolist()}\n"
        "Please change TEXT_COLUMN in this script."
    )


# Remove missing documents
df = df.dropna(subset=[TEXT_COLUMN])

documents = df[TEXT_COLUMN].astype(str).tolist()

print("\nValid documents:", len(documents))


# LOAD EMBEDDING MODEL
print("\nLoading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


# CREATE EXPERIMENT DIRECTORY
os.makedirs(EXPERIMENT_PATH, exist_ok=True)


# RUN CHUNK SIZE EXPERIMENT
experiment_summary = []


for chunk_size in CHUNK_SIZES:

    print("\n")
    print("=" * 60)
    print(f"CHUNK SIZE: {chunk_size}")
    print("=" * 60)

    start_time = time.time()

    # Create separate database path
    db_path = os.path.join(
        EXPERIMENT_PATH,
        f"chroma_{chunk_size}"
    )

    # Delete previous experiment with same chunk size
    if os.path.exists(db_path):

        print("Removing previous database...")

        shutil.rmtree(db_path)


    # Create ChromaDB
    print("Creating ChromaDB...")

    client = chromadb.PersistentClient(
        path=db_path
    )

    collection_name = f"ag_news_{chunk_size}"

    collection = client.get_or_create_collection(
        name=collection_name
    )

    # Create text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=50
    )

    # Split documents
    print("Creating chunks...")

    all_chunks = []
    all_ids = []

    chunk_counter = 0

    for document in documents:

        chunks = splitter.split_text(document)

        for chunk in chunks:

            if chunk.strip():

                all_chunks.append(chunk)

                all_ids.append(
                    f"chunk_{chunk_size}_{chunk_counter}"
                )

                chunk_counter += 1

    print("Total chunks:", len(all_chunks))

    # Generate embeddings
    print("\nGenerating embeddings...")

    embeddings = model.encode(
        all_chunks,
        show_progress_bar=True
    )

    embeddings = embeddings.tolist()

    print("Embeddings generated.")

    # Add documents to ChromaDB
    print("\nAdding documents to ChromaDB...")

    # ChromaDB can handle large datasets better in batches
    batch_size = 5000

    for start in range(0, len(all_chunks), batch_size):

        end = min(
            start + batch_size,
            len(all_chunks)
        )

        collection.add(
            ids=all_ids[start:end],
            documents=all_chunks[start:end],
            embeddings=embeddings[start:end]
        )

        print(
            f"Added {start} - {end} "
            f"of {len(all_chunks)} chunks"
        )

    # Calculate time
    elapsed_time = time.time() - start_time

    # Save experiment information
    experiment_summary.append({
        "chunk_size": chunk_size,
        "number_of_chunks": len(all_chunks),
        "database_path": db_path,
        "collection_name": collection_name,
        "time_seconds": round(elapsed_time, 2)
    })

    print("\nExperiment completed.")
    print("Chunk size:", chunk_size)
    print("Chunks:", len(all_chunks))
    print("Time:", round(elapsed_time, 2), "seconds")


# DISPLAY FINAL SUMMARY
print("\n")
print("=" * 60)
print("CHUNK SIZE EXPERIMENT COMPLETED")
print("=" * 60)

summary_df = pd.DataFrame(experiment_summary)

print("\n")
print(summary_df.to_string(index=False))

# Save summary
summary_df.to_csv(
    "chunk_size_summary.csv",
    index=False
)

print("\nSummary saved to:")
print("chunk_size_summary.csv")

print("\nAll experiments completed successfully.")