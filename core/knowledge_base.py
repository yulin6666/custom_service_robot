"""
Knowledge base RAG system
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from .config import vector_store, KNOWLEDGE_BASE_PATH, TOP_K_RESULTS


class KnowledgeBase:
    """Knowledge base management class"""

    def __init__(self):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", "!", "?", ";", ",", " "]
        )
        self.initialized = False

    def load_knowledge_base(self, file_path: str = KNOWLEDGE_BASE_PATH):
        """Load knowledge base file"""
        try:
            # Clear old vector store data (important! avoids interference from stale data)
            # Since InMemoryVectorStore has no clear method, we need to recreate the instance
            from .config import embeddings
            from langchain_core.vectorstores import InMemoryVectorStore
            self.vector_store = InMemoryVectorStore(embeddings)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split documents
            chunks = self.text_splitter.split_text(content)

            # Create Document objects
            documents = [
                Document(page_content=chunk, metadata={"source": file_path})
                for chunk in chunks
            ]

            # Add to vector store
            self.vector_store.add_documents(documents)
            self.initialized = True

            print(f"Knowledge base loaded successfully. Total {len(documents)} document chunks.")
            print(f"Knowledge base file: {file_path}")
            return True

        except Exception as e:
            print(f"Failed to load knowledge base: {e}")
            return False

    def search(self, query: str, k: int = TOP_K_RESULTS) -> List[Document]:
        """Search for relevant documents"""
        if not self.initialized:
            print("Warning: Knowledge base not initialized")
            return []

        try:
            print(f"\n{'='*60}")
            print(f"[RAG Retrieval] Starting retrieval")
            print(f"[RAG Retrieval] Query: {query}")
            print(f"[RAG Retrieval] Retrieving Top-{k} results")

            results = self.vector_store.similarity_search(query, k=k)

            print(f"[RAG Retrieval] Found {len(results)} relevant documents")
            if results:
                for i, doc in enumerate(results, 1):
                    preview = doc.page_content[:100].replace('\n', ' ')
                    print(f"[RAG Retrieval] Document {i}: {preview}...")
            else:
                print("[RAG Retrieval] No relevant documents found")
            print(f"{'='*60}\n")

            return results
        except Exception as e:
            print(f"Search failed: {e}")
            return []

    def search_with_score(self, query: str, k: int = TOP_K_RESULTS):
        """Search for relevant documents and return similarity scores"""
        if not self.initialized:
            print("Warning: Knowledge base not initialized")
            return []

        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            print(f"Search failed: {e}")
            return []


# Create global knowledge base instance
knowledge_base = KnowledgeBase()
