# Week 06 - RAG Generation with OpenRouter

## Overview

In Week 6, the Retrieval-Augmented Generation (RAG) system developed during Week 5 was extended by integrating the OpenRouter API for answer generation.

The system retrieves relevant chunks from the ChromaDB vector database and uses an available free language model through OpenRouter to generate answers based on the retrieved context.

This week focused on connecting retrieval with generation, implementing prompt engineering, adding robust API error handling, measuring response latency, logging system performance, and creating a simple command-line interface.

---

## Objectives

The main objectives of Week 6 were:

- Integrate the OpenRouter API with the existing RAG system.
- Generate answers using retrieved chunks from Week 5.
- Implement prompt engineering best practices.
- Create a system prompt for the language model.
- Inject retrieved context into the prompt.
- Provide clear instructions to the language model.
- Add robust API error handling.
- Handle rate-limit errors.
- Handle token and request-limit errors.
- Handle network timeouts.
- Handle connection errors.
- Handle malformed API responses.
- Measure retrieval latency.
- Measure generation latency.
- Measure total end-to-end latency.
- Log queries and latency information.
- Create a simple CLI interface for interacting with the RAG system.

---

## Technologies Used

- Python
- ChromaDB
- Sentence Transformers
- OpenRouter API
- OpenRouter Free Model Router
- Requests
- Python-dotenv
- Python Logging
- Command Line Interface (CLI)

---

## Project Structure

```text
Week6_RAG_Generation/
│
├── .env
├── .gitignore
├── config.py
├── prompt.py
├── llm_client.py
├── rag.py
├── cli.py
├── requirements.txt
├── README.md
│
└── logs/
    └── rag.log
````

---

## File Description

### `config.py`

This file contains the main configuration settings for the RAG system.

It includes:

* ChromaDB path
* Collection name
* Embedding model
* Number of retrieved chunks
* OpenRouter API key
* OpenRouter API URL
* LLM model
* API timeout
* Log file location

The retrieval configuration from Week 5 was reused.

The system retrieves the top 5 relevant chunks:

```python
TOP_K = 5
```

OpenRouter's free model router is used for generation:

```python
LLM_MODEL = "openrouter/free"
```

---

### `prompt.py`

This file handles prompt engineering.

It contains the system prompt and the logic for combining the retrieved chunks with the user's question.

The system prompt instructs the language model to:

* Use the provided context.
* Answer based on the retrieved information.
* Avoid making up information.
* Avoid using unsupported external information.
* Clearly indicate when the answer cannot be found in the context.
* Keep the answer relevant and understandable.

The retrieved chunks are inserted into the user prompt as context.

---

### `llm_client.py`

This file handles communication with the OpenRouter API.

It is responsible for:

* Sending requests to OpenRouter.
* Passing the system prompt.
* Passing the retrieved context and user question.
* Receiving the generated answer.
* Checking the API response.
* Handling API errors.
* Handling network problems.
* Handling timeout errors.
* Handling malformed responses.

The API request uses the OpenRouter chat completions endpoint.

---

### `rag.py`

This file connects the retrieval and generation components.

The RAG pipeline performs the following operations:

1. Receives the user's question.
2. Converts the question into an embedding.
3. Searches the existing ChromaDB collection.
4. Retrieves the top 5 relevant chunks.
5. Builds the prompt using the retrieved context.
6. Sends the prompt to OpenRouter.
7. Receives the generated answer.
8. Measures retrieval time.
9. Measures generation time.
10. Calculates total response latency.
11. Logs useful information.

The ChromaDB database created during Week 5 was reused instead of creating a new database.

---

### `cli.py`

This file provides the command-line interface.

The user can enter questions directly into the terminal.

Example:

```text
Question: What is happening in the technology industry?
```

The system then:

* Retrieves relevant chunks.
* Builds the prompt.
* Sends the request to OpenRouter.
* Generates an answer.
* Displays the answer.
* Displays latency information.

The CLI also supports:

```text
exit
```

and:

```text
quit
```

to close the program.

---

### `.env`

The `.env` file stores the OpenRouter API key separately from the Python source code.

Example:

```text
OPENROUTER_API_KEY=your_actual_api_key
```

The API key should never be uploaded to GitHub.

The `.env` file is therefore included in `.gitignore`.

---

### `.gitignore`

The `.gitignore` file prevents sensitive and unnecessary files from being uploaded to GitHub.

It should ignore:

```text
.env
.venv/
__pycache__/
*.pyc
logs/
chroma_db/
```

---

### `requirements.txt`

This file contains the Python packages required by the project.

Example:

```text
chromadb
sentence-transformers
python-dotenv
requests
```

---

### `logs/rag.log`

This file stores information about RAG queries and system performance.

It records information such as:

* User questions
* Number of retrieved chunks
* Retrieval time
* Generation time
* Total latency
* Errors

---

# RAG Pipeline

The complete Week 6 RAG pipeline works as follows:

```text
User Question
      |
      v
