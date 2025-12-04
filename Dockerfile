# 使用官方 Python 镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # HuggingFace 模型缓存目录
    TRANSFORMERS_CACHE=/app/.cache/huggingface \
    HF_HOME=/app/.cache/huggingface \
    # 默认端口
    PORT=8080 \
    # 使用国内镜像加速（可选）
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    # 预下载 embedding 模型以加快启动速度
    python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p /app/.cache/huggingface

# 创建非 root 用户（Railway 可能需要 root，所以这部分可选）
# RUN useradd -m -u 1000 appuser && \
#     chown -R appuser:appuser /app
# USER appuser

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 启动命令 - 直接使用 8080 端口
CMD uvicorn api:app --host 0.0.0.0 --port 8080
