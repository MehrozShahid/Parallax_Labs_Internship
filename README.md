# Parallax Labs Internship

## RAG-Based News Intelligence System

This repository contains the complete work completed during my **Parallax Labs Internship**, covering the development of a Retrieval-Augmented Generation (RAG) system using the **AG News dataset**.

The project progresses from data acquisition and preprocessing to vector search, retrieval evaluation, RAG generation, hallucination detection, NLP analysis, API development, and finally complete system evaluation and testing.

---

# Project Overview

The main project is a **RAG-based News Intelligence System** built using the AG News dataset.

The system processes news articles, converts them into vector embeddings, stores them in a vector database, retrieves relevant information for a user query, and generates an answer using a Large Language Model.

Throughout the internship, the system was gradually improved by adding:

* Data preprocessing
* Text chunking
* Embeddings
* Vector database storage
* Retrieval evaluation
* RAG generation
* Hallucination detection
* Topic modeling
* Named Entity Recognition
* Entity-aware retrieval
* FastAPI API development
* System evaluation
* Automated testing
* Performance analysis

---

# Repository Structure

```text
Parallax_Labs_Internship/
│
├── Week1_Environment_Data_Acquisition/
├── Week2_Data-Cleaning_Preprocessing/
├── Week3_Chunking_Embeddings/
├── Week4_Vector_Database/
├── Week5_Retrieval_Evaluation/
├── Week6_RAG_Generation/
├── Week7_Hallucination_Detection_Mitigation/
├── Week8_NLP_Topic_Modeling/
├── Week9_NLP_Analysis/
├── Week10_API_Development/
├── Week11_System_Testing/
│
└── README.md
```

Each week contains the implementation, documentation, and outputs related to that stage of the project.

---

# Week 1 — Environment & Data Acquisition

### Folder

```text
Week1_Environment_Data_Acquisition/
```

### Objective

The first week focused on setting up the development environment and acquiring the AG News dataset.

### Work Completed

* Set up the Python development environment
* Installed required libraries
* Downloaded and inspected the AG News dataset
* Explored the dataset structure
* Identified available fields and news categories
* Performed initial dataset inspection

### Main Outcome

A clean working environment and the initial AG News dataset were prepared for the following preprocessing stages.

---

# Week 2 — Data Cleaning & Preprocessing

### Folder

```text
Week2_Data-Cleaning_Preprocessing/
```

### Objective

Clean and prepare the AG News text before creating embeddings.

### Work Completed

* Removed unnecessary data
* Handled missing values
* Removed duplicate records
* Normalized text
* Cleaned textual content
* Prepared the dataset for chunking and embedding

### Main Outcome

The raw news dataset was transformed into a cleaner dataset suitable for downstream NLP processing.

---

# Week 3 — Chunking & Embeddings

### Folder

```text
Week3_Chunking_Embeddings/
```

### Objective

Convert news documents into manageable chunks and generate vector embeddings.

### Work Completed

* Implemented text chunking
* Used chunk overlap to preserve contextual information
* Generated sentence embeddings
* Used the `all-MiniLM-L6-v2` embedding model
* Prepared vector representations for database storage

### Main Outcome

The processed news documents were converted into vector embeddings that could be searched using semantic similarity.

---

# Week 4 — Vector Database

### Folder

```text
Week4_Vector_Database/
```

### Objective

Store the generated embeddings in a vector database for efficient semantic retrieval.

### Work Completed

* Set up ChromaDB
* Created the `ag_news` collection
* Stored document chunks and embeddings
* Added document metadata
* Implemented vector similarity search
* Tested retrieval from ChromaDB

The collection eventually contained approximately **120,526 documents/chunks**.

### Main Outcome

A functional vector database was created for semantic search over the AG News dataset.

---

# Week 5 — Retrieval Evaluation

### Folder

```text
Week5_Retrieval_Evaluation/
```

### Objective

Evaluate whether the vector database retrieves relevant documents for user queries.

### Work Completed

* Created test queries
* Retrieved top relevant documents
* Evaluated retrieval results
* Compared query intent with retrieved context
* Analyzed retrieval quality
* Experimented with retrieval parameters

### Main Outcome

The retrieval pipeline was evaluated and prepared for integration into the complete RAG system.

---

# Week 6 — RAG Generation

### Folder

```text
Week6_RAG_Generation/
```

### Objective

Combine document retrieval with Large Language Model generation.

### RAG Pipeline

```text
User Query
     ↓
Query Embedding
     ↓
ChromaDB Retrieval
     ↓
Relevant Context
     ↓
LLM
     ↓
Generated Answer
```

### Work Completed

* Connected retrieval with LLM generation
* Retrieved relevant AG News context
* Passed retrieved context to the LLM
* Generated answers based on retrieved information
* Tested different queries
* Evaluated the complete RAG workflow

