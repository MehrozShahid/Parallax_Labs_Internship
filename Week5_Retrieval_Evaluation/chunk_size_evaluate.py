import os
import csv

import chromadb
from sentence_transformers import SentenceTransformer

from test_queries import test_queries


# CONFIGURATION
MODEL_NAME = "all-MiniLM-L6-v2"

EXPERIMENT_PATH = "./chunk_experiments"

CHUNK_SIZES = [250, 500, 750, 1000]

K_VALUES = [1, 3, 5, 10]

OUTPUT_FILE = "evaluation_results.csv"

# LOAD EMBEDDING MODEL
print("=" * 60)
print("CHUNK SIZE RETRIEVAL EVALUATION")
print("=" * 60)

print("\nLoading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded.")


# PRECISION FUNCTION
def precision_at_k(retrieved_ids, ground_truth_ids, k):

    retrieved = retrieved_ids[:k]

    if len(retrieved) == 0:
        return 0.0

    relevant = sum(
        1 for doc_id in retrieved
        if doc_id in ground_truth_ids
    )

    return relevant / len(retrieved)


# RECALL FUNCTION
def recall_at_k(retrieved_ids, ground_truth_ids, k):

    retrieved = retrieved_ids[:k]

    if len(ground_truth_ids) == 0:
        return 0.0

    relevant = sum(
        1 for doc_id in retrieved
        if doc_id in ground_truth_ids
    )

    return relevant / len(ground_truth_ids)


# EVALUATE EACH CHUNK SIZE
all_results = []


for chunk_size in CHUNK_SIZES:

    print("\n")
    print("=" * 60)
    print(f"CHUNK SIZE = {chunk_size}")
    print("=" * 60)

    db_path = os.path.join(
        EXPERIMENT_PATH,
        f"chroma_{chunk_size}"
    )

    collection_name = f"ag_news_{chunk_size}"

    # Connect to database
    client = chromadb.PersistentClient(
        path=db_path
    )

    collection = client.get_collection(
        name=collection_name
    )

    print(
        "Documents in collection:",
        collection.count()
    )

    # Evaluate each K
    for k in K_VALUES:

        precision_scores = []
        recall_scores = []

        print("\n")
        print("-" * 50)
        print(f"K = {k}")
        print("-" * 50)

        # Run all test queries
        for test in test_queries:

            query = test["query"]

            ground_truth = set(
                test["ground_truth"]
            )

            # Generate query embedding
            query_embedding = model.encode(
                query
            ).tolist()

            # Retrieve documents
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )

            retrieved_ids = results["ids"][0]

            # Calculate metrics
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

            precision_scores.append(
                precision
            )

            recall_scores.append(
                recall
            )

        # Average metrics
        avg_precision = (
            sum(precision_scores)
            / len(precision_scores)
        )

        avg_recall = (
            sum(recall_scores)
            / len(recall_scores)
        )

        print(
            f"Precision@{k}: "
            f"{avg_precision:.4f}"
        )

        print(
            f"Recall@{k}: "
            f"{avg_recall:.4f}"
        )

        # Store results
        all_results.append({
            "chunk_size": chunk_size,
            "k": k,
            "precision": round(
                avg_precision,
                4
            ),
            "recall": round(
                avg_recall,
                4
            )
        })


# SAVE RESULTS
print("\n")
print("=" * 60)
print("FINAL RESULTS")
print("=" * 60)

with open(
    OUTPUT_FILE,
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "chunk_size",
            "k",
            "precision",
            "recall"
        ]
    )

    writer.writeheader()

    writer.writerows(
        all_results
    )


# DISPLAY RESULTS
for result in all_results:

    print(
        f"Chunk Size: {result['chunk_size']} | "
        f"K: {result['k']} | "
        f"Precision: {result['precision']:.4f} | "
        f"Recall: {result['recall']:.4f}"
    )


print("\nResults saved to:")
print(OUTPUT_FILE)