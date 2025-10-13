
from typing import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app_agent.api import health_routes, project_routers, query_routes
from app_agent.core.config import settings
from app_agent.core.exception_handlers import register_exception_handlers
from app_agent.lifespan import lifespan

# 配置日志
logger.add("logs/app.log", rotation="10 MB", retention="10 days", level="INFO")

# 创建FastAPI应用
app = FastAPI(
    title="Data Project AI Agent",
    version=settings.app_version,
    debug=True,
    lifespan=lifespan
)

# 注册全局异常处理器
register_exception_handlers(app)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health_routes.router, prefix="/api/v1", tags=["Health"])
app.include_router(project_routers.router, prefix="/api/v1", tags=["Project"])
app.include_router(query_routes.router, prefix="/api/v1", tags=["Agent"])

@app.get("/")
async def root():
    return {
        "message": "欢迎使用 Data Project AI Agent",
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app_agent.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )
