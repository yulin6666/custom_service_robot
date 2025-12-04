# Railway 部署指南

本文档介绍如何将智能客服机器人部署到 Railway 平台。

## 前置准备

1. **注册 Railway 账号**
   - 访问 [Railway.app](https://railway.app)
   - 使用 GitHub 账号登录（推荐）

2. **准备 API Key**
   - DeepSeek API Key（或其他 OpenAI 兼容的 API）
   - 确保 API Key 有足够的额度

## 部署步骤

### 方式一：从 GitHub 仓库部署（推荐）

#### 1. 推送代码到 GitHub

```bash
# 初始化 Git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit for Railway deployment"

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 推送到 GitHub
git push -u origin main
```

#### 2. 在 Railway 上部署

1. 登录 [Railway Dashboard](https://railway.app/dashboard)
2. 点击 **"New Project"**
3. 选择 **"Deploy from GitHub repo"**
4. 选择你的仓库
5. Railway 会自动检测 `Dockerfile` 并开始构建

#### 3. 配置环境变量

在 Railway 项目的 **Variables** 标签页中添加以下环境变量：

```bash
# 必需配置
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat

# 可选配置
TOP_K_RESULTS=3
INTENT_CONFIDENCE_THRESHOLD=0.6
```

#### 4. 部署完成

- Railway 会自动分配一个公网域名，如：`https://your-app.railway.app`
- 首次部署可能需要 5-10 分钟（需要下载 embedding 模型）

---

### 方式二：使用 Railway CLI 部署

#### 1. 安装 Railway CLI

```bash
# macOS/Linux
curl -fsSL https://railway.app/install.sh | sh

# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex
```

#### 2. 登录 Railway

```bash
railway login
```

#### 3. 初始化项目

```bash
# 在项目目录下
railway init

# 选择 "Create a new project"
```

#### 4. 设置环境变量

```bash
railway variables set OPENAI_API_KEY=sk-your-api-key-here
railway variables set OPENAI_BASE_URL=https://api.deepseek.com/v1
railway variables set LLM_MODEL=deepseek-chat
```

#### 5. 部署

```bash
railway up
```

---

## 验证部署

### 1. 检查健康状态

```bash
curl https://your-app.railway.app/health
```

期望响应：
```json
{
  "status": "healthy",
  "message": "服务运行正常"
}
```

### 2. 测试对话接口

```bash
curl -X POST https://your-app.railway.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好"
  }'
```

### 3. 查看 API 文档

访问：`https://your-app.railway.app/docs`

### 4. 查看状态图

访问：`https://your-app.railway.app/api/v1/graph`

---

## 监控和日志

### 查看实时日志

在 Railway Dashboard 中：
1. 进入你的项目
2. 点击 **Deployments** 标签
3. 选择最新的部署
4. 查看 **Logs** 实时输出

### 使用 CLI 查看日志

```bash
railway logs
```

---

## 自定义域名

### 1. 在 Railway 添加自定义域名

1. 进入项目 → **Settings** → **Domains**
2. 点击 **"Add Custom Domain"**
3. 输入你的域名（如 `api.yourdomain.com`）

### 2. 配置 DNS

在你的域名服务商添加 CNAME 记录：

```
Type: CNAME
Name: api (或你的子域名)
Value: your-app.railway.app
```

### 3. 等待 SSL 证书生成

Railway 会自动为你的自定义域名生成 SSL 证书（Let's Encrypt）。

---

## 性能优化

### 1. 增加内存

如果遇到 OOM（内存不足）错误：

1. 进入项目 → **Settings** → **Resources**
2. 增加 Memory 限制到 2GB 或更高

### 2. 使用 Railway 的持久化存储

如果需要持久化数据：

```bash
railway volume create --name data --mount-path /app/data
```

### 3. 优化模型加载

embedding 模型首次加载较慢，已在 Dockerfile 中预下载：

```dockerfile
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"
```

---

## 常见问题

### 1. 构建失败

**问题**：`ERROR: failed to solve: process "/bin/sh -c python -c ..."`

**解决**：可能是网络问题导致模型下载失败。

**临时方案**：注释掉 Dockerfile 中的模型预下载行，让模型在首次运行时下载。

```dockerfile
# 注释这一行
# python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"
```

### 2. 启动超时

**问题**：服务启动超过 Railway 的超时限制。

**解决**：
- 增加 `start_period` 在 HEALTHCHECK 中（已设置为 60s）
- 确保模型已在构建时预下载

### 3. API Key 报错

**问题**：`AuthenticationError: Invalid API key`

**解决**：
1. 检查环境变量 `OPENAI_API_KEY` 是否正确设置
2. 确保 API Key 有效且有余额
3. 在 Railway Dashboard 中重新检查环境变量

### 4. 内存不足

**问题**：`Killed` 或 OOM 错误

**解决**：
- 升级 Railway 计划以获取更多内存
- 或使用更小的 embedding 模型：
  ```bash
  railway variables set EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
  ```

---

## 成本估算

Railway 定价（2024）：

- **Hobby Plan（免费）**：
  - $5 免费额度/月
  - 适合测试和小规模使用

- **Pro Plan**：
  - $20/月
  - 包含 $20 使用额度
  - 超出按量付费

预估成本：
- CPU：约 $0.01/小时
- 内存：约 $0.01/GB/小时
- 网络：前 100GB 免费

**示例**：
- 1GB 内存，24/7 运行：~$7/月
- 加上 API 调用费用（DeepSeek）：~$10-20/月

---

## 自动部署（CI/CD）

Railway 支持自动部署：

1. **监听 GitHub Push**：
   - 每次推送到 main 分支自动部署
   - 在 Railway 项目设置中启用

2. **使用 GitHub Actions**：

创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Railway CLI
        run: npm install -g @railway/cli
      - name: Deploy to Railway
        run: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## 安全建议

1. **不要在代码中硬编码 API Key**
   - 使用环境变量
   - `.env.example` 仅作为模板

2. **定期轮换 API Key**
   - 在 Railway Variables 中更新
   - 重启服务生效

3. **限制访问**
   - 考虑添加 API Key 认证
   - 使用 Railway 的 IP 白名单功能（Pro Plan）

4. **监控使用情况**
   - 定期检查 Railway 和 API 提供商的使用统计
   - 设置预算告警

---

## 技术支持

- **Railway 文档**：https://docs.railway.app
- **Railway Discord**：https://discord.gg/railway
- **项目 Issues**：提交到你的 GitHub 仓库

---

## 快速命令参考

```bash
# 查看服务状态
railway status

# 查看日志
railway logs

# 查看环境变量
railway variables

# 设置环境变量
railway variables set KEY=VALUE

# 重新部署
railway up

# 打开项目仪表板
railway open
```

---

## 总结

恭喜！你已经成功将智能客服机器人部署到 Railway。

**下一步**：
- 配置自定义域名
- 添加监控和告警
- 优化性能和成本
- 集成到你的应用中

有问题欢迎查看文档或提交 Issue！
