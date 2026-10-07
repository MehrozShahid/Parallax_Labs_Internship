# API Examples

## 1. API Overview

The Week 10 RAG API provides a FastAPI-based interface for querying the AG News knowledge base.

The API supports health monitoring, metadata inspection, and question answering through a Retrieval-Augmented Generation (RAG) pipeline.

**Base URL:**

```text
http://127.0.0.1:8000
```

**Swagger UI:**

```text
http://127.0.0.1:8000/docs
```

---

## 2. Available Endpoints

| Method | Endpoint    | Purpose                             |
| ------ | ----------- | ----------------------------------- |
| GET    | `/`         | Check that the API is running       |
| GET    | `/health`   | Check system health                 |
| GET    | `/metadata` | View RAG system configuration       |
| POST   | `/query`    | Submit a question to the RAG system |

---

## 3. Root Endpoint

### GET `/`

### Request

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/' \
  -H 'accept: */*'
```

### Response

**HTTP 200 OK**

```json
{
  "message": "Working RAG API",
  "version": "1.0.0"
}
```

---

## 4. Health Endpoint

### GET `/health`

### Request

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/health' \
  -H 'accept: */*'
```

### Response

**HTTP 200 OK**

```json
{
  "status": "healthy",
  "details": true
}
```

---

## 5. Metadata Endpoint

### GET `/metadata`

### Request

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/metadata' \
  -H 'accept: */*'
```

### Response

**HTTP 200 OK**

```json
{
  "collection": "ag_news",
  "document_count": 120526,
  "embedding_model": "all-MiniLM-L6-v2",
  "retrieval_type": "Semantic retrieval with entity-aware reranking",
  "top_k": 5,
  "candidate_k": 30,
  "entity_boost": 0.2,
  "ner_model": "en_core_web_sm",
  "llm_model": "openrouter/free"
}
```

---

# 6. Query Endpoint

### POST `/query`

The `/query` endpoint is the main RAG endpoint.

### Request Format

```json
{
  "question": "Your question here"
}
```

The endpoint retrieves relevant context from ChromaDB and uses the retrieved context for answer generation.

---

# 7. Technology Query

### Request

```json
{
  "question": "What technology development is discussed?"
}
```

### Response

The actual Swagger response for this query returned:

```json
{
  "answer": "I don't know.",
  "sources": [],
  "supported": false,
  "retrieved_chunks": [
    {
      "id": "chunk_19120",
      "document": "Newbiz an Unconventional AssetThe Past Reuters Reuters When businesses consider theirassets they may look at obvious things like productsbuildings equipment patents even valued employees But thecompanys history",
      "metadata": {
        "entities": "Newbiz:PERSON",
        "entity_types": "PERSON"
      },
      "semantic_score": 0.565378565732205,
      "entity_score": 0,
      "final_score": 0.565378565732205,
      "matched_entities": []
    }
  ],
  "retrieval_time": 0.15297370008192956,
  "generation_time": 5.662402299931273,
  "total_time": 5.815485900035128,
  "latency_ms": 5816.01
}
```

> The actual response contained five retrieved chunks. Only the first chunk is shown here to keep the documentation concise.

This example demonstrates that the retrieval component can return context even when the generation component produces an `"I don't know."` response.

---

# 8. Sports Query

### Request

```json
{
  "question": "What happened to the team or player?"
}
```

### Response

The actual Swagger response returned:

```json
{
  "answer": "I don't know.",
  "sources": [],
  "supported": false,
  "retrieved_chunks": [
    {
      "id": "chunk_34568",
      "document": "Kennedy suffers knee injury It didn 39t look good when it happened on the field and it looked worse in the clubhouse Angels second baseman Adam Kennedy left the Angels 39 52 win over the Seattle Mariners",
      "metadata": {
        "entity_types": "CARDINAL; DATE; ORDINAL; ORG; PERSON",
        "entities": "Kennedy:PERSON; 39:CARDINAL; Angels:ORG; second:ORDINAL; Adam Kennedy:PERSON; Angels:ORG; 39 52:DATE; the Seattle Mariners:ORG"
      },
      "semantic_score": 0.4906947319654386,
      "entity_score": 0,
      "final_score": 0.4906947319654386,
      "matched_entities": []
    }
  ],
  "retrieval_time": 0.16056460002437234,
  "generation_time": 13.842622800031677,
  "total_time": 23.533712200121954,
  "latency_ms": 23534.04
}
```

> The actual response contained five retrieved chunks. Only the first retrieved chunk is shown here.

The retrieved context included information about Adam Kennedy, Serginho, Tim Duncan, Milton Bradley, and Andy Pettitte.

---

# 9. Business Query

### Request

```json
{
  "question": "What company activity is described?"
}
```

This question was also included in the Week 11 evaluation benchmark.

The recorded evaluation result was:

| Metric                   | Result |
| ------------------------ | -----: |
| HTTP Status              |    200 |
| Retrieval                |   PASS |
| Supported                |    Yes |
| Generation Quality Proxy | 83.33% |
| Retrieved Chunks         |      5 |

The query demonstrates successful retrieval and supported generation.

---

# 10. Example Questions

The API can be tested with questions from different AG News categories.

### Technology

```text
What technology development is discussed?
```

### Business

```text
What company activity is described?
```

### Sports

```text
What happened to the team or player?
```

### World

```text
What country or international issue appears in the context?
```

---

# 11. Response Fields

| Field              | Description                        |
| ------------------ | ---------------------------------- |
| `answer`           | Generated answer                   |
| `sources`          | Sources associated with the answer |
| `supported`        | Support status of the answer       |
| `retrieved_chunks` | Retrieved context chunks           |
| `id`               | Chunk identifier                   |
| `document`         | Retrieved document text            |
| `metadata`         | Entity and NER metadata            |
| `semantic_score`   | Semantic retrieval score           |
| `entity_score`     | Entity ranking score               |
| `final_score`      | Final ranking score                |
| `matched_entities` | Matched query/document entities    |
| `retrieval_time`   | Retrieval processing time          |
| `generation_time`  | Generation processing time         |
| `total_time`       | Total processing time              |
| `latency_ms`       | End-to-end latency                 |

---

# 12. Testing with Swagger UI

Start the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Then:

1. Select an endpoint.
2. Click **Try it out**.
3. Enter the request.
4. Click **Execute**.
5. Review the HTTP status and JSON response.

---

# 13. API Performance

The Week 11 evaluation tested 30 questions.

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
| Average Retrieval Time   |      52.7 ms |
| P95 Retrieval Time       |     71.63 ms |
| Average Generation Time  | 16,756.49 ms |
| P95 Generation Time      | 47,172.94 ms |

Retrieval is significantly faster than LLM generation. The benchmark also recorded five requests that reached the 60-second timeout.

---

# 14. Grounded Answer Behavior

The system can return:

```text
I don't know.
```

when the generated answer is not sufficiently supported.

This behavior is useful for reducing unsupported or hallucinated responses.

The evaluation results show that retrieval and generation should be considered separately when analyzing system performance.

---

## Conclusion

The API provides a simple interface for interacting with the AG News RAG system.

The documented endpoints demonstrate system status checking, health monitoring, configuration inspection, and RAG-based question answering.

Swagger UI provides the easiest method for manually testing the API during development and the final Demo Day presentation.
