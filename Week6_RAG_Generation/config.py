import os
from dotenv import load_dotenv


# Load the API key and other settings from the .env file
load_dotenv()


# ChromaDB settings from Week 5
CHROMA_PATH = "../Week5_Retrieval_Evaluation/chroma_db"
COLLECTION_NAME = "ag_news"


# Same embedding model we used in Week 5
MODEL_NAME = "all-MiniLM-L6-v2"


# Retrieve the top 5 chunks because this worked well in Week 5
TOP_K = 5


# OpenRouter settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# DeepSeek model available through OpenRouter
LLM_MODEL = "openrouter/free"


# Don't wait forever if the API doesn't respond
REQUEST_TIMEOUT = 30


# File where we will save query and latency information
LOG_FILE = "logs/rag.log"