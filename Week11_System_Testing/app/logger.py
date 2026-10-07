import os
import logging

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# ============================================================
# ChromaDB settings
# ============================================================

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    r"C:\Users\HP\Week4_Vector_Database\chroma_db"
)

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "ag_news"
)


# ============================================================
# Embedding model
# ============================================================

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "all-MiniLM-L6-v2"
)


# ============================================================
# Retrieval settings
# ============================================================

TOP_K = 5
CANDIDATE_K = 30
ENTITY_BOOST = 0.20


# ============================================================
# OpenRouter settings
# ============================================================

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)

LLM_MODEL = "openrouter/free"
REQUEST_TIMEOUT = 30


# ============================================================
# API settings
# ============================================================

API_TITLE = "Week 10 RAG API"

API_DESCRIPTION = (
    "FastAPI service wrapping the Week 9 "
    "entity-aware RAG system."
)

API_VERSION = "1.0.0"


# ============================================================
# Logging
# ============================================================

LOG_FILE = "logs/api.log"

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# RAG request logging
# ============================================================

def log_request(
    query: str,
    retrieved_chunks: list,
    answer: str,
    latency_ms: float,
    status: str,
    error: str = None
):
    """
    Log details of a RAG API request.
    """

    log_data = {
        "query": query,
        "retrieved_chunks": retrieved_chunks,
        "answer": answer,
        "latency_ms": round(latency_ms, 2),
        "status": status
    }

    if error:
        log_data["error"] = error

    logger.info(
        "RAG Request: %s",
        log_data
    )