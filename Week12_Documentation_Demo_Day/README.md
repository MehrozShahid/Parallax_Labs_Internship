# Week 12 — Documentation & Demo Day

## Project Title

**AG News Retrieval-Augmented Generation (RAG) API**

---

## 1. Project Overview

This project is a Retrieval-Augmented Generation (RAG) system built using the AG News dataset.

The system retrieves relevant news content from a ChromaDB vector database and uses an LLM to generate answers based on the retrieved context.

The project was developed progressively during the Parallax Labs internship.

The complete workflow includes:

```text
Data Acquisition
      ↓
Data Cleaning & Preprocessing
      ↓
Chunking & Embeddings
      ↓
Vector Database
      ↓
Retrieval Evaluation
      ↓
RAG Generation
      ↓
Hallucination Detection & Mitigation
      ↓
NLP Topic Modeling
      ↓
NER & Entity-Aware Retrieval
      ↓
FastAPI API
      ↓
System Evaluation & Testing
      ↓
Documentation & Demo
```

---

# 2. Problem Statement

A conventional language model may generate an answer without having direct access to the required knowledge source.

This can lead to unsupported or hallucinated answers.

The purpose of this project is to build a RAG pipeline that retrieves relevant information from a known knowledge base before generating an answer.

---

# 3. Objectives

The main objectives are:

* Build a complete RAG pipeline.
* Store AG News content in a vector database.
* Perform semantic retrieval.
* Improve retrieval using entity-aware reranking.
* Generate context-based answers.
* Expose the system through a FastAPI REST API.
* Evaluate retrieval and generation performance.
* Measure API latency.
* Test API behavior automatically.
* Document the complete system for demonstration and reuse.

---

# 4. Main Features

The final system provides:

* AG News knowledge base
* Text chunking
* Sentence embeddings
* ChromaDB vector search
* Semantic retrieval
* Entity-aware reranking
* Named Entity Recognition
* Context-based LLM generation
* Grounded `"I don't know."` behavior
* FastAPI REST API
* Swagger documentation
* Health monitoring
* Metadata endpoint
* Automated testing
* Performance evaluation

---

# 5. Technology Stack

| Technology            | Purpose                    |
| --------------------- | -------------------------- |
| Python                | Main programming language  |
| FastAPI               | REST API                   |
| ChromaDB              | Vector database            |
| Sentence Transformers | Text embeddings            |
| `all-MiniLM-L6-v2`    | Embedding model            |
| spaCy                 | Named Entity Recognition   |
| `en_core_web_sm`      | NER model                  |
| OpenRouter            | LLM access                 |
| `openrouter/free`     | Configured LLM             |
| Pytest                | Automated testing          |
| Pandas                | Evaluation/data processing |
| NumPy                 | Numerical processing       |

---

# 6. Architecture

The high-level architecture is:

```text
AG News Dataset
      │
      ▼
Preprocessing
      │
      ▼
Chunking
      │
      ▼
all-MiniLM-L6-v2
      │
      ▼
ChromaDB
      │
      │
      │       User Question
      │             │
      │             ▼
      │          FastAPI
      │             │
      │             ▼
      │       Query Embedding
      │             │
      │             ▼
      │      Candidate Retrieval
      │             │
      │             ▼
      │    Entity-Aware Reranking
      │             │
      │             ▼
      │        Top 5 Context
      │             │
      │             ▼
      │            LLM
      │             │
      │             ▼
      │       Generated Answer
      │             │
      │             ▼
      └──────── API Response
```

A detailed explanation is available in:

```text
docs/architecture.md
```

The visual architecture diagram is located at:

```text
images/architecture_diagram.png
```

---

# 7. Vector Database Configuration

The API metadata reports the following configuration:

