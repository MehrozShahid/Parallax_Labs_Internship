# Week 5 – Retrieval Evaluation

## Overview

This week focused on evaluating and improving the document retrieval system developed in the previous weeks.

The main goal was to measure how accurately the retrieval system returns relevant document chunks for user queries and to improve retrieval performance by experimenting with different hyperparameters.

The project uses the **AG News dataset**, **Sentence Transformers**, and **ChromaDB** for semantic search and retrieval.

---

## Objectives

* Create a manual test set containing 20 user queries.
* Identify the expected ground-truth chunks for each query.
* Implement retrieval evaluation using **Precision@K** and **Recall@K**.
* Test different K values.
* Experiment with different chunk sizes.
* Compare evaluation results.
* Refine the retrieval logic based on the evaluation findings.
* Document the final results and improvements.

---

## Technologies Used

* Python
* Pandas
* ChromaDB
* Sentence Transformers
* `all-MiniLM-L6-v2`
* LangChain Text Splitters
* AG News Dataset

---

## Project Structure

```text
Week5_Retrieval_Evaluation/
│
├── chroma_db/
│
├── chunk_experiments/
│   ├── chroma_250/
│   ├── chroma_500/
│   ├── chroma_750/
│   └── chroma_1000/
│
├── dataset/
│   └── cleaned_train.csv
│
├── check_chroma.py
├── chunk_size_evaluate.py
├── chunk_size_experiment.py
├── chunk_size_summary.csv
├── evaluation_report.md
├── evaluation_results.csv
├── inspect_chroma.py
├── README.md
├── retrieval_evaluate.py
├── retrieval_refined.py
└── test_queries.py
```
---

## 1. Manual Test Set

A manual test set of **20 user queries** was created to evaluate the retrieval system.

Each query contains:

* A user query
* Expected relevant document/chunk IDs

Example:

```python
test_queries = [
    {
        "query": "Intel develops new computer technology",
        "ground_truth": ["chunk_50012"]
    }
]
```

The ground-truth chunks were identified by manually checking the indexed documents and selecting the chunks that are relevant to each query.

---

## 2. Retrieval Evaluation

The retrieval evaluation script connects to the existing ChromaDB collection and retrieves documents for each test query.

The embedding model used is:

```text
all-MiniLM-L6-v2
```

The evaluation was performed using different K values:

```python
K_VALUES = [1, 3, 5, 10]
```

This allows the system to be evaluated based on how many retrieved results are considered.

---

## 3. Precision@K

Precision@K measures how many of the top K retrieved results are relevant.

```text
Precision@K = Relevant Retrieved Documents / K
```

For example, if 3 relevant documents are found among the top 5 results:

```text
Precision@5 = 3 / 5 = 0.60
```

A higher Precision@K means that the retrieval results contain more relevant documents.

---

## 4. Recall@K

Recall@K measures how many of the relevant ground-truth documents were successfully retrieved.

```text
Recall@K = Relevant Retrieved Documents / Total Relevant Documents
```

For example, if there are 4 relevant documents and the system retrieves 3 of them:

```text
Recall@K = 3 / 4 = 0.75
```

A higher Recall@K means that the system is better at finding the relevant documents.

---

## 5. K Value Experiment

Different K values were tested:

```text
K = 1
K = 3
K = 5
K = 10
```

Testing different K values helps determine how many search results should be returned.

A small K value provides fewer but more focused results, while a larger K value improves the chance of retrieving relevant documents but may also introduce irrelevant results.

---

## 6. Chunk Size Experiment

Different chunk sizes were also tested to determine their effect on retrieval quality.

The chunking process uses:

```python
RecursiveCharacterTextSplitter
```

The experiment compares retrieval performance using different chunk sizes.

For example:

```text
Chunk Size = 250
Chunk Size = 500
Chunk Size = 750
Chunk Size = 1000
```

The results were compared using Precision@K and Recall@K.

---

## 7. Evaluation Findings

The evaluation showed that retrieval performance depends on both the number of returned results and the chunking strategy.

### K Value

Increasing K generally improves the chance of retrieving the correct ground-truth chunk, which can improve recall.

However, larger K values may also return more irrelevant results, which can reduce precision.

### Chunk Size

Smaller chunks can provide more focused information and reduce unnecessary text.

Larger chunks contain more context but may include unrelated information.

Therefore, the chunk size needs to balance:

* Relevance
* Context
* Retrieval accuracy
* Number of unnecessary results

---

## 8. Retrieval Refinement

The final refined retrieval implementation is contained in:

retrieval_refined.py

The refined retrieval system uses the configuration:

CHROMA_PATH = "./chroma_db"

COLLECTION_NAME = "ag_news"


MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5

The value: TOP_K = 5

was selected based on the Week 5 retrieval evaluation.

Refined Retrieval Workflow

The retrieval process works as follows:

User Query
     ↓
Sentence Transformer
     ↓
Query Embedding
     ↓
ChromaDB Similarity Search
     ↓
Top 5 Results
     ↓
Display Retrieved Documents

---

## 10. How to Run

### Step 1: Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

---

### Step 2: Install dependencies

```bash
pip install chromadb pandas sentence-transformers langchain-text-splitters
```

---

### Step 3: Make sure ChromaDB exists

The existing ChromaDB database should be available in:

```text
./chroma_db
```

The collection name used by the project is:

```text
ag_news
```

---

### Step 4: Run the retrieval evaluation

```bash
python retrieval_evaluate.py
```

The script evaluates the test queries using different K values and displays the retrieval metrics.

---

### Step 5: Run the chunk-size experiment

```bash
python chunk_size_experiment.py
```

This tests different chunk sizes and compares their retrieval performance.

---

### Step 6: Run the refined retrieval

```bash
python retrieval_refined.py
```

This runs the improved retrieval logic based on the evaluation findings.

---

## 11. Example Output

The evaluation produces results similar to:

```text
K = 1
Precision@1: ...
Recall@1: ...

K = 3
Precision@3: ...
Recall@3: ...

K = 5
Precision@5: ...
Recall@5: ...

K = 10
Precision@10: ...
Recall@10: ...
```

The exact values depend on the selected test queries, ground-truth chunks, chunk size, and retrieval configuration.

---

## 12. Conclusion

Week 5 focused on measuring and improving the performance of the semantic retrieval system.

A manual test set was created, Precision@K and Recall@K were implemented, and different K values and chunk sizes were tested.

The experiments demonstrated that retrieval performance depends on selecting appropriate chunk sizes and K values. The retrieval logic was then refined using the evaluation findings while keeping the implementation simple and compatible with the existing ChromaDB setup.

This evaluation provides a measurable way to assess the quality of the retrieval system and creates a foundation for further improvements in future weeks.

## Week 5 Completed Tasks

* [x] Created 20 manual test queries.
* [x] Identified ground-truth chunks.
* [x] Implemented retrieval evaluation.
* [x] Calculated Precision@K.
* [x] Calculated Recall@K.
* [x] Tested different K values.
* [x] Experimented with chunk sizes.
* [x] Compared retrieval performance.
* [x] Refined the retrieval logic.
* [x] Documented the evaluation process and findings.
