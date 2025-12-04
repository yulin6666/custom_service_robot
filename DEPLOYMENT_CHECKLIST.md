# Railway 部署检查清单

在部署到 Railway 之前，请确保完成以下检查：

## ✅ 代码准备

- [ ] 所有代码已提交到 Git 仓库
- [ ] `.gitignore` 已配置，不包含敏感信息
- [ ] `customer_service_kb.txt` 知识库文件存在
- [ ] 所有 Python 依赖已在 `requirements.txt` 中声明

## ✅ 配置文件

- [ ] `Dockerfile` 存在且可用
- [ ] `railway.json` 配置正确
- [ ] `.dockerignore` 已创建
- [ ] `.env.example` 提供了环境变量模板

## ✅ API 密钥准备

- [ ] 已获取 OpenAI 兼容的 API Key（如 DeepSeek）
- [ ] API Key 有足够的余额
- [ ] 已记录 API Base URL

## ✅ 本地测试

- [ ] 本地 Docker 构建成功
  ```bash
  docker build -t customer-service-bot .
  ```

- [ ] 本地 Docker 运行正常
  ```bash
  docker run -p 8000:8000 -e OPENAI_API_KEY=your-key customer-service-bot
  ```

- [ ] 健康检查通过
  ```bash
  curl http://localhost:8000/health
  ```

- [ ] API 测试通过
  ```bash
  python test_api.py
  ```

## ✅ Railway 账号

- [ ] 已注册 Railway 账号
- [ ] 已连接 GitHub 账号（如果从 GitHub 部署）
- [ ] 了解 Railway 的定价和免费额度

## ✅ 部署配置

- [ ] 已准备好要部署的 Git 分支（通常是 `main`）
- [ ] 已确认项目不包含大文件（< 500MB）
- [ ] 已规划好环境变量配置

## ✅ 环境变量清单

必需设置：
```bash
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

可选设置：
```bash
TOP_K_RESULTS=3
INTENT_CONFIDENCE_THRESHOLD=0.6
```

## ✅ 部署后验证

- [ ] 服务启动成功（查看 Railway 日志）
- [ ] 健康检查端点可访问
  ```bash
  curl https://your-app.railway.app/health
  ```

- [ ] API 文档可访问
  ```
  https://your-app.railway.app/docs
  ```

- [ ] 创建会话成功
  ```bash
  curl -X POST https://your-app.railway.app/api/v1/sessions \
    -H "Content-Type: application/json" \
    -d '{"user_id": "test"}'
  ```

- [ ] 对话功能正常
  ```bash
  curl -X POST https://your-app.railway.app/api/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "你好"}'
  ```

- [ ] 状态图可访问
  ```
  https://your-app.railway.app/api/v1/graph
  ```

## ✅ 监控和维护

- [ ] 设置 Railway 的构建通知
- [ ] 定期查看日志和错误
- [ ] 监控 API 使用量和成本
- [ ] 备份重要配置和数据

## ✅ 安全检查

- [ ] API Key 只通过环境变量配置，未硬编码
- [ ] `.env` 文件已添加到 `.gitignore`
- [ ] 考虑为 API 添加认证（如果需要）
- [ ] 定期更换 API Key

## ✅ 文档

- [ ] `README_RAILWAY.md` 已更新
- [ ] `RAILWAY_DEPLOY.md` 提供了详细步骤
- [ ] `API_README.md` 提供了 API 使用说明

## 🚀 准备部署！

当所有检查项都完成后，你就可以开始部署了：

### 方式一：通过 GitHub
1. 推送代码到 GitHub
2. 在 Railway 选择仓库部署
3. 配置环境变量
4. 等待构建完成

### 方式二：使用 CLI
```bash
railway login
railway init
railway up
```

---

## 🆘 遇到问题？

- 查看 [RAILWAY_DEPLOY.md](./RAILWAY_DEPLOY.md) 中的"常见问题"章节
- 检查 Railway 日志查找错误信息
- 在 GitHub Issues 提问
- 访问 Railway Discord 社区

---

**祝部署顺利！** 🎉
