import json
import time

import chromadb
import spacy

from sentence_transformers import SentenceTransformer

from app.config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    MODEL_NAME,
    TOP_K,
    CANDIDATE_K,
    ENTITY_BOOST,
    OPENROUTER_API_KEY,
    OPENROUTER_URL,
    LLM_MODEL,
    REQUEST_TIMEOUT
)


# ============================================================
# Load models and database once
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    MODEL_NAME
)

print("Embedding model loaded.")


print("Loading spaCy NER model...")

nlp = spacy.load(
    "en_core_web_sm"
)

print("spaCy NER model loaded.")


print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print("ChromaDB connected.")

print(
    f"Collection: {COLLECTION_NAME}"
)

print(
    f"Total chunks: {collection.count()}"
)


# ============================================================
# Entity extraction
# ============================================================

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


# ============================================================
# Entity-aware retrieval
# ============================================================

def retrieve_chunks(query, k=TOP_K):
    """
    Retrieve and rerank chunks using:

    1. Semantic similarity
    2. Query entity matching
    """

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=CANDIDATE_K,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    ids = results["ids"][0]

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]


    query_entities = extract_query_entities(
        query
    )


    scored_results = []


    for (
        chunk_id,
        document,
        metadata,
        distance
    ) in zip(
        ids,
        documents,
        metadatas,
        distances
    ):

        # Same semantic score calculation
        # used in your Week 9 implementation.
        semantic_score = 1 / (1 + distance)


        entity_score = 0.0

        matched_entities = []


        chunk_entities = metadata.get(
            "entities",
            ""
        )


        if chunk_entities:

            stored_entities = []


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

                    matched_entities.append(
                        query_entity
                    )


        final_score = (
            semantic_score +
            entity_score
        )


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


    # Highest score first
    scored_results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )


    return scored_results[:k]


# ============================================================
# Prompt
# ============================================================

SYSTEM_PROMPT = """
You are a question answering assistant.

Answer the question using only the provided context.

Rules:
1. Use only the information in the context.
2. Do not use outside knowledge.
3. Do not guess or make up facts.
4. If the answer is not in the context, say "I don't know."
5. If the question is unrelated to the context, say "I don't know."
6. Return the answer together with the context numbers that support it.
"""


def build_prompt(question, chunks):
    """
    Build the Week 7 RAG prompt using the
    entity-aware retrieved chunks.
    """

    context = ""


    for i, chunk in enumerate(
        chunks,
        start=1
    ):

        context += (
            f"\n[Context {i}]\n"
        )

        context += chunk

        context += "\n"


    prompt = f"""
Here is the information retrieved from the knowledge base:

{context}

User question:

{question}

Answer the question using only the information above.

If the information is not enough to answer the question,
say "I don't know."

If the question is unrelated to the context,
also say "I don't know."

Return the result in this format:

{{
    "answer": "your answer",
    "sources": ["Context 1"],
    "supported": true
}}

If you cannot answer:

{{
    "answer": "I don't know.",
    "sources": [],
    "supported": false
}}
"""

    return prompt


# ============================================================
# OpenRouter
# ============================================================

def generate_answer(
    system_prompt,
    user_prompt
):
    """
    Send a request to OpenRouter.
    """

    if not OPENROUTER_API_KEY:

        raise RuntimeError(
            "OpenRouter API key is missing."
        )


    import requests


    headers = {
        "Authorization": (
            f"Bearer {OPENROUTER_API_KEY}"
        ),
        "Content-Type": "application/json"
    }


    data = {
        "model": LLM_MODEL,

        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        "temperature": 0
    }


    try:

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=data,
            timeout=REQUEST_TIMEOUT
        )


        if response.status_code != 200:

            raise RuntimeError(
                "OpenRouter returned "
                f"status code {response.status_code}"
            )


        result = response.json()


        if "choices" not in result:

            raise RuntimeError(
                "Unexpected response from OpenRouter."
            )


        if not result["choices"]:

            raise RuntimeError(
                "OpenRouter returned no answer."
            )


        answer = (
            result["choices"][0]
            ["message"]
            .get("content")
        )


        if not answer:

            raise RuntimeError(
                "No answer was returned."
            )


        return answer.strip()


    except requests.exceptions.Timeout:

        raise RuntimeError(
            "OpenRouter request timed out."
        )


    except requests.exceptions.ConnectionError:

        raise RuntimeError(
            "Could not connect to OpenRouter."
        )


    except requests.exceptions.RequestException as error:

        raise RuntimeError(
            f"API request failed: {error}"
        )


