"""
FastAPI REST API service
"""
import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

from core.main import EnterpriseQueryBot


# Request models
class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., description="User input message", min_length=1)
    session_id: Optional[str] = Field(None, description="Session ID; if empty, a new session will be created")


class SessionRequest(BaseModel):
    """Create session request model"""
    user_id: Optional[str] = Field(None, description="User ID; if empty, one will be auto-generated")


# Response models
class ChatResponse(BaseModel):
    """Chat response model"""
    response: str = Field(..., description="Bot reply")
    session_id: str = Field(..., description="Session ID")
    logs: List[str] = Field(..., description="Execution logs showing LangGraph runtime flow")
    status: str = Field(..., description="Status: success or error")
    error: Optional[str] = Field(None, description="Error message (if any)")


class SessionResponse(BaseModel):
    """Session response model"""
    session_id: str = Field(..., description="Session ID")
    user_id: str = Field(..., description="User ID")
    message: str = Field(..., description="Prompt message")


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Prompt message")


# Global variable storing bot instance
bot: Optional[EnterpriseQueryBot] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Initialize bot on startup
    global bot
    print("Initializing internal enterprise query assistant...")
    bot = EnterpriseQueryBot()

    # Generate state graph PNG
    print("Generating state graph...")
    bot.save_graph_to_png("customer_service_graph.png")
    print("State graph generated")

    yield

    # Clean up resources on shutdown
    print("Shutting down internal enterprise query assistant...")


# Create FastAPI application
app = FastAPI(
    title="Internal Enterprise Query Assistant API",
    description="REST API service for internal enterprise query assistant based on LangGraph",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; in production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (including OPTIONS)
    allow_headers=["*"],  # Allow all request headers
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root path, returns API info"""
    return {
        "status": "running",
        "message": "Internal enterprise query assistant API service is running"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if bot is None:
        raise HTTPException(status_code=503, detail="Bot has not been initialized yet")

    return {
        "status": "healthy",
        "message": "Service is running normally"
    }


@app.post("/api/v1/sessions", response_model=SessionResponse)
async def create_session(request: SessionRequest):
    """
    Create a new session

    Args:
        request: Session request, optionally containing user_id

    Returns:
        Session information including session_id and user_id
    """
    if bot is None:
        raise HTTPException(status_code=503, detail="Bot has not been initialized yet")

    try:
        session_id = bot.create_session(user_id=request.user_id)
        session = bot.sessions[session_id]

        return {
            "session_id": session_id,
            "user_id": session["user_id"],
            "message": "Session created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Internal enterprise query

    Args:
        request: Chat request including message and optional session ID

    Returns:
        Bot reply with full execution logs
    """
    if bot is None:
        raise HTTPException(status_code=503, detail="Bot has not been initialized yet")

    try:
        # Call bot and capture logs
        result = bot.chat(
            user_input=request.message,
            session_id=request.session_id,
            capture_logs=True
        )

        return result

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": error_trace
            }
        )


@app.get("/api/v1/graph")
async def get_graph():
    """
    Get state graph PNG image

    Returns:
        PNG image file
    """
    graph_path = "customer_service_graph.png"

    if not os.path.exists(graph_path):
        raise HTTPException(status_code=404, detail="State graph file does not exist")

    return FileResponse(
        graph_path,
        media_type="image/png",
        filename="customer_service_graph.png"
    )


@app.get("/api/v1/sessions/{session_id}")
async def get_session(session_id: str):
    """
    Get session information

    Args:
        session_id: Session ID

    Returns:
        Session information
    """
    if bot is None:
        raise HTTPException(status_code=503, detail="Bot has not been initialized yet")

    if session_id not in bot.sessions:
        raise HTTPException(status_code=404, detail="Session does not exist")

    session = bot.sessions[session_id]

    return {
        "session_id": session_id,
        "user_id": session["user_id"],
        "message_count": len(session["messages"])
    }


@app.get("/api/v1/knowledge-base")
async def get_knowledge_base():
    """
    Get knowledge base content

    Returns:
        Full content of the knowledge base file
    """
    from core.config import KNOWLEDGE_BASE_PATH

    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        raise HTTPException(status_code=404, detail="Knowledge base file does not exist")

    try:
        with open(KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "content": content,
            "file_path": KNOWLEDGE_BASE_PATH,
            "message": "Knowledge base retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read knowledge base: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    # Support PORT environment variable for Railway and other PaaS platforms
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
