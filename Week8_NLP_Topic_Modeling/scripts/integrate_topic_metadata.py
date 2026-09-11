import chromadb
import pandas as pd
import os

# --------------------------------------------------
# Paths
# --------------------------------------------------

CHROMA_PATH = "../Week5_Retrieval_Evaluation/chroma_db"
COLLECTION_NAME = "ag_news"

TOPIC_DATA_PATH = "data/topic_documents.csv"

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

print("Connected successfully.")

print(f"Collection: {COLLECTION_NAME}")
print(f"Documents in ChromaDB: {collection.count()}")

# --------------------------------------------------
# Load topic assignments
# --------------------------------------------------

print("\nLoading topic assignments...")

df = pd.read_csv(TOPIC_DATA_PATH)

print(f"Topic documents loaded: {len(df)}")

required_columns = [
    "document",
    "topic_id",
    "topic_name"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# --------------------------------------------------
# Verify document count
# --------------------------------------------------

chroma_count = collection.count()
topic_count = len(df)

if chroma_count != topic_count:
    raise ValueError(
        f"Document count mismatch!\n"
        f"ChromaDB: {chroma_count}\n"
        f"Topic data: {topic_count}"
    )

print("Document counts match successfully.")

# --------------------------------------------------
# Verify expected ID structure
# --------------------------------------------------

print("\nChecking ChromaDB document IDs...")

sample = collection.get(
    limit=10,
    include=["documents"]
)

for i, doc_id in enumerate(sample["ids"]):
    expected_id = f"chunk_{i}"

    if doc_id != expected_id:
        raise ValueError(
            f"Unexpected document ID.\n"
            f"Expected: {expected_id}\n"
            f"Found: {doc_id}"
        )

print("ChromaDB IDs follow the expected chunk_0, chunk_1, ... structure.")

# --------------------------------------------------
# Update metadata
# --------------------------------------------------

print("\nStarting metadata integration...")
print("No embeddings will be regenerated.")

total_updated = 0

for start in range(0, len(df), BATCH_SIZE):

    end = min(
        start + BATCH_SIZE,
        len(df)
    )

    batch_df = df.iloc[start:end]

    ids = [
        f"chunk_{i}"
        for i in range(start, end)
    ]

    metadatas = []

    for _, row in batch_df.iterrows():

        metadata = {
            "topic_id": int(row["topic_id"]),
            "topic_name": str(row["topic_name"])
        }

        metadatas.append(metadata)

    collection.update(
        ids=ids,
        metadatas=metadatas
    )

    total_updated += len(ids)

    print(
        f"Updated {total_updated}/{len(df)} documents"
    )

# --------------------------------------------------
# Verify metadata
# --------------------------------------------------

print("\n===================================")
print("VERIFYING METADATA")
print("===================================")

verification = collection.get(
    ids=[
        "chunk_0",
        "chunk_1",
        "chunk_2",
        "chunk_3",
        "chunk_4"
    ],
    include=[
        "documents",
        "metadatas"
    ]
)

for i in range(len(verification["ids"])):

    print(f"\nID: {verification['ids'][i]}")
    print(
        f"Metadata: "
        f"{verification['metadatas'][i]}"
    )

# --------------------------------------------------
# Final output
# --------------------------------------------------

print("\n===================================")
print("TOPIC METADATA INTEGRATION COMPLETE")
print("===================================")

print(
    f"Total documents updated: {total_updated}"
)

print(
    "Added metadata fields:"
)

print(" - topic_id")
print(" - topic_name")

print(
    "\nExisting embeddings were reused."
)

print(
    "\nStep 5 completed successfully."
)