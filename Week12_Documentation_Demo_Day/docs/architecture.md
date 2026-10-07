# RAG System Architecture

## 1. Overview

The project is a Retrieval-Augmented Generation (RAG) system built around the AG News dataset.

The system combines semantic vector retrieval, entity-aware reranking, and Large Language Model (LLM) generation. A FastAPI application provides an API interface through which users can submit natural-language questions.

The main purpose of the architecture is to retrieve relevant information from the AG News knowledge base before generating an answer.

---

## 2. High-Level Architecture

```text
                    AG News Dataset
                          │
                          ▼
                Data Preprocessing
                          │
                          ▼
                   Text Chunking
                    500 / 50
                          │
                          ▼
              Sentence Embeddings
             all-MiniLM-L6-v2
                          │
                          ▼
                     ChromaDB
                  ag_news collection
                          │
                          │
                    User Question
                          │
                          ▼
                    FastAPI API
                          │
                          ▼
                  Query Embedding
                          │
                          ▼
                 Candidate Retrieval
                     Candidate K=30
                          │
                          ▼
              Entity-Aware Reranking
                   Entity Boost=0.20
                          │
                          ▼
                  Top K Context
                       Top K=5
                          │
                          ▼
                    LLM Generation
                  openrouter/free
                          │
                          ▼
                   Generated Answer
                          │
                          ▼
                     API Response
                          │
                          ▼
                 Evaluation & Testing
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        Retrieval     Generation    Latency
          Metrics       Metrics      Metrics
```

The visual version of this architecture is available in:

```text
images/architecture_diagram.png
```

---

## 3. System Components

### 3.1 AG News Dataset

The project uses the AG News dataset as the knowledge source.

The dataset contains news articles covering major categories including:

* World
* Sports
* Business
* Technology

The processed content is stored in the vector database for semantic retrieval.

---

### 3.2 Data Preprocessing

Before indexing, the news data is processed to make it suitable for retrieval.

The preprocessing stage prepares the text and associated information for downstream chunking, embedding, and entity extraction.

---

### 3.3 Text Chunking

Long documents are divided into smaller chunks.

The project uses:

* Chunk size: **500**
* Chunk overlap: **50**

Chunking allows the retrieval system to retrieve focused sections of documents rather than unnecessarily large documents.

---

### 3.4 Sentence Embeddings

Each text chunk is converted into a numerical vector representation using:

```text
all-MiniLM-L6-v2
```

These embeddings allow semantically similar questions and documents to be compared.

---

### 3.5 ChromaDB

ChromaDB is used as the vector database.

The main collection is:

```text
ag_news
```

The Week 10 API metadata reports:

```text
Document count: 120526
```

The vector database stores the embedded chunks and metadata required for retrieval and reranking.

---

## 4. Query Processing

When a user submits a question, the following process occurs.

### Step 1 — User Question

The user submits a natural-language question through:

```text
POST /query
```

Example:

```json
{
  "question": "What technology development is discussed?"
}
```

---

### Step 2 — Query Embedding

The question is converted into an embedding using the same:

```text
all-MiniLM-L6-v2
```

embedding model used for the stored documents.

---

### Step 3 — Candidate Retrieval

The system performs semantic retrieval against ChromaDB.

The configured candidate pool is:

```text
Candidate K = 30
```

The initial retrieval therefore provides up to 30 candidate chunks for further ranking.

---

### Step 4 — Entity-Aware Reranking

The system also uses Named Entity Recognition (NER) information.

The NER model is:

```text
en_core_web_sm
```

Entity information is stored as metadata.

The configured entity boost is:

```text
0.20
```

The final ranking combines semantic relevance with entity-related information.

---

### Step 5 — Top-K Selection

After reranking, the system selects:

```text
Top K = 5
```

chunks as the final retrieval context.

---

## 5. Entity-Aware Retrieval

The project extends basic semantic retrieval with entity-aware information.

The retrieved chunks can contain metadata such as:

```text
entities
entity_types
```

Example:

```json
{
  "entities": "Adam Kennedy:PERSON; Angels:ORG",
  "entity_types": "PERSON; ORG"
}
```

The system calculates an entity contribution and combines it with the semantic score.

The response exposes:

```text
semantic_score
entity_score
final_score
matched_entities
```

This makes the retrieval process more transparent.

---

## 6. LLM Generation

The retrieved chunks are passed to the configured LLM.

The Week 10 configuration uses:

```text
openrouter/free
```

