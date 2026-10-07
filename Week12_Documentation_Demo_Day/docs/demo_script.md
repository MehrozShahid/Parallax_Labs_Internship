# Week 12 — Demo Day Presentation Script

## 1. Introduction

Hello everyone.

This project is a Retrieval-Augmented Generation system built using the AG News dataset.

The goal of the project was to build a complete RAG pipeline that can retrieve relevant news information and use that context to generate answers to user questions.

The project was developed progressively throughout the internship, covering data preparation, embeddings, vector databases, retrieval, generation, hallucination handling, NLP analysis, API development, and system evaluation.

---

# 2. Project Problem

Traditional question-answering systems can generate answers without checking whether the information exists in a trusted knowledge source.

This can lead to unsupported or hallucinated answers.

Our RAG approach addresses this by retrieving relevant information from the AG News knowledge base before generating an answer.

---

# 3. Project Architecture

The main pipeline is:

```text
AG News
   ↓
Preprocessing
   ↓
Chunking
   ↓
Embeddings
   ↓
ChromaDB
   ↓
User Query
   ↓
FastAPI
   ↓
Semantic Retrieval
   ↓
Entity-Aware Reranking
   ↓
Top-5 Context
   ↓
LLM
   ↓
Answer
```

The architecture diagram is available at:

```text
images/architecture_diagram.png
```

---

# 4. Technology Stack

The main technologies used are:

* Python
* FastAPI
* ChromaDB
* Sentence Transformers
* spaCy
* OpenRouter
* Pydantic
* Pytest
* Pandas
* NumPy

The embedding model is:

```text
all-MiniLM-L6-v2
```

The NER model is:

```text
en_core_web_sm
```

The LLM configuration is:

```text
openrouter/free
```

---

# 5. Dataset and Vector Database

The project uses the AG News dataset.

The final ChromaDB collection is:

```text
ag_news
```

The API metadata reports:

```text
120,526 documents/chunks
```

The retrieval configuration is:

```text
Candidate K = 30
Top K = 5
Entity Boost = 0.20
```

---

# 6. Start the API

Before starting the demonstration, activate the Python environment.

```bash
C:\Users\HP\Week2_Data_Cleaning_Preprocessing\.venv\Scripts\activate
```

Then go to the Week 11 application:

