import time
import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

BATCH_SIZE = 64


# Load cleaned dataset
df = pd.read_csv(
    "../dataset/cleaned_train.csv"
)

print(f"Loaded {len(df)} rows from cleaned dataset.")


# Create text splitter
# Same settings used in Week 3
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


# Create chunks
all_chunks = []

for text in df["clean_text"]:

    if not isinstance(text, str):
        continue

    if text.strip() == "":
        continue

    chunks = text_splitter.split_text(text)

    all_chunks.extend(chunks)


print(f"Total chunks created: {len(all_chunks)}")

# Load embedding model
# Same model used in Week 3
print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Generate embeddings
print("Generating embeddings...")

start_time = time.perf_counter()

embeddings = model.encode(
    all_chunks,
    batch_size=BATCH_SIZE,
    show_progress_bar=True
)

end_time = time.perf_counter()

print(
    f"Embedding generation completed in "
    f"{end_time - start_time:.2f} seconds."
)

# Convert embeddings to Python lists
embeddings = embeddings.tolist()

# Create ChromaDB client
client = chromadb.PersistentClient(
    path="../chroma_db"
)

# Create / get collection
collection = client.get_or_create_collection(
    name="ag_news"
)

print(
    f"Documents currently in ChromaDB: "
    f"{collection.count()}"
)

# Create IDs
ids = [
    f"chunk_{i}"
    for i in range(len(all_chunks))
]

# Store data in ChromaDB
print("Ingesting data into ChromaDB...")

batch_size = 5000

for start in range(0, len(all_chunks), batch_size):

    end = start + batch_size

    collection.upsert(
        ids=ids[start:end],
        documents=all_chunks[start:end],
        embeddings=embeddings[start:end]
    )

    print(f"Stored {min(end, len(all_chunks))} / {len(all_chunks)} chunks")

# Verify
print("\nIngestion completed successfully.")

print(
    f"Total documents in ChromaDB: "
    f"{collection.count()}"
)