# Parallax Labs Internship

This repository contains my weekly tasks and projects completed during the **Parallax Labs Internship**. Each week's work is organized in a separate folder with its own implementation, documentation, and results.

---

## Repository Structure

```text
Parallax_Labs_Internship/
│
├── Week1_Environment_Data_Acquisition/
│
├── Week2_Data-Cleaning_Preprocessing/
│
├── Week3_Chunking_Embeddings/
│
├── Week4_Vector_Database/
│
├── Week5_Retrieval_Evaluation/
│
├── Week6_RAG_Generation/
│
├── Week7_Hallucination_Detection_Mitigation/
│
├── Week8_NLP_Topic_Modeling/
│
├── Week9_NLP_Analysis/
│
└── README.md
```

---

# Week 01 - Environment Setup & Data Acquisition

### Completed Tasks

* Set up the Python development environment.
* Installed the required libraries.
* Downloaded and validated the AG News dataset.
* Performed basic data quality checks.
* Created a dataset validation report.

---

# Week 02 - Data Cleaning & Preprocessing

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

# Week 03 - Chunking & Embeddings

### Completed Tasks

* Implemented Recursive Character Text Splitting.
* Generated embeddings using the **all-MiniLM-L6-v2** Sentence Transformer model.
* Measured embedding generation time for each chunk.
* Calculated the total indexing time.
* Added unit tests for the chunking function.

---

# Week 04 - Vector Database (ChromaDB)

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

* Created a manual test set containing 20 user queries.
* Identified expected ground-truth chunks for the test queries.
* Implemented retrieval evaluation using **Precision@K**.
* Implemented retrieval evaluation using **Recall@K**.
* Tested different K values: **1, 3, 5, and 10**.
* Experimented with different chunk sizes.
* Tested chunk sizes of **250, 500, 750, and 1000** characters.
* Created separate ChromaDB databases for chunk-size experiments.
* Compared retrieval performance across different configurations.
* Documented the evaluation results.
* Refined the retrieval logic based on the evaluation findings.
* Selected **TOP_K = 5** for the refined retrieval implementation.
* Implemented the final refined retrieval script using ChromaDB and Sentence Transformers.

---

# Week 06 - RAG Generation with OpenRouter

### Completed Tasks

* Integrated the OpenRouter API.
* Connected the OpenRouter LLM with the Week 5 retrieval system.
* Reused the existing ChromaDB database.
* Reused the `all-MiniLM-L6-v2` embedding model.
* Retrieved the top 5 relevant chunks for each query.
* Implemented a system prompt.
* Implemented context injection.
* Added clear instructions for the language model.
* Implemented prompt engineering best practices.
* Added API error handling.
* Added missing API key handling.
* Added authentication error handling.
* Added rate-limit handling.
* Added request/token-limit error handling.
* Added timeout handling.
* Added connection error handling.
* Added malformed response handling.
* Added server error handling.
* Measured retrieval latency.
* Measured generation latency.
* Measured total end-to-end latency.
* Added logging for RAG queries and performance.
* Created a command-line interface.
* Tested successful API requests.
* Tested API error handling.
* Tested timeout and connection handling.
* Tested CLI input handling.

---

# Week 07 - Hallucination Detection & Mitigation

### Completed Tasks

* Created a separate Week 7 project based on the Week 6 RAG system.
* Continued using the existing ChromaDB retrieval approach.
* Added instructions to the LLM to use only the retrieved context.
* Added `"I don't know."` behavior when the answer is not available in the context.
* Added protection against unsupported answers.
* Added handling for off-topic questions.
* Implemented structured JSON output from the LLM.
* Added answer and source information to the structured response.
* Added a `supported` field to identify whether an answer is supported by the context.
* Implemented a hallucination checking step.
* Compared generated answers against the retrieved context.
* Rejected answers that were not supported by the retrieved information.
* Returned `"I don't know."` when an answer could not be supported.
* Added logging for unsupported generated answers.
* Updated the command-line interface to display sources and hallucination-check status.
* Tested the system with questions outside the knowledge base.
* Kept the Week 6 project unchanged while developing the Week 7 improvements.

---

# Week 08 - NLP Topic Modeling

### Completed Tasks

* Applied **BERTopic** to the complete AG News corpus.
* Generated topic assignments for the entire corpus.
* Discovered underlying themes and topic clusters.
* Generated topic information and representative topic terms.
* Created visualizations for the discovered topic clusters.
* Validated topic assignments through manual document review.
* Reviewed **20 random documents per topic cluster** as part of topic validation.
* Considered extremely short documents as an edge case.
* Considered documents containing heavy or specialized jargon as an edge case.
* Integrated topic information into the existing ChromaDB collection.
* Added `topic_id` metadata to the documents.
* Added `topic_name` metadata to the documents.
* Verified that the topic assignment data matched the **120,526 documents** in ChromaDB.
* Verified that ChromaDB document IDs followed the expected structure.
* Tested topic-based filtering using ChromaDB metadata.
* Confirmed that filtered documents belonged to the requested topic.

### Topic Metadata Example

```text
topic_id: 0
topic_name: its | to | on | the | oil
```

### Topic Filtering Verification

An additional verification test was performed using:

```python
where={
    "topic_id": 0
}
```

The test successfully returned documents belonging to topic `0`, and all returned documents were verified to contain the expected `topic_id`.

```text
SUCCESS: All returned documents belong to topic_id = 0
```

---

# Week 09 - NLP Analysis: Named Entity Recognition

