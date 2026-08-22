import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="ag_news"
)

print("Collection:", collection.name)
print("Number of documents:", collection.count())