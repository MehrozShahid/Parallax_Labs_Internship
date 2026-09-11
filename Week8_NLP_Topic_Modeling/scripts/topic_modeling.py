import os
import pandas as pd

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer


# ==================================================
# Configuration
# ==================================================

INPUT_PATH = "data/topic_documents.csv"

MODEL_PATH = "models/topic_model"

TOPIC_INFO_PATH = "results/topic_info.csv"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

MIN_TOPIC_SIZE = 100


# ==================================================
# Load corpus
# ==================================================

print("Loading corpus...")

df = pd.read_csv(INPUT_PATH)

print(f"Documents loaded: {len(df)}")


# ==================================================
# Clean documents
# ==================================================

df["document"] = (
    df["document"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ==================================================
# Handle extremely short documents
# ==================================================

print("\nHandling short documents...")

documents = []

short_document_count = 0

for document in df["document"]:

    word_count = len(document.split())

    if word_count < 5:

        short_document_count += 1

        # Keep the original text but provide
        # additional context for the model.
        if document:
            processed_text = (
                "short document: " + document
            )
        else:
            processed_text = (
                "short document"
            )

        documents.append(processed_text)

    else:

        documents.append(document)


print(
    f"Short documents handled: "
    f"{short_document_count}"
)


# ==================================================
# Load embedding model
# ==================================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print(
    f"Embedding model loaded: "
    f"{EMBEDDING_MODEL}"
)


# ==================================================
# Create BERTopic model
# ==================================================

print("\nCreating BERTopic model...")

topic_model = BERTopic(

    embedding_model=embedding_model,

    min_topic_size=MIN_TOPIC_SIZE,

    nr_topics="auto",

    calculate_probabilities=False,

    verbose=True
)


# ==================================================
# Train BERTopic
# ==================================================

print("\n===================================")
print("STARTING BERTopic TRAINING")
print("===================================")

print(
    "This may take some time because "
    "the corpus contains 120,526 documents."
)

topics, probabilities = (
    topic_model.fit_transform(documents)
)


# ==================================================
# Add topic IDs to dataframe
# ==================================================

df["topic_id"] = topics


# ==================================================
# Get topic information
# ==================================================

print("\nGetting topic information...")

topic_info = topic_model.get_topic_info()


# ==================================================
# Create readable topic names
# ==================================================

print("Creating topic names...")

topic_names = {}


for topic_id in topic_info["Topic"]:

    # BERTopic uses -1 for outliers
    if topic_id == -1:

        topic_names[
            topic_id
        ] = "Outlier / Unclassified"

        continue


    topic_words = topic_model.get_topic(
        topic_id
    )


    if topic_words:

        top_words = [
            word
            for word, score
            in topic_words[:5]
        ]

        topic_names[
            topic_id
        ] = " | ".join(top_words)

    else:

        topic_names[
            topic_id
        ] = "Unknown"


# ==================================================
# Add topic names
# ==================================================

df["topic_name"] = (
    df["topic_id"]
    .map(topic_names)
)


# ==================================================
# Create output directories
# ==================================================

os.makedirs(
    MODEL_PATH,
    exist_ok=True
)

os.makedirs(
    "results",
    exist_ok=True
)


# ==================================================
# Save document-topic assignments
# ==================================================

print("\nSaving topic assignments...")

df.to_csv(
    INPUT_PATH,
    index=False
)


# ==================================================
# Save topic information
# ==================================================

print("Saving topic information...")

topic_info.to_csv(
    TOPIC_INFO_PATH,
    index=False
)


# ==================================================
# Save BERTopic model
# ==================================================

print("Saving BERTopic model...")

topic_model.save(
    MODEL_PATH,
    serialization="safetensors",
    save_ctfidf=True
)


# ==================================================
# Calculate statistics
# ==================================================

real_topics = [
    topic
    for topic in topic_info["Topic"]
    if topic != -1
]


number_of_topics = len(
    real_topics
)


outlier_count = sum(
    1
    for topic in topics
    if topic == -1
)


outlier_percentage = (
    outlier_count / len(topics)
) * 100


# ==================================================
# Display discovered topics
# ==================================================

print("\n===================================")
print("DISCOVERED TOPICS")
print("===================================")

for _, row in topic_info.iterrows():

    topic_id = row["Topic"]

    document_count = row["Count"]

    topic_name = topic_names.get(
        topic_id,
        "Unknown"
    )

    print(
        f"Topic {topic_id}: "
        f"{topic_name} "
        f"({document_count} documents)"
    )


# ==================================================
# Final summary
# ==================================================

print("\n===================================")
print("TOPIC MODELING COMPLETE")
print("===================================")

print(
    f"Total documents: {len(df)}"
)

print(
    f"Discovered topics: "
    f"{number_of_topics}"
)

print(
    f"Outlier documents: "
    f"{outlier_count}"
)

print(
    f"Outlier percentage: "
    f"{outlier_percentage:.2f}%"
)

print("\nFiles created:")

print(
    "1. data/topic_documents.csv"
)

print(
    "2. results/topic_info.csv"
)

print(
    "3. models/topic_model/"
)

print("\nStep 2 completed successfully.")