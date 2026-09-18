import pandas as pd

# Load the manually reviewed evaluation data
input_path = r"C:\Users\HP\Week9_NLP_Analysis\data\ner_manual_evaluation.csv"

df = pd.read_csv(input_path)


def parse_entities(entity_string):
    """
    Convert:
        Apple:ORG; London:GPE

    into:
        {("Apple", "ORG"), ("London", "GPE")}
    """
    entities = set()

    if pd.isna(entity_string) or str(entity_string).strip() == "":
        return entities

    for item in str(entity_string).split(";"):
        item = item.strip()

        if ":" not in item:
            continue

        entity_text, entity_type = item.rsplit(":", 1)

        entities.add(
            (entity_text.strip(), entity_type.strip())
        )

    return entities


true_positive = 0
false_positive = 0
false_negative = 0

for _, row in df.iterrows():

    predicted = parse_entities(row["predicted_entities"])
    actual = parse_entities(row["manual_entities"])

    true_positive += len(predicted & actual)
    false_positive += len(predicted - actual)
    false_negative += len(actual - predicted)


# Calculate metrics
if true_positive + false_positive > 0:
    precision = true_positive / (true_positive + false_positive)
else:
    precision = 0

if true_positive + false_negative > 0:
    recall = true_positive / (true_positive + false_negative)
else:
    recall = 0

if precision + recall > 0:
    f1 = 2 * (precision * recall) / (precision + recall)
else:
    f1 = 0


print("===== NER EVALUATION =====")
print("Number of samples:", len(df))

print("\nEntity-level results:")
print("True Positives :", true_positive)
print("False Positives:", false_positive)
print("False Negatives:", false_negative)

print("\n===== METRICS =====")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")


# Save evaluation summary
output_path = r"C:\Users\HP\Week9_NLP_Analysis\results\ner_evaluation_summary.txt"

with open(output_path, "w", encoding="utf-8") as file:
    file.write("NER Evaluation Summary\n")
    file.write("======================\n\n")

    file.write(f"Number of samples: {len(df)}\n\n")

    file.write("Entity-level results:\n")
    file.write(f"True Positives: {true_positive}\n")
    file.write(f"False Positives: {false_positive}\n")
    file.write(f"False Negatives: {false_negative}\n\n")

    file.write("Metrics:\n")
    file.write(f"Precision: {precision:.4f}\n")
    file.write(f"Recall: {recall:.4f}\n")
    file.write(f"F1-score: {f1:.4f}\n")

print("\nEvaluation summary saved to:")
print(output_path)