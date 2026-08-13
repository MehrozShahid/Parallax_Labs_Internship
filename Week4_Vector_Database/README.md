# Week 4 — Vector Database with ChromaDB

## Overview

This week focuses on integrating ChromaDB as a local vector database.

The cleaned text data and embeddings generated in the previous weeks are used to store document chunks and their embeddings in ChromaDB. Semantic search is then implemented to retrieve the most relevant chunks for a given query.

Retrieval performance is also tested using 10 different queries, and retrieval latency is recorded for each query.

---

## Objectives

The main objectives of Week 4 were:

- Set up and configure ChromaDB locally.
- Store text chunks and their embeddings in ChromaDB.
- Implement semantic search.
- Retrieve the Top-K most relevant chunks for a query.
- Test retrieval performance using 10 different queries.
- Record retrieval latency.
- Handle edge cases such as empty databases and invalid queries.

---

## Technologies Used

- Python
- ChromaDB
- Pandas
- Sentence Transformers
- `all-MiniLM-L6-v2`

---

## Project Structure

```text
Week4_Vector_Database/
│
├── chroma_db/
│
├── dataset/
│   └── cleaned_train.csv
│
├── logs/
│   └── retrieval_log.csv
│
├── src/
│   ├── chroma_db.py
│   ├── ingest.py
│   ├── search.py
│   └── retrieval_test.py
│
├── .gitignore
└── README.md