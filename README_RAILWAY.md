# Intelligent customer service robot - Railway Rapid deployment

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

## 🚀 One-click deployment to Railway

### step 1：Click the deploy button

Click above "Deploy on Railway" button, or visit:
- [Railway Dashboard](https://railway.app/dashboard)

### step 2：Configure environment variables

Set the following required environment variables on the deployment page:

```bash
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

### step 3：Wait for deployment to complete

- Initial deployment takes approx. 5-10 Minutes (download dependencies and models)
- Railway A public network will be automatically assigned URL

### step 4：Verify deployment

access your Railway URL：

```bash
# health check
https://your-app.railway.app/health

# API document
https://your-app.railway.app/docs

# state diagram
https://your-app.railway.app/api/v1/graph
```

## 📝 test API

```bash
# Create session
curl -X POST https://your-app.railway.app/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

# Send message
curl -X POST customservicerobot-production.up.railway.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "session_id": "your-session-id"
  }'
```

## 🔧 Environment variable description

| variable name | required | default value | illustrate |
|--------|------|--------|------|
| `OPENAI_API_KEY` | ✅ | - | OpenAI compatible API Key |
| `OPENAI_BASE_URL` | ✅ | - | API Base URL |
| `LLM_MODEL` | ❌ | `deepseek-chat` | model name to use |
| `TOP_K_RESULTS` | ❌ | `3` | Number of knowledge base searches |
| `INTENT_CONFIDENCE_THRESHOLD` | ❌ | `0.6` | Intent recognition threshold |
| `PORT` | ❌ | automatic allocation | Railway Automatically set |

## 📊 API endpoint

- `GET /health` - health check
- `POST /api/v1/sessions` - Create session
- `POST /api/v1/chat` - Conversation (returns full execution log)
- `GET /api/v1/graph` - Get state diagram
- `GET /api/v1/sessions/{session_id}` - query session

## 📖 Full documentation

- [API Use documentation](./API_README.md)
- [Railway Detailed deployment guide](./RAILWAY_DEPLOY.md)

## 💰 cost estimate

- **Free quota**：Railway supply $5/Monthly free quota
- **Estimated cost**：about $7-10/Month (1GB RAM, 24/7 operation)
- **API call**：DeepSeek about $0.14/Millions of tokens

## ⚡ Performance optimization

- embedding Models are pre-downloaded at build time
- First launch approx. 30-60 Second
- Support concurrent requests
- Automatic caching of models

## 🐛 FAQ

### Build failed?
- examine Railway log
- It may be that the model download times out and the build is re-triggered.

### API Report an error?
- Check environment variables `OPENAI_API_KEY` Is it correct?
- confirm API Key Have balance

### Not enough memory?
- upgrade Railway plan
- or use smaller embedding Model

## 🔗 Link

- [Railway Official website](https://railway.app)
- [Railway document](https://docs.railway.app)
- [DeepSeek API](https://platform.deepseek.com)

## 📞 support

- submit Issue arrive GitHub
- join in Railway Discord Community

---

**Enjoy! 🎉**
