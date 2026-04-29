# Enterprise Internal Query Assistant - LangGraph Version

A LangGraph-based enterprise internal query assistant that helps employees quickly look up information on administration, human resources, IT, legal, finance, procurement, and other internal enterprise topics. Supports intelligent intent recognition, knowledge base retrieval (RAG), multi-turn conversations, and other core features.

**Now supports REST API and Web interface!**

## Features

- Smart intent recognition (automatically identifies query types: administration, HR, IT, legal, finance, procurement, etc.)
- Knowledge base retrieval (RAG) - vector search-based enterprise knowledge base
- Six module support:
  - Administration (office supplies, meeting rooms, shuttle bus, badges, etc.)
  - Human Resources (annual leave, salary, social insurance, training, resignation, etc.)
  - IT Office (OA system, software permissions, computer issues, VPN, etc.)
  - Legal Compliance (contract review, NDAs, intellectual property, etc.)
  - Finance & Reimbursement (travel expenses, daily reimbursement, invoices, petty cash, etc.)
  - Procurement Management (purchase requests, suppliers, acceptance process, etc.)
- Multi-turn conversation management (session context retention)
- State machine workflow control (LangGraph)
- REST API interface (FastAPI)
- Web frontend interface (Next.js + React)
- Complete execution log output (visualized LangGraph workflow)
- Docker containerized deployment

## Project Structure

```
service_robot/
├── custom_service_robot/          # Backend service
│   ├── core/                      # Core modules
│   │   ├── config.py             # Configuration (LLM, embeddings, vector store)
│   │   ├── models.py             # State definitions
│   │   ├── knowledge_base.py     # Knowledge base RAG system
│   │   ├── tools.py              # Tool functions (employee info, department info queries)
│   │   ├── nodes.py              # LangGraph node definitions
│   │   ├── graph.py              # LangGraph state graph
│   │   └── main.py               # Main entry point
│   ├── customer_service_kb.txt   # Enterprise knowledge base file
│   ├── api.py                    # REST API service
│   ├── requirements.txt          # Python dependencies
│   └── run.py                    # Command-line startup script
│
└── custom_service_robot_web/      # Frontend interface
    ├── app/                       # Next.js application
    │   ├── components/            # React components
    │   │   └── ChatInterface.js  # Chat interface component
    │   ├── layout.js             # Layout
    │   └── page.js               # Home page
    ├── package.json              # Node.js dependencies
    └── next.config.js            # Next.js configuration
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (frontend only)
- DeepSeek API Key (or other OpenAI-compatible LLM API)

### Option 1: Using the Web Interface (Recommended)

#### 1. Start the backend service

```bash
cd custom_service_robot

# Install Python dependencies
pip install -r requirements.txt

# Configure API key (edit core/config.py)
# Change openai_api_key to your actual API key

# Start API service
python api.py
# Service will start at http://localhost:8000
```

#### 2. Start the frontend interface

```bash
cd custom_service_robot_web

# Install Node.js dependencies
npm install

# Configure backend API address (if needed)
# Create .env.local file:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
# Frontend will start at http://localhost:3000
```

#### 3. Access the system

Open your browser and visit `http://localhost:3000` to use the enterprise internal query assistant!

### Option 2: Command-line interaction

```bash
cd custom_service_robot

# Install dependencies
pip install -r requirements.txt

# Run the bot
python run.py
```

Example conversation:
```
You: Hello
Assistant: Hello! I am the enterprise internal query assistant, happy to help you!

I can help you look up:
- Administration: office supplies, meeting rooms, shuttle bus, badges, etc.
- Human Resources: annual leave, salary, social insurance, training, resignation, etc.
- IT Office: OA system, software permissions, computer issues, VPN, etc.
...

You: How do I apply for annual leave?
Assistant: [Returns annual leave application process details]

You: exit  # Exit
```

### Option 3: Direct API calls

```bash
# Test API
python test_api.py

# Or use curl
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I apply for annual leave?"}'
```

Visit API documentation: `http://localhost:8000/docs`

## Core Configuration

### 1. Configure LLM API (Required)

Edit `core/config.py` and set your API key:

