import chromadb
from sentence_transformers import SentenceTransformer


# Configuration

COLLECTION_NAME = "ag_news"
DEFAULT_TOP_K = 5


# Connect to ChromaDB

client = chromadb.PersistentClient(
    path="../chroma_db"
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

# Load embedding model

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Semantic Search Function
def semantic_search(query, top_k=DEFAULT_TOP_K):

    # Handle malformed query
    if not isinstance(query, str):
        print("Invalid query. Query must be a string.")
        return []

    # Handle empty query
    if not query.strip():
        print("Invalid query. Query cannot be empty.")
        return []

    # Handle invalid top_k
    if not isinstance(top_k, int) or top_k <= 0:
        print("Invalid top_k. It must be a positive integer.")
        return []

    # Check whether database is empty
    total_documents = collection.count()

    if total_documents == 0:
        print("ChromaDB is empty. No documents available for search.")
        return []

    # Don't request more documents than available
    top_k = min(top_k, total_documents)

    # Generate embedding for query
    query_embedding = model.encode(query).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # Return results
    return results


# Test Search
if __name__ == "__main__":

    query = input(
        "Enter your search query: "
    )

    results = semantic_search(
        query,
        top_k=5
    )

    if results:

        print("\nSearch Results")
        print("=" * 60)

        documents = results["documents"][0]
        distances = results["distances"][0]
        ids = results["ids"][0]

        for index, (doc, distance, doc_id) in enumerate(
            zip(documents, distances, ids),
            start=1
        ):

            print(f"\nResult {index}")
            print(f"ID: {doc_id}")
            print(f"Distance: {distance:.4f}")
            print(f"Chunk: {doc}")

            print("-" * 60)