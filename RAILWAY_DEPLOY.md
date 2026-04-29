# Railway Deployment Guide

This document describes how to deploy intelligent customer service robots to Railway platform.

## Preparation

1. **register Railway account**
   - access [Railway.app](https://railway.app)
   - use GitHub Account login (recommended)

2. **Prepare API Key**
   - DeepSeek API Key（or other OpenAI compatible API）
   - make sure API Key Have enough credit

## Deployment steps

### Method 1: From GitHub Warehouse deployment (recommended)

#### 1. push code to GitHub

```bash
# initialization Git Warehouse (if you don't have one yet)
git init

# add all files
git add .

# Submit code
git commit -m "Initial commit for Railway deployment"

# Add remote warehouse
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# push to GitHub
git push -u origin main
```

#### 2. exist Railway Deploy on

1. Log in [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. choose **"Deploy from GitHub repo"**
4. Choose your warehouse
5. Railway Will automatically detect `Dockerfile` and start building

#### 3. Configure environment variables

exist Railway project **Variables** Add the following environment variables to the tab:

```bash
# Required configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat

# Optional configuration
TOP_K_RESULTS=3
INTENT_CONFIDENCE_THRESHOLD=0.6
```

#### 4. Deployment completed

- Railway A public domain name will be automatically assigned, such as:`https://your-app.railway.app`
- First deployment may require 5-10 minutes (requires download embedding Model)

---

### Method 2: Use Railway CLI deploy

#### 1. Install Railway CLI

```bash
# macOS/Linux
curl -fsSL https://railway.app/install.sh | sh

# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex
```

#### 2. Log in Railway

```bash
railway login
```

#### 3. Initialize project

```bash
# in the project directory
railway init

# choose "Create a new project"
```

#### 4. Set environment variables

```bash
railway variables set OPENAI_API_KEY=sk-your-api-key-here
railway variables set OPENAI_BASE_URL=https://api.deepseek.com/v1
railway variables set LLM_MODEL=deepseek-chat
```

#### 5. deploy

```bash
railway up
```

---

## Verify deployment

### 1. Check health status

```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "The service is running normally"
}
```

### 2. Test conversational interface

```bash
curl -X POST https://your-app.railway.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello"
  }'
```

### 3. Check API document

access:`https://your-app.railway.app/docs`

### 4. View status diagram

access:`https://your-app.railway.app/api/v1/graph`

---

## Monitoring and logging

### View real-time logs

exist Railway Dashboard middle:
1. Go to your project
2. Click **Deployments** Label
3. Select the latest deployment
4. Check **Logs** real time output

### use CLI View log

```bash
railway logs
```

---

## Custom domain name

### 1. exist Railway Add custom domain name

1. Enter project → **Settings** → **Domains**
2. Click **"Add Custom Domain"**
3. Enter your domain name (e.g. `api.yourdomain.com`）

### 2. Configuration DNS

Add it to your domain name service provider CNAME Record:

```
Type: CNAME
Name: api (or your subdomain)
Value: your-app.railway.app
```

### 3. wait SSL Certificate generation

Railway Will be automatically generated for your custom domain name SSL Certificate (Let's Encrypt）。

---

## Performance optimization

### 1. Docker BuildKit Cache acceleration (recommended)

Dockerfile Already configured to use BuildKit Cache mounts can significantly speed up builds:

**Enabled when building locally BuildKit**：
```bash
# Method 1: Environment variables
export DOCKER_BUILDKIT=1
docker build -t customer-service-bot .

# Method 2: Use directly docker buildx
docker buildx build -t customer-service-bot .
```

**Optimization effect**：
- ✅ pip Dependency cache: will not be re-downloaded on the second build torch（899.8 MB）Waiting for big package
- ✅ HuggingFace Model cache: embedding The model is only downloaded once
- ✅ Build time: from 5-10 minutes reduced to 30 Seconds or so (when cache hits)

**Railway automatically used BuildKit**：Railway Platform enabled by default BuildKit，No additional configuration is required.

### 2. increase memory

If you encounter OOM（Out of memory) error:

1. Enter project → **Settings** → **Resources**
2. Increase Memory limited to 2GB or higher

### 3. use Railway persistent storage

If you need to persist data:

```bash
railway volume create --name data --mount-path /app/data
```

### 4. Optimize model loading

embedding The model loads slowly for the first time and has been Dockerfile Pre-download and use cache:

```dockerfile
# Use cache mounts to avoid repeated downloads
RUN --mount=type=cache,target=/app/.cache/huggingface \
    python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"
```

---

## FAQ

### 1. Build failed

**question**：`ERROR: failed to solve: process "/bin/sh -c python -c ..."`

**solve**：It may be a network problem that causes the model download to fail.

**temporary solution**：Comment out Dockerfile The model predownload line in has the model downloaded the first time it is run.

```dockerfile
# Comment this line
# python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"
```

### 2. Start timeout

**question**：Service startup exceeds Railway timeout limit.

**solve**：
- Increase `start_period` exist HEALTHCHECK Medium (set to 60s）
- Make sure the model is pre-downloaded at build time

### 3. API Key Report an error

**question**：`AuthenticationError: Invalid API key`

**solve**：
1. Check environment variables `OPENAI_API_KEY` Is it set correctly?
2. make sure API Key Valid and with balance
3. exist Railway Dashboard Recheck environment variables in

### 4. Out of memory

**question**：`Killed` or OOM mistake

**solve**：
- upgrade Railway Plan for more memory
- or use smaller embedding Model:
  ```bash
  railway variables set EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
  ```

---

## cost estimate

Railway Pricing (2024):

- **Hobby Plan（free)**：
  - $5 Free quota/month
  - Suitable for testing and small-scale use

- **Pro Plan**：
  - $20/moon
  - Include $20 Usage quota
  - Pay as you go

Estimated cost:
- CPU：about $0.01/Hour
- Memory: approx. $0.01/GB/Hour
- Network: former 100GB free

**Example**：
- 1GB Memory, 24/7 run:~$7/moon
- plus API Call cost (DeepSeek):~$10-20/moon

---

## Automated deployment (CI/CD)

Railway Support automatic deployment:

1. **monitor GitHub Push**：
   - Push to main Branch automatic deployment
   - exist Railway Enable in project settings

2. **use GitHub Actions**：

create `.github/workflows/deploy.yml`：

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

## Security advice

1. **Don't hardcode it in your code API Key**
   - Use environment variables
   - `.env.example` only as a template

2. **Regular rotation API Key**
   - exist Railway Variables Updating
   - Restarting the service takes effect

3. **Restrict access**
   - Consider adding API Key Certification
   - use Railway of IP Whitelist function (Pro Plan）

4. **Monitor usage**
   - Regular inspection Railway and API Provider usage statistics
   - Set budget alerts

---

## Technical support

- **Railway document**：https://docs.railway.app
- **Railway Discord**：https://discord.gg/railway
- **project Issues**：Submit to your GitHub storehouse

---

## Quick command reference

```bash
# Check service status
railway status

# View log
railway logs

# View environment variables
railway variables

# Set environment variables
railway variables set KEY=VALUE

# Redeploy
railway up

# Open project dashboard
railway open
```

---

## Summarize

Congratulations! You have successfully deployed the intelligent customer service robot to Railway。

**Next step**：
- Configure a custom domain name
- Add monitoring and alarms
- Optimize performance and cost
- Integrate into your app

If you have any questions, please check the document or submit Issue！