### Completed Tasks

* Implemented **Named Entity Recognition (NER)** using spaCy.
* Created a manually labeled evaluation set containing **50 samples**.
* Evaluated NER predictions using **Precision, Recall, and F1-score**.
* Calculated NER evaluation metrics using True Positives, False Positives, and False Negatives.
* Applied NER to the complete corpus containing **120,526 documents**.
* Extracted entities and their corresponding entity types.
* Stored extracted entity information alongside document chunks.
* Added `entities` metadata to the existing ChromaDB collection.
* Added `entity_types` metadata to the existing ChromaDB collection.
* Reused the existing `ag_news` ChromaDB collection instead of creating a new database.
* Updated the retrieval logic to optionally boost chunks containing query entities.
* Implemented entity-based reranking of retrieved chunks.
* Tested entity-aware retrieval using multiple queries.
* Evaluated the effect of entity boosting on retrieval rankings.
* Documented the accuracy and usefulness of the extracted entity metadata.

### NER Evaluation Results

The NER system was evaluated using 50 manually labeled samples.

| Metric          | Result |
| --------------- | -----: |
| Samples         |     50 |
| True Positives  |    174 |
| False Positives |    111 |
| False Negatives |     91 |
| Precision       | 0.6105 |
| Recall          | 0.6566 |
| F1-score        | 0.6327 |

### Entity Extraction Results

NER was applied to all **120,526 documents** in the corpus.

```text
Documents containing detected entities: 118,934
Documents without detected entities:      1,592
```

The extracted metadata includes:

```text
entities
entity_types
```

### Entity-Aware Retrieval

The retrieval system was extended to use detected query entities as an additional reranking signal.

The system:

```text
User Query
    ↓
Query Entity Extraction
    ↓
ChromaDB Candidate Retrieval
    ↓
Entity Matching
    ↓
Entity Boost
    ↓
Reranking
    ↓
Top Results
```

Five test queries were used to evaluate the entity-aware retrieval:

```text
Iraq oil
Microsoft technology
US economy
China business
football players
```

The experiment showed that rankings changed for **3 out of 5 queries**. Across the evaluated top-5 results, **20 out of 25** contained a matching entity.

These results demonstrate that entity metadata can influence retrieval when relevant entities are detected. The experiment measures retrieval behavior and usefulness; it does not by itself establish an improvement in retrieval accuracy because no manually labeled retrieval ground truth was used for this experiment.

### Limitations

The NER model is a pretrained general-purpose spaCy model and was not specifically trained on the AG News dataset. As a result, some entity predictions can be noisy or incorrectly classified.

The entity-boost mechanism is a heuristic reranking approach rather than a learned ranking model.

The complete Week 9 implementation and evaluation details are available in:

```text
Week9_NLP_Analysis/README.md
```

---

# Dependencies

The project uses different Python libraries across the weekly tasks.

Some of the main dependencies include:

* pandas
* NumPy
* spaCy
* NLTK
* sentence-transformers
* langchain-text-splitters
* ChromaDB
* PyTorch
* requests
* python-dotenv
* BERTopic
* UMAP
* HDBSCAN

Individual weeks may contain additional dependencies in their respective `requirements.txt` files.

Install the required libraries for a specific week using the instructions provided in that week's README.

---

# Running the Projects

Each week's folder contains its own source code and README with instructions for running that week's task.

For example, to run Week 3:

```bash
cd Week3_Chunking_Embeddings
python main.py
```

To run Week 6:

```bash
cd Week6_RAG_Generation
python cli.py
```

To run Week 7:

```bash
cd Week7_Hallucination_Detection_Mitigation
python cli.py
```

For Week 8, refer to the README inside:

```text
Week8_NLP_Topic_Modeling/
```

For Week 9, refer to the README inside:

```text
Week9_NLP_Analysis/
```

for the NER implementation, evaluation, metadata integration, and entity-aware retrieval workflow.

---

# Dataset

This project uses the **AG News** dataset for:

* Text preprocessing
* Chunking
* Embedding generation
* Vector database storage
* Retrieval evaluation
* Retrieval-Augmented Generation
* Topic modeling
* Named Entity Recognition
* Entity-aware retrieval

The corpus used during the NLP analysis stages contained **120,526 documents**.

---

# RAG Pipeline

The RAG system developed during Weeks 6 and 7 follows these main steps:

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
Structured JSON Response
      ↓
Hallucination Check
      ↓
Final Answer
```

If the answer cannot be supported by the retrieved context, the Week 7 system returns:

```text
I don't know.
```

---

# Topic Modeling Pipeline

The Week 8 topic modeling workflow extends the project with NLP topic discovery:

```text
AG News Corpus
      ↓
Cleaned Documents
      ↓
BERTopic
      ↓
Topic Assignment
      ↓
Topic Validation
      ↓
Topic Visualization
      ↓
Topic Metadata
      ↓
ChromaDB Integration
      ↓
Topic-Based Filtering
```

---

# Named Entity Recognition Pipeline

The Week 9 workflow extends the NLP pipeline with named entity extraction and entity-aware retrieval:

```text
AG News Corpus
      ↓
NER with spaCy
      ↓
Entity Extraction
      ↓
NER Evaluation
      ↓
Entity Metadata
      ↓
ChromaDB Integration
      ↓
Query Entity Extraction
      ↓
Entity-Based Reranking
      ↓
Retrieved Results
```

---

# Author

**Mehroz Shahid**

