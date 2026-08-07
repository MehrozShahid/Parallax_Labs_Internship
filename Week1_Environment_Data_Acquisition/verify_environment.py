"""
Environment Verification Script

Author: Mehroz Shahid
"""

# 1. Check Python Version

import sys

print("=" * 60)
print("ENVIRONMENT VERIFICATION")
print("=" * 60)

print(f"\nPython Version: {sys.version.split()[0]}")

# 2. Verify Pandas

try:
    import pandas as pd

    # Create sample data to verify Pandas is working
    student_data = pd.DataFrame({
        "Name": ["Ali", "Ayesha", "Usman"],
        "Marks": [83, 91, 70]
    })

    print("\n✅ Pandas imported successfully")
    print("DataFrame Created:")
    print(student_data)

except Exception as e:
    print(f"\n❌ Pandas Error: {e}")

# 3. Verify spaCy

try:
    import spacy

    print("\n✅ spaCy imported successfully")
    print("spaCy Version:", spacy.__version__)

except Exception as e:
    print(f"\n❌ spaCy Error: {e}")

# 4. Verify NLTK

try:
    import nltk

    print("\n✅ NLTK imported successfully")
    print("NLTK Version:", nltk.__version__)

except Exception as e:
    print(f"\n❌ NLTK Error: {e}")

# 5. Verify Sentence Transformers

try:
    from sentence_transformers import SentenceTransformer

    # Load a pretrained model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Sample text for embedding generation
    sentence = "Artificial Intelligence is transforming the world."

    # Generate embedding
    embedding = model.encode(sentence)

    print("\n✅ Sentence Transformers imported successfully")
    print("Embedding Dimension:", len(embedding))

except Exception as e:
    print(f"\n❌ Sentence Transformers Error: {e}")

# 6. Verify ChromaDB

try:
    import chromadb

    # Create an in-memory client
    client = chromadb.Client()

    # Create a temporary collection for testing
    collection = client.create_collection(name="environment_test")

    print("\n✅ ChromaDB imported successfully")
    print("Collection Name:", collection.name)

except Exception as e:
    print(f"\n❌ ChromaDB Error: {e}")

# Final Status

print("\n" + "=" * 60)
print("Environment verification completed.")
print("=" * 60)