| Setting         | Value                                          |
| --------------- | ---------------------------------------------- |
| Collection      | `ag_news`                                      |
| Document Count  | `120526`                                       |
| Embedding Model | `all-MiniLM-L6-v2`                             |
| Retrieval Type  | Semantic retrieval with entity-aware reranking |
| Top K           | `5`                                            |
| Candidate K     | `30`                                           |
| Entity Boost    | `0.2`                                          |
| NER Model       | `en_core_web_sm`                               |
| LLM Model       | `openrouter/free`                              |

---

# 8. Chunking

The project uses:

```text
Chunk size: 500
Overlap: 50
```

Chunking allows large documents to be divided into smaller retrieval units.

---

# 9. Entity-Aware Retrieval

The project extends semantic retrieval by incorporating named entities.

NER information is stored in the retrieved document metadata.

Example:

```json
{
  "entities": "Adam Kennedy:PERSON; Angels:ORG",
  "entity_types": "PERSON; ORG"
}
```

The configured entity boost is:

```text
0.20
```

The API exposes:

```text
semantic_score
entity_score
final_score
matched_entities
```

This provides greater visibility into how retrieved chunks are ranked.

---

# 10. API Endpoints

The API provides four main endpoints.

| Method | Endpoint    | Description        |
| ------ | ----------- | ------------------ |
| GET    | `/`         | API status         |
| GET    | `/health`   | Health check       |
| GET    | `/metadata` | RAG configuration  |
| POST   | `/query`    | Question answering |

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# 11. Setup

## Step 1 — Open Week 11

The executable API remains in the Week 11 project:

```text
C:\Users\HP\Week11_System_Testing
```

Week 12 contains the documentation and Demo Day materials.

---

## Step 2 — Activate Python Environment

The project can use the existing Python environment:

```bat
C:\Users\HP\Week2_Data_Cleaning_Preprocessing\.venv\Scripts\activate
```

---

## Step 3 — Go to the API Project

```bat
cd C:\Users\HP\Week11_System_Testing
```

---

## Step 4 — Configure Environment Variables

The actual API key should remain in the local `.env` file used by Week 11.

Never commit the real API key to Git.

The Week 12 `.env.example` file contains only the variable name and a placeholder.

---

# 12. Run the API

Start FastAPI using:

```bash
uvicorn app.main:app --reload
```

The server should start at:

```text
http://127.0.0.1:8000
```

---

# 13. Open Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger provides an interactive interface for testing the API.

---

# 14. Example Query

Send a POST request to:

```text
/query
```

with:

```json
{
  "question": "What company activity is described?"
}
```

The API returns a structured response containing the generated answer, support status, retrieved chunks, ranking scores, and timing information.

More API examples are available in:

```text
docs/api_examples.md
```

---

# 15. Example Questions

### Business

```text
What company activity is described?
```

### Sports

```text
What happened to the team or player?
```

### Technology

```text
What technology development is discussed?
```

### World

```text
What country or international issue appears in the context?
```

---

# 16. Grounded Answer Behavior

The system may return:

```text
I don't know.
```

when the generated answer is not sufficiently supported by the retrieved context.

This behavior helps prevent the system from producing unsupported information.

The evaluation demonstrated that retrieval and generation performance are separate aspects of the system.

---

# 17. Week 11 Evaluation

The API was evaluated using 30 questions.

The questions covered:

* Business — 8
* Sports — 7
* Technology — 8
* World — 7

### Final Results

| Metric                   |           Result |
| ------------------------ | ---------------: |
| Total Questions          |               30 |
| Successful Requests      |               25 |
| Failed Requests          |                5 |
| Retrieval Accuracy Proxy |        **96.0%** |
| Generation Quality Proxy |       **41.33%** |
| Supported Answer Rate    |        **56.0%** |
| Average Latency          | **23,556.23 ms** |
| Median Latency           | **17,468.09 ms** |
| P95 Latency              | **55,321.89 ms** |
| Minimum Latency          |   **3,760.1 ms** |
| Maximum Latency          | **57,558.81 ms** |
| Average Retrieval Time   |      **52.7 ms** |
| P95 Retrieval Time       |     **71.63 ms** |
| Average Generation Time  | **16,756.49 ms** |
| P95 Generation Time      | **47,172.94 ms** |