```bash
cd C:\Users\HP\Week11_System_Testing
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 7. Open Swagger

Open the following URL:

```text
http://127.0.0.1:8000/docs
```

Swagger provides an interactive interface for testing the API.

---

# 8. Demonstrate Root Endpoint

Open:

```text
GET /
```

Click **Try it out** and then **Execute**.

The API returns:

```json
{
  "message": "Working RAG API",
  "version": "1.0.0"
}
```

This confirms that the API is running.

---

# 9. Demonstrate Health Endpoint

Open:

```text
GET /health
```

Execute the request.

The API returns:

```json
{
  "status": "healthy",
  "details": true
}
```

This confirms that the system health check is successful.

---

# 10. Demonstrate Metadata Endpoint

Open:

```text
GET /metadata
```

Execute the request.

The API returns information such as:

```text
Collection: ag_news
Documents: 120526
Embedding Model: all-MiniLM-L6-v2
Top K: 5
Candidate K: 30
Entity Boost: 0.2
NER Model: en_core_web_sm
LLM Model: openrouter/free
```

This demonstrates the configuration of the RAG system.

---

# 11. Demonstrate Query Endpoint

Now open:

```text
POST /query
```

Use the following question:

```json
{
  "question": "What company activity is described?"
}
```

Click **Execute**.

Explain that the system:

1. Converts the question into an embedding.
2. Searches ChromaDB.
3. Retrieves candidate documents.
4. Applies entity-aware reranking.
5. Selects the top five chunks.
6. Sends the retrieved context to the LLM.
7. Returns the final API response.

---

# 12. Demonstrate Sports Query

Use:

```json
{
  "question": "What happened to the team or player?"
}
```

The retrieved context includes multiple sports stories.

Explain that the retrieved chunks contain information about:

* Adam Kennedy
* Serginho
* Tim Duncan
* Milton Bradley
* Andy Pettitte

The API may return:

```text
I don't know.
```

This demonstrates that retrieval and generation are separate components.

---

# 13. Explain the `"I don't know."` Behavior

If the system cannot generate a sufficiently supported answer, it returns:

```text
I don't know.
```

This is preferable to generating an unsupported answer.

The evaluation showed that some questions retrieved relevant documents but still resulted in an unsupported generated answer.

This is one of the areas identified for future improvement.

---

# 14. Week 11 Evaluation

The system was evaluated using:

```text
30 questions
```

The questions covered:

* Business
* Sports
* Technology
* World

The final results were:

| Metric                   |        Result |
| ------------------------ | ------------: |
| Successful Requests      |       25 / 30 |
| Failed Requests          |        5 / 30 |
| Retrieval Accuracy Proxy |         96.0% |
| Generation Quality Proxy |        41.33% |
| Supported Answer Rate    |         56.0% |
| Average Latency          | 23.56 seconds |
| Median Latency           | 17.47 seconds |
| P95 Latency              | 55.32 seconds |

---

# 15. Performance Discussion

One important finding from the evaluation is that retrieval is relatively fast.

Average retrieval time:

```text
52.7 ms
```

Average generation time:

```text
16,756.49 ms
```

Therefore, generation is the main contributor to the system's overall latency.

The P95 generation time was:

```text
47,172.94 ms
```

Five requests reached the 60-second timeout.

This gives a clear direction for future optimization.

---

# 16. Testing

The project also includes automated testing from Week 11.

The tests cover:

* API endpoints
* API behavior
* Concurrent requests

Pytest was used for automated testing.

The evaluation script was also used to measure the system over 30 questions.

---

# 17. Project Documentation

The Week 12 documentation contains:

```text
README.md
docs/architecture.md
docs/api_examples.md
docs/demo_script.md
```

The documentation explains:

* Project purpose
* Architecture
* API endpoints
* Setup
* Example queries
* Evaluation
* Performance
* Limitations
* Future improvements

---

# 18. Limitations

The current system has several limitations.

### LLM Dependency

The generation component depends on an external LLM service.

### Generation Latency

LLM generation is considerably slower than vector retrieval.

### Evaluation Proxies

The retrieval and generation metrics are proxies rather than manually labeled benchmark metrics.

### Timeout Failures

Five out of thirty evaluation requests reached the configured 60-second timeout.

### Small Evaluation Set

The benchmark contains only 30 questions.

### No Authentication

The current API does not implement user authentication.

### No Rate Limiting

The API does not currently include production-level rate limiting.

---

# 19. Future Improvements

Possible future improvements include:

* Use a faster or more reliable LLM.
* Reduce generation latency.
* Improve prompt design.
* Improve answer grounding.
* Add human evaluation.
* Create manually labeled retrieval benchmarks.
* Add authentication.
* Add rate limiting.
* Add caching.
* Add asynchronous processing.
* Add continuous regression testing.
* Track performance across multiple evaluation runs.

---

# 20. Closing

To conclude, the project demonstrates a complete RAG workflow from data processing to API deployment and evaluation.

The system combines semantic retrieval, entity-aware reranking, vector search, and LLM generation.

The Week 11 evaluation showed strong retrieval performance with a 96% retrieval accuracy proxy, while also identifying generation quality and latency as important areas for improvement.

Thank you.

---

# 21. Demo Checklist

Before Demo Day:

* [ ] Start the Week 11 FastAPI server.
* [ ] Confirm `/` works.
* [ ] Confirm `/health` returns healthy.
* [ ] Confirm `/metadata` works.
* [ ] Open Swagger UI.
* [ ] Test a business query.
* [ ] Test a sports query.
* [ ] Test a technology query.
* [ ] Keep the architecture diagram available.
* [ ] Keep the evaluation results available.
* [ ] Keep the Week 12 README available.
