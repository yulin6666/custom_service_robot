"""
测试向量相似度
"""
from core.config import embeddings

# 测试问题
questions = [
    "如何申请年假？",
    "如何报销差旅费？",
    "如何采购物品？"
]

# 知识库片段
docs = [
    "问：如何申请年假？答：年假申请流程...",
    "问：如何报销差旅费？答：差旅费报销流程...",
    "问：如何发起采购申请？答：采购申请流程..."
]

print("=" * 60)
print("测试Embedding模型对中文的理解")
print("=" * 60)

# 生成embeddings
question_embeddings = embeddings.embed_documents(questions)
doc_embeddings = embeddings.embed_documents(docs)

# 计算相似度 (余弦相似度)
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("\n相似度矩阵（行=问题，列=文档）：")
print("           年假    差旅费   采购")
for i, q in enumerate(questions):
    print(f"\n{q}")
    similarities = []
    for j, d in enumerate(doc_embeddings):
        sim = cosine_similarity(question_embeddings[i], d)
        similarities.append(sim)

    for j, sim in enumerate(similarities):
        doc_name = ["年假", "差旅费", "采购"][j]
        print(f"  与{doc_name}: {sim:.4f} {'✅' if sim > 0.7 else '❌'}")

    # 最相似的文档
    max_idx = np.argmax(similarities)
    print(f"  → 最匹配: {['年假', '差旅费', '采购'][max_idx]} (相似度: {similarities[max_idx]:.4f})")

print("\n" + "=" * 60)
print("结论：")
print("如果'如何报销差旅费'没有匹配到'差旅费'文档，")
print("说明英文embedding模型对中文的语义理解不够好。")
print("=" * 60)
