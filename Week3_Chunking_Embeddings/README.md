# Week 03 - Chunking & Embeddings

## Overview

This week's task focuses on splitting the cleaned text from Week 2 into smaller chunks and generating embeddings for each chunk. The embeddings can be used for semantic search and other NLP applications.

## Objectives

* Implement text chunking.
* Generate embeddings using a Sentence Transformer model.
* Measure the embedding generation time for each chunk.
* Calculate the total indexing time.
* Write unit tests for the chunking function.

## Project Files

```text
Wee3_Chunking_Embeddings/
│
├── chunking.py
├── embedding.py
├── main.py
├── test_chunking.py
└── README.md
```

## Chunking Strategy

This project uses **Recursive Character Text Splitting**.

The text is split in the following order whenever possible:

* Paragraphs
* New lines
* Sentences
* Words
* Characters

### Configuration

* Chunk Size: 500 characters
* Chunk Overlap: 50 characters

The overlap helps preserve context between consecutive chunks.

## Embedding Model

**Model Used**

```text
all-MiniLM-L6-v2
```

### Why this model?

This model was selected because it:

* Generates good quality sentence embeddings.
* Is lightweight and fast.
* Works well for semantic similarity and retrieval tasks.

## Output

After running the project:

* The cleaned text is divided into smaller chunks.
* Embeddings are generated for each chunk.
* Embedding generation time is recorded.
* Total indexing time is displayed.

## How to Run

Run the main program:

```bash
python main.py
```

Run the unit tests:

```bash
python test_chunking.py
```

## Dependencies

This project uses the same virtual environment created in Week 2.

Required libraries:

* pandas
* spaCy
* sentence-transformers
* langchain-text-splitters
* torch

## Week 3 Summary

* Implemented Recursive Character Text Splitting.
* Generated embeddings using the `all-MiniLM-L6-v2` model.
* Logged embedding generation time for each chunk.
* Calculated the total indexing time.
* Added unit tests for the chunking function.
