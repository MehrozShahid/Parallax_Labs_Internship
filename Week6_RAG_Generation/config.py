import os
from dotenv import load_dotenv


# Load API key from .env
load_dotenv()


# ChromaDB settings
CHROMA_PATH = "../Week5_Retrieval_Evaluation/chroma_db"
COLLECTION_NAME = "ag_news"


# Embedding model
MODEL_NAME = "all-MiniLM-L6-v2"


# Number of chunks to retrieve
TOP_K = 5


# OpenRouter settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

LLM_MODEL = "openrouter/free"


# API timeout
REQUEST_TIMEOUT = 30


# Log file
LOG_FILE = "logs/rag.log"