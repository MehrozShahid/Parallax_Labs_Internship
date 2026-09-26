import time

from fastapi import (
    FastAPI,
    HTTPException
)

from app.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION
)

from app.logger import log_request

from app.rag import (
    answer_question,
    get_system_metadata,
    check_system_health
)

from app.schemas import (
    QueryRequest,
    QueryResponse,
    HealthResponse,
    MetadataResponse
)


# ============================================================
# FastAPI application
# ============================================================

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)


# ============================================================
# Root endpoint
# ============================================================

@app.get(
    "/",
    tags=["System"]
)
def root():

    return {
        "message": "Week 10 RAG API is running.",
        "docs": "/docs"
    }


# ============================================================
# Health endpoint
# ============================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"]
)
def health_check():

    healthy = check_system_health()


    if not healthy:

        raise HTTPException(
            status_code=500,
            detail="RAG system is not healthy."
        )


    return {
        "status": "healthy",
        "service": "Week 10 RAG API",
        "rag_system": "ready",
        "chromadb": "connected"
    }


# ============================================================
# Metadata endpoint
# ============================================================

@app.get(
    "/metadata",
    response_model=MetadataResponse,
    tags=["System"]
)
def metadata():

    try:

        return get_system_metadata()

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail="Could not fetch system metadata."
        ) from error


# ============================================================
# Query endpoint
# ============================================================

@app.post(
    "/query",
    response_model=QueryResponse,
    tags=["RAG"]
)
def query_rag(
    request: QueryRequest
):

    start_time = time.perf_counter()


    query = request.query.strip()


    # --------------------------------------------------------
    # 400 - Bad Request
    # --------------------------------------------------------

    if not query:

        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )


    try:

        # ----------------------------------------------------
        # Run complete RAG pipeline
        # ----------------------------------------------------

        result = answer_question(
            query
        )


        latency_ms = (
            time.perf_counter()
            - start_time
        ) * 1000


        # ----------------------------------------------------
        # Prepare chunks for structured logging
        # ----------------------------------------------------

        retrieved_chunks = []

        for chunk in result[
            "retrieved_chunks"
        ]:

            retrieved_chunks.append(
                {
                    "id": chunk["id"],
                    "document": chunk["document"],
                    "metadata": chunk["metadata"],
                    "semantic_score": round(
                        chunk["semantic_score"],
                        4
                    ),
                    "entity_score": round(
                        chunk["entity_score"],
                        4
                    ),
                    "final_score": round(
                        chunk["final_score"],
                        4
                    ),
                    "matched_entities": chunk[
                        "matched_entities"
                    ]
                }
            )


        # ----------------------------------------------------
        # Structured success log
        # ----------------------------------------------------

        log_request(
            query=query,
            retrieved_chunks=retrieved_chunks,
            answer=result["answer"],
            latency_ms=latency_ms,
            status="success"
        )


        # ----------------------------------------------------
        # Return API response
        # ----------------------------------------------------

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "supported": result["supported"],
            "retrieved_chunks": retrieved_chunks,
            "retrieval_time": result[
                "retrieval_time"
            ],
            "generation_time": result[
                "generation_time"
            ],
            "total_time": result[
                "total_time"
            ],
            "latency_ms": latency_ms
        }


    except HTTPException:

        raise


    except Exception as error:

        latency_ms = (
            time.perf_counter()
            - start_time
        ) * 1000


        # Log failed request
        log_request(
            query=query,
            retrieved_chunks=[],
            answer="",
            latency_ms=latency_ms,
            status="error",
            error=str(error)
        )


        # ----------------------------------------------------
        # 500 - Internal Server Error
        # ----------------------------------------------------

        raise HTTPException(
            status_code=500,
            detail="Internal RAG processing error."
        ) from error