The LLM generates an answer using the retrieved context.

The system can also return:

```text
I don't know.
```

when the generation process does not produce a sufficiently supported answer.

This helps reduce unsupported responses.

---

## 7. FastAPI Layer

FastAPI provides the HTTP interface for the system.

The main endpoints are:

| Method | Endpoint    | Purpose                |
| ------ | ----------- | ---------------------- |
| GET    | `/`         | API status             |
| GET    | `/health`   | System health          |
| GET    | `/metadata` | System configuration   |
| POST   | `/query`    | RAG question answering |

Swagger documentation is available through:

```text
http://127.0.0.1:8000/docs
```

---

## 8. API Response

The `/query` endpoint returns structured information including:

* Generated answer
* Support status
* Retrieved chunks
* Metadata
* Semantic scores
* Entity scores
* Final scores
* Matched entities
* Retrieval timing
* Generation timing
* Total latency

Example response fields:

```json
{
  "answer": "I don't know.",
  "sources": [],
  "supported": false,
  "retrieved_chunks": [],
  "retrieval_time": 0.15,
  "generation_time": 5.66,
  "total_time": 5.81,
  "latency_ms": 5816.01
}
```

---

## 9. Evaluation Layer

Week 11 evaluated the API using 30 questions distributed across:

| Category   | Questions |
| ---------- | --------: |
| Business   |         8 |
| Sports     |         7 |
| Technology |         8 |
| World      |         7 |
| **Total**  |    **30** |

The evaluation measured:

* Retrieval Accuracy Proxy
* Generation Quality Proxy
* Supported Answer Rate
* End-to-end latency
* Retrieval latency
* Generation latency
* Request failures

---

## 10. Final Evaluation Results

The final Week 11 benchmark produced:

| Metric                   |       Result |
| ------------------------ | -----------: |
| Questions                |           30 |
| Successful Requests      |           25 |
| Failed Requests          |            5 |
| Retrieval Accuracy Proxy |        96.0% |
| Generation Quality Proxy |       41.33% |
| Supported Answer Rate    |        56.0% |
| Average Latency          | 23,556.23 ms |
| Median Latency           | 17,468.09 ms |
| P95 Latency              | 55,321.89 ms |
| Minimum Latency          |   3,760.1 ms |
| Maximum Latency          | 57,558.81 ms |
| Average Retrieval Time   |      52.7 ms |
| P95 Retrieval Time       |     71.63 ms |
| Average Generation Time  | 16,756.49 ms |
| P95 Generation Time      | 47,172.94 ms |

---

## 11. Performance Interpretation

The evaluation indicates that the retrieval component is comparatively fast.

Average retrieval time was:

```text
52.7 ms
```

while average generation time was:

```text
16,756.49 ms
```

Therefore, LLM generation contributes substantially more to overall response latency than vector retrieval.

The P95 generation time was:

```text
47,172.94 ms
```

The evaluation also recorded five requests that reached the 60-second HTTP timeout.

This identifies LLM generation latency and generation quality as important areas for future optimization.

---

## 12. End-to-End Request Flow

The complete request flow is:

```text
User
  │
  ▼
POST /query
  │
  ▼
FastAPI
  │
  ▼
Create Query Embedding
  │
  ▼
ChromaDB Semantic Retrieval
  │
  ▼
Candidate K = 30
  │
  ▼
Entity-Aware Reranking
  │
  ▼
Top K = 5
  │
  ▼
Retrieved Context
  │
  ▼
LLM
  │
  ▼
Generated Answer
  │
  ▼
FastAPI JSON Response
```

---

## 13. Evaluation and Testing Flow

```text
FastAPI API
     │
     ├── API Tests
     │
     ├── Concurrent Tests
     │
     └── Evaluation Script
             │
             ▼
        30 Questions
             │
             ▼
       Metric Calculation
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
   Retrieval Generation Latency
      Proxy    Proxy
       │        │
       └────┬───┘
            ▼
      Evaluation Report
```

---

## 14. Architecture Summary

The final system combines:

1. AG News as the knowledge source.
2. Text preprocessing and chunking.
3. `all-MiniLM-L6-v2` embeddings.
4. ChromaDB vector storage.
5. Semantic candidate retrieval.
6. Entity-aware reranking.
7. Top-5 context selection.
8. LLM-based answer generation.
9. FastAPI REST endpoints.
10. Automated evaluation and testing.

This architecture provides a complete RAG pipeline from data ingestion to API-based question answering and system evaluation.
