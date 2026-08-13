import time
import pandas as pd

from search import semantic_search


queries = [
    "technology companies",
    "international sports",
    "US politics",
    "business and finance",
    "computer technology",
    "football match",
    "stock market",
    "scientific research",
    "world news",
    "economic growth"
]


results_log = []


for query in queries:

    start_time = time.perf_counter()

    results = semantic_search(
        query,
        top_k=5
    )

    end_time = time.perf_counter()

    retrieval_time = (end_time - start_time) * 1000

    if results:
        result_count = len(results["documents"][0])
    else:
        result_count = 0

    results_log.append({
        "query": query,
        "top_k": 5,
        "retrieval_time_ms": retrieval_time,
        "results": result_count
    })

    print(
        f"Query: {query} | "
        f"Time: {retrieval_time:.2f} ms | "
        f"Results: {result_count}"
    )


df = pd.DataFrame(results_log)

df.to_csv(
    "../logs/retrieval_log.csv",
    index=False
)

print("\nRetrieval testing completed.")
print("Log saved to logs/retrieval_log.csv")