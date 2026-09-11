import chromadb

# --------------------------------------------------
# Configuration
# --------------------------------------------------

CHROMA_PATH = "../Week5_Retrieval_Evaluation/chroma_db"
COLLECTION_NAME = "ag_news"

TEST_TOPIC_ID = 0

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

print("\n===================================")
print("TOPIC FILTERING TEST")
print("===================================")

print(f"Collection: {COLLECTION_NAME}")
print(f"Total documents: {collection.count()}")

# --------------------------------------------------
# Test topic filter
# --------------------------------------------------

print(f"\nTesting topic_id = {TEST_TOPIC_ID}")

results = collection.get(
    where={
        "topic_id": TEST_TOPIC_ID
    },
    limit=10,
    include=[
        "documents",
        "metadatas"
    ]
)

# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\n===================================")
print("FILTERED RESULTS")
print("===================================")

print(f"Documents returned: {len(results['ids'])}")

for i in range(len(results["ids"])):

    print("\n-----------------------------------")

    print(f"ID: {results['ids'][i]}")

    print(
        f"Metadata: "
        f"{results['metadatas'][i]}"
    )

    print(
        f"Document: "
        f"{results['documents'][i][:200]}..."
    )

# --------------------------------------------------
# Verify topic IDs
# --------------------------------------------------

print("\n===================================")
print("VERIFYING FILTER")
print("===================================")

invalid_results = []

for metadata in results["metadatas"]:

    if metadata.get("topic_id") != TEST_TOPIC_ID:
        invalid_results.append(metadata)

if len(invalid_results) == 0:

    print(
        f"SUCCESS: All returned documents "
        f"belong to topic_id = {TEST_TOPIC_ID}"
    )

else:

    print(
        "ERROR: Some documents have an "
        "incorrect topic_id."
    )

    print(invalid_results)

# --------------------------------------------------
# Final result
# --------------------------------------------------

print("\n===================================")
print("TOPIC FILTERING TEST COMPLETE")
print("===================================")