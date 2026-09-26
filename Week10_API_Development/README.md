# Week 10 — RAG API Development

A FastAPI-based REST API that exposes the entity-aware Retrieval-Augmented Generation (RAG) system developed in Week 9.

The API provides endpoints for checking system health, viewing RAG metadata, and sending user queries to the RAG pipeline.

## Project Overview

In the previous week, an entity-aware RAG system was developed for the AG News dataset.

This week, the RAG system is wrapped inside a FastAPI application so it can be accessed through HTTP endpoints.

The API handles:

1. User query input
2. Query processing
3. Entity-aware retrieval
4. Relevant document retrieval from ChromaDB
5. Response generation through the configured LLM
6. Returning the generated answer and retrieval information as JSON

The API also provides system health and metadata endpoints for easier monitoring and testing.

---

## Features

* FastAPI REST API
* POST endpoint for RAG queries
* ChromaDB integration
* Sentence-transformer embedding model
* spaCy NER model
* Entity-aware retrieval
* LLM-based response generation
* Retrieved source information
* Retrieval and generation timing
* Health check endpoint
* RAG system metadata endpoint
* Interactive Swagger API documentation
* Pydantic request and response validation

---

## API Endpoints

### 1. Root

**GET `/`**

Returns basic information about the API.

---

### 2. Health Check

**GET `/health`**

Checks whether the API and its main RAG components are ready.

Example response:

```json
{
  "status": "healthy",
  "service": "Week 10 RAG API",
  "rag_system": "ready",
  "chromadb": "connected"
}
```

---

### 3. Metadata

**GET `/metadata`**

Returns information about the RAG configuration.

The response includes information such as:

* ChromaDB collection
* Number of documents/chunks
* Embedding model
* Retrieval type
* Top-K value
* Candidate-K value
* Entity boost
* NER model
* LLM model

---

### 4. RAG Query

**POST `/query`**

Sends a user question to the RAG system.

Example request:

```json
{
  "query": "What are the latest developments in technology?"
}
```

The API processes the query and returns information including:

```json
{
  "answer": "Generated answer...",
  "sources": [],
  "supported": true,
  "retrieved_chunks": [],
  "retrieval_time": 0,
  "generation_time": 0,
  "total_time": 0,
  "latency_ms": 0
}
```

The exact response depends on the retrieved documents and generated response.

---

## Technology Stack

* **Python**
* **FastAPI**
* **Uvicorn**
* **Pydantic**
* **ChromaDB**
* **Sentence Transformers**
* **spaCy**
* **OpenRouter / LLM API**
* **AG News Dataset**

---

## RAG Architecture

```text
User
  │
  ▼
FastAPI
  │
  ▼
POST /query
  │
  ▼
Query Processing
  │
  ├──────────────► spaCy NER
  │                    │
  │                    ▼
  │              Entity Extraction
  │
  ▼
Entity-Aware Retrieval
  │
  ├──────────────► ChromaDB
  │
  ▼
Retrieved Chunks
  │
  ▼
Reranking / Final Retrieval
  │
  ▼
LLM Generation
  │
  ▼
FastAPI Response
  │
  ▼
JSON Response
```

---

## Project Structure

```text
Week10_API_Development/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── ...
│
├── requirements.txt
├── README.md
└── .gitignore
```

The exact files may vary depending on the implementation of the Week 9 RAG system.

---

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Week10_API_Development
```

### 2. Create a virtual environment

```bash
py -3.10 -m venv .venv
```

### 3. Activate the environment

On Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

If the project uses an external LLM provider such as OpenRouter, create a `.env` file in the project root.

Example:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Do not commit API keys or other secrets to GitHub.

The `.env` file should be included in `.gitignore`.

---

## Running the API

From the project root:

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

---

## Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

From Swagger UI, you can test:

* `GET /`
* `GET /health`
* `GET /metadata`
* `POST /query`

For the RAG query endpoint, use:

```json
{
  "query": "What are the latest developments in technology?"
}
```

---

## ChromaDB

The API connects to the ChromaDB collection created during the previous RAG development work.

Current collection:

```text
ag_news
```

The collection contains approximately:

```text
120,526 chunks
```

These chunks are used as the retrieval source for answering user questions.

---

## Retrieval Pipeline

The query follows an entity-aware retrieval process.

### Step 1 — Query Input

The user sends a question through the API.

### Step 2 — Entity Extraction

spaCy is used to identify relevant named entities from the query.

### Step 3 — Semantic Retrieval

The embedding model converts the query into an embedding and retrieves semantically relevant chunks from ChromaDB.

### Step 4 — Entity-Aware Scoring

Retrieved candidates can receive additional scoring based on entity matches.

### Step 5 — Final Context

The highest-scoring chunks are selected as context for generation.

### Step 6 — LLM Generation

The selected context and user query are passed to the configured language model.

### Step 7 — API Response

The API returns the generated answer along with retrieval information and timing metrics.

---

## Response Information

The `/query` response contains several useful fields.

| Field              | Description                                                       |
| ------------------ | ----------------------------------------------------------------- |
| `answer`           | Generated answer from the RAG system                              |
| `sources`          | Sources associated with the answer                                |
| `supported`        | Indicates whether the query is supported by the retrieved context |
| `retrieved_chunks` | Retrieved documents/chunks                                        |
| `semantic_score`   | Semantic similarity score                                         |
| `entity_score`     | Entity matching score                                             |
| `final_score`      | Final retrieval score                                             |
| `matched_entities` | Entities matched during retrieval                                 |
| `retrieval_time`   | Time spent retrieving documents                                   |
| `generation_time`  | Time spent generating the answer                                  |
| `total_time`       | Total processing time                                             |
| `latency_ms`       | Overall API latency in milliseconds                               |

---

## Testing

The API can be tested using Swagger UI, curl, Postman, or another HTTP client.

### Example curl request

```bash
curl -X POST "http://127.0.0.1:8000/query" ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"What are the latest developments in technology?\"}"
```

### Example health check

```bash
curl "http://127.0.0.1:8000/health"
```

---

## Error Handling

The API uses FastAPI and Pydantic validation to validate incoming requests.

For example, an invalid request can result in:

```text
422 Unprocessable Entity
```

while unexpected errors inside the RAG pipeline may result in:

```text
500 Internal Server Error
```

---

## Learning Outcomes

This week focused on moving from a standalone RAG pipeline toward an API-based application.

Key concepts practiced:

* REST API development
* FastAPI
* HTTP methods
* POST requests
* Request and response schemas
* Pydantic validation
* API documentation with Swagger
* Connecting an existing ML/RAG system to an API
* API health monitoring
* Returning structured JSON responses
* Measuring retrieval and generation latency

---

## Previous Work

This project builds on the RAG system developed during the previous weeks.

### Week 9

Entity-aware RAG and NLP analysis were used to improve retrieval by combining semantic relevance with entity information.

### Week 10

The RAG system was exposed through a FastAPI service, making it possible for external applications to communicate with the system through HTTP requests.

---

## Future Improvements

Possible improvements include:

* Add authentication
* Add request logging
* Add rate limiting
* Add better exception handling
* Add API versioning
* Add automated tests
* Add Docker support
* Add a frontend client
* Add streaming LLM responses
* Add monitoring and performance tracking
* Deploy the API to a cloud platform

---

## Author

**Mehroz Shahid**
