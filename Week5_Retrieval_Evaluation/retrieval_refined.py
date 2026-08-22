import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

CHROMA_PATH = "./chroma_db"

COLLECTION_NAME = "ag_news"

MODEL_NAME = "all-MiniLM-L6-v2"

# Selected after Week 5 evaluation
TOP_K = 5


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print(
    f"Connected successfully."
)

print(
    f"Total chunks: {collection.count()}"
)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

model = SentenceTransformer(
    MODEL_NAME
)

print("Embedding model loaded.")



# RETRIEVAL FUNCTION
def retrieve_documents(query, k=TOP_K):

    """
    Retrieve the top-k most relevant chunks
    for a user query.
    """

    # Create embedding for the query
    query_embedding = model.encode(
        query
    ).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=k
    )

    documents = results["documents"][0]

    distances = results["distances"][0]

    return documents, distances


# TEST RETRIEVAL
query = input(
    "\nEnter your search query: "
)


documents, distances = retrieve_documents(
    query
)

# DISPLAY RESULTS
print("\n" + "=" * 70)

print(
    f"TOP {TOP_K} RETRIEVAL RESULTS"
)

print("=" * 70)


for i, (document, distance) in enumerate(
    zip(documents, distances),
    start=1
):

    print(
        f"\nResult {i}"
    )

    print(
        f"Distance: {distance:.4f}"
    )

    print(
        f"Document:\n{document}"
    )

    print("-" * 70)