```python
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    openai_api_key="sk-your-api-key-here",  # Change to your API key
    base_url="https://api.deepseek.com/v1"
)
```

Supported LLMs:
- DeepSeek (recommended, cost-effective)
- OpenAI GPT-4
- Other OpenAI-compatible APIs

### 2. Update the enterprise knowledge base

Edit the `customer_service_kb.txt` file according to your company's actual situation:

```
Enterprise Internal Query Knowledge Base - Employee FAQ

===================
I. Administration
===================

Q: How to apply for office supplies?
A: Office supply application process is as follows...

Q: How to book a meeting room?
A: There are two ways to book a meeting room...
```

Knowledge base supported domains:
- Administration (office supplies, meeting rooms, shuttle bus, courier, etc.)
- Human Resources (annual leave, salary, social insurance, training, resignation, etc.)
- IT Office (OA password, software permissions, computer issues, VPN, etc.)
- Legal Compliance (contract review, NDAs, intellectual property, etc.)
- Finance & Reimbursement (travel expenses, daily reimbursement, invoices, petty cash, etc.)
- Procurement Management (purchase requests, suppliers, acceptance process, etc.)

### 3. Adjust retrieval parameters (Optional)

In `core/config.py`:

```python
TOP_K_RESULTS = 3  # Number of RAG retrieval results
INTENT_CONFIDENCE_THRESHOLD = 0.6  # Intent recognition confidence threshold
```

## System Architecture

### LangGraph Workflow

```
Employee question
   ↓
Intent recognition (identify query type: admin/HR/IT/legal/finance/procurement)
   ↓
Route dispatch
   ├→ Greeting → Return welcome message
   ├→ Enterprise query → Knowledge base retrieval (RAG) → Response generation → Return answer
   ├→ Chitchat → Friendly reply
   └→ Transfer to human → Return department contact info
```

### Supported Intent Types

| Intent Type | Description | Example Questions |
|---------|------|---------|
| `greeting` | Greeting | Hello, are you there |
| `admin_inquiry` | Administration inquiry | How to book a meeting room? Shuttle bus schedule? |
| `hr_inquiry` | HR inquiry | How to apply for annual leave? When is payday? |
| `it_inquiry` | IT inquiry | Forgot OA password? How to connect VPN? |
| `legal_inquiry` | Legal compliance inquiry | How to apply for contract review? NDA content? |
| `finance_inquiry` | Finance reimbursement inquiry | How to reimburse travel expenses? How to verify invoices? |
| `procurement_inquiry` | Procurement inquiry | How to initiate a purchase request? Acceptance process? |
| `general_inquiry` | General query | Enterprise information queries that cannot be clearly categorized |
| `chitchat` | Chitchat | Weather, jokes, and other non-business topics |
| `transfer_human` | Transfer to human | Transfer to human, contact HR, contact admin |

### Tool Functions

The system provides the following tool functions (extensible):

- `query_employee_info(employee_id, name)` - Query employee information
- `query_department_info(department_name)` - Query department information

You can add more tools in `core/tools.py` as needed.

## REST API Endpoints

| Method | Endpoint | Description |
|-----|------|-----|
| GET | `/` | API status check |
| GET | `/health` | Health check |
| POST | `/api/v1/sessions` | Create new session |
| POST | `/api/v1/chat` | Send message and get reply (with execution logs) |
| GET | `/api/v1/graph` | Get state graph PNG |
| GET | `/api/v1/sessions/{session_id}` | Query session information |
| GET | `/docs` | Swagger API documentation |

### API Request Examples

**Create session:**
```bash
curl -X POST "http://localhost:8000/api/v1/sessions" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "employee_001"}'
```

**Send message:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I apply for annual leave?",
    "session_id": "your-session-id"
  }'
```

**Response example:**
```json
{
  "response": "Annual leave application process:\n1. Log in to OA system 'Leave Management' module\n2. Select 'Annual Leave' type...",
  "logs": [
    "[Node] Entering intent recognition node",
    "[Node] Recognized intent: hr_inquiry (confidence: 0.95)",
    "[Router] Routing to knowledge_retrieval",
    "[RAG Retrieval] Found 3 relevant documents",
    "[Response Generation] Response generated successfully"
  ],
  "session_id": "uuid-xxx",
  "status": "success"
}
```

## Using as a Module

```python
from core.main import EnterpriseQueryBot

