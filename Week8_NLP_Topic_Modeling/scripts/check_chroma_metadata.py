import chromadb

CHROMA_PATH = "../Week5_Retrieval_Evaluation/chroma_db"
COLLECTION_NAME = "ag_news"

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print("\n===================================")
print("CHROMA DATABASE INFORMATION")
print("===================================")

print(f"Collection: {COLLECTION_NAME}")
print(f"Total documents: {collection.count()}")

print("\nGetting sample documents...")

sample = collection.get(
    limit=5,
    include=["documents", "metadatas"]
)

print("\n===================================")
print("SAMPLE DOCUMENTS")
print("===================================")

for i in range(len(sample["ids"])):
    print(f"\nID: {sample['ids'][i]}")
    print(f"Metadata: {sample['metadatas'][i]}")
    print(f"Document: {sample['documents'][i][:200]}...")

print("\n===================================")
print("CHECK COMPLETED")
print("===================================")