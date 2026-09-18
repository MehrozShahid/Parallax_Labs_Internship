import pandas as pd
import chromadb


# CONFIGURATION
CHROMA_PATH = r"C:\Users\HP\Week4_Vector_Database\chroma_db"
COLLECTION_NAME = "ag_news"

NER_CSV_PATH = r"C:\Users\HP\Week9_NLP_Analysis\results\ner_topic_documents.csv"


# LOAD NER DATA
print("Loading NER metadata...")

df = pd.read_csv(NER_CSV_PATH)

print("NER documents loaded:", len(df))


# CONNECT TO CHROMADB
print("\nConnecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print("ChromaDB connected successfully.")
print("Collection:", COLLECTION_NAME)
print("Total chunks:", collection.count())


# UPDATE METADATA IN BATCHES
batch_size = 1000
updated = 0

print("\nUpdating ChromaDB metadata...")

for start in range(0, len(df), batch_size):

    batch = df.iloc[start:start + batch_size]

    ids = batch["id"].astype(str).tolist()

    # Get existing metadata
    existing = collection.get(
        ids=ids,
        include=["metadatas"]
    )

    existing_metadata = {}

    for chunk_id, metadata in zip(
        existing["ids"],
        existing["metadatas"]
    ):
        existing_metadata[chunk_id] = metadata or {}

    update_ids = []
    update_metadatas = []

    for _, row in batch.iterrows():

        chunk_id = str(row["id"])

        if chunk_id not in existing_metadata:
            continue

        # Keep existing metadata
        metadata = dict(
            existing_metadata[chunk_id]
        )

        # Add NER metadata
        entities = row["entities"]

        if pd.isna(entities):
            entities = ""

        entity_types = row["entity_types"]

        if pd.isna(entity_types):
            entity_types = ""

        metadata["entities"] = str(entities)
        metadata["entity_types"] = str(entity_types)

        update_ids.append(chunk_id)
        update_metadatas.append(metadata)

    if update_ids:
        collection.update(
            ids=update_ids,
            metadatas=update_metadatas
        )

        updated += len(update_ids)

    print(
        f"Updated {min(start + batch_size, len(df))}/{len(df)} chunks"
    )


# FINAL RESULT
print("\n" + "=" * 60)
print("NER METADATA UPDATE COMPLETE")
print("=" * 60)

print("Chunks updated:", updated)
print("Collection total:", collection.count())