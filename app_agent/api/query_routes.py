from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from loguru import logger
from langchain_core.runnables import Runnable

from app_agent.deps import get_agent, get_current_user
from app_agent.services.agent_service import run_agent, stream_agent

router = APIRouter(tags=["Agent"])

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str
    session_id: str

@router.post("/chat", response_model=ChatResponse, summary="与AI助手聊天")
async def chat_with_agent(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    agent: Runnable = Depends(get_agent)
):
    """
    与AI助手进行非流式聊天对话
    """
    try:
        # 生成会话ID（如果未提供）
        session_id = request.session_id or f"session_{hash(request.message) % 10000}"
        
        logger.info(f"💬 非流式聊天请求 [Session: {session_id}]: {request.message}")
        
        # 调用Agent服务
        response = await run_agent(agent, request.message, session_id)
        
        return ChatResponse(
            response=response,
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"❌ 聊天请求处理失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"处理聊天请求时出错: {str(e)}"
        )

@router.post("/chat/stream", summary="与AI助手进行流式聊天")
async def stream_chat_with_agent(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    agent: Runnable = Depends(get_agent)
):
    """
    与AI助手进行流式聊天对话（Server-Sent Events）
    """
    try:
        # 生成会话ID（如果未提供）
        session_id = request.session_id or f"session_{hash(request.message) % 10000}"
        
        logger.info(f"🌊 流式聊天请求 [Session: {session_id}]: {request.message}")
        
        # 创建流式响应
        async def event_stream():
            try:
                async for event in stream_agent(agent, request.message, session_id):
                    yield event
            except Exception as e:
                logger.error(f"❌ 流式聊天处理失败: {e}")
                yield f"data: {{\"type\": \"error\", \"content\": \"处理流式响应时出错: {str(e)}\"}}\n\n"
            finally:
                yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            }
        )
        
    except Exception as e:
        logger.error(f"❌ 流式聊天请求处理失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"处理流式聊天请求时出错: {str(e)}"
        )

@router.get("/sessions/{session_id}/history", summary="获取会话历史")
async def get_chat_history(session_id: str):
    """
    获取特定会话的聊天历史（需要实现会话存储）
    """
    # TODO: 实现会话历史存储和检索
    return {
        "session_id": session_id,
        "history": [],
        "message": "会话历史功能待实现"
    }
