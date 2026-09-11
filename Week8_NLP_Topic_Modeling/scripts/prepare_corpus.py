import os
import pandas as pd
import chromadb


# --------------------------------------------------
# Configuration
# --------------------------------------------------

CHROMA_PATH = "../Week5_Retrieval_Evaluation/chroma_db"
COLLECTION_NAME = "ag_news"

OUTPUT_PATH = "data/topic_documents.csv"

# Number of documents retrieved at one time
BATCH_SIZE = 5000


# --------------------------------------------------
# Connect to ChromaDB
# --------------------------------------------------

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

total_documents = collection.count()

print(f"Collection found: {COLLECTION_NAME}")
print(f"Total documents: {total_documents}")


# --------------------------------------------------
# Retrieve documents in batches
# --------------------------------------------------

print("\nRetrieving documents in batches...")

all_rows = []

for start in range(0, total_documents, BATCH_SIZE):

    end = min(
        start + BATCH_SIZE,
        total_documents
    )

    print(
        f"Retrieving documents "
        f"{start + 1} to {end} "
        f"of {total_documents}..."
    )

    data = collection.get(
        limit=BATCH_SIZE,
        offset=start,
        include=[
            "documents",
            "metadatas"
        ]
    )

    ids = data["ids"]
    documents = data["documents"]
    metadatas = data["metadatas"]


    # --------------------------------------------------
    # Process current batch
    # --------------------------------------------------

    for i in range(len(ids)):

        document = documents[i]

        if document is None:
            document = ""

        metadata = (
            metadatas[i]
            if metadatas
            else {}
        )

        all_rows.append({

            "id": ids[i],

            "document": document,

            "original_metadata": str(
                metadata
            )

        })


# --------------------------------------------------
# Create DataFrame
# --------------------------------------------------

print("\nCreating dataframe...")

df = pd.DataFrame(all_rows)


# --------------------------------------------------
# Clean text
# --------------------------------------------------

df["document"] = (
    df["document"]
    .fillna("")
    .astype(str)
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
    .str.strip()
)


# --------------------------------------------------
# Calculate document length
# --------------------------------------------------

df["word_count"] = df["document"].apply(
    lambda text: len(text.split())
)


# --------------------------------------------------
# Identify extremely short documents
# --------------------------------------------------

df["is_short"] = (
    df["word_count"] < 5
)


# --------------------------------------------------
# Corpus statistics
# --------------------------------------------------

print("\n===================================")
print("CORPUS STATISTICS")
print("===================================")

print(
    f"Documents retrieved: {len(df)}"
)

print(
    f"Short documents: "
    f"{df['is_short'].sum()}"
)

print(
    f"Average words/document: "
    f"{df['word_count'].mean():.2f}"
)

print(
    f"Minimum words/document: "
    f"{df['word_count'].min()}"
)

print(
    f"Maximum words/document: "
    f"{df['word_count'].max()}"
)


# --------------------------------------------------
# Verify document count
# --------------------------------------------------

if len(df) != total_documents:

    print("\nWARNING!")
    print(
        f"Expected {total_documents} documents "
        f"but retrieved {len(df)}."
    )

else:

    print(
        "\nDocument count verified successfully."
    )


# --------------------------------------------------
# Create output directory
# --------------------------------------------------

os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)


# --------------------------------------------------
# Save dataset
# --------------------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# Final message
# --------------------------------------------------

print("\n===================================")
print("CORPUS PREPARATION COMPLETE")
print("===================================")

print(
    f"Saved {len(df)} documents to:"
)

print(OUTPUT_PATH)