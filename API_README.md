# 智能客服机器人 REST API 文档

基于 LangGraph 的智能客服机器人 REST API 服务，支持完整的执行日志输出。

## 快速开始

### 方式一：使用 Docker Compose（推荐）

```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 方式二：使用 Docker

```bash
# 构建镜像
docker build -t customer-service-bot .

# 运行容器
docker run -d -p 8000:8000 --name customer-service-bot customer-service-bot

# 查看日志
docker logs -f customer-service-bot

# 停止容器
docker stop customer-service-bot
```

### 方式三：本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn api:app --host 0.0.0.0 --port 8000

# 或者直接运行
python api.py
```

## API 端点

### 1. 健康检查

**GET** `/health`

检查服务是否正常运行。

**响应示例：**
```json
{
  "status": "healthy",
  "message": "服务运行正常"
}
```

---

### 2. 创建会话

**POST** `/api/v1/sessions`

创建一个新的对话会话。

**请求体：**
```json
{
  "user_id": "user123"  // 可选，不提供则自动生成
}
```

**响应示例：**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "message": "会话创建成功"
}
```

---

### 3. 对话接口（核心）

**POST** `/api/v1/chat`

与客服机器人对话，**返回完整的 LangGraph 执行日志**。

**请求体：**
```json
{
  "message": "我想查询订单ORD001",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"  // 可选
}
```

**响应示例：**
```json
{
  "response": "您的订单 ORD001 当前状态为：已发货\n预计送达时间：2024-01-15\n物流信息：包裹正在配送中",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "logs": [
    "",
    "[节点] 进入意图识别节点 (intent_recognition_node)",
    "[节点] 用户消息: 我想查询订单ORD001",
    "[节点] 识别意图: order_query (置信度: 0.95)",
    "",
    "[路由] 进入路由节点",
    "[路由] 意图: order_query, 置信度: 0.95",
    "[路由] 决策: 路由到 order_handler",
    "",
    "[节点] 进入响应生成节点 (response_generation_node)",
    "[响应生成] 使用工具调用结果: ['order']",
    "[响应生成] 正在调用LLM生成最终响应...",
    "[响应生成] 响应生成成功"
  ],
  "status": "success"
}
```

---

### 4. 查看状态图

**GET** `/api/v1/graph`

获取 LangGraph 状态图的 PNG 图像。

**响应：** 返回 PNG 图像文件

可以在浏览器中直接访问：`http://localhost:8000/api/v1/graph`

---

### 5. 查询会话信息

**GET** `/api/v1/sessions/{session_id}`

查询指定会话的信息。

**响应示例：**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "message_count": 5
}
```

---

## 使用示例

### Python 示例

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. 创建会话
response = requests.post(f"{BASE_URL}/api/v1/sessions", json={
    "user_id": "test_user"
})
session_data = response.json()
session_id = session_data["session_id"]
print(f"会话创建成功: {session_id}")

# 2. 发送消息并查看执行日志
response = requests.post(f"{BASE_URL}/api/v1/chat", json={
    "message": "你好",
    "session_id": session_id
})

result = response.json()
print(f"\n机器人回复: {result['response']}")
print(f"\n执行日志:")
for log in result['logs']:
    print(log)

# 3. 继续对话
response = requests.post(f"{BASE_URL}/api/v1/chat", json={
    "message": "退货流程是什么？",
    "session_id": session_id
})

result = response.json()
print(f"\n机器人回复: {result['response']}")
```

### cURL 示例

```bash
# 健康检查
curl http://localhost:8000/health

# 创建会话
curl -X POST http://localhost:8000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

# 发送消息
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我想查询订单ORD001",
    "session_id": "your-session-id"
  }'

# 查看状态图
curl http://localhost:8000/api/v1/graph --output graph.png
```

### JavaScript/Node.js 示例

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

async function chatWithBot() {
  // 1. 创建会话
  const sessionResponse = await axios.post(`${BASE_URL}/api/v1/sessions`, {
    user_id: 'test_user'
  });
  const sessionId = sessionResponse.data.session_id;
  console.log(`会话创建成功: ${sessionId}`);

  // 2. 发送消息
  const chatResponse = await axios.post(`${BASE_URL}/api/v1/chat`, {
    message: '你好',
    session_id: sessionId
  });

  console.log(`\n机器人回复: ${chatResponse.data.response}`);
  console.log(`\n执行日志:`);
  chatResponse.data.logs.forEach(log => console.log(log));
}

chatWithBot().catch(console.error);
```

---

## API 文档

启动服务后，可以访问以下地址查看交互式 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 日志说明

每次对话都会返回完整的执行日志，展示 LangGraph 的运行过程：

1. **意图识别节点**: 识别用户意图和置信度
2. **路由节点**: 根据意图决定下一步流程
3. **业务处理节点**: 处理具体业务（订单查询、知识库检索等）
4. **响应生成节点**: 使用 LLM 生成最终回复

这些日志对于：
- 理解机器人的决策过程
- 调试问题
- 优化对话流程

非常有帮助。

---

## 配置说明

### 环境变量

可以通过环境变量配置服务：

```bash
# 示例：通过环境变量配置
export OPENAI_API_KEY="your-api-key"
export BASE_URL="https://api.openai.com/v1"
```

### 修改配置文件

编辑 `core/config.py` 文件来修改：
- LLM 模型配置
- 知识库路径
- 意图识别阈值
- 等其他参数

---

## Docker 管理命令

```bash
# 查看容器状态
docker ps

# 查看容器日志
docker logs -f customer-service-bot

# 进入容器内部
docker exec -it customer-service-bot bash

# 重启容器
docker restart customer-service-bot

# 停止并删除容器
docker stop customer-service-bot
docker rm customer-service-bot

# 删除镜像
docker rmi customer-service-bot
```

---

## 常见问题

### 1. 端口被占用

如果 8000 端口已被占用，可以修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "8080:8000"  # 将主机端口改为 8080
```

### 2. 知识库更新

如果需要更新知识库文件，可以：
- 修改 `customer_service_kb.txt` 文件
- 重启容器：`docker-compose restart`

### 3. 查看详细错误信息

通过日志查看详细错误：
```bash
docker-compose logs -f customer-service-bot
```

---

## 性能优化建议

1. **使用 GPU 加速**：如果有 GPU，可以修改 Dockerfile 使用 GPU 版本的 PyTorch
2. **缓存 Embedding 模型**：首次启动会下载模型，可以挂载缓存目录
3. **调整并发设置**：修改 uvicorn 启动参数增加 workers

---

## 许可证

MIT License
