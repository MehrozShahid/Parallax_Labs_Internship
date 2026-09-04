import time
import logging
import json

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


def check_hallucination(answer, chunks):
    """
    Check whether the generated answer is supported
    by the retrieved context.
    """

    # If the model already says I don't know,
    # there is no hallucination to check.
    if answer.strip().lower() == "i don't know.":

        return False


    # Combine all retrieved chunks
    context = "\n".join(chunks)


    # If there is no context, the answer cannot
    # be supported.
    if not context.strip():

        return False


    # Prompt used to check the generated answer
    checker_prompt = f"""
Check whether the answer is completely supported
by the provided context.

Context:

{context}

Answer:

{answer}

Rules:

1. Use only the provided context.
2. Do not use outside knowledge.
3. If the important claims in the answer are supported,
   return true.
4. If any important claim is not supported,
   return false.

Return ONLY valid JSON:

{{
    "supported": true
}}

or:

{{
    "supported": false
}}
"""


    checker_system_prompt = """
You are a hallucination checker.

Check whether the answer is supported by the
provided context.

Do not use outside knowledge.

Return ONLY valid JSON.
"""


    # Ask the LLM to check the answer
    result = generate_answer(
        checker_system_prompt,
        checker_prompt
    )


    # Convert the checker response to JSON
    try:

        result = json.loads(result)

        return result.get(
            "supported",
            False
        )


    except json.JSONDecodeError:

        # If the checker does not return valid JSON,
        # treat the answer as unsupported.
        return False


def answer_question(question):
    """
    Run the complete RAG process.
    """

    # Start the timer for the complete process
    total_start = time.perf_counter()


    logging.info(
        f"Question received: {question}"
    )


    # Retrieve relevant chunks

    retrieval_start = time.perf_counter()


    try:

        chunks = retrieve_chunks(question)


    except Exception as error:

        logging.error(
            f"Retrieval error: {error}"
        )

        return {
            "answer": "ERROR: Could not retrieve information.",
            "sources": [],
            "supported": False,
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
            "answer": "I don't know.",
            "sources": [],
            "supported": False,
            "retrieval_time": retrieval_time,
            "generation_time": 0,
            "total_time": retrieval_time
        }


    # Build the prompt

    user_prompt = build_prompt(
        question,
        chunks
    )

    # Generate the answer

    generation_start = time.perf_counter()


    response = generate_answer(
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

    # Read the JSON response

    try:

        result = json.loads(response)


        answer = result.get(
            "answer",
            "I don't know."
        )


        sources = result.get(
            "sources",
            []
        )


        supported = result.get(
            "supported",
            False
        )


    except json.JSONDecodeError:

        # If the LLM does not return valid JSON,
        # we don't trust the answer.
        answer = "I don't know."

        sources = []

        supported = False


    # Hallucination check

    if supported:

        supported = check_hallucination(
            answer,
            chunks
        )


    # If the answer is not supported,
    # return I don't know.
    if not supported:

        answer = "I don't know."

        sources = []


        logging.warning(
            "Generated answer was not supported by context."
        )


    # Calculate total response time

    total_time = (
        time.perf_counter()
        - total_start
    )


    logging.info(
        f"Total latency: {total_time:.4f} seconds"
    )


    # Return all useful information
    return {
        "answer": answer,
        "sources": sources,
        "supported": supported,
        "retrieval_time": retrieval_time,
        "generation_time": generation_time,
        "total_time": total_time
    }