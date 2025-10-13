from typing import cast
import sqlite3
import jwt
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from langchain_core.runnables import Runnable

from app_agent.core.config import settings

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

def get_llm(request: Request):
    """
    一个 FastAPI 依赖项，用于从 request.state 中获取 LLM 实例。
    """
    if not hasattr(request.state, "llm"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service is not initialized."
        )
    return request.state.llm

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

# JWT认证相关依赖
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    验证JWT token并获取当前用户
    """
    token = credentials.credentials
    
    try:
        # 从主后端获取用户信息来验证token
        # 这里需要与主后端的JWT配置保持一致
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
