# Week 8 — NLP Topic Modeling

## Overview

In Week 8, the AG News dataset from the previous weeks was used for topic modeling to discover the main themes present across the corpus.

BERTopic was applied to the complete corpus to identify groups of documents with similar semantic content. The resulting topics were analyzed, visualized, and validated by reviewing documents from the generated topic clusters.

The discovered topic information was also integrated into the existing ChromaDB collection so that documents can be associated with their corresponding topic.

---

## Objectives

The main objectives of this week were:

* Apply topic modeling to the complete AG News corpus.
* Discover underlying themes and topic clusters.
* Visualize the generated topics.
* Validate topic assignments by manually reviewing documents.
* Handle edge cases such as very short documents and documents containing heavy or specialized terminology.

---

## Dataset

The project uses the **AG News dataset** that was prepared during the previous weeks.

### Dataset Information

* Dataset: AG News
* Total documents processed: **120,526**
* Main text field: `clean_text`
* Vector database: ChromaDB
* ChromaDB collection: `ag_news`

The topic modeling process was applied to the complete corpus rather than using only a small sample.

---

## Topic Modeling

### BERTopic

BERTopic was selected for topic modeling because it can identify semantic topics from text by combining embeddings, dimensionality reduction, clustering, and topic representation.

The trained BERTopic model was used to generate topic assignments for the documents in the corpus.

The resulting topic information was saved for further analysis and validation.

### Topic Information

Each document was associated with:

* `topic_id`
* `topic_name`

An example of the generated metadata is:

```text
topic_id: 0
topic_name: its | to | on | the | oil
```

The topic names represent the most representative words identified for each topic.

---

## Topic Visualization

Topic modeling results were visualized to understand the structure and distribution of the discovered topics.

The visualizations provide a way to inspect:

* Topic clusters
* Relationships between topics
* Topic distribution
* Representative terms associated with topics

These visualizations were used as part of the topic analysis and validation process.

---

## Topic Validation

The generated topics were validated by manually reviewing documents from the topic clusters.

Random documents were inspected to determine whether the assigned documents were semantically related to the topic they belonged to.

This helped verify that the discovered topics represented meaningful groups rather than arbitrary clusters.

The validation process included reviewing **20 random documents per topic cluster** as required by the Week 8 task.

---

## Edge Case Handling

The topic modeling process also considered documents that could cause difficulties for topic discovery.

### Extremely Short Documents

Very short documents contain limited semantic information and may not provide enough context for reliable topic assignment.

These cases were considered during topic validation to ensure that the topic modeling process could handle documents with limited textual information.

### Heavy Jargon

Some AG News documents contain specialized terminology, particularly in areas such as:

* Technology
* Business
* Finance
* Science

These documents were reviewed during validation to ensure that technical vocabulary did not prevent the topic model from producing meaningful topic groups.

---

## ChromaDB Metadata Integration

After generating the topic assignments, the topic information was integrated into the existing ChromaDB collection.

The following metadata fields were added to the documents:

```text
topic_id
topic_name
```

The integration was performed across the complete collection of:

```text
120,526 documents
```

The number of documents in the topic assignment data was also checked against the number of documents in ChromaDB to ensure that the datasets matched.

No embeddings were regenerated during the metadata integration process.

---

## Topic Filtering Verification

As an additional integration test, topic-based filtering was tested using ChromaDB metadata.

For example:

```python
where={
    "topic_id": 0
}
```

The test returned documents belonging to topic `0`.

The returned metadata was checked programmatically to ensure that every returned document had the expected topic ID.

The verification completed successfully:

```text
SUCCESS: All returned documents belong to topic_id = 0
```

This confirms that the generated topic metadata can also be used for topic-based filtering in ChromaDB.

> Note: Topic filtering was an additional verification step and was not a separate requirement in the Week 8 objectives.

---

## Project Structure

```text
Week8_NLP_Topic_Modeling/
│
├── data/
│
├── models/
│
├── results/
│
├── scripts/
│   ├── ...
│   └── test_topic_filtering.py
│
├── visualizations/
│
└── README.md
```

The exact files may vary depending on the scripts and outputs generated during the implementation.

---

## Technologies Used

* Python
* BERTopic
* Sentence Transformers
* Pandas
* NumPy
* ChromaDB
* NLP / Text Preprocessing
* Embeddings
* Clustering
* Data Visualization

---

## Results

The Week 8 implementation successfully:

* Applied BERTopic to the complete AG News corpus.
* Generated topic assignments for the corpus.
* Identified representative terms for the discovered topics.
* Generated topic visualizations.
* Validated topic assignments through manual document review.
* Considered short documents and documents containing specialized terminology.
* Integrated topic metadata into all **120,526 ChromaDB documents**.
* Verified that topic IDs and document IDs were correctly aligned.
* Successfully tested topic-based filtering using ChromaDB.

---

## Conclusion

Week 8 extended the previous RAG system by adding topic modeling capabilities to the AG News corpus.

BERTopic was used to discover underlying themes in the complete dataset, while manual validation and edge-case checking were used to assess the quality of the generated topics.

The topic information was then integrated into ChromaDB as metadata, providing an additional way to organize and filter the existing document collection.

The Week 8 topic modeling and validation tasks have been completed successfully.
