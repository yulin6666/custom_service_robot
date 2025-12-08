"""
FastAPI REST API 服务
"""
import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

from core.main import EnterpriseQueryBot


# 请求模型
class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Field(..., description="用户输入的消息", min_length=1)
    session_id: Optional[str] = Field(None, description="会话ID，如果为空则创建新会话")


class SessionRequest(BaseModel):
    """创建会话请求模型"""
    user_id: Optional[str] = Field(None, description="用户ID，如果为空则自动生成")


# 响应模型
class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str = Field(..., description="机器人的回复")
    session_id: str = Field(..., description="会话ID")
    logs: List[str] = Field(..., description="执行日志，展示LangGraph的运行过程")
    status: str = Field(..., description="状态：success 或 error")
    error: Optional[str] = Field(None, description="错误信息（如果有）")


class SessionResponse(BaseModel):
    """会话响应模型"""
    session_id: str = Field(..., description="会话ID")
    user_id: str = Field(..., description="用户ID")
    message: str = Field(..., description="提示信息")


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    message: str = Field(..., description="提示信息")


# 全局变量，存储机器人实例
bot: Optional[EnterpriseQueryBot] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化机器人
    global bot
    print("正在初始化企业内部查询助手...")
    bot = EnterpriseQueryBot()

    # 生成状态图PNG
    print("正在生成状态图...")
    bot.save_graph_to_png("customer_service_graph.png")
    print("状态图已生成")

    yield

    # 关闭时清理资源
    print("正在关闭企业内部查询助手...")


# 创建FastAPI应用
app = FastAPI(
    title="企业内部查询助手 API",
    description="基于 LangGraph 的企业内部查询助手 REST API 服务",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法（包括OPTIONS）
    allow_headers=["*"],  # 允许所有请求头
)


@app.get("/", response_model=HealthResponse)
async def root():
    """根路径，返回API信息"""
    return {
        "status": "running",
        "message": "企业内部查询助手 API 服务正在运行"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    if bot is None:
        raise HTTPException(status_code=503, detail="机器人尚未初始化")

    return {
        "status": "healthy",
        "message": "服务运行正常"
    }


@app.post("/api/v1/sessions", response_model=SessionResponse)
async def create_session(request: SessionRequest):
    """
    创建新会话

    Args:
        request: 会话请求，可选包含 user_id

    Returns:
        会话信息，包含 session_id 和 user_id
    """
    if bot is None:
        raise HTTPException(status_code=503, detail="机器人尚未初始化")

    try:
        session_id = bot.create_session(user_id=request.user_id)
        session = bot.sessions[session_id]

        return {
            "session_id": session_id,
            "user_id": session["user_id"],
            "message": "会话创建成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建会话失败: {str(e)}")


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    企业内部查询

    Args:
        request: 聊天请求，包含消息和可选的会话ID

    Returns:
        机器人的回复，包含完整的执行日志
    """
    if bot is None:
        raise HTTPException(status_code=503, detail="机器人尚未初始化")

    try:
        # 调用机器人，捕获日志
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
    获取状态图PNG图像

    Returns:
        PNG图像文件
    """
    graph_path = "customer_service_graph.png"

    if not os.path.exists(graph_path):
        raise HTTPException(status_code=404, detail="状态图文件不存在")

    return FileResponse(
        graph_path,
        media_type="image/png",
        filename="customer_service_graph.png"
    )


@app.get("/api/v1/sessions/{session_id}")
async def get_session(session_id: str):
    """
    获取会话信息

    Args:
        session_id: 会话ID

    Returns:
        会话信息
    """
    if bot is None:
        raise HTTPException(status_code=503, detail="机器人尚未初始化")

    if session_id not in bot.sessions:
        raise HTTPException(status_code=404, detail="会话不存在")

    session = bot.sessions[session_id]

    return {
        "session_id": session_id,
        "user_id": session["user_id"],
        "message_count": len(session["messages"])
    }


@app.get("/api/v1/knowledge-base")
async def get_knowledge_base():
    """
    获取知识库内容

    Returns:
        知识库文件的完整内容
    """
    from core.config import KNOWLEDGE_BASE_PATH

    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        raise HTTPException(status_code=404, detail="知识库文件不存在")

    try:
        with open(KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "content": content,
            "file_path": KNOWLEDGE_BASE_PATH,
            "message": "知识库获取成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取知识库失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    # 支持 Railway 等 PaaS 平台的 PORT 环境变量
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
