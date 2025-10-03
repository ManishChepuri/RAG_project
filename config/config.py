# Read API keys from .env, chunk sizes, model settings
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the APIs
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

# Search Configuration
TOP_K_RESULTS = 3
EMBEDDING_MODEL = "voyage-3-large"
CLAUDE_MODEL = "claude-3-sonnet-20240229"

# File Paths
DOCUMENTS_DIR = "documents"
CHUNKS_DIR = "data/chunks"
EMBEDDINGS_DIR = "data/embeddings"
INDEXES_DIR = "data/indexes"
