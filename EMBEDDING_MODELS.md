# Embedding 模型选择指南

## 问题描述

原始配置使用 `sentence-transformers/all-mpnet-base-v2` 英文模型，对中文语义理解不够好，导致"如何报销差旅费"无法正确匹配到相关文档。

## 推荐的中文 Embedding 模型

### 方案1: BAAI/bge-base-zh-v1.5 （推荐）✅

**优点：**
- 专门针对中文优化
- 效果好，准确度高
- 模型大小适中（约400MB）

**配置：**
```python
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-zh-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

### 方案2: paraphrase-multilingual-MiniLM-L12-v2

**优点：**
- 支持多语言（包括中文）
- 模型较小（约470MB）
- 速度快

**配置：**
```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

### 方案3: BAAI/bge-large-zh-v1.5

**优点：**
- 最高准确度
- 专业场景推荐

**缺点：**
- 模型较大（约1.3GB）
- 速度较慢

**配置：**
```python
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-zh-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

## 如何切换模型

编辑 `core/config.py` 文件，修改第35行的 `model_name` 参数：

```python
embeddings = HuggingFaceEmbeddings(
    model_name="你选择的模型名称",  # 改这里
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

然后重启API服务。

## 模型下载加速

如果HuggingFace下载速度慢，可以使用镜像：

```bash
# 设置环境变量
export HF_ENDPOINT=https://hf-mirror.com

# 然后启动服务
python api.py
```

或者在代码中配置：

```python
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
```

## 测试模型效果

运行测试脚本：

```bash
python test_embedding.py
```

这个脚本会测试不同问题和文档之间的相似度，帮助你验证模型效果。

## 性能对比

| 模型 | 大小 | 中文准确度 | 速度 | 推荐场景 |
|------|------|-----------|------|---------|
| bge-base-zh-v1.5 | 400MB | ⭐⭐⭐⭐⭐ | 快 | 通用推荐 |
| bge-large-zh-v1.5 | 1.3GB | ⭐⭐⭐⭐⭐ | 中 | 专业场景 |
| paraphrase-multilingual | 470MB | ⭐⭐⭐⭐ | 快 | 多语言支持 |
| all-mpnet-base-v2 | 420MB | ⭐⭐ | 快 | 仅适合英文 |

## 常见问题

### Q: 为什么"如何报销差旅费"找不到相关文档？

A: 原因是英文 embedding 模型对中文的语义理解不够准确。切换到中文模型后可以解决。

### Q: 切换模型后需要重新处理知识库吗？

A: 不需要。重启服务时会自动使用新模型重新向量化知识库。

### Q: 如何验证模型是否生效？

A: 重启后查询"如何报销差旅费？"，检索日志应该显示匹配到财务报销相关文档，而不是采购文档。
