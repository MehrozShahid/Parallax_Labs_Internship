# Parallax Labs Internship

This repository contains my weekly tasks completed during the Parallax Labs Internship. Each week's work is organized in a separate folder and builds on the previous week's implementation.

---

## Repository Structure

```text
Parallax_Labs_Internship/
│
├── Week1_Environment_Setup_Data_Acquisition/
├── Week2_Data-Cleaning_Preprocessing/
├── Week3_Chunking_Embeddings/
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

## Dependencies

The project uses the following Python libraries:

* pandas
* spaCy
* NLTK
* sentence-transformers
* langchain-text-splitters
* ChromaDB
* torch

Install the dependencies using:

```bash
pip install pandas spacy nltk sentence-transformers chromadb langchain-text-splitters torch
```

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
