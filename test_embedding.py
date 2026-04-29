"""
Test vector similarity
"""
from core.config import embeddings

# Test questions
questions = [
    "How to apply for annual leave?",
    "How to reimburse travel expenses?",
    "How to purchase items?"
]

# Knowledge base snippets
docs = [
    "Q: How to apply for annual leave? A: Annual leave application process...",
    "Q: How to reimburse travel expenses? A: Travel expense reimbursement process...",
    "Q: How to initiate a purchase request? A: Purchase request process..."
]

print("=" * 60)
print("Testing Embedding Model's Understanding of Chinese")
print("=" * 60)

# Generate embeddings
question_embeddings = embeddings.embed_documents(questions)
doc_embeddings = embeddings.embed_documents(docs)

# Calculate similarity (cosine similarity)
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("\nSimilarity Matrix (rows=questions, columns=documents):")
print("           Leave    Travel   Purchase")
for i, q in enumerate(questions):
    print(f"\n{q}")
    similarities = []
    for j, d in enumerate(doc_embeddings):
        sim = cosine_similarity(question_embeddings[i], d)
        similarities.append(sim)

    for j, sim in enumerate(similarities):
        doc_name = ["Leave", "Travel", "Purchase"][j]
        print(f"  vs {doc_name}: {sim:.4f} {'✅' if sim > 0.7 else '❌'}")

    # Most similar document
    max_idx = np.argmax(similarities)
    print(f"  → Best match: {['Leave', 'Travel', 'Purchase'][max_idx]} (similarity: {similarities[max_idx]:.4f})")

print("\n" + "=" * 60)
print("Conclusion:")
print("If 'How to reimburse travel expenses' doesn't match the 'Travel' document,")
print("it means the English embedding model doesn't understand Chinese semantics well.")
print("=" * 60)