# ============================================================
# Hallucination detection
# ============================================================

def check_hallucination(
    answer,
    chunks
):
    """
    Check whether the generated answer is supported
    by the retrieved context.

    This follows the Week 7 hallucination-checking logic.
    """

    if (
        answer.strip().lower()
        == "i don't know."
    ):

        return False


    context = "\n".join(
        chunks
    )


    if not context.strip():

        return False


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


    result = generate_answer(
        checker_system_prompt,
        checker_prompt
    )


    try:

        parsed = json.loads(
            result
        )


        return parsed.get(
            "supported",
            False
        )


    except json.JSONDecodeError:

        return False


# ============================================================
# Complete RAG pipeline
# ============================================================

def answer_question(question):
    """
    Run the complete Week 10 RAG pipeline.

    Week 9:
        Entity-aware retrieval

    Week 7:
        OpenRouter generation
        Structured answer
        Hallucination detection
    """

    total_start = time.perf_counter()


    # --------------------------------------------------------
    # Retrieval
    # --------------------------------------------------------

    retrieval_start = time.perf_counter()


    retrieved_results = retrieve_chunks(
        question
    )


    retrieval_time = (
        time.perf_counter()
        - retrieval_start
    )


    if not retrieved_results:

        total_time = (
            time.perf_counter()
            - total_start
        )


        return {
            "answer": "I don't know.",
            "sources": [],
            "supported": False,
            "retrieved_chunks": [],
            "retrieval_time": retrieval_time,
            "generation_time": 0.0,
            "total_time": total_time
        }


    # Extract only document text for LLM
    documents = [
        result["document"]
        for result in retrieved_results
    ]


    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    user_prompt = build_prompt(
        question,
        documents
    )


    # --------------------------------------------------------
    # Generation
    # --------------------------------------------------------

    generation_start = time.perf_counter()


    response = generate_answer(
        SYSTEM_PROMPT,
        user_prompt
    )


    generation_time = (
        time.perf_counter()
        - generation_start
    )


    # --------------------------------------------------------
    # Parse LLM JSON
    # --------------------------------------------------------

    try:

        result = json.loads(
            response
        )


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

        answer = "I don't know."

        sources = []

        supported = False


    # --------------------------------------------------------
    # Hallucination check
    # --------------------------------------------------------

    if supported:

        supported = check_hallucination(
            answer,
            documents
        )


    # --------------------------------------------------------
    # Reject unsupported answer
    # --------------------------------------------------------

    if not supported:

        answer = "I don't know."

        sources = []


    # --------------------------------------------------------
    # Total latency
    # --------------------------------------------------------

    total_time = (
        time.perf_counter()
        - total_start
    )


    return {
        "answer": answer,
        "sources": sources,
        "supported": supported,
        "retrieved_chunks": retrieved_results,
        "retrieval_time": retrieval_time,
        "generation_time": generation_time,
        "total_time": total_time
    }


# ============================================================
# System metadata
# ============================================================

def get_system_metadata():
    """
    Return metadata about the current RAG system.
    """

    return {
        "collection": COLLECTION_NAME,
        "document_count": collection.count(),
        "embedding_model": MODEL_NAME,
        "retrieval_type": (
            "Semantic retrieval with "
            "entity-aware reranking"
        ),
        "top_k": TOP_K,
        "candidate_k": CANDIDATE_K,
        "entity_boost": ENTITY_BOOST,
        "ner_model": "en_core_web_sm",
        "llm_model": LLM_MODEL
    }


def check_system_health():
    """
    Check whether the main RAG components are available.
    """

    try:

        count = collection.count()

        if count <= 0:

            return False

        if embedding_model is None:

            return False

        if nlp is None:

            return False

        return True

    except Exception:

        return False