### Main Outcome

A working Retrieval-Augmented Generation pipeline was created.

---

# Week 7 — Hallucination Detection & Mitigation

### Folder

```text
Week7_Hallucination_Detection_Mitigation/
```

### Objective

Identify and reduce unsupported information in generated answers.

### Work Completed

* Added answer support checking
* Compared generated answers with retrieved context
* Identified potentially unsupported responses
* Implemented hallucination-related evaluation
* Improved answer grounding

### Main Outcome

The RAG system became more focused on generating answers supported by retrieved information.

---

# Week 8 — NLP Topic Modeling

### Folder

```text
Week8_NLP_Topic_Modeling/
```

### Objective

Perform deeper NLP analysis on the news dataset using topic modeling.

### Work Completed

* Applied topic modeling
* Used BERTopic
* Identified major topics within the news dataset
* Analyzed topic distributions
* Examined outlier documents
* Generated topic information

### Results

The topic modeling stage produced:

* **71 topic entries**
* Approximately **38,315 outlier documents**

### Main Outcome

The news dataset was analyzed beyond simple retrieval by identifying underlying semantic topics.

---

# Week 9 — NLP Analysis & Named Entity Recognition

### Folder

```text
Week9_NLP_Analysis/
```

### Objective

Enhance the RAG system with NLP-based entity analysis.

### Work Completed

* Applied spaCy Named Entity Recognition
* Extracted entities from news documents
* Identified entity types
* Added entity information to document metadata
* Analyzed documents with and without detected entities
* Used entity information to improve retrieval

### NER Evaluation

The implemented NER system achieved approximately:

```text
Precision: 0.6105
Recall:    0.6566
F1 Score:  0.6327
```

The dataset contained approximately:

```text
Documents with entities:    118,934
Documents without entities:   1,592
```

### Entity-Aware Retrieval

Entity boosting was also evaluated.

The evaluation showed that entity boosting changed rankings for **3 out of 5 queries**, with **20 out of 25 top-5 retrieval results matching** the evaluated expected results.

The implemented entity boost value was:

```text
ENTITY_BOOST = 0.20
```

### Main Outcome

Entity information was integrated into the retrieval process to make retrieval more context-aware.

---

# Week 10 — API Development

### Folder

```text
Week10_API_Development/
```

### Objective

Convert the working RAG pipeline into a REST API using FastAPI.

### Technology

* FastAPI
* Uvicorn
* ChromaDB
* Sentence Transformers
* OpenRouter
* Pydantic
* Python

### API Endpoints

```text
GET  /
GET  /health
GET  /metadata
POST /query
```

### Main Configuration

```text
TOP_K = 5
CANDIDATE_K = 30
LLM_MODEL = openrouter/free
```

### Main Outcome

The RAG system was converted into a working API that can receive user questions and return generated answers.

The API was also tested successfully with the RAG pipeline and ChromaDB.

---

# Week 11 — System Evaluation & Testing

### Folder

```text
Week11_System_Testing/
```

### Objective

Evaluate and test the complete Week 10 FastAPI RAG system.

Week 11 focuses on measuring the system's **retrieval performance, answer quality, latency, API functionality, concurrent requests, and limitations**.

### Work Completed

* Created a 30-question evaluation benchmark
* Added Business, Sports, Technology, and World categories
* Evaluated retrieval performance
* Evaluated generated answer quality
* Measured retrieval latency
* Measured generation latency
* Measured end-to-end latency
* Calculated average latency
* Calculated median latency
* Calculated P95 latency
* Recorded minimum and maximum latency
* Generated Markdown evaluation reports
* Generated JSON evaluation reports
* Generated CSV results
* Added pytest API tests
* Added FastAPI TestClient testing
* Added test isolation through `conftest.py`
* Added concurrent request testing
* Added API logging
* Documented system limitations

---

## Week 11 Evaluation Benchmark

The evaluation contains **30 questions**.

| Category   | Questions |
| ---------- | --------: |
| Business   |         8 |
| Sports     |         7 |
| Technology |         8 |
| World      |         7 |
| **Total**  |    **30** |

---

## Week 11 Evaluation Metrics

### Retrieval Accuracy Proxy

The evaluation checks whether the retrieved context contains information related to the expected topic or keywords.

This is explicitly treated as a **retrieval accuracy proxy**, not true Precision@K or Recall@K, because manually labeled gold document IDs were not created for all benchmark questions.

### Generation Quality Proxy

Generated answers are evaluated using automated signals such as:

* Existing support information
* Expected keyword coverage

This provides an automated indication of answer quality but is not a replacement for human evaluation.

### Latency

The system measures:

* Retrieval latency
* Generation latency
* End-to-end latency
* Average latency
* Median latency
* P95 latency
* Minimum latency
* Maximum latency

---

# Week 11 Structure

