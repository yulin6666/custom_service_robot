"""
配置文件
"""
import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

# ===== 项目根目录 =====
PROJECT_ROOT = Path(__file__).parent.parent

# ===== LLM配置（支持环境变量）=====
openai_api_key = os.getenv("OPENAI_API_KEY", "sk-c62c4cde8fe747faa4d919780339295f")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
model_name = os.getenv("LLM_MODEL", "deepseek-chat")

# 创建LLM实例
llm = ChatOpenAI(
    model=model_name,
    temperature=0,
    timeout=30,  # 增加超时时间适应云环境
    max_tokens=1000,
    openai_api_key=openai_api_key,
    base_url=base_url
)

# ===== Embedding模型配置 =====
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# ===== Vector Store配置 =====
vector_store = InMemoryVectorStore(embeddings)

# ===== 系统配置 =====
# 使用相对路径，支持云部署
KNOWLEDGE_BASE_PATH = os.getenv(
    "KNOWLEDGE_BASE_PATH",
    str(PROJECT_ROOT / "customer_service_kb.txt")
)
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))  # 知识库检索返回结果数
INTENT_CONFIDENCE_THRESHOLD = float(os.getenv("INTENT_CONFIDENCE_THRESHOLD", "0.6"))  # 意图识别置信度阈值
