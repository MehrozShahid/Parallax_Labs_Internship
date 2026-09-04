# RAG Question Answering System

## Overview

This project is a Retrieval-Augmented Generation (RAG) system built using Python.

The system retrieves relevant information from a ChromaDB knowledge base and uses an LLM through OpenRouter to generate an answer based only on the retrieved information.

The project was developed as part of the Parallax Labs internship.

---

## Week 7: Hallucination Detection & Mitigation

In Week 7, the RAG system was improved to reduce hallucinations.

The main improvements were:

* Added instructions to the LLM to use only the retrieved context.
* Added `"I don't know."` behavior when the answer is not available.
* Added protection against off-topic questions.
* Added structured JSON output.
* Added source information to generated answers.
* Added a hallucination checking step.
* Added logging for unsupported answers.
* Kept the existing ChromaDB retrieval system from previous weeks.

---

## How the System Works

The system follows this process:

```text
User Question
      ↓
Question Embedding
      ↓
ChromaDB Retrieval
      ↓
Top 5 Relevant Chunks
      ↓
Prompt Construction
      ↓
LLM Generation
      ↓
JSON Response
      ↓
Hallucination Check
      ↓
Final Answer
```

If the retrieved context does not support the answer, the system returns:

```text
I don't know.
```

---

## Project Structure

```text
Week6_RAG_Generation/
│
├── cli.py
├── config.py
├── llm_client.py
├── prompt.py
├── rag.py
├── logs/
│   └── rag.log
└── .env
```

### `cli.py`

Provides the command-line interface.

It allows the user to enter questions and displays:

* Answer
* Sources
* Hallucination status
* Retrieval time
* Generation time
* Total latency

### `config.py`

Contains the main configuration settings, including:

* ChromaDB path
* Collection name
* Embedding model
* Number of retrieved chunks
* OpenRouter API settings
* Log file location

### `rag.py`

Contains the main RAG pipeline.

It handles:

1. Retrieving relevant chunks.
2. Building the prompt.
3. Generating the answer.
4. Reading the JSON response.
5. Checking whether the answer is supported.
6. Returning the final result.

### `prompt.py`

Contains the prompts used by the LLM.

The prompt instructs the model to:

* Use only the provided context.
* Avoid outside knowledge.
* Avoid guessing.
* Avoid making up facts.
* Say `"I don't know."` when the answer is unavailable.
* Return the answer in JSON format.

### `llm_client.py`

Handles communication with the OpenRouter API.

It sends the system prompt and user prompt to the selected LLM and returns the generated response.

### `logs/rag.log`

Stores useful information such as:

* User questions
* Number of retrieved chunks
* Retrieval time
* Generation time
* Total latency
* Unsupported answers

---

## Technologies Used

* Python
* ChromaDB
* Sentence Transformers
* PyTorch
* LangChain Text Splitters
* OpenRouter API
* DeepSeek / OpenRouter models
* python-dotenv
* Requests

---

## Embedding Model

The project uses:

```text
all-MiniLM-L6-v2
```

The same embedding model used in the previous retrieval evaluation was kept for consistency.

---

## Retrieval

The system uses ChromaDB as the vector database.

The configuration retrieves the top 5 most relevant chunks:

```python
TOP_K = 5
```

The retrieved chunks are then passed to the LLM as context.

---

## Hallucination Mitigation

The system uses several strategies to reduce hallucinations.

### 1. Context-only instructions

The LLM is instructed to answer using only the retrieved context.

### 2. No guessing

The model is explicitly told not to guess or use outside knowledge.

### 3. "I don't know" response

If the context does not contain enough information, the model should return:

```text
I don't know.
```

### 4. Structured output

The LLM is instructed to return JSON such as:

```json
{
    "answer": "Example answer",
    "sources": ["Context 1"],
    "supported": true
}
```

### 5. Hallucination checking

After generating an answer, the system checks whether the answer is supported by the retrieved context.

If the answer is considered unsupported, the system replaces it with:

```text
I don't know.
```

---

## Off-Topic Questions

The system is also tested with questions that are unrelated to the knowledge base.

For example:

```text
What is the capital of France?
```

or:

```text
How do I cook biryani?
```

If the retrieved context does not contain information that can answer the question, the system should respond:

```text
I don't know.
```

This prevents the LLM from answering using its general knowledge.

---

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install pandas spacy nltk sentence-transformers langchain-text-splitters chromadb torch requests python-dotenv
```

---

## Environment Variables

Create a `.env` file in the project directory.

Add the OpenRouter API key:

```text
OPENROUTER_API_KEY=your_api_key_here
```

Do not upload or share the `.env` file publicly.

---

## Running the Project

Make sure the virtual environment is activated.

Then run:

```bash
python cli.py
```

The program will start the command-line interface.

Example:

```text
============================================================
             WEEK 7 RAG SYSTEM
============================================================

Ask a question about the knowledge base.
Type 'exit' or 'quit' to close the program.

Question:
```

Enter a question and the system will retrieve relevant information and generate an answer.

To close the program:

```text
exit
```

or:

```text
quit
```

---

## Example Output

A supported answer may look like:

```text
------------------------------------------------------------
ANSWER
------------------------------------------------------------
The article discusses the latest developments in the
technology sector.

------------------------------------------------------------
SOURCES
------------------------------------------------------------
- Context 1
- Context 3

------------------------------------------------------------
HALLUCINATION CHECK
------------------------------------------------------------
Answer is supported by the retrieved context.
```

For an unsupported or off-topic question:

```text
------------------------------------------------------------
ANSWER
------------------------------------------------------------
I don't know.

------------------------------------------------------------
SOURCES
------------------------------------------------------------
No sources.

------------------------------------------------------------
HALLUCINATION CHECK
------------------------------------------------------------
Answer is not supported by the retrieved context.
```

---

## Conclusion

The Week 7 version improves the previous RAG system by adding hallucination mitigation and structured responses.

The system now attempts to ensure that generated answers are grounded in the retrieved knowledge base instead of relying on information outside the provided context.
