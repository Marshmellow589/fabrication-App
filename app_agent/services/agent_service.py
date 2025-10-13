import json
from typing import AsyncGenerator
from loguru import logger
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage

async def run_agent(agent: Runnable, query: str, session_id: str) -> str:
    """
    以非流式的方式异步调用 Agent，并传入会话ID。
    """
    logger.info(f"非流式调用 Agent [Session: {session_id}], 查询: '{query}'")

    config: RunnableConfig = {"configurable": {"thread_id": session_id}}

    result = await agent.ainvoke({"messages": [HumanMessage(content=query)]}, config)

    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage):
            content = message.content
            if isinstance(content, str):
                logger.success(f"成功获取非流式响应 [Session: {session_id}]。")
                return content
            elif isinstance(content, list):
                text_parts = [
                    part["text"]
                    for part in content
                    if isinstance(part, dict) and part.get("type") == "text"
                ]
                if text_parts:
                    return "\n".join(text_parts)

    raise ValueError("Agent 未能生成有效的 AI 响应。")


async def stream_agent(
    agent: Runnable, query: str, session_id: str
) -> AsyncGenerator[str, None]:
    """
    以流式的方式异步调用 Agent，并传入会话ID。
    增强版：包含工具调用事件
    """
    logger.info(f"流式调用 Agent [Session: {session_id}], 查询: '{query}'")

    config: RunnableConfig = {"configurable": {"thread_id": session_id}}

    logger.debug(f"准备调用 Agent.astream_events，传入的 config: {config}")

    # 1. 模型流式输出
    async for event in agent.astream_events(
        {"messages": [HumanMessage(content=query)]}, version="v1", config=config
    ):
        event_type = event["event"]
        
        # 处理模型输出流
        if event_type == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            if chunk and hasattr(chunk, "content"):
                content = chunk.content
                if content:
                    yield f"data: {json.dumps({'type': 'chunk', 'content': content})}\n\n"
        
        # 处理工具开始调用事件
        elif event_type == "on_tool_start":
            tool_name = event.get("name", "unknown_tool")
            yield f"data: {json.dumps({'type': 'tool_start', 'content': f'调用工具: {tool_name}'})}\n\n"
        
        # 处理工具结束调用事件
        elif event_type == "on_tool_end":
            output = event.get("data", {}).get("output", "无输出")
            # 截断过长的输出
            if len(str(output)) > 100:
                output = str(output)[:100] + "..."
            yield f"data: {json.dumps({'type': 'tool_end', 'content': f'工具返回: {output}'})}\n\n"
        
        # 处理Agent思考过程
        elif event_type == "on_chain_stream":
            if "chunk" in event.get("data", {}):
                chunk = event["data"]["chunk"]
                if hasattr(chunk, "reasoning") and chunk.reasoning:
                    yield f"data: {json.dumps({'type': 'reasoning', 'content': chunk.reasoning})}\n\n"