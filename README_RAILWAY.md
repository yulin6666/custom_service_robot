# 智能客服机器人 - Railway 快速部署

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

## 🚀 一键部署到 Railway

### 步骤 1：点击部署按钮

点击上方的 "Deploy on Railway" 按钮，或访问：
- [Railway Dashboard](https://railway.app/dashboard)

### 步骤 2：配置环境变量

在部署页面设置以下必需的环境变量：

```bash
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

### 步骤 3：等待部署完成

- 首次部署约需 5-10 分钟（下载依赖和模型）
- Railway 会自动分配一个公网 URL

### 步骤 4：验证部署

访问你的 Railway URL：

```bash
# 健康检查
https://your-app.railway.app/health

# API 文档
https://your-app.railway.app/docs

# 状态图
https://your-app.railway.app/api/v1/graph
```

## 📝 测试 API

```bash
# 创建会话
curl -X POST https://your-app.railway.app/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

# 发送消息
curl -X POST customservicerobot-production.up.railway.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "session_id": "your-session-id"
  }'
```

## 🔧 环境变量说明

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | ✅ | - | OpenAI 兼容的 API Key |
| `OPENAI_BASE_URL` | ✅ | - | API Base URL |
| `LLM_MODEL` | ❌ | `deepseek-chat` | 使用的模型名称 |
| `TOP_K_RESULTS` | ❌ | `3` | 知识库检索数量 |
| `INTENT_CONFIDENCE_THRESHOLD` | ❌ | `0.6` | 意图识别阈值 |
| `PORT` | ❌ | 自动分配 | Railway 自动设置 |

## 📊 API 端点

- `GET /health` - 健康检查
- `POST /api/v1/sessions` - 创建会话
- `POST /api/v1/chat` - 对话（返回完整执行日志）
- `GET /api/v1/graph` - 获取状态图
- `GET /api/v1/sessions/{session_id}` - 查询会话

## 📖 完整文档

- [API 使用文档](./API_README.md)
- [Railway 详细部署指南](./RAILWAY_DEPLOY.md)

## 💰 成本估算

- **免费额度**：Railway 提供 $5/月免费额度
- **预估成本**：约 $7-10/月（1GB内存，24/7运行）
- **API 调用**：DeepSeek 约 $0.14/百万tokens

## ⚡ 性能优化

- embedding 模型已在构建时预下载
- 首次启动约 30-60 秒
- 支持并发请求
- 自动缓存模型

## 🐛 常见问题

### 构建失败？
- 检查 Railway 日志
- 可能是模型下载超时，重新触发构建

### API 报错？
- 检查环境变量 `OPENAI_API_KEY` 是否正确
- 确认 API Key 有余额

### 内存不足？
- 升级 Railway 计划
- 或使用更小的 embedding 模型

## 🔗 链接

- [Railway 官网](https://railway.app)
- [Railway 文档](https://docs.railway.app)
- [DeepSeek API](https://platform.deepseek.com)

## 📞 支持

- 提交 Issue 到 GitHub
- 加入 Railway Discord 社区

---

**Enjoy! 🎉**