Create Question Embedding
      |
      v
ChromaDB Retrieval
      |
      v
Top 5 Relevant Chunks
      |
      v
Context Injection
      |
      v
Prompt Engineering
      |
      v
OpenRouter API
      |
      v
Available Free LLM
      |
      v
Generated Answer
      |
      v
Latency Measurement
      |
      v
CLI Output + Logging
```

---

# Prompt Engineering

Prompt engineering was implemented to improve the quality and reliability of generated answers.

## System Prompt

The system prompt defines the behavior of the language model.

It instructs the model to use the retrieved context when answering the user's question and avoid unsupported information.

The system prompt helps reduce hallucinations and keeps the generated answer related to the retrieved documents.

## Context Injection

The retrieved chunks from ChromaDB are inserted into the prompt.

The basic structure is:

```text
Retrieved Context:

[Context 1]

[Context 2]

[Context 3]

[Context 4]

[Context 5]


User Question:

[Question]


Answer the question using the provided context.
```

This allows the language model to generate an answer based on information retrieved from the knowledge base.

---

# Retrieval Configuration

The retrieval configuration from Week 5 was reused.

## Embedding Model

```text
all-MiniLM-L6-v2
```

## Vector Database

```text
ChromaDB
```

## Collection

```text
ag_news
```

## Top K

```text
5
```

The value `TOP_K = 5` was selected based on the retrieval evaluation performed during Week 5.

---

# OpenRouter Integration

OpenRouter was integrated as the generation API.

The API endpoint used is:

```text
https://openrouter.ai/api/v1/chat/completions
```

The project uses:

```python
LLM_MODEL = "openrouter/free"
```

The `openrouter/free` router automatically selects an available free model for the request.

The OpenRouter API key is loaded securely from the `.env` file.

---

# API Error Handling

Robust error handling was added so that the application does not crash when API or network problems occur.

## Missing API Key

If the API key is missing, the system displays an appropriate error message instead of attempting to make an unauthenticated request.

Example:

```text
ERROR: OpenRouter API key is missing.
```

## Invalid API Key

Authentication errors are handled when an invalid API key is provided.

Example:

```text
ERROR: OpenRouter returned status code 401
```

## Rate Limit

HTTP status code `429` is handled when the API rate limit is reached.

The application reports the error instead of crashing.

## Bad Request

HTTP status code `400` is handled for invalid API requests.

This can occur when the request format or input is invalid.

## Token or Request Limit

The system handles API errors related to request size or token limitations so that an oversized request does not cause the entire application to crash.

## Server Errors

Server-side errors such as HTTP `500` and other `5xx` errors are handled.

## Timeout

A request timeout is configured so that the application does not wait indefinitely for the API.

```python
REQUEST_TIMEOUT = 30
```

## Connection Error

Network connection problems are handled using request exception handling.

## Malformed Response

The system checks whether the API response contains the expected fields before extracting the generated answer.

For example, the response is checked for the expected `choices` field.

If the expected information is missing, an appropriate error message is returned.

---

# Latency Measurement

The project measures the response time of different stages of the RAG pipeline.

## Retrieval Time

Retrieval time measures the time required to:

* Create the question embedding.
* Search ChromaDB.
* Retrieve the relevant chunks.

## Generation Time

Generation time measures how long the OpenRouter API takes to generate the answer.

## Total Latency

Total latency measures the complete RAG response time.

It includes both retrieval and generation.

Example:

```text
Retrieval time : 0.0286 seconds
Generation time: 2.1483 seconds
Total latency  : 2.1779 seconds
```

The actual values vary depending on the question, computer performance, network connection, and API response time.

---

# Logging

Python's logging functionality is used to record important information about the RAG system.

The log file is:

```text
logs/rag.log
```

Example information recorded in the log:

```text
Question received: What is happening in the technology industry?
Retrieved 5 chunks
Retrieval time: 0.0286 seconds
Generation time: 2.1483 seconds
Total latency: 2.1779 seconds
```

Logging makes it easier to monitor system performance and troubleshoot errors.

---

# CLI Usage

## Start the Application

Activate the virtual environment created during the previous weeks and run:

```bash
python cli.py
```

The application displays:

```text
============================================================
             WEEK 6 RAG SYSTEM
============================================================

Ask a question about the knowledge base.
Type 'exit' or 'quit' to close the program.

Question:
```

Enter a question such as:

```text
What is happening in the technology industry?
```

The system retrieves relevant chunks and generates an answer.

---

# Example Output

```text
Searching documents...

------------------------------------------------------------
ANSWER
------------------------------------------------------------

[Generated answer based on retrieved context]

