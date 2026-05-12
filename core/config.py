"""
Configuration file
"""
import os
from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
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
# Using DeepSeek embedding API (OpenAI-compatible), no local PyTorch needed
embeddings = OpenAIEmbeddings(
    model="text-embedding-v3",
    openai_api_key=openai_api_key,
    openai_api_base=base_url,
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
