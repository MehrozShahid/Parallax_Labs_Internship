import os
import pandas as pd
from bertopic import BERTopic


# ==================================================
# Configuration
# ==================================================

MODEL_PATH = "models/topic_model"
DATA_PATH = "data/topic_documents.csv"

OUTPUT_PATH = "results/topic_validation.csv"

SAMPLES_PER_TOPIC = 20
RANDOM_STATE = 42


# ==================================================
# Create results directory
# ==================================================

os.makedirs("results", exist_ok=True)


# ==================================================
# Load topic model
# ==================================================

print("Loading BERTopic model...")

topic_model = BERTopic.load(
    MODEL_PATH
)

print("BERTopic model loaded successfully.")


# ==================================================
# Load document-topic assignments
# ==================================================

print("\nLoading topic assignments...")

df = pd.read_csv(DATA_PATH)

print(
    f"Documents loaded: {len(df)}"
)


# ==================================================
# Check required columns
# ==================================================

required_columns = [
    "document",
    "topic_id",
    "topic_name"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ==================================================
# Get topic information
# ==================================================

print("\nGetting topic information...")

topic_info = topic_model.get_topic_info()

print(
    f"Total topic entries: {len(topic_info)}"
)


# ==================================================
# Create topic-name mapping
# ==================================================

topic_names = {}

for topic_id in topic_info["Topic"]:

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
# Validate topic counts
# ==================================================

print("\n===================================")
print("TOPIC VALIDATION")
print("===================================")

real_topics = sorted(
    topic_id
    for topic_id in df["topic_id"].unique()
    if topic_id != -1
)

print(
    f"Real topics found: {len(real_topics)}"
)

print(
    f"Outlier documents: "
    f"{(df['topic_id'] == -1).sum()}"
)


# ==================================================
# Random sampling
# ==================================================

print("\nSampling documents...")


validation_rows = []


# --------------------------------------------------
# Sample 20 documents from every real topic
# --------------------------------------------------

for topic_id in real_topics:

    topic_documents = df[
        df["topic_id"] == topic_id
    ]

    sample_size = min(
        SAMPLES_PER_TOPIC,
        len(topic_documents)
    )

    sampled_documents = topic_documents.sample(
        n=sample_size,
        random_state=RANDOM_STATE
    )

    print(
        f"Topic {topic_id}: "
        f"{len(topic_documents)} documents → "
        f"{sample_size} sampled"
    )

    for _, row in sampled_documents.iterrows():

        validation_rows.append({

            "topic_id": topic_id,

            "topic_name": topic_names.get(
                topic_id,
                "Unknown"
            ),

            "document": row["document"],

            "manual_label": "",

            "notes": ""

        })


# --------------------------------------------------
# Sample 20 outlier documents
# --------------------------------------------------

outlier_documents = df[
    df["topic_id"] == -1
]

if len(outlier_documents) > 0:

    sample_size = min(
        SAMPLES_PER_TOPIC,
        len(outlier_documents)
    )

    sampled_outliers = outlier_documents.sample(
        n=sample_size,
        random_state=RANDOM_STATE
    )

    print(
        f"\nOutliers: "
        f"{len(outlier_documents)} documents → "
        f"{sample_size} sampled"
    )

    for _, row in sampled_outliers.iterrows():

        validation_rows.append({

            "topic_id": -1,

            "topic_name": "Outlier / Unclassified",

            "document": row["document"],

            "manual_label": "",

            "notes": ""

        })


# ==================================================
# Create validation dataframe
# ==================================================

print("\nCreating validation dataframe...")

validation_df = pd.DataFrame(
    validation_rows
)


# ==================================================
# Add validation columns
# ==================================================

validation_df.insert(
    0,
    "sample_id",
    range(1, len(validation_df) + 1)
)


# ==================================================
# Save validation dataset
# ==================================================

validation_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==================================================
# Validation statistics
# ==================================================

real_sample_count = len(
    validation_df[
        validation_df["topic_id"] != -1
    ]
)

outlier_sample_count = len(
    validation_df[
        validation_df["topic_id"] == -1
    ]
)


# ==================================================
# Final summary
# ==================================================

print("\n===================================")
print("VALIDATION DATASET CREATED")
print("===================================")

print(
    f"Real topics sampled: "
    f"{len(real_topics)}"
)

print(
    f"Documents per topic: "
    f"{SAMPLES_PER_TOPIC}"
)

print(
    f"Real-topic documents sampled: "
    f"{real_sample_count}"
)

print(
    f"Outlier documents sampled: "
    f"{outlier_sample_count}"
)

print(
    f"Total validation documents: "
    f"{len(validation_df)}"
)

print("\nSaved validation file:")

print(
    OUTPUT_PATH
)

print("\nStep 4 preparation completed successfully.")

