from typing import cast
import sqlite3
from fastapi import Request, HTTPException, status
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama

from app.core.config import settings

def get_agent(request: Request) -> Runnable:
    """
    一个 FastAPI 依赖项。
    它从 lifespan state (request.state) 中获取 Agent 实例。
    """
    if not hasattr(request.state, "agent"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent service is not initialized."
        )
    return cast(Runnable, request.state.agent)

def get_llm(request: Request) -> ChatOllama:
    """
    一个 FastAPI 依赖项，用于从 request.state 中获取 LLM 实例。
    """
    if not hasattr(request.state, "llm"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service is not initialized."
        )
    return cast(ChatOllama, request.state.llm)

def get_db_connection() -> sqlite3.Connection:
    """
    获取SQLite数据库连接
    """
    try:
        conn = sqlite3.connect(settings.sqlite_db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {e}"
        )