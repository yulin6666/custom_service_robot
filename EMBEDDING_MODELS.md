# Embedding Model Selection Guide

## Problem description

Original configuration used `sentence-transformers/all-mpnet-base-v2` The English model does not understand Chinese semantics well enough, resulting in"How to claim travel expenses"Unable to correctly match related documents.

## Recommended Chinese Embedding Model

### Option 1: BAAI/bge-base-zh-v1.5 （recommend)✅

**advantage:**
- Specifically optimized for Chinese
- Good effect and high accuracy
- The model is of medium size (approximately 400MB)

**Configuration:**
```python
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-zh-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

### Option 2: paraphrase-multilingual-MiniLM-L12-v2

**advantage:**
- Support multiple languages ​​(including Chinese)
- The model is smaller (about 470MB)
- fast

**Configuration:**
```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

### Option 3: BAAI/bge-large-zh-v1.5

**advantage:**
- highest accuracy
- Professional scene recommendation

**shortcoming:**
- The model is larger (approximately 1.3GB）
- slower

**Configuration:**
```python
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-zh-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

## How to switch models

edit `core/config.py` file, modify line 35 `model_name` parameter:

```python
embeddings = HuggingFaceEmbeddings(
    model_name="Model name of your choice",  # Change here
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

Then restart the API service.

## Model download acceleration

If HuggingFace is slow to download, you can use mirroring:

```bash
# Set environment variables
export HF_ENDPOINT=https://hf-mirror.com

# Then start the service
python api.py
```

Or configure it in code:

```python
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
```

## Test model effect

Run the test script:

```bash
python test_embedding.py
```

This script will test the similarity between different questions and documents to help you verify the model effect.

## Performance comparison

| Model | size | Chinese accuracy | speed | Recommended scenarios |
|------|------|-----------|------|---------|
| bge-base-zh-v1.5 | 400MB | ⭐⭐⭐⭐⭐ | quick | General recommendation |
| bge-large-zh-v1.5 | 1.3GB | ⭐⭐⭐⭐⭐ | middle | Professional scene |
| paraphrase-multilingual | 470MB | ⭐⭐⭐⭐ | quick | Multi-language support |
| all-mpnet-base-v2 | 420MB | ⭐⭐ | quick | Only suitable for English |

## FAQ

### Q: Why"How to claim travel expenses"Can't find relevant documentation?

A: The reason is English embedding The model's semantic understanding of Chinese is not accurate enough. It can be solved after switching to Chinese model.

### Q: Do I need to reprocess the knowledge base after switching models?

A: unnecessary. The knowledge base will automatically be re-vectorized using the new model when the service is restarted.

### Q: How to verify whether the model is valid?

A: Query after restart"How to claim travel expenses?"，Retrieval logs should show matches to financial reimbursement related documents, not procurement documents.
