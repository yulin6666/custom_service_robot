# 企业内部查询助手 - LangGraph版本

基于LangGraph构建的企业内部查询助手，帮助员工快速查询行政、人力资源、IT办公、法务、财务、采购等企业内部信息。支持智能意图识别、知识库检索（RAG）、多轮对话等核心功能。

**✨ 现已支持 REST API 和 Web 界面！**

## 功能特性

- 🤖 智能意图识别（自动识别行政、人力、IT、法务、财务、采购等查询类型）
- 📚 知识库检索（RAG）- 基于向量搜索的企业知识库
- 💼 六大模块支持：
  - 📋 行政管理（办公用品、会议室、班车、工牌等）
  - 👥 人力资源（年假、工资、社保、培训、离职等）
  - 💻 IT办公（OA系统、软件权限、电脑故障、VPN等）
  - ⚖️ 法务合规（合同审核、保密协议、知识产权等）
  - 💰 财务报销（差旅费、日常报销、发票、备用金等）
  - 🛒 采购管理（采购申请、供应商、验收流程等）
- 💬 多轮对话管理（会话上下文保持）
- 🔄 状态机流程控制（LangGraph）
- 🌐 REST API 接口（FastAPI）
- 🎨 Web 前端界面（Next.js + React）
- 📊 完整执行日志输出（可视化 LangGraph 流程）
- 🐳 Docker 容器化部署

## 项目结构

```
service_robot/
├── custom_service_robot/          # 后端服务
│   ├── core/                      # 核心模块
│   │   ├── config.py             # 配置（LLM、embeddings、vector store）
│   │   ├── models.py             # 状态定义
│   │   ├── knowledge_base.py     # 知识库RAG系统
│   │   ├── tools.py              # 工具函数（员工信息、部门信息查询）
│   │   ├── nodes.py              # LangGraph节点定义
│   │   ├── graph.py              # LangGraph状态图
│   │   └── main.py               # 主入口
│   ├── customer_service_kb.txt   # 企业知识库文件
│   ├── api.py                    # REST API服务
│   ├── requirements.txt          # Python依赖
│   └── run.py                    # 命令行启动脚本
│
└── custom_service_robot_web/      # 前端界面
    ├── app/                       # Next.js应用
    │   ├── components/            # React组件
    │   │   └── ChatInterface.js  # 聊天界面组件
    │   ├── layout.js             # 布局
    │   └── page.js               # 首页
    ├── package.json              # Node.js依赖
    └── next.config.js            # Next.js配置
```

## 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+（仅前端需要）
- DeepSeek API Key（或其他OpenAI兼容的LLM API）

### 方式一：使用 Web 界面（推荐）

#### 1. 启动后端服务

```bash
cd custom_service_robot

# 安装Python依赖
pip install -r requirements.txt

# 配置API密钥（编辑 core/config.py）
# 将 openai_api_key 改为你的实际API密钥

# 启动API服务
python api.py
# 服务将在 http://localhost:8000 启动
```

#### 2. 启动前端界面

```bash
cd custom_service_robot_web

# 安装Node.js依赖
npm install

# 配置后端API地址（如果需要）
# 创建 .env.local 文件：
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 启动开发服务器
npm run dev
# 前端将在 http://localhost:3000 启动
```

#### 3. 访问系统

打开浏览器访问 `http://localhost:3000`，即可使用企业内部查询助手！

### 方式二：命令行交互

```bash
cd custom_service_robot

# 安装依赖
pip install -r requirements.txt

# 运行机器人
python run.py
```

示例对话：
```
您: 你好
助手: 您好！我是企业内部查询助手，很高兴为您服务！

我可以帮您查询：
- 📋 行政管理：办公用品、会议室、班车、工牌等
- 👥 人力资源：年假、工资、社保、培训、离职等
- 💻 IT办公：OA系统、软件权限、电脑故障、VPN等
...

您: 如何申请年假？
助手: [返回年假申请流程详情]

您: exit  # 退出
```

### 方式三：直接调用 API

```bash
# 测试API
python test_api.py

# 或使用curl
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "如何申请年假？"}'
```

