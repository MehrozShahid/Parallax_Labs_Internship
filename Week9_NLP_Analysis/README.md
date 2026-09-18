# Week 9 — NLP Analysis: Named Entity Recognition

## Overview

This project implements Named Entity Recognition (NER) on the AG News corpus used in the previous RAG pipeline.

The goal was to extract meaningful entities from the document chunks, evaluate the quality of the extracted entities, store the entity information as metadata in ChromaDB, and use the metadata to improve retrieval through entity-based reranking.

## Objectives

* Implement Named Entity Recognition on the AG News corpus.
* Evaluate NER performance using manually labeled samples.
* Extract entities and entity types from the complete corpus.
* Store extracted entities alongside document chunks as ChromaDB metadata.
* Update the RAG retrieval logic to optionally boost chunks containing query entities.
* Evaluate the usefulness of entity-aware retrieval.

## Dataset

The project uses the AG News corpus from the previous RAG pipeline.

The existing ChromaDB collection contains:

* Collection: `ag_news`
* Total chunks: `120,526`
* Embedding model: `all-MiniLM-L6-v2`

The existing ChromaDB database from the previous project was reused rather than creating a new database.

## Technologies Used

* Python
* spaCy
* ChromaDB
* Sentence Transformers
* Pandas
* NumPy

## Project Structure

```text
Week9_NLP_Analysis/
│
├── data/
│   └── ner_manual_evaluation.csv
│
├── results/
│   ├── ner_evaluation_summary.txt
│   ├── ner_predictions.csv
│   └── ner_topic_documents.csv
│
├── src/
│   ├── evaluate_ner.py
│   ├── extract_corpus_entities.py
│   ├── update_chroma_ner_metadata.py
│   ├── entity_boost_retrieval.py
│   └── evaluate_entity_boost.py
│
└── README.md
```

## 1. Named Entity Recognition

NER was implemented using the spaCy English model `en_core_web_sm`.

The system extracts entities such as:

* `PERSON`
* `ORG`
* `GPE`
* `DATE`
* `LOC`
* and other entity types supported by the model.

For example, a document containing references to organizations, people, locations, and dates can have those entities extracted and stored with their corresponding entity types.

## 2. NER Evaluation

To evaluate the NER system, 50 documents were manually labeled and compared with the entities predicted by spaCy.

The evaluation produced the following results:

| Metric             | Result |
| ------------------ | -----: |
| Evaluation samples |     50 |
| True Positives     |    174 |
| False Positives    |    111 |
| False Negatives    |     91 |
| Precision          | 0.6105 |
| Recall             | 0.6566 |
| F1-score           | 0.6327 |

### Interpretation

The precision of `0.6105` indicates that a portion of the predicted entities did not match the manually labeled entities.

The recall of `0.6566` indicates that the system successfully identified a majority of the manually labeled entities, while some entities were missed.

The F1-score of `0.6327` provides a combined measure of precision and recall.

The results show that the pretrained spaCy NER model can extract useful entities from the AG News corpus, but the predictions are not perfect.

## 3. Full Corpus Entity Extraction

After evaluation, NER was applied to the complete corpus containing 120,526 document chunks.

The extracted information was stored in:

```text
results/ner_topic_documents.csv
```

The generated file contains the following fields:

```text
id
document
original_metadata
word_count
is_short
topic_id
topic_name
entities
entity_types
```

The `entities` field stores extracted entity text, while `entity_types` stores the corresponding entity categories.

Out of the 120,526 documents:

* 118,934 documents contained at least one detected entity.
* 1,592 documents did not contain a detected entity.

This means that approximately 98.7% of the corpus contained at least one entity detected by the NER model.

## 4. ChromaDB Metadata Integration

The extracted entities were added to the existing `ag_news` ChromaDB collection.

Two metadata fields were added:

```text
entities
entity_types
```

The existing embeddings were not regenerated.

The metadata update was applied to all 120,526 chunks.

This allows the retrieval system to access entity information alongside the original document content.

## 5. Entity-Aware Retrieval

The retrieval logic was updated in:

```text
src/entity_boost_retrieval.py
```

The updated retrieval process works as follows:

1. The user enters a query.
2. NER is applied to the query to identify entities.
3. ChromaDB retrieves an initial set of candidate chunks.
4. The retrieved chunks are checked for matching entities.
5. Chunks containing matching query entities receive an additional boost.
6. The candidates are reranked using the combined score.
7. The top results are returned.

The entity boost used in this experiment was:

```text
ENTITY_BOOST = 0.20
```

The system first retrieves 30 candidate chunks and then reranks them to return the top 5 results.

## 6. Entity Boost Evaluation

Entity-aware retrieval was tested using five queries:

```text
Iraq oil
Microsoft technology
US economy
China business
football players
```

The results showed:

* Ranking changed for 3 out of 5 queries.
* 20 out of 25 returned top-5 results contained a matching entity.
* The `football players` query did not receive an entity boost because no specific entity was detected in the query.

These results demonstrate that entity metadata can influence the ranking of retrieved chunks when relevant entities are present.

However, ranking changes do not by themselves prove that retrieval accuracy improved. A larger manually labeled retrieval evaluation would be required to measure retrieval accuracy directly.

## 7. Usefulness of the Extracted Metadata

The extracted entity metadata provides additional information that is not represented only by the document text.

It is useful for:

* identifying people, organizations, locations, and dates;
* filtering or analyzing documents based on entities;
* improving retrieval when a query contains a recognizable entity;
* adding structured information to the existing RAG pipeline.

The retrieval experiment showed that entity information can be used as an additional signal during reranking.

## 8. Limitations

The NER model is a pretrained general-purpose model and was not specifically trained on the AG News dataset.

Some entity predictions can therefore be noisy or incorrect. For example, certain news phrases may be incorrectly classified as entities or entity boundaries may not always be detected correctly.

The entity-boost mechanism is also a simple heuristic rather than a learned ranking model.

The retrieval experiment demonstrates usefulness and behavior of the metadata, but it does not provide a formal retrieval-accuracy improvement measurement because no manually labeled retrieval ground truth was used.

## 9. Conclusion

This project extends the previous RAG pipeline with Named Entity Recognition.

NER was evaluated on manually labeled samples, applied to the complete 120,526-document corpus, and integrated into ChromaDB metadata.

The retrieval system was then modified to use detected entities as an additional reranking signal.

The results demonstrate that structured entity metadata can be incorporated into a RAG pipeline and can influence retrieval when the query contains relevant entities.
