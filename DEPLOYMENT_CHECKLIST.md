# Railway Deployment checklist

After deploying to Railway Before doing so, make sure you complete the following checks:

## ✅ Code preparation

- [ ] All code has been submitted to Git storehouse
- [ ] `.gitignore` Configured, does not contain sensitive information
- [ ] `customer_service_kb.txt` Knowledge base file exists
- [ ] all Python The dependency is already there `requirements.txt` Statement in

## ✅ Configuration file

- [ ] `Dockerfile` exists and is available
- [ ] `railway.json` Configured correctly
- [ ] `.dockerignore` Created
- [ ] `.env.example` Provides environment variable templates

## ✅ API Key preparation

- [ ] Obtained OpenAI compatible API Key（like DeepSeek）
- [ ] API Key Have enough balance
- [ ] Recorded API Base URL

## ✅ local test

- [ ] local Docker Build successful
  ```bash
  docker build -t customer-service-bot .
  ```

- [ ] local Docker Running normally
  ```bash
  docker run -p 8000:8000 -e OPENAI_API_KEY=your-key customer-service-bot
  ```

- [ ] Health check passed
  ```bash
  curl http://localhost:8000/health
  ```

- [ ] API Test passed
  ```bash
  python test_api.py
  ```

## ✅ Railway account

- [ ] Registered Railway account
- [ ] Connected GitHub Account number (if from GitHub deploy)
- [ ] learn Railway Pricing and free credits

## ✅ Deployment configuration

- [ ] ready for deployment Git branch (usually `main`）
- [ ] Confirmed project does not contain large files (< 500MB）
- [ ] Environment variable configuration has been planned

## ✅ Environment variable list

Required settings:
```bash
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

Optional settings:
```bash
TOP_K_RESULTS=3
INTENT_CONFIDENCE_THRESHOLD=0.6
```

## ✅ Post-deployment verification

- [ ] The service started successfully (see Railway log)
- [ ] The health check endpoint is accessible
  ```bash
  curl https://your-app.railway.app/health
  ```

- [ ] API Documentation is accessible
  ```
  https://your-app.railway.app/docs
  ```

- [ ] Session created successfully
  ```bash
  curl -X POST https://your-app.railway.app/api/v1/sessions \
    -H "Content-Type: application/json" \
    -d '{"user_id": "test"}'
  ```

- [ ] Conversations function normally
  ```bash
  curl -X POST https://your-app.railway.app/api/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello"}'
  ```

- [ ] The state diagram is accessible
  ```
  https://your-app.railway.app/api/v1/graph
  ```

## ✅ Monitor and maintain

- [ ] set up Railway build notification
- [ ] Check logs and errors regularly
- [ ] monitor API Usage and cost
- [ ] Back up important configurations and data

## ✅ security check

- [ ] API Key Only configured through environment variables, not hard-coded
- [ ] `.env` File added to `.gitignore`
- [ ] Consider as API Add certification (if needed)
- [ ] Regular replacement API Key

## ✅ document

- [ ] `README_RAILWAY.md` updated
- [ ] `RAILWAY_DEPLOY.md` Detailed steps provided
- [ ] `API_README.md` provided API Instructions for use

## 🚀 Ready to deploy!

When all checks are completed, you can start deployment:

### Method 1: Pass GitHub
1. push code to GitHub
2. exist Railway Select warehouse deployment
3. Configure environment variables
4. Wait for the build to complete

### Method 2: Use CLI
```bash
railway login
railway init
railway up
```

---

## 🆘 Having a problem?

- Check [RAILWAY_DEPLOY.md](./RAILWAY_DEPLOY.md) in"FAQ"chapter
- examine Railway Log search error message
- exist GitHub Issues Ask a question
- access Railway Discord Community

---

**Good luck with the deployment!** 🎉
