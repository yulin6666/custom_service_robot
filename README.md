# 智能客服机器人 - LangGraph版本

基于LangGraph构建的智能客服机器人，支持意图识别、知识库检索（RAG）、工具调用等核心功能。

**✨ 现已支持 REST API 和 Docker 部署！**

## 功能特性

- 🤖 智能意图识别（问候、咨询、订单、投诉等）
- 📚 知识库检索（RAG）- 基于向量搜索
- 🔧 工具调用（订单查询、支付、退款、物流）
- 💬 多轮对话管理
- 🔄 状态机流程控制（LangGraph）
- 🌐 **REST API 接口**（FastAPI）
- 📊 **完整执行日志输出**（可视化 LangGraph 流程）
- 🐳 **Docker 容器化**
- ☁️ **支持 Railway 一键部署**

## 项目结构

```
custom_service_robot/
├── core/                      # 核心模块
│   ├── __init__.py
│   ├── config.py             # 配置（LLM、embeddings、vector store）
│   ├── models.py             # 状态定义
│   ├── knowledge_base.py     # 知识库RAG系统
│   ├── tools.py              # 模拟工具（订单、支付等）
│   ├── nodes.py              # LangGraph节点定义
│   ├── graph.py              # LangGraph状态图
│   └── main.py               # 主入口
├── customer_service_kb.txt   # 知识库文件
├── requirements.txt          # 依赖包
└── run.py                    # 启动脚本
```

## 快速开始

### 方式一：REST API（推荐）

```bash
# 使用 Docker Compose
docker-compose up -d

# 或使用 Docker
docker build -t customer-service-bot .
docker run -p 8000:8000 customer-service-bot

# 访问 API 文档
open http://localhost:8000/docs
```

测试 API：
```bash
python test_api.py
```

📖 **详细文档**：[API_README.md](./API_README.md)

### 方式二：命令行交互

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行机器人
python run.py
```

示例对话：
```
您: 你好
客服: 您好！我是智能客服助手，很高兴为您服务！...

您: 我想查询订单ORD001
客服: [返回订单信息]

您: exit  # 退出
```

### 方式三：Railway 云部署

🚀 **一键部署到 Railway**：[README_RAILWAY.md](./README_RAILWAY.md)

完整部署指南：[RAILWAY_DEPLOY.md](./RAILWAY_DEPLOY.md)

## 核心组件说明

### 1. LLM配置 (config.py)

使用DeepSeek的OpenAI兼容API：
```python
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    openai_api_key="sk-...",
    base_url="https://api.deepseek.com/v1"
)
```

### 2. Embedding模型

使用HuggingFace的sentence-transformers：
```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
```

### 3. 向量存储

使用LangChain的InMemoryVectorStore（内存向量库）

### 4. 状态图流程

```
用户输入 → 意图识别 → 路由分发 → 处理节点 → 响应生成 → 输出
                                ↓
                          (知识库检索/工具调用)
```

## 支持的意图类型

- `greeting`: 问候
- `inquiry`: 产品/政策咨询
- `order_query`: 订单查询
- `payment`: 支付处理
- `refund`: 退换货
- `logistics`: 物流查询
- `complaint`: 投诉建议
- `transfer_human`: 转人工
- `chitchat`: 闲聊

## 模拟工具

所有工具都是模拟的（不连接真实数据库）：

- `query_order(order_id)`: 查询订单
- `process_payment(order_id, amount)`: 处理支付（返回模拟链接）
- `process_refund(order_id, reason)`: 申请退款
- `query_logistics(tracking_number)`: 查询物流

## 自定义配置

### 修改LLM API密钥

编辑 `core/config.py`:
```python
openai_api_key = "your-api-key"
base_url = "your-api-endpoint"
```

### 更新知识库

编辑 `customer_service_kb.txt` 文件，添加您的业务知识。

### 调整检索参数

在 `core/config.py` 中：
```python
TOP_K_RESULTS = 3  # 检索返回结果数
INTENT_CONFIDENCE_THRESHOLD = 0.6  # 意图置信度阈值
```

## 使用示例

### 作为模块使用

```python
from core import CustomerServiceBot

# 创建机器人实例
bot = CustomerServiceBot()

# 单次对话
response = bot.chat("你好")
print(response)

# 持续对话（保持会话）
session_id = bot.create_session(user_id="user123")
response1 = bot.chat("查询订单ORD001", session_id)
response2 = bot.chat("这个订单什么时候发货？", session_id)
```

## 技术栈

- **LangGraph**: 状态机和工作流管理
- **LangChain**: LLM交互和RAG
- **DeepSeek**: LLM服务
- **HuggingFace**: Embedding模型
- **Python 3.10+**

## REST API 端点

- `GET /health` - 健康检查
- `POST /api/v1/sessions` - 创建会话
- `POST /api/v1/chat` - 对话接口（**包含完整 LangGraph 执行日志**）
- `GET /api/v1/graph` - 获取状态图 PNG
- `GET /api/v1/sessions/{session_id}` - 查询会话信息
- `GET /docs` - Swagger API 文档

### 日志输出示例

```json
{
  "response": "您的订单 ORD001 当前状态为：已发货",
  "logs": [
    "[节点] 进入意图识别节点",
    "[节点] 识别意图: order_query (置信度: 0.95)",
    "[路由] 路由到 order_handler",
    "[响应生成] 正在调用LLM生成最终响应...",
    "[响应生成] 响应生成成功"
  ],
  "session_id": "...",
  "status": "success"
}
```

## 文档索引

- 📖 [API 使用文档](./API_README.md)
- 🚀 [Railway 快速部署](./README_RAILWAY.md)
- 📝 [Railway 详细部署指南](./RAILWAY_DEPLOY.md)
- ✅ [部署检查清单](./DEPLOYMENT_CHECKLIST.md)
- 📋 [部署完成总结](./DEPLOY_SUMMARY.md)

## 后续扩展方向

- [x] ✅ 添加 FastAPI 接口
- [x] ✅ Docker 容器化
- [x] ✅ 添加监控和日志（执行日志完整输出）
- [ ] 接入真实数据库
- [ ] 添加用户认证
- [ ] 实现人工转接队列
- [ ] 添加对话历史持久化
- [ ] 支持多模态（图片、语音）

## License

MIT