```text
Week11_System_Testing/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── main.py
│   ├── rag.py
│   └── schemas.py
│
├── reports/
│   ├── evaluation_report.json
│   ├── evaluation_report.md
│   └── evaluation_results.csv
│
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_concurrent.py
│
├── evaluate.py
├── limitations.md
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

The real `.env` file is kept locally and is excluded from version control because it contains the API key.

---

# Running Week 11

Navigate to the Week 11 directory:

```bash
cd Week11_System_Testing
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Then run the evaluation from another terminal:

```bash
python evaluate.py
```

Run API tests:

```bash
pytest tests/test_api.py -v
```

Run concurrent tests:

```bash
pytest tests/test_concurrent.py -v
```

Run all tests:

```bash
pytest -v
```

---

# Week 11 Evaluation Reports

The evaluation generates:

```text
reports/
├── evaluation_report.md
├── evaluation_report.json
└── evaluation_results.csv
```

### Markdown Report

Human-readable evaluation summary.

### JSON Report

Machine-readable evaluation results.

### CSV Results

Query-level results suitable for spreadsheet analysis and further processing.

---

# Complete System Architecture

The final RAG system developed during the internship follows this architecture:

```text
                    AG News Dataset
                           │
                           ▼
                Data Cleaning & Processing
                           │
                           ▼
                     Text Chunking
                           │
                           ▼
                  Sentence Embeddings
                           │
                           ▼
                       ChromaDB
                           │
                           ▼
                    Vector Retrieval
                           │
                           ▼
                 Entity-Aware Retrieval
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
                       FastAPI
                           │
                           ▼
                 Evaluation & Testing
                           │
                ┌──────────┼──────────┐
                ▼          ▼          ▼
             Retrieval  Generation  Latency
             Evaluation Evaluation  Analysis
                │          │          │
                └──────────┼──────────┘
                           ▼
                    Reports & Results
```

---

# Technologies Used

The project uses the following technologies throughout the internship:

### Programming

* Python

### Data Processing

* Pandas
* NumPy

### NLP

* spaCy
* BERTopic
* Sentence Transformers

### Embeddings

* `all-MiniLM-L6-v2`

### Vector Database

* ChromaDB

### RAG / LLM

* OpenRouter
* LLM-based generation

### API

* FastAPI
* Uvicorn
* Pydantic

### Testing

* pytest
* FastAPI TestClient

### Evaluation

* Pandas
* CSV
* JSON
* Markdown reports

---

# Overall Internship Progression

The project evolved through the following stages:

```text
Week 1
Environment & Data Acquisition
        ↓
Week 2
Data Cleaning & Preprocessing
        ↓
Week 3
Chunking & Embeddings
        ↓
Week 4
Vector Database
        ↓
Week 5
Retrieval Evaluation
        ↓
Week 6
RAG Generation
        ↓
Week 7
Hallucination Detection & Mitigation
        ↓
Week 8
NLP Topic Modeling
        ↓
Week 9
NLP Analysis & NER
        ↓
Week 10
FastAPI API Development
        ↓
Week 11
System Evaluation & Testing
```

---

# Key Project Outcomes

By the end of Week 11, the internship project progressed from a raw news dataset to a tested RAG-based API system.

The final system includes:

* Processed AG News data
* Chunked documents
* Sentence embeddings
* ChromaDB vector storage
* Semantic retrieval
* Retrieval evaluation
* RAG-based generation
* Hallucination/support checking
* Topic modeling
* Named Entity Recognition
* Entity-aware retrieval
* FastAPI endpoints
* Automated API testing
* Concurrent request testing
* 30-question system evaluation
* Retrieval quality analysis
* Generation quality analysis
* Latency analysis
* JSON, Markdown, and CSV reports
* Documented system limitations

---

# Future Improvements

The system can be further improved by adding:

* Larger evaluation benchmarks
* Human-based answer evaluation
* More accurate retrieval metrics using labeled gold documents
* Automated regression testing
* Performance monitoring
* Authentication
* API rate limiting
* Asynchronous request processing
* Production deployment
* Cloud-based vector database
* Better hallucination evaluation
* Evaluation dashboards
* Historical performance tracking
* Automated CI/CD testing

---

# Conclusion

This internship project demonstrates the complete development lifecycle of a practical **Retrieval-Augmented Generation system**.

The project started with data acquisition and preprocessing and gradually progressed through embeddings, vector search, retrieval evaluation, LLM generation, hallucination mitigation, NLP analysis, API development, and system testing.

By Week 11, the RAG system had evolved into a **working, evaluated, and tested API-based application**, with automated evaluation reports and test suites providing a foundation for further development and production deployment.

---

## Internship

**Parallax Labs Internship**

**Project:** RAG-Based News Intelligence System

**Final Stage:** System Evaluation & Testing