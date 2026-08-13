import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="ag_news"
)

print("ChromaDB initialized successfully.")
print("Documents:", collection.count())