# Create assistant instance
bot = EnterpriseQueryBot()

# Single query
response = bot.chat("How do I apply for annual leave?")
print(response)

# Continuous conversation (maintain session context)
session_id = bot.create_session(user_id="employee_001")
response1 = bot.chat("How do I apply for annual leave?", session_id)
response2 = bot.chat("How many days in advance do I need to apply?", session_id)  # Context linked

# Get execution logs
result = bot.chat("How do I book a meeting room?", capture_logs=True)
print(result["response"])
print(result["logs"])
```

## Docker Deployment

### Backend service

```bash
cd custom_service_robot

# Build image
docker build -t enterprise-query-bot .

# Run container
docker run -p 8000:8000 enterprise-query-bot
```

### Using Docker Compose (Recommended)

```bash
# In project root directory
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

Access:
- Frontend interface: http://localhost:3000
- Backend API: http://localhost:8000
- API documentation: http://localhost:8000/docs

## FAQ

### 1. How to modify knowledge base content?

Edit the `customer_service_kb.txt` file and restart the service for changes to take effect. The knowledge base uses a Q&A format, and the system will automatically vectorize and retrieve it.

### 2. How to connect to an internal enterprise database?

Modify the tool functions in `core/tools.py`, replacing simulated data with real database queries:

```python
def query_employee_info(employee_id: str):
    # Replace with actual database query
    from your_db import get_employee
    return get_employee(employee_id)
```

### 3. How to improve answer accuracy?

- Improve knowledge base content (`customer_service_kb.txt`)
- Adjust RAG retrieval parameters (`TOP_K_RESULTS`)
- Use a more powerful LLM model
- Optimize intent recognition prompts (`intent_prompt` in `nodes.py`)

### 4. How to add new query types?

1. Add relevant knowledge to `customer_service_kb.txt`
2. Add new intent types to intent recognition in `nodes.py`
3. Add routing rules in `router_node`

### 5. Frontend interface shows connection failure?

Check:
- Is the backend service running normally (http://localhost:8000/health)
- Is the frontend environment variable configured correctly (`NEXT_PUBLIC_API_URL`)
- Does the CORS configuration allow the frontend domain

## Tech Stack

**Backend:**
- **LangGraph**: State machine and workflow management
- **LangChain**: LLM interaction and RAG framework
- **FastAPI**: REST API framework
- **DeepSeek**: LLM service
- **HuggingFace**: Embedding model (sentence-transformers)
- **Python 3.10+**

**Frontend:**
- **Next.js 14**: React framework
- **React 18**: UI component library
- **Tailwind CSS**: Styling framework

## Extension Suggestions

The current system is a basic version that can be extended based on enterprise needs:

- [ ] Connect to internal enterprise databases (employee info, department info, etc.)
- [ ] Add user authentication and permission management
- [ ] Implement human transfer queue (integrate with enterprise IM systems)
- [ ] Add conversation history persistence (database storage)
- [ ] Support multimodal (image recognition, voice interaction)
- [ ] Integrate enterprise OA system API (auto-query, auto-submit requests)
- [ ] Add statistical analysis (common questions, department inquiry volume, etc.)
- [ ] Multi-language support
- [ ] Mobile adaptation

## Production Deployment Recommendations

1. **Security**:
   - Add user authentication (JWT, OAuth, etc.)
   - API rate limiting and access control
   - Sensitive information encrypted storage

2. **Performance Optimization**:
   - Use persistent vector database (e.g., Milvus, Pinecone)
   - Add caching layer (Redis)
   - Load balancing and horizontal scaling

3. **Monitoring and Logging**:
   - Integrate APM tools (e.g., Sentry)
   - Log collection and analysis
   - Monitoring and alerting

4. **High Availability**:
   - Multi-instance deployment
   - Database primary-replica replication
   - Regular backups

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License

---

**Contact**

For questions or suggestions, please reach out via:
- Submit a GitHub Issue
- Email: your-email@company.com