访问 API 文档：`http://localhost:8000/docs`

## 核心配置

### 1. 配置 LLM API（必需）

编辑 `core/config.py`，设置你的 API 密钥：

```python
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    openai_api_key="sk-your-api-key-here",  # 改为你的API密钥
    base_url="https://api.deepseek.com/v1"
)
```

支持的LLM：
- DeepSeek（推荐，性价比高）
- OpenAI GPT-4
- 其他OpenAI兼容API

### 2. 更新企业知识库

编辑 `customer_service_kb.txt` 文件，根据你的企业实际情况修改：

```
企业内部查询知识库 - 员工常见问题解答

===================
一、行政管理
===================

问：如何申请办公用品？
答：办公用品申请流程如下...

问：会议室如何预订？
答：会议室预订有两种方式...
```

知识库支持的领域：
- 行政管理（办公用品、会议室、班车、快递等）
- 人力资源（年假、工资、社保、培训、离职等）
- IT办公（OA密码、软件权限、电脑故障、VPN等）
- 法务合规（合同审核、保密协议、知识产权等）
- 财务报销（差旅费、日常报销、发票、备用金等）
- 采购管理（采购申请、供应商、验收流程等）

### 3. 调整检索参数（可选）

在 `core/config.py` 中：

```python
TOP_K_RESULTS = 3  # RAG检索返回结果数
INTENT_CONFIDENCE_THRESHOLD = 0.6  # 意图识别置信度阈值
```

## 系统架构

### LangGraph 工作流程

```
员工提问
   ↓
意图识别（识别查询类型：行政/人力/IT/法务/财务/采购）
   ↓
路由分发
   ├→ 问候 → 返回欢迎语
   ├→ 企业查询 → 知识库检索(RAG) → 响应生成 → 返回答案
   ├→ 闲聊 → 友好回复
   └→ 转人工 → 返回部门联系方式
```

### 支持的意图类型

| 意图类型 | 说明 | 示例问题 |
|---------|------|---------|
| `greeting` | 问候打招呼 | 你好、在吗 |
| `admin_inquiry` | 行政管理咨询 | 如何预订会议室？班车时刻表？ |
| `hr_inquiry` | 人力资源咨询 | 如何申请年假？工资什么时候发？ |
| `it_inquiry` | IT办公咨询 | 忘记OA密码怎么办？如何连接VPN？ |
| `legal_inquiry` | 法务合规咨询 | 如何申请合同审核？保密协议内容？ |
| `finance_inquiry` | 财务报销咨询 | 如何报销差旅费？发票如何查验？ |
| `procurement_inquiry` | 采购管理咨询 | 如何发起采购申请？验收流程？ |
| `general_inquiry` | 通用查询 | 无法明确分类的企业信息查询 |
| `chitchat` | 闲聊 | 天气、笑话等非业务话题 |
| `transfer_human` | 转人工 | 转人工、联系HR、联系行政 |

### 工具函数

系统提供以下工具函数（可扩展）：

- `query_employee_info(employee_id, name)` - 查询员工信息
- `query_department_info(department_name)` - 查询部门信息

可根据需要在 `core/tools.py` 中添加更多工具。

## REST API 端点

| 方法 | 端点 | 说明 |
|-----|------|-----|
| GET | `/` | API状态检查 |
| GET | `/health` | 健康检查 |
| POST | `/api/v1/sessions` | 创建新会话 |
| POST | `/api/v1/chat` | 发送消息并获取回复（含执行日志） |
| GET | `/api/v1/graph` | 获取状态图PNG |
| GET | `/api/v1/sessions/{session_id}` | 查询会话信息 |
| GET | `/docs` | Swagger API文档 |

### API 请求示例

**创建会话：**
```bash
curl -X POST "http://localhost:8000/api/v1/sessions" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "employee_001"}'
```

**发送消息：**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "如何申请年假？",
    "session_id": "your-session-id"
  }'
