import pandas as pd
import spacy

# File paths
input_path = r"C:\Users\HP\Week8_NLP_Topic_Modeling\data\topic_documents.csv"

output_path = r"C:\Users\HP\Week9_NLP_Analysis\results\ner_topic_documents.csv"


# Load spaCy NER model
nlp = spacy.load("en_core_web_sm")


# Load Week 8 corpus
df = pd.read_csv(input_path)

print("===== CORPUS LOADED =====")
print("Number of documents:", len(df))

# Extract entities
entities_list = []
entity_types_list = []

texts = df["document"].fillna("").astype(str).tolist()

batch_size = 1000

for start in range(0, len(texts), batch_size):

    batch = texts[start:start + batch_size]

    docs = nlp.pipe(batch, batch_size=100)

    for doc in docs:

        entities = []
        entity_types = []

        for ent in doc.ents:
            entities.append(f"{ent.text}:{ent.label_}")
            entity_types.append(ent.label_)

        entities_list.append("; ".join(entities))
        entity_types_list.append("; ".join(sorted(set(entity_types))))

    processed = min(start + batch_size, len(texts))

    print(f"Processed {processed}/{len(texts)} documents")

# Add NER metadata
df["entities"] = entities_list
df["entity_types"] = entity_types_list

# Save Week 9 dataset
df.to_csv(output_path, index=False)


print("\n===== NER EXTRACTION COMPLETE =====")
print("Number of documents:", len(df))
print("New columns:")
print("- entities")
print("- entity_types")

print("\nSaved to:")
print(output_path)