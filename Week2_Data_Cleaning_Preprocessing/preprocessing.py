import pandas as pd
import spacy

from cleaning import clean_text

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load dataset
df = pd.read_csv("dataset/train.csv")

original_rows = len(df)

# Combine title and description
df["text"] = (
    df["Title"].fillna("")
    + " "
    + df["Description"].fillna("")
)

# Clean text
df["clean_text"] = df["text"].apply(clean_text)

# Remove rows with empty cleaned text
df = df[df["clean_text"].str.strip() != ""]

remaining_rows = len(df)

# Process only first 100 rows with spaCy
sample = df.head(100).copy()

tokens = []
lemmas = []

for doc in nlp.pipe(sample["clean_text"]):

    tokens.append([token.text for token in doc])
    lemmas.append([token.lemma_ for token in doc])

sample["tokens"] = tokens
sample["lemmas"] = lemmas

print(sample[["clean_text", "tokens", "lemmas"]].head())

# Save cleaned dataset
df.to_csv("dataset/cleaned_train.csv", index=False)

# Cleaning report
rows_removed = original_rows - remaining_rows
percentage_removed = (rows_removed / original_rows) * 100

print("\nCleaning Report")
print(f"Original rows: {original_rows}")
print(f"Remaining rows: {remaining_rows}")
print(f"Rows removed: {rows_removed}")
print(f"Percentage removed: {percentage_removed:.2f}%")