---

# 18. Evaluation Methodology

### Retrieval Accuracy Proxy

Retrieval accuracy is a proxy metric.

It checks whether at least one expected keyword occurs in the retrieved documents.

It is not true Precision@K or Recall@K because the evaluation does not contain manually labeled gold document IDs for all questions.

### Generation Quality Proxy

Generation quality is also a proxy.

It combines:

* Existing `supported` flag
* Expected keyword coverage

The metric should therefore not be interpreted as a human evaluation score.

### Latency

Latency measures the end-to-end HTTP request time.

The API separately reports retrieval and generation timings.

---

# 19. Performance Analysis

The evaluation showed that retrieval is relatively fast.

Average retrieval time:

```text
52.7 ms
```

Average generation time:

```text
16,756.49 ms
```

Therefore, generation is the main contributor to total latency.

The P95 generation time was:

```text
47,172.94 ms
```

Five requests failed because they reached the 60-second HTTP timeout.

These results identify LLM generation latency and generation quality as the main areas for future improvement.

---

# 20. Testing

Week 11 includes automated tests for the API.

Testing includes:

* API endpoint testing
* Request/response behavior
* Concurrent request testing

Pytest is used for automated testing.

The evaluation script tests the running API using a 30-question benchmark.

---

# 21. Reports

The Week 11 evaluation reports are located in:

```text
Week11_System_Testing/reports/
```

They include:

```text
evaluation_report.json
evaluation_report.md
evaluation_results.csv
```

These files contain the detailed evaluation results and benchmark information.

---

# 22. Project Documentation

Week 12 contains:

```text
Week12_Documentation_Demo_Day/
│
├── docs/
│   ├── architecture.md
│   ├── api_examples.md
│   └── demo_script.md
│
├── images/
│   └── architecture_diagram.png
│
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

---

# 23. Limitations

The current system has several limitations.

### External LLM Dependency

The generation stage depends on an external LLM service.

### Generation Latency

Generation is significantly slower than retrieval.

### Proxy Evaluation Metrics

The retrieval and generation metrics are automated proxies rather than human-labeled quality metrics.

### Timeout Failures

Five of the 30 benchmark requests reached the 60-second timeout.

### Limited Benchmark Size

Only 30 questions were used for the final benchmark.

### No Authentication

The API does not currently provide authentication.

### No Rate Limiting

Production-level rate limiting has not been implemented.

### Synchronous Processing

The current request flow is not optimized for high-concurrency production workloads.

---

# 24. Future Improvements

Potential improvements include:

* Faster LLM generation
* Better prompt engineering
* Improved answer grounding
* Human-based evaluation
* Gold retrieval datasets
* Response caching
* Authentication
* Rate limiting
* Asynchronous processing
* Larger evaluation datasets
* Automated regression thresholds
* Historical performance tracking

---

# 25. Demo Day

The recommended demonstration sequence is:

1. Start FastAPI.
2. Open Swagger UI.
3. Show `/`.
4. Show `/health`.
5. Show `/metadata`.
6. Demonstrate `/query`.
7. Test a business question.
8. Test a sports or technology question.
9. Explain retrieved chunks.
10. Explain entity-aware reranking.
11. Show evaluation results.
12. Discuss performance and limitations.
13. Explain future improvements.

The complete presentation script is available in:

```text
docs/demo_script.md
```

---

# 26. Conclusion

This project demonstrates a complete Retrieval-Augmented Generation workflow built around the AG News dataset.

The system combines vector embeddings, ChromaDB semantic retrieval, entity-aware reranking, NER metadata, LLM generation, FastAPI, automated testing, and system evaluation.

The final benchmark achieved a **96.0% Retrieval Accuracy Proxy**, while the evaluation also identified LLM generation quality and latency as important areas for future improvement.

The Week 12 documentation provides the architecture, API examples, setup information, benchmark results, limitations, and Demo Day presentation flow required to present and explain the completed system.
