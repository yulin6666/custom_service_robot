"""
Configuration file
"""
import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

# ===== Project root directory =====
PROJECT_ROOT = Path(__file__).parent.parent

# ===== LLM configuration (supports environment variables) =====
openai_api_key = os.getenv("OPENAI_API_KEY", "sk-c62c4cde8fe747faa4d919780339295f")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
model_name = os.getenv("LLM_MODEL", "deepseek-chat")

# Create LLM instance
llm = ChatOpenAI(
    model=model_name,
    temperature=0,
    timeout=30,  # Increased timeout for cloud environments
    max_tokens=1000,
    openai_api_key=openai_api_key,
    base_url=base_url
)

# ===== Embedding model configuration =====
# Using multilingual embedding model (recommended)
# Option 1: BAAI/bge-base-zh-v1.5 - Chinese optimized, good performance, moderate speed
# Option 2: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 - Multilingual support
# Option 3: sentence-transformers/all-mpnet-base-v2 - English model (original config, poor Chinese performance)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# ===== Vector Store configuration =====
vector_store = InMemoryVectorStore(embeddings)

# ===== System configuration =====
# Using relative paths to support cloud deployment
KNOWLEDGE_BASE_PATH = os.getenv(
    "KNOWLEDGE_BASE_PATH",
    str(PROJECT_ROOT / "customer_service_kb.txt")
)
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))  # Number of knowledge base retrieval results
INTENT_CONFIDENCE_THRESHOLD = float(os.getenv("INTENT_CONFIDENCE_THRESHOLD", "0.6"))  # Intent recognition confidence threshold
