import logging
import time

from fastapi import FastAPI, HTTPException

from app.config import (
    API_TITLE,
    API_VERSION,
)

from app.logger import log_request

from app.rag import (
    answer_question,
    check_system_health,
    get_system_metadata,
)

from app.schemas import QueryRequest


# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# FastAPI application
# ============================================================

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
)


# ============================================================
# Root endpoint
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Working RAG API",
        "version": API_VERSION,
    }


# ============================================================
# Health endpoint
# ============================================================

@app.get("/health")
def health():
    try:
        health_status = check_system_health()

        return {
            "status": "healthy",
            "details": health_status,
        }

    except Exception as e:
        logger.exception("Health check failed")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# Metadata endpoint
# ============================================================

@app.get("/metadata")
def metadata():
    try:
        return get_system_metadata()

    except Exception as e:
        logger.exception("Metadata retrieval failed")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# Query endpoint
# ============================================================

@app.post("/query")
def query(request: QueryRequest):

    start_time = time.perf_counter()

    try:

        logger.info(
            "Received query: %s",
            request.query,
        )

        # ----------------------------------------------------
        # Run RAG pipeline
        # ----------------------------------------------------

        result = answer_question(request.query)

        # ----------------------------------------------------
        # Calculate latency
        # ----------------------------------------------------

        latency_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        logger.info(
            "Query completed successfully | latency=%.2f ms",
            latency_ms,
        )

        # ----------------------------------------------------
        # Log request
        # ----------------------------------------------------

        try:
            log_request(
                query=request.query,
                latency_ms=latency_ms,
            )
        except Exception:
            logger.exception("Request logging failed")

        # ----------------------------------------------------
        # Return RAG result
        # ----------------------------------------------------

        if isinstance(result, dict):

            response = dict(result)

            # Add latency if it is not already returned
            if "latency_ms" not in response:
                response["latency_ms"] = latency_ms

            return response

        return {
            "answer": str(result),
            "latency_ms": latency_ms,
        }

    except Exception as e:

        # IMPORTANT:
        # logger.exception() prints the complete traceback
        # in the Uvicorn terminal.
        logger.exception(
            "RAG processing error"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )