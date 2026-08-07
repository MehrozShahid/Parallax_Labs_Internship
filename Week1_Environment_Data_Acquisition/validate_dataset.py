import pandas as pd

try:
    df = pd.read_csv("dataset/train.csv", encoding="utf-8")
    print("✓ Dataset uses UTF-8 encoding.")
except UnicodeDecodeError:
    print("✗ Encoding issue detected. File is not UTF-8.")
    exit()

print("Rows:", len(df))
print("Columns:", list(df.columns))

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

expected_columns = ["Class Index", "Title", "Description"]

missing = [col for col in expected_columns if col not in df.columns]

if not missing:
    print("✓ All expected columns are present.")
else:
    print("Missing columns:", missing)