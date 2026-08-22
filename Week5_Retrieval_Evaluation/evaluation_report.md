# Week 5 Retrieval Evaluation Report

## 1. Objective

The objective of this experiment was to evaluate the performance of the
AG News semantic retrieval system and determine suitable hyperparameter
values for retrieval.

The evaluation focused on:

- Precision@K
- Recall@K
- Different K values
- Different chunk sizes

A manually created test set containing 20 queries was used for evaluation.

The same embedding model and test queries were used throughout the
evaluation to maintain consistency.

---

## 2. Test Set

The evaluation used 20 manually created user queries.

Each query was associated with one expected relevant ground-truth chunk.

The same 20 test queries were used for the K-value experiment and the
chunk-size experiment.

The ground-truth identifiers were based on the original ChromaDB
chunking configuration.

---

## 3. K Value Experiment

The following K values were evaluated:

- K = 1
- K = 3
- K = 5
- K = 10

### Results

| K | Precision@K | Recall@K |
|---:|---:|---:|
| 1 | 0.3500 | 0.3500 |
| 3 | 0.1667 | 0.5000 |
| 5 | 0.1200 | 0.6000 |
| 10 | 0.0700 | 0.7000 |

### Findings

The results show a clear trade-off between Precision and Recall as K
increases.

At K=1, the system achieved a Precision@1 of 0.3500 and Recall@1 of
0.3500.

When K increased to 3, Recall increased to 0.5000 while Precision
decreased to 0.1667.

At K=5, Recall increased further to 0.6000, while Precision decreased
to 0.1200.

At K=10, the system achieved the highest recall of 0.7000, but
Precision decreased to 0.0700.

This indicates that retrieving more documents increases the probability
of finding the relevant document, but it also introduces more irrelevant
documents.

### Best K

Based on the balance between Precision and Recall, K=5 provides a
reasonable compromise between retrieving relevant information and
limiting irrelevant results.

K=10 provides the highest recall, but its precision is considerably
lower.

Therefore, the initial selected value is:

**Best K: 5**

---

## 4. Chunk Size Experiment

The following chunk sizes were tested:

- 250
- 500
- 750
- 1000

Each chunk size was stored in a separate ChromaDB database so that the
experiments could be compared independently.

### Initial Results

| Chunk Size | K | Precision | Recall |
|---:|---:|---:|---:|
| 250 | 1 | 0.0000 | 0.0000 |
| 250 | 3 | 0.0000 | 0.0000 |
| 250 | 5 | 0.0000 | 0.0000 |
| 250 | 10 | 0.0000 | 0.0000 |
| 500 | 1 | 0.0000 | 0.0000 |
| 500 | 3 | 0.0000 | 0.0000 |
| 500 | 5 | 0.0000 | 0.0000 |
| 500 | 10 | 0.0000 | 0.0000 |
| 750 | 1 | 0.0000 | 0.0000 |
| 750 | 3 | 0.0000 | 0.0000 |
| 750 | 5 | 0.0000 | 0.0000 |
| 750 | 10 | 0.0000 | 0.0000 |
| 1000 | 1 | 0.0000 | 0.0000 |
| 1000 | 3 | 0.0000 | 0.0000 |
| 1000 | 5 | 0.0000 | 0.0000 |
| 1000 | 10 | 0.0000 | 0.0000 |

### Evaluation Issue

The initial chunk-size evaluation returned zero Precision and Recall
for every chunk size.

This result was caused by a mismatch between the ground-truth chunk IDs
used by the test set and the chunk IDs generated for the new
chunk-size databases.

For example, the existing test set contains ground-truth identifiers
such as:

`chunk_50001`

The new chunk-size experiment generates different chunk identifiers
for each chunk-size configuration.

Therefore, the ground-truth IDs from the original database cannot be
directly used to evaluate the newly generated chunk-size databases.

As a result, the zero values should not be interpreted as evidence that
all four chunk sizes have zero retrieval performance.

The chunk-size evaluation requires refinement so that the same original
documents can be correctly matched to their corresponding chunks under
each chunk-size configuration.

---

## 5. Impact of Chunk Size

Different chunk sizes can affect semantic retrieval performance.

Smaller chunks can provide more focused pieces of information and may
improve retrieval precision for specific questions. However, very small
chunks may lose important contextual information.

Larger chunks preserve more context but can contain additional
information that is not directly relevant to the query.

The experiment tested chunk sizes of 250, 500, 750, and 1000 characters.

The initial evaluation successfully created separate ChromaDB
collections for all four configurations.

However, the retrieval metrics cannot yet be used to determine the best
chunk size because the current ground-truth identifiers are tied to the
original chunking configuration.

### Best Chunk Size

**Best chunk size: To be determined after ground-truth alignment is refined.**

---

## 6. Final Configuration

Based on the completed K-value experiment:

**Best K: 5**

The chunk-size configuration is still under evaluation because the
initial experiment identified a ground-truth ID mismatch.

Therefore, the final chunk-size value will be selected after correcting
the evaluation logic.

**Best chunk size: To be determined**

**Best K: 5**

---

## 7. Retrieval Refinement

The K-value experiment demonstrated that increasing K improves recall
but reduces precision.

The results were:

- K=1: Precision 0.3500, Recall 0.3500
- K=3: Precision 0.1667, Recall 0.5000
- K=5: Precision 0.1200, Recall 0.6000
- K=10: Precision 0.0700, Recall 0.7000

Based on the balance between precision and recall, K=5 was selected as
the initial retrieval configuration.

The chunk-size experiment also identified an evaluation limitation:
the ground-truth IDs must be mapped to the corresponding documents
rather than directly reused across different chunking configurations.

The retrieval evaluation logic will therefore be refined so that
different chunk sizes can be compared using the same underlying
ground-truth documents.

---

## 8. Conclusion

The Week 5 retrieval evaluation measured the effect of different K
values on semantic retrieval performance using 20 test queries.

The K-value experiment showed that increasing K improves Recall but
reduces Precision.

K=10 achieved the highest recall of 0.7000, while K=1 achieved the
highest precision of 0.3500.

K=5 was selected as a reasonable balance, providing Recall@5 of 0.6000
while maintaining Precision@5 of 0.1200.

The chunk-size experiment successfully created separate vector
databases for chunk sizes 250, 500, 750, and 1000.

However, the initial chunk-size evaluation produced zero scores because
the existing ground-truth chunk IDs were associated with the original
chunking configuration and could not be directly matched to the newly
generated chunks.

This issue was identified during evaluation and will be addressed by
refining the ground-truth mapping. This will allow the four chunk sizes
to be compared fairly using the same underlying test documents.

The evaluation therefore provided both quantitative retrieval results
and a clear direction for improving the retrieval evaluation logic.