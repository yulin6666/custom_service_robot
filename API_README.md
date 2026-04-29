# Intelligent customer service robot REST API document

based on LangGraph Intelligent customer service robot REST API Service, supports complete execution log output.

## quick start

### Method 1: Use Docker Compose（recommend)

```bash
# Build and start the service
docker-compose up -d

# View log
docker-compose logs -f

# Stop service
docker-compose down
```

### Method 2: Use Docker

```bash
# Build image
docker build -t customer-service-bot .

# Run container
docker run -d -p 8000:8000 --name customer-service-bot customer-service-bot

# View log
docker logs -f customer-service-bot

# Stop container
docker stop customer-service-bot
```

### Method 3: Run locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start service
uvicorn api:app --host 0.0.0.0 --port 8000

# Or run directly
python api.py
```

## API endpoint

### 1. health check

**GET** `/health`

Check whether the service is running properly.

**Response example:**
```json
{
  "status": "healthy",
  "message": "The service is running normally"
}
```

---

### 2. Create session

**POST** `/api/v1/sessions`

Create a new conversation session.

**Request body:**
```json
{
  "user_id": "user123"  // Optional, automatically generated if not provided
}
```

**Response example:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "message": "Session created successfully"
}
```

---

### 3. Conversational interface (core)

**POST** `/api/v1/chat`

Talk to the customer service robot,**return complete LangGraph execution log**。

**Request body:**
```json
{
  "message": "I want to query order ORD001",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"  // Optional
}
```

**Response example:**
```json
{
  "response": "your order ORD001 The current status is: shipped\nEstimated delivery time: 2024-01-15\nLogistics information: The package is being delivered",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "logs": [
    "",
    "[node] Enter the intent recognition node (intent_recognition_node)",
    "[node] User messages: I want to query order ORD001",
    "[node] Identify intent: order_query (Confidence: 0.95)",
    "",
    "[routing] Enter routing node",
    "[routing] intention: order_query, Confidence: 0.95",
    "[routing] decision making: route to order_handler",
    "",
    "[node] Enter the response generation node (response_generation_node)",
    "[response generation] Use tools to call results: ['order']",
    "[response generation] LLM is being called to generate the final response...",
    "[response generation] Response generated successfully"
  ],
  "status": "success"
}
```

---

### 4. View status diagram

**GET** `/api/v1/graph`

get LangGraph state diagram PNG image.

**response:** return PNG image file

Can be accessed directly in the browser:`http://localhost:8000/api/v1/graph`

---

### 5. Query session information

**GET** `/api/v1/sessions/{session_id}`

Query information about a specified session.

**Response example:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "message_count": 5
}
```

---

## Usage example

### Python Example

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Create session
response = requests.post(f"{BASE_URL}/api/v1/sessions", json={
    "user_id": "test_user"
})
session_data = response.json()
session_id = session_data["session_id"]
print(f"Session created successfully: {session_id}")

# 2. Send messages and view execution logs
response = requests.post(f"{BASE_URL}/api/v1/chat", json={
    "message": "Hello",
    "session_id": session_id
})

result = response.json()
print(f"\nRobot reply: {result['response']}")
print(f"\nexecution log:")
for log in result['logs']:
    print(log)

# 3. continue the conversation
response = requests.post(f"{BASE_URL}/api/v1/chat", json={
    "message": "What is the return process?",
    "session_id": session_id
})

result = response.json()
print(f"\nRobot reply: {result['response']}")
```

### cURL Example

```bash
# health check
curl http://localhost:8000/health

# Create session
curl -X POST http://localhost:8000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

# Send message
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to query order ORD001",
    "session_id": "your-session-id"
  }'

# View status diagram
curl http://localhost:8000/api/v1/graph --output graph.png
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

async function chatWithBot() {
  // 1. Create session
  const sessionResponse = await axios.post(`${BASE_URL}/api/v1/sessions`, {
    user_id: 'test_user'
  });
  const sessionId = sessionResponse.data.session_id;
  console.log(`Session created successfully: ${sessionId}`);

  // 2. Send message
  const chatResponse = await axios.post(`${BASE_URL}/api/v1/chat`, {
    message: 'Hello',
    session_id: sessionId
  });

  console.log(`\nRobot reply: ${chatResponse.data.response}`);
  console.log(`\nexecution log:`);
  chatResponse.data.logs.forEach(log => console.log(log));
}

chatWithBot().catch(console.error);
```

---

## API document

After starting the service, you can visit the following address to view the interactive API document:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Log description

Each conversation returns a complete execution log, showing LangGraph The running process:

1. **Intent recognition node**: Identify user intent and confidence
2. **routing node**: Determine the next step based on intention
3. **business processing node**: Handle specific business (order query, knowledge base retrieval, etc.)
4. **Response generation node**: use LLM generate final reply

These logs are for:
- Understand the robot’s decision-making process
- Debugging issues
- Optimize conversation flow

Very helpful.

---

## Configuration instructions

### environment variables

The service can be configured through environment variables:

```bash
# Example: Configuration via environment variables
export OPENAI_API_KEY="your-api-key"
export BASE_URL="https://api.openai.com/v1"
```

### Modify configuration file

edit `core/config.py` file to modify:
- LLM Model configuration
- Knowledge base path
- Intent recognition threshold
- and other parameters

---

## Docker Administrative commands

```bash
# View container status
docker ps

# View container logs
docker logs -f customer-service-bot

# Get inside the container
docker exec -it customer-service-bot bash

# Restart container
docker restart customer-service-bot

# Stop and delete the container
docker stop customer-service-bot
docker rm customer-service-bot

# Delete image
docker rmi customer-service-bot
```

---

## FAQ

### 1. Port is occupied

if 8000 The port is occupied and can be modified. `docker-compose.yml` Port mapping in:

```yaml
ports:
  - "8080:8000"  # Change the host port to 8080
```

### 2. Knowledge base updates

If you need to update the knowledge base files, you can:
- Revise `customer_service_kb.txt` document
- Restart the container:`docker-compose restart`

### 3. View detailed error information

View detailed errors through the log:
```bash
docker-compose logs -f customer-service-bot
```

---

## Performance optimization suggestions

1. **use GPU accelerate**：if there is GPU，Can be modified Dockerfile use GPU version PyTorch
2. **cache Embedding Model**：The model will be downloaded on first startup and the cache directory can be mounted.
3. **Adjust concurrency settings**：Revise uvicorn Startup parameters increased workers

---

## license

MIT License
