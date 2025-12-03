"""
配置文件
"""
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

# ===== LLM配置 =====
openai_api_key = "sk-c62c4cde8fe747faa4d919780339295f"
base_url = "https://api.deepseek.com/v1"

# 创建LLM实例
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    timeout=10,
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
KNOWLEDGE_BASE_PATH = "/Users/linofficemac/Documents/AI/custom_service_robot/customer_service_kb.txt"
TOP_K_RESULTS = 3  # 知识库检索返回结果数
INTENT_CONFIDENCE_THRESHOLD = 0.6  # 意图识别置信度阈值
