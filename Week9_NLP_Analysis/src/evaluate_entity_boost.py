import chromadb
import spacy
from sentence_transformers import SentenceTransformer


# CONFIGURATION
CHROMA_PATH = r"C:\Users\HP\Week4_Vector_Database\chroma_db"
COLLECTION_NAME = "ag_news"

MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5
CANDIDATE_K = 30
ENTITY_BOOST = 0.20


# TEST QUERIES
test_queries = [
    "Iraq oil",
    "Microsoft technology",
    "US economy",
    "China business",
    "football players"
]


# CONNECT TO CHROMADB
print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print("ChromaDB connected.")
print("Total chunks:", collection.count())


# LOAD MODELS
print("\nLoading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded.")


print("\nLoading spaCy NER model...")

nlp = spacy.load("en_core_web_sm")

print("spaCy model loaded.")


# EXTRACT QUERY ENTITIES
def extract_query_entities(query):

    doc = nlp(query)

    entities = []

    for ent in doc.ents:

        entity = ent.text.strip().lower()

        if entity:
            entities.append(entity)

    return list(set(entities))


# NORMAL RETRIEVAL
def normal_retrieval(query):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"]
    )

    return results


# ENTITY-BOOSTED RETRIEVAL
def boosted_retrieval(query):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=CANDIDATE_K,
        include=["documents", "metadatas", "distances"]
    )

    query_entities = extract_query_entities(query)

    scored_results = []

    for chunk_id, document, metadata, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):

        semantic_score = 1 / (1 + distance)

        entity_score = 0.0

        chunk_entities = metadata.get(
            "entities",
            ""
        )

        stored_entities = []

        if chunk_entities:

            for item in str(
                chunk_entities
            ).split(";"):

                item = item.strip()

                if ":" in item:

                    entity_text = item.rsplit(
                        ":",
                        1
                    )[0]

                    stored_entities.append(
                        entity_text.strip().lower()
                    )

        for query_entity in query_entities:

            if query_entity in stored_entities:

                entity_score += ENTITY_BOOST

        final_score = (
            semantic_score +
            entity_score
        )

        scored_results.append(
            {
                "id": chunk_id,
                "entity_score": entity_score,
                "final_score": final_score
            }
        )

    scored_results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return scored_results[:TOP_K]


# MAIN EVALUATION
def main():

    print("\n" + "=" * 70)
    print("ENTITY BOOST EVALUATION")
    print("=" * 70)

    total_changes = 0
    total_entity_matches = 0

    for query in test_queries:

        print("\n" + "-" * 70)
        print("Query:", query)
        print("-" * 70)

        # Normal results
        normal = normal_retrieval(query)

        normal_ids = normal["ids"][0]

        # Boosted results
        boosted = boosted_retrieval(query)

        boosted_ids = [
            result["id"]
            for result in boosted
        ]

        # Check ranking change
        if normal_ids != boosted_ids:

            total_changes += 1

            print("Ranking changed: YES")

        else:

            print("Ranking changed: NO")

        # Count boosted results with entity matches
        entity_matches = sum(
            1
            for result in boosted
            if result["entity_score"] > 0
        )

        total_entity_matches += entity_matches

        print(
            "Entity-matched results:",
            entity_matches
        )

        print("\nNormal Top-K:")

        for i, chunk_id in enumerate(
            normal_ids,
            start=1
        ):

            print(
                f"{i}. {chunk_id}"
            )

        print("\nBoosted Top-K:")

        for i, result in enumerate(
            boosted,
            start=1
        ):

            print(
                f"{i}. {result['id']} "
                f"(entity score: "
                f"{result['entity_score']})"
            )


    print("\n" + "=" * 70)
    print("FINAL EVALUATION")
    print("=" * 70)

    print(
        "Queries evaluated:",
        len(test_queries)
    )

    print(
        "Queries with ranking changes:",
        total_changes
    )

    print(
        "Total entity-matched results:",
        total_entity_matches
    )


if __name__ == "__main__":
    main()