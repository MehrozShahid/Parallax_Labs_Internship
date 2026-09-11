import os
import pandas as pd

INPUT_PATH = "results/topic_validation.csv"
SUMMARY_PATH = "results/validation_summary.csv"
TOPIC_SUMMARY_PATH = "results/topic_validation_by_topic.csv"

print("Loading validation results...")

if not os.path.exists(INPUT_PATH):
    raise FileNotFoundError(
        f"Validation file not found: {INPUT_PATH}"
    )

df = pd.read_csv(INPUT_PATH)

print(f"Documents loaded: {len(df)}")

required_columns = [
    "sample_id",
    "topic_id",
    "topic_name",
    "document",
    "manual_label",
    "notes"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# Clean labels
df["manual_label"] = (
    df["manual_label"]
    .astype(str)
    .str.strip()
    .str.title()
)

# Check for invalid labels
valid_labels = ["Yes", "No", "Unclear"]

invalid_labels = df[
    ~df["manual_label"].isin(valid_labels)
]

if len(invalid_labels) > 0:
    print("\nWARNING: Invalid or empty labels found.")
    print(invalid_labels["manual_label"].value_counts())
    raise ValueError(
        "Please make sure manual_label contains only "
        "Yes, No, or Unclear."
    )

# --------------------------------------------------
# Overall validation results
# --------------------------------------------------

total_documents = len(df)

yes_count = (df["manual_label"] == "Yes").sum()
no_count = (df["manual_label"] == "No").sum()
unclear_count = (df["manual_label"] == "Unclear").sum()

agreement_percentage = (
    yes_count / total_documents
) * 100

clear_documents = yes_count + no_count

clear_agreement_percentage = (
    yes_count / clear_documents
) * 100 if clear_documents > 0 else 0

print("\n===================================")
print("VALIDATION RESULTS")
print("===================================")

print(f"Total documents reviewed: {total_documents}")
print(f"Yes: {yes_count}")
print(f"No: {no_count}")
print(f"Unclear: {unclear_count}")

print(
    f"\nOverall agreement: "
    f"{agreement_percentage:.2f}%"
)

print(
    f"Agreement among clear labels: "
    f"{clear_agreement_percentage:.2f}%"
)

# --------------------------------------------------
# Validation by topic
# --------------------------------------------------

print("\nCalculating results by topic...")

topic_results = []

for topic_id, group in df.groupby("topic_id"):

    total = len(group)

    yes = (group["manual_label"] == "Yes").sum()
    no = (group["manual_label"] == "No").sum()
    unclear = (group["manual_label"] == "Unclear").sum()

    agreement = (
        yes / total
    ) * 100 if total > 0 else 0

    topic_name = group["topic_name"].iloc[0]

    topic_results.append({
        "topic_id": topic_id,
        "topic_name": topic_name,
        "documents_reviewed": total,
        "yes": yes,
        "no": no,
        "unclear": unclear,
        "agreement_percentage": round(agreement, 2)
    })

topic_summary = pd.DataFrame(topic_results)

# Sort from weakest to strongest
topic_summary = topic_summary.sort_values(
    by="agreement_percentage"
)

topic_summary.to_csv(
    TOPIC_SUMMARY_PATH,
    index=False
)

# --------------------------------------------------
# Overall summary
# --------------------------------------------------

summary = pd.DataFrame([{
    "total_documents_reviewed": total_documents,
    "yes_count": yes_count,
    "no_count": no_count,
    "unclear_count": unclear_count,
    "overall_agreement_percentage": round(
        agreement_percentage, 2
    ),
    "clear_label_agreement_percentage": round(
        clear_agreement_percentage, 2
    ),
    "topics_reviewed": (
        df[df["topic_id"] != -1]["topic_id"].nunique()
    ),
    "outlier_documents_reviewed": (
        (df["topic_id"] == -1).sum()
    )
}])

summary.to_csv(
    SUMMARY_PATH,
    index=False
)

# --------------------------------------------------
# Display strongest and weakest topics
# --------------------------------------------------

real_topics = topic_summary[
    topic_summary["topic_id"] != -1
]

print("\n===================================")
print("WEAKEST TOPICS")
print("===================================")

print(
    real_topics
    .head(10)
    .to_string(index=False)
)

print("\n===================================")
print("STRONGEST TOPICS")
print("===================================")

print(
    real_topics
    .sort_values(
        by="agreement_percentage",
        ascending=False
    )
    .head(10)
    .to_string(index=False)
)

# --------------------------------------------------
# Outlier results
# --------------------------------------------------

outliers = df[df["topic_id"] == -1]

print("\n===================================")
print("OUTLIER VALIDATION")
print("===================================")

print(
    f"Outlier documents reviewed: {len(outliers)}"
)

print(
    outliers["manual_label"]
    .value_counts()
    .to_string()
)

print("\n===================================")
print("FILES SAVED")
print("===================================")

print(f"Overall summary:")
print(SUMMARY_PATH)

print(f"\nTopic-by-topic summary:")
print(TOPIC_SUMMARY_PATH)

print("\nStep 4 completed successfully.")