------------------------------------------------------------
Retrieval time : 0.0286 seconds
Generation time: 2.1483 seconds
Total latency  : 2.1779 seconds
------------------------------------------------------------
```

The latency values will be different for different queries and system conditions.

---

# Testing

The RAG system was tested for successful requests, invalid inputs, API errors, network problems, and performance measurement.

| Test                  | Expected Result         | Status      |
| --------------------- | ----------------------- | ----------- |
| Valid API request     | Generated answer        | Passed      |
| OpenRouter connection | Successful API response | Passed      |
| Missing API key       | API key error           | Passed      |
| Invalid API key       | Authentication error    | Passed      |
| Empty question        | Input warning           | Passed      |
| `exit` command        | Program closes          | Passed      |
| `quit` command        | Program closes          | Passed      |
| API timeout           | Timeout error           | Passed      |
| Connection error      | Connection error        | Passed      |
| Rate limit            | 429 handled             | Implemented |
| Bad request           | 400 handled             | Implemented |
| Server error          | 5xx handled             | Implemented |
| Token/request limit   | Error handled           | Implemented |
| Malformed response    | Response error handled  | Implemented |
| Retrieval latency     | Measured                | Passed      |
| Generation latency    | Measured                | Passed      |
| Total latency         | Measured                | Passed      |
| Logging               | Information saved       | Passed      |

---

# Installation

The virtual environment created during previous weeks was reused for Week 6.

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file in the Week 6 project directory.

Add the OpenRouter API key:

```text
OPENROUTER_API_KEY=your_actual_api_key
```

The API key should not be placed directly inside Python source files.

The `.env` file should not be committed to GitHub.

---

# Running the Project

## Step 1 - Activate the Virtual Environment

Use the virtual environment created during the previous weeks.

Example:

```bash
.venv\Scripts\activate
```

On Windows, the activated environment should show:

```text
(.venv)
```

in the terminal.

---

## Step 2 - Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## Step 3 - Check the Environment File

Make sure `.env` contains:

```text
OPENROUTER_API_KEY=your_actual_api_key
```

---

## Step 4 - Run the CLI

Run:

```bash
python cli.py
```

---

## Step 5 - Ask a Question

Example:

```text
Question: What is happening in the technology industry?
```

The system will retrieve relevant information and generate an answer.

---

## Step 6 - Exit the Application

Use:

```text
exit
```

or:

```text
quit
```

---

# Connection with Week 5

Week 6 builds directly on the retrieval system developed in Week 5.

## Week 5

```text
Documents
   |
   v
Text Chunking
   |
   v
Embeddings
   |
   v
ChromaDB
   |
   v
Retrieval Evaluation
   |
   v
Top K = 5
```

## Week 6

```text
User Question
   |
   v
Week 5 Retrieval System
   |
   v
Top 5 Relevant Chunks
   |
   v
Prompt Engineering
   |
   v
OpenRouter API
   |
   v
Free LLM
   |
   v
Generated Answer
```

The existing ChromaDB database from Week 5 was reused.

A new ingestion process was not required for Week 6.

---

# Week 6 Deliverables

The following tasks were completed:

* [x] Integrated OpenRouter API.
* [x] Connected LLM generation with Week 5 retrieval.
* [x] Reused the existing ChromaDB database.
* [x] Used the existing `all-MiniLM-L6-v2` embedding model.
* [x] Retrieved the top 5 relevant chunks.
* [x] Added a system prompt.
* [x] Added context injection.
* [x] Added clear instructions for the language model.
* [x] Added API error handling.
* [x] Added missing API key handling.
* [x] Added authentication error handling.
* [x] Added rate-limit handling.
* [x] Added timeout handling.
* [x] Added connection error handling.
* [x] Added malformed response handling.
* [x] Added token/request-limit error handling.
* [x] Added latency measurement.
* [x] Added retrieval latency measurement.
* [x] Added generation latency measurement.
* [x] Added total latency measurement.
* [x] Added logging.
* [x] Created a CLI interface.
* [x] Tested successful API generation.
* [x] Tested API error handling.
* [x] Tested CLI input handling.

---

# Conclusion

Week 6 successfully extended the Week 5 retrieval system into a complete Retrieval-Augmented Generation pipeline.

The system can now retrieve relevant information from ChromaDB, inject the retrieved information into a carefully designed prompt, send the prompt to a language model through OpenRouter, and display the generated answer through a command-line interface.

The system also includes API error handling, network error handling, timeout handling, malformed response handling, latency measurement, and logging.

The final RAG pipeline is:

```text
User Question
      |
      v
Question Embedding
      |
      v
ChromaDB Retrieval
      |
      v
Top 5 Relevant Chunks
      |
      v
Context Injection
      |
      v
Prompt Engineering
      |
      v
OpenRouter API
      |
      v
Available Free LLM
      |
      v
Generated Answer
      |
      v
Latency Measurement
      |
      v
CLI Output
      |
      v
Logging
```

Week 6 therefore completes the generation stage of the RAG system and provides a working end-to-end pipeline from user query to generated answer.

```
    
