import time
import logging

import chromadb
from sentence_transformers import SentenceTransformer

from config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    MODEL_NAME,
    TOP_K,
    LOG_FILE
)

from prompt import (
    SYSTEM_PROMPT,
    build_prompt
)

from llm_client import generate_answer


# Save useful information such as queries and response times
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# Load the same embedding model used in Week 5
print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)


# Connect to the existing ChromaDB
print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


# Use the collection created during Week 5
collection = client.get_collection(
    name=COLLECTION_NAME
)


print("ChromaDB connected.")
print(f"Total chunks: {collection.count()}")


def retrieve_chunks(question):
    """
    Find the most relevant chunks for the user's question.
    """

    # Convert the question into an embedding
    question_embedding = model.encode(
        question
    ).tolist()


    # Search ChromaDB for the most similar chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K
    )


    # Get the text of the retrieved chunks
    chunks = results["documents"][0]

    return chunks


def answer_question(question):
    """
    Run the complete RAG process from retrieval to answer generation.
    """

    # Start the timer for the complete process
    total_start = time.perf_counter()


    logging.info(
        f"Question received: {question}"
    )


    # -----------------------------
    # Retrieve relevant chunks
    # -----------------------------

    retrieval_start = time.perf_counter()


    try:
        chunks = retrieve_chunks(question)

    except Exception as error:

        logging.error(
            f"Retrieval error: {error}"
        )

        return {
            "answer": "ERROR: Could not retrieve information.",
            "retrieval_time": 0,
            "generation_time": 0,
            "total_time": 0
        }


    retrieval_time = (
        time.perf_counter()
        - retrieval_start
    )


    logging.info(
        f"Retrieved {len(chunks)} chunks"
    )

    logging.info(
        f"Retrieval time: {retrieval_time:.4f} seconds"
    )


    # Nothing was found in the database
    if not chunks:

        logging.warning(
            "No relevant chunks found."
        )

        return {
            "answer": "No relevant information was found.",
            "retrieval_time": retrieval_time,
            "generation_time": 0,
            "total_time": retrieval_time
        }


    # -----------------------------
    # Build the prompt
    # -----------------------------

    user_prompt = build_prompt(
        question,
        chunks
    )


    # -----------------------------
    # Generate the answer
    # -----------------------------

    generation_start = time.perf_counter()


    answer = generate_answer(
        SYSTEM_PROMPT,
        user_prompt
    )


    generation_time = (
        time.perf_counter()
        - generation_start
    )


    logging.info(
        f"Generation time: {generation_time:.4f} seconds"
    )


    # -----------------------------
    # Calculate total response time
    # -----------------------------

    total_time = (
        time.perf_counter()
        - total_start
    )


    logging.info(
        f"Total latency: {total_time:.4f} seconds"
    )


    return {
        "answer": answer,
        "retrieval_time": retrieval_time,
        "generation_time": generation_time,
        "total_time": total_time
    }