```

**响应示例：**
```json
{
  "response": "年假申请流程：\n1. 登录OA系统'请假管理'模块\n2. 选择'年假'类型...",
  "logs": [
    "[节点] 进入意图识别节点",
    "[节点] 识别意图: hr_inquiry (置信度: 0.95)",
    "[路由] 路由到 knowledge_retrieval",
    "[RAG检索] 找到 3 个相关文档",
    "[响应生成] 响应生成成功"
  ],
  "session_id": "uuid-xxx",
  "status": "success"
}
```

## 作为模块使用

```python
from core.main import EnterpriseQueryBot

# 创建助手实例
bot = EnterpriseQueryBot()

# 单次查询
response = bot.chat("如何申请年假？")
print(response)

# 持续对话（保持会话上下文）
session_id = bot.create_session(user_id="employee_001")
response1 = bot.chat("如何申请年假？", session_id)
response2 = bot.chat("需要提前几天申请？", session_id)  # 上下文关联

# 获取执行日志
result = bot.chat("如何预订会议室？", capture_logs=True)
print(result["response"])
print(result["logs"])
```

## Docker 部署

### 后端服务

```bash
cd custom_service_robot

# 构建镜像
docker build -t enterprise-query-bot .

# 运行容器
docker run -p 8000:8000 enterprise-query-bot
```

### 使用 Docker Compose（推荐）

```bash
# 在项目根目录
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

访问：
- 前端界面：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

## 常见问题

### 1. 如何修改知识库内容？

编辑 `customer_service_kb.txt` 文件，重启服务即可生效。知识库采用问答格式，系统会自动进行向量化和检索。

### 2. 如何接入企业内部数据库？

在 `core/tools.py` 中修改工具函数，将模拟数据替换为真实数据库查询：

```python
def query_employee_info(employee_id: str):
    # 替换为实际数据库查询
    from your_db import get_employee
    return get_employee(employee_id)
```

### 3. 如何提高回答准确性？

- 完善知识库内容（`customer_service_kb.txt`）
- 调整 RAG 检索参数（`TOP_K_RESULTS`）
- 使用更强大的 LLM 模型
- 优化意图识别提示词（`nodes.py` 中的 `intent_prompt`）

### 4. 如何添加新的查询类型？

1. 在 `customer_service_kb.txt` 添加相关知识
2. 在 `nodes.py` 的意图识别中添加新意图类型
3. 在 `router_node` 中添加路由规则

### 5. 前端界面显示连接失败？

检查：
- 后端服务是否正常运行（http://localhost:8000/health）
- 前端环境变量配置是否正确（`NEXT_PUBLIC_API_URL`）
- CORS 配置是否允许前端域名

## 技术栈

**后端：**
- **LangGraph**: 状态机和工作流管理
- **LangChain**: LLM交互和RAG框架
- **FastAPI**: REST API框架
- **DeepSeek**: LLM服务
- **HuggingFace**: Embedding模型（sentence-transformers）
- **Python 3.10+**

**前端：**
- **Next.js 14**: React框架
- **React 18**: UI组件库
- **Tailwind CSS**: 样式框架

## 扩展功能建议

当前系统是基础版本，可根据企业需求扩展：

- [ ] 接入企业内部数据库（员工信息、部门信息等）
- [ ] 添加用户认证和权限管理
- [ ] 实现人工转接队列（集成企业IM系统）
- [ ] 添加对话历史持久化（数据库存储）
- [ ] 支持多模态（图片识别、语音交互）
- [ ] 集成企业OA系统API（自动查询、自动提交申请）
- [ ] 添加统计分析（常见问题、部门咨询量等）
- [ ] 多语言支持
- [ ] 移动端适配

## 生产环境部署建议

1. **安全性**：
   - 添加用户认证（JWT、OAuth等）
   - API限流和访问控制
   - 敏感信息加密存储

2. **性能优化**：
   - 使用持久化向量数据库（如Milvus、Pinecone）
   - 添加缓存层（Redis）
   - 负载均衡和水平扩展

3. **监控和日志**：
   - 集成APM工具（如Sentry）
   - 日志收集和分析
   - 监控告警机制

4. **高可用性**：
   - 多实例部署
   - 数据库主从复制
   - 定期备份

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## License

MIT License

---

**联系方式**

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 邮件联系：your-email@company.com
