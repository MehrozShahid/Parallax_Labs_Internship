import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="ag_news"
)

print("Total chunks:", collection.count())

results = collection.get(
    limit=50,
    offset=50000,
    include=["documents", "metadatas"]
)

for i in range(len(results["documents"])):

    print("\n" + "=" * 80)

    print("INDEX:", i + 50000)
    print("ID:", results["ids"][i])

    print("DOCUMENT:")
    print(results["documents"][i])

    print("METADATA:")
    print(results["metadatas"][i])