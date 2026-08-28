# Parallax Labs Internship

This repository contains my weekly tasks completed during the Parallax Labs Internship. Each week's work is organized in a separate folder.

---

## Repository Structure

```text
Parallax_Labs_Internship/
│
├── Week1_Environment_Data_Acquisition/
├── Week2_Data-Cleaning_Preprocessing/
├── Week3_Chunking_Embeddings/
├── Week4_Vector_Database/
├── Week5_Retrieval_Evaluation/
├── Week6_RAG_Generation/   
└── README.md
```

---

## Week 01 - Environment Setup & Data Acquisition

### Completed Tasks

* Set up the Python development environment.
* Installed the required libraries.
* Downloaded and validated the AG News dataset.
* Performed basic data quality checks.
* Created a dataset validation report.

---

## Week 02 - Data Cleaning & Preprocessing

### Completed Tasks

* Removed HTML tags from the text.
* Removed special characters.
* Normalized whitespace.
* Combined the title and description into a single text field.
* Removed empty records after cleaning.
* Applied tokenization and lemmatization using spaCy.
* Saved the cleaned dataset.
* Added unit tests for the cleaning functions.

---

## Week 03 - Chunking & Embeddings

### Completed Tasks

* Implemented Recursive Character Text Splitting.
* Generated embeddings using the **all-MiniLM-L6-v2** Sentence Transformer model.
* Measured embedding generation time for each chunk.
* Calculated the total indexing time.
* Added unit tests for the chunking function.

---

## Week 04 - Vector Database (ChromaDB)

### Completed Tasks

* Set up and configured ChromaDB locally.
* Created a persistent ChromaDB collection.
* Ingested text chunks and their embeddings into ChromaDB.
* Implemented basic semantic search.
* Implemented Top-K retrieval for search queries.
* Tested retrieval performance using 10 different queries.
* Measured retrieval latency for each query.
* Saved retrieval performance results in `retrieval_log.csv`.
* Handled empty database cases.
* Handled empty and malformed queries.
* Handled invalid `top_k` values.

---

# Week 05 - Retrieval Evaluation

### Completed Tasks

- Created a manual test set containing 20 user queries.
- Identified expected ground-truth chunks for the test queries.
- Implemented retrieval evaluation using **Precision@K**.
- Implemented retrieval evaluation using **Recall@K**.
- Tested different K values: **1, 3, 5, and 10**.
- Experimented with different chunk sizes.
- Tested chunk sizes of **250, 500, 750, and 1000** characters.
- Created separate ChromaDB databases for chunk-size experiments.
- Compared retrieval performance across different configurations.
- Documented the evaluation results.
- Refined the retrieval logic based on the evaluation findings.
- Selected **TOP_K = 5** for the refined retrieval implementation.
- Implemented the final refined retrieval script using ChromaDB and Sentence Transformers.

---

## Week 06 - RAG Generation with OpenRouter

### Completed Tasks

- Integrated the OpenRouter API.
- Connected the OpenRouter LLM with the Week 5 retrieval system.
- Reused the existing ChromaDB database.
- Reused the all-MiniLM-L6-v2 embedding model.
- Retrieved the top 5 relevant chunks for each query.
- Implemented a system prompt.
- Implemented context injection.
- Added clear instructions for the language model.
- Implemented prompt engineering best practices.
- Added API error handling.
- Added missing API key handling.
- Added authentication error handling.
- Added rate-limit handling.
- Added request/token-limit error handling.
- Added timeout handling.
- Added connection error handling.
- Added malformed response handling.
- Added server error handling.
- Measured retrieval latency.
- Measured generation latency.
- Measured total end-to-end latency.
- Added logging for RAG queries and performance.
- Created a command-line interface.
- Tested successful API requests.
- Tested API error handling.
- Tested timeout and connection handling.
- Tested CLI input handling.

## Dependencies

The project uses the following Python libraries:

- pandas
- spaCy
- NLTK
- sentence-transformers
- langchain-text-splitters
- ChromaDB
- PyTorch
- requests
- python-dotenv

Install the required libraries using:

```bash
pip install pandas spacy nltk sentence-transformers chromadb langchain-text-splitters torch requests python-dotenv
---

## Running the Project

Each week's folder contains its own source code and README with instructions for running that week's task.

For example, to run Week 3:

```bash
cd Week3_Chunking_Embeddings
python main.py
```

---

## Dataset

This project uses the **AG News** dataset for text preprocessing, chunking, and embedding generation.

---

## Author

**Mehroz Shahid**
