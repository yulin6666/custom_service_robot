"""
Configuration file
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from zai import ZhipuAiClient

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
zhipu_api_key = os.getenv("ZHIPU_API_KEY", "")

class ZhipuEmbeddings(Embeddings):
    """ZhipuAI embedding wrapper compatible with LangChain"""

    def __init__(self, api_key: str, model: str = "embedding-2"):
        self.client = ZhipuAiClient(api_key=api_key)
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        results = []
        batch_size = 64
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embeddings.create(model=self.model, input=batch)
            results.extend([item.embedding for item in response.data])
        return results

    def embed_query(self, text: str) -> List[float]:
        response = self.client.embeddings.create(model=self.model, input=[text])
        return response.data[0].embedding

embeddings = ZhipuEmbeddings(api_key=zhipu_api_key)

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
