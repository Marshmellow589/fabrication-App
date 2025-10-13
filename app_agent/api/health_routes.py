from loguru import logger
from fastapi import APIRouter, Depends, status
# from langchain_ollama import ChatOllama  # Temporarily disabled due to dependency issues
from sqlalchemy import text
from sqlite3 import Connection

from app_agent.deps import get_db_connection  # Removed get_llm temporarily
from app_agent.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health", summary="健康检查")
async def health_check(
    db: Connection = Depends(get_db_connection)
):
    """
    检查应用及其依赖的健康状态。
    """
    checks = {}
    
    # 检查Ollama服务 (暂时禁用)
    checks["ollama"] = {"status": "disabled", "message": "Temporarily disabled due to dependency issues"}
    
    # 检查数据库连接
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = {"status": "healthy", "path": settings.sqlite_db_path}
    except Exception as e:
        logger.error(f"数据库健康检查失败: {e}")
        checks["database"] = {"status": "unhealthy", "error": str(e)}
    
    # 确定整体状态
    all_healthy = all(check["status"] in ["healthy", "disabled"] for check in checks.values())
    status_code = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "version": settings.app_version,
        "environment": settings.environment,
        "checks": checks
    }, status_code
