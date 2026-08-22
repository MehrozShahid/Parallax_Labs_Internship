import chromadb
from sentence_transformers import SentenceTransformer

from test_queries import test_queries


# CONFIGURATION
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "ag_news"

MODEL_NAME = "all-MiniLM-L6-v2"

# K values that we want to evaluate
K_VALUES = [1, 3, 5, 10]


# CONNECT TO CHROMADB
print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print("ChromaDB connected successfully.")
print("Collection:", COLLECTION_NAME)
print("Total chunks:", collection.count())


# LOAD EMBEDDING MODEL
print("\nLoading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


# PRECISION@K
def precision_at_k(retrieved_ids, ground_truth_ids, k):
    """
    Calculate Precision@K.

    Precision@K =
        Relevant retrieved chunks / Total retrieved chunks
    """

    retrieved_at_k = retrieved_ids[:k]

    if len(retrieved_at_k) == 0:
        return 0.0

    relevant_count = sum(
        1
        for chunk_id in retrieved_at_k
        if chunk_id in ground_truth_ids
    )

    return relevant_count / len(retrieved_at_k)


# RECALL@K
def recall_at_k(retrieved_ids, ground_truth_ids, k):
    """
    Calculate Recall@K.

    Recall@K =
        Relevant retrieved chunks / Total ground-truth chunks
    """

    if len(ground_truth_ids) == 0:
        return 0.0

    retrieved_at_k = retrieved_ids[:k]

    relevant_count = sum(
        1
        for chunk_id in retrieved_at_k
        if chunk_id in ground_truth_ids
    )

    return relevant_count / len(ground_truth_ids)


# RETRIEVE DOCUMENTS
def retrieve_chunks(query, k):
    """
    Convert the query into an embedding and
    retrieve the top K chunks from ChromaDB.
    """

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    retrieved_ids = results["ids"][0]

    return retrieved_ids


# MAIN EVALUATION
def main():

    print("\n")
    print("=" * 80)
    print("RETRIEVAL EVALUATION")
    print("=" * 80)

    print("Number of test queries:", len(test_queries))
    print("K values:", K_VALUES)

    # Store results for every K
    evaluation_results = {
        k: {
            "precision": [],
            "recall": []
        }
        for k in K_VALUES
    }

    # Maximum K required
    max_k = max(K_VALUES)

    # EVALUATE EACH QUERY
    for test in test_queries:

        query_id = test["id"]
        query = test["query"]
        ground_truth = test["ground_truth"]

        print("\n" + "=" * 80)
        print(f"Query ID: {query_id}")
        print(f"Query: {query}")
        print(f"Ground Truth: {ground_truth}")

        # Retrieve top max_k chunks
        retrieved_ids = retrieve_chunks(
            query,
            max_k
        )

        print(f"Retrieved Chunks: {retrieved_ids}")

        # Calculate metrics for each K
        for k in K_VALUES:

            precision = precision_at_k(
                retrieved_ids,
                ground_truth,
                k
            )

            recall = recall_at_k(
                retrieved_ids,
                ground_truth,
                k
            )

            evaluation_results[k]["precision"].append(
                precision
            )

            evaluation_results[k]["recall"].append(
                recall
            )

            print(
                f"K={k} | "
                f"Precision@{k}: {precision:.4f} | "
                f"Recall@{k}: {recall:.4f}"
            )

    # FINAL AVERAGE RESULTS
    print("\n")
    print("=" * 80)
    print("FINAL RETRIEVAL EVALUATION RESULTS")
    print("=" * 80)

    for k in K_VALUES:

        precision_values = evaluation_results[k]["precision"]
        recall_values = evaluation_results[k]["recall"]

        average_precision = (
            sum(precision_values)
            / len(precision_values)
        )

        average_recall = (
            sum(recall_values)
            / len(recall_values)
        )

        print(f"\nK = {k}")
        print(
            f"Average Precision@{k}: "
            f"{average_precision:.4f}"
        )
        print(
            f"Average Recall@{k}: "
            f"{average_recall:.4f}"
        )

    print("\n")
    print("=" * 80)
    print("Evaluation completed successfully.")
    print("=" * 80)


# RUN PROGRAM
if __name__ == "__main__":
    main()