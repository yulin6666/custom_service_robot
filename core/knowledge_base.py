"""
知识库RAG系统
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from .config import vector_store, KNOWLEDGE_BASE_PATH, TOP_K_RESULTS


class KnowledgeBase:
    """知识库管理类"""

    def __init__(self):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " "]
        )
        self.initialized = False

    def load_knowledge_base(self, file_path: str = KNOWLEDGE_BASE_PATH):
        """加载知识库文件"""
        try:
            # 清空旧的向量存储数据（重要！避免旧数据干扰）
            # 由于InMemoryVectorStore没有clear方法，我们需要重新创建实例
            from .config import embeddings
            from langchain_core.vectorstores import InMemoryVectorStore
            self.vector_store = InMemoryVectorStore(embeddings)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 分割文档
            chunks = self.text_splitter.split_text(content)

            # 创建Document对象
            documents = [
                Document(page_content=chunk, metadata={"source": file_path})
                for chunk in chunks
            ]

            # 添加到向量存储
            self.vector_store.add_documents(documents)
            self.initialized = True

            print(f"✅ 成功加载知识库，共 {len(documents)} 个文档块")
            print(f"📄 知识库文件: {file_path}")
            return True

        except Exception as e:
            print(f"❌ 加载知识库失败: {e}")
            return False

    def search(self, query: str, k: int = TOP_K_RESULTS) -> List[Document]:
        """搜索相关文档"""
        if not self.initialized:
            print("警告: 知识库未初始化")
            return []

        try:
            print(f"\n{'='*60}")
            print(f"[RAG检索] 开始检索")
            print(f"[RAG检索] 查询: {query}")
            print(f"[RAG检索] 检索Top-{k}结果")

            results = self.vector_store.similarity_search(query, k=k)

            print(f"[RAG检索] 找到 {len(results)} 个相关文档")
            if results:
                for i, doc in enumerate(results, 1):
                    preview = doc.page_content[:100].replace('\n', ' ')
                    print(f"[RAG检索] 文档{i}: {preview}...")
            else:
                print(f"[RAG检索] 未找到相关文档")
            print(f"{'='*60}\n")

            return results
        except Exception as e:
            print(f"搜索失败: {e}")
            return []

    def search_with_score(self, query: str, k: int = TOP_K_RESULTS):
        """搜索相关文档并返回相似度分数"""
        if not self.initialized:
            print("警告: 知识库未初始化")
            return []

        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            print(f"搜索失败: {e}")
            return []


# 创建全局知识库实例
knowledge_base = KnowledgeBase()
