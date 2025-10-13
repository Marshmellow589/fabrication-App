from typing import AsyncIterator, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from langchain_core.runnables import Runnable
import os

from app_agent.agent.project_agent import assemble_project_agent
from app_agent.agent.deepseek_wrapper import DeepSeekWrapper
from app_agent.db.init_project_database import init_project_database
from app_agent.core.config import settings

# 定义应用状态类型
AppState = dict[str, Any]

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[AppState]:
    """
    应用生命周期管理，负责初始化和清理资源
    """
    logger.info("🚀 启动应用生命周期...")
    
    # 1. 初始化项目数据库
    logger.info("📊 初始化项目数据库...")
    init_project_database()
    
    # 2. 初始化DeepSeek LLM - 使用wrapper
    logger.info("🧠 初始化DeepSeek LLM模型")
    
    # 检查DeepSeek API密钥
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        logger.warning("⚠️ DEEPSEEK_API_KEY环境变量未设置，请设置您的DeepSeek API密钥")
        # 创建一个模拟的LLM用于测试
        from langchain_core.language_models import FakeListChatModel
        llm = FakeListChatModel(responses=["这是一个测试响应，请设置DEEPSEEK_API_KEY环境变量来使用真实的DeepSeek API"])
        logger.warning("⚠️ 使用模拟LLM进行测试，请设置DEEPSEEK_API_KEY环境变量")
    else:
        try:
            # Create DeepSeek wrapper for langgraph compatibility
            llm = DeepSeekWrapper(
                model_name="deepseek-chat",
                api_key=deepseek_api_key,
                base_url="https://api.deepseek.com/v1",
                temperature=0.7
            )
            logger.success("✅ DeepSeek LLM初始化成功")
        except Exception as e:
            logger.error(f"❌ DeepSeek LLM初始化失败: {e}")
            raise
    
    # 3. 组装 LangGraph Agent
    logger.info("🤖 组装项目LangGraph Agent...")
    agent = await assemble_project_agent(llm)
    
    # 将资源存储在应用状态中
    app_state = {
        "llm": llm,
        "agent": agent
    }
    
    logger.success("✅ 应用启动完成")
    
    # 应用运行期间
    yield app_state
    
    # 清理资源（如果需要）
    logger.info("🛑 清理应用资源...")
