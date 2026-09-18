import chromadb
import spacy
from sentence_transformers import SentenceTransformer


# CONFIGURATION
CHROMA_PATH = r"C:\Users\HP\Week4_Vector_Database\chroma_db"
COLLECTION_NAME = "ag_news"

MODEL_NAME = "all-MiniLM-L6-v2"

# Number of final results
TOP_K = 5

# Number of candidates retrieved before reranking
CANDIDATE_K = 30

# Entity boost value
ENTITY_BOOST = 0.20


# CONNECT TO CHROMADB
print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print("ChromaDB connected successfully.")
print("Collection:", COLLECTION_NAME)
print("Total chunks:", collection.count())


# LOAD EMBEDDING MODEL
print("\nLoading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


# LOAD SPACY NER MODEL
print("\nLoading spaCy NER model...")

nlp = spacy.load("en_core_web_sm")

print("spaCy model loaded successfully.")


# EXTRACT ENTITIES FROM QUERY
def extract_query_entities(query):
    """
    Extract named entities from the user query.
    """

    doc = nlp(query)

    entities = []

    for ent in doc.ents:
        entity = ent.text.strip().lower()

        if entity:
            entities.append(entity)

    return list(set(entities))


# NORMAL RETRIEVAL
def normal_retrieval(query, k=TOP_K):
    """
    Retrieve chunks using normal semantic similarity.
    """

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    return results


# ENTITY-BOOSTED RETRIEVAL
def entity_boosted_retrieval(query, k=TOP_K):
    """
    Retrieve candidate chunks using semantic similarity
    and rerank them using entity matching.
    """

    query_embedding = model.encode(query).tolist()

    # Retrieve more candidates first
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=CANDIDATE_K,
        include=["documents", "metadatas", "distances"]
    )

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # Extract entities from query
    query_entities = extract_query_entities(query)

    print("\nQuery entities:", query_entities)

    scored_results = []

    for chunk_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances
    ):

        # Convert distance into a simple similarity score
        semantic_score = 1 / (1 + distance)

        entity_score = 0.0
        matched_entities = []

        chunk_entities = metadata.get("entities", "")

        if chunk_entities:
            # Extract entity text from:
            # "Microsoft:ORG; Apple:ORG"
            stored_entities = []

            for item in str(chunk_entities).split(";"):

                item = item.strip()

                if ":" in item:
                    entity_text = item.rsplit(":", 1)[0]
                    stored_entities.append(
                        entity_text.strip().lower()
                    )

            # Check query entities
            for query_entity in query_entities:

                if query_entity in stored_entities:

                    entity_score += ENTITY_BOOST
                    matched_entities.append(query_entity)

        final_score = semantic_score + entity_score

        scored_results.append(
            {
                "id": chunk_id,
                "document": document,
                "metadata": metadata,
                "semantic_score": semantic_score,
                "entity_score": entity_score,
                "final_score": final_score,
                "matched_entities": matched_entities
            }
        )

    # Sort by final score
    scored_results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return scored_results[:k]


# TEST
def main():

    print("\n" + "=" * 70)
    print("ENTITY-BOOSTED RAG RETRIEVAL")
    print("=" * 70)

    query = input("\nEnter your query: ")

    # Normal retrieval
    print("\n" + "=" * 70)
    print("NORMAL RETRIEVAL")
    print("=" * 70)

    normal_results = normal_retrieval(
        query,
        TOP_K
    )

    for i, (chunk_id, document, metadata, distance) in enumerate(
        zip(
            normal_results["ids"][0],
            normal_results["documents"][0],
            normal_results["metadatas"][0],
            normal_results["distances"][0]
        ),
        start=1
    ):

        print(f"\nResult {i}")
        print("ID:", chunk_id)
        print("Distance:", round(distance, 4))
        print("Entities:", metadata.get("entities", ""))
        print("Document:", document[:300])


    # Entity boosted retrieval
    print("\n" + "=" * 70)
    print("ENTITY-BOOSTED RETRIEVAL")
    print("=" * 70)

    boosted_results = entity_boosted_retrieval(
        query,
        TOP_K
    )

    for i, result in enumerate(
        boosted_results,
        start=1
    ):

        print(f"\nResult {i}")
        print("ID:", result["id"])
        print(
            "Semantic Score:",
            round(result["semantic_score"], 4)
        )
        print(
            "Entity Score:",
            round(result["entity_score"], 4)
        )
        print(
            "Final Score:",
            round(result["final_score"], 4)
        )
        print(
            "Matched Entities:",
            result["matched_entities"]
        )
        print(
            "Document:",
            result["document"][:300]
        )


if __name__ == "__main__":
    main()