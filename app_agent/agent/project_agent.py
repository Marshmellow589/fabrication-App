from langchain_core.runnables import Runnable
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_agent_executor
from loguru import logger

from app_agent.tools.project_tools import project_tools
from app_agent.core.config import settings
from app_agent.agent.deepseek_wrapper import DeepSeekWrapper

async def assemble_project_agent(llm: DeepSeekWrapper) -> Runnable:
    """
    组装一个包含项目和通用工具的LangGraph Agent。
    """
    logger.info("开始组装项目LangGraph Agent...")

    # 只使用可用的项目工具
    all_tools = project_tools

    # 使用SqliteSaver持久化存储会话状态
    memory = SqliteSaver.from_conn_string(settings.sqlite_db_path)
    
    logger.info(f"使用SQLite数据库存储会话: {settings.sqlite_db_path}")

    # 创建Agent - using create_agent_executor for compatibility with langgraph 0.0.34
    runnable_agent = create_agent_executor(
        agent_runnable=llm,
        tools=all_tools,
    )

    model_name = getattr(llm, 'model', '模拟LLM')
    logger.success(f"✅ 项目LangGraph Agent 组装完成，使用模型: {model_name}")
    return runnable_agent
