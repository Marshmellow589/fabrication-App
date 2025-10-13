from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import sys
sys.path.insert(0, 'app_agent')
from db.inspection_queries import inspection_query

router = APIRouter(tags=["Project"])

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str
    session_id: str

@router.get("/projects", summary="获取项目列表")
async def get_projects():
    """
    获取所有项目列表
    """
    return {"message": "项目列表功能暂时不可用，需要数据库连接"}

@router.get("/projects/{project_id}", summary="获取项目详情")
async def get_project(project_id: int):
    """
    获取特定项目的详细信息
    """
    return {"message": f"项目 {project_id} 详情功能暂时不可用", "project_id": project_id}

def analyze_query_and_generate_response(message: str) -> str:
    """分析用户查询并生成智能响应"""
    message_lower = message.lower()
    
    # 获取统计数据
    stats = inspection_query.get_inspection_stats()
    pending = inspection_query.get_pending_actions()
    
    # 查询理解与响应生成
    if any(keyword in message_lower for keyword in ["统计", "总数", "有多少", "数量"]):
        return generate_stats_response(stats, pending)
    
    elif any(keyword in message_lower for keyword in ["材料", "material"]):
        return generate_material_response()
    
    elif any(keyword in message_lower for keyword in ["装配", "fitup", "fit up"]):
        return generate_fitup_response()
    
    elif any(keyword in message_lower for keyword in ["最终", "final", "完工"]):
        return generate_final_response()
    
    elif any(keyword in message_lower for keyword in ["焊接", "weld"]):
        return generate_weld_response()
    
    elif any(keyword in message_lower for keyword in ["尺寸", "dimensional"]):
        return generate_dimensional_response()
    
    elif any(keyword in message_lower for keyword in ["ndt", "无损", "检测"]):
        return generate_ndt_response()
    
    elif any(keyword in message_lower for keyword in ["待处理", "pending", "需要处理"]):
        return generate_pending_response(pending)
    
    elif any(keyword in message_lower for keyword in ["最近", "最新", "recent"]):
        return generate_recent_response()
    
    else:
        return generate_general_response(stats, pending)

def generate_stats_response(stats: dict, pending: dict) -> str:
    """生成统计信息响应"""
    return f"""📊 检验统计信息：
• 总检验记录: {stats['total_inspections']} 条
• 检验类型分布: {', '.join([f'{k}: {v}' for k, v in stats['inspections_by_type'].items()])}
• 检验状态: {', '.join([f'{k}: {v}' for k, v in stats['inspections_by_status'].items()])}
• NDT请求: {stats['total_ndt_requests']} 条
• 待处理操作: 检验({pending['pending_inspections']}), NDT({pending['pending_ndt']})
• 过期任务: 检验({pending['overdue_inspections']}), NDT({pending['overdue_ndt']})"""

def generate_material_response() -> str:
    """生成材料检验响应"""
    inspections = inspection_query.search_inspections(inspection_type="material", limit=5)
    response = "📦 材料检验信息：\n"
    for i, insp in enumerate(inspections, 1):
        response += f"{i}. {insp['component_id']} - {insp['status']} - {insp['inspector']}\n"
    return response + "需要查看特定材料的详细检验记录吗？"

def generate_fitup_response() -> str:
    """生成装配检验响应"""
    inspections = inspection_query.search_inspections(inspection_type="fitup", limit=5)
    response = "🔧 装配检验信息：\n"
    for i, insp in enumerate(inspections, 1):
        response += f"{i}. {insp['component_id']} - {insp['status']} - {insp['inspector']}\n"
    return response + "需要查看特定装配的详细检验记录吗？"

def generate_final_response() -> str:
    """生成最终检验响应"""
    inspections = inspection_query.search_inspections(inspection_type="final", limit=5)
    response = "✅ 最终检验信息：\n"
    for i, insp in enumerate(inspections, 1):
        response += f"{i}. {insp['component_id']} - {insp['status']} - {insp['inspector']}\n"
    return response + "需要查看特定最终检验的详细记录吗？"

def generate_weld_response() -> str:
    """生成焊接检验响应"""
    inspections = inspection_query.search_inspections(inspection_type="weld", limit=5)
    response = "🔥 焊接检验信息：\n"
    for i, insp in enumerate(inspections, 1):
        response += f"{i}. {insp['component_id']} - {insp['status']} - {insp['inspector']}\n"
    return response + "需要查看特定焊接检验的详细记录吗？"

def generate_dimensional_response() -> str:
    """生成尺寸检验响应"""
    inspections = inspection_query.search_inspections(inspection_type="dimensional", limit=5)
    response = "📏 尺寸检验信息：\n"
    for i, insp in enumerate(inspections, 1):
        response += f"{i}. {insp['component_id']} - {insp['status']} - {insp['inspector']}\n"
    return response + "需要查看特定尺寸检验的详细记录吗？"

def generate_ndt_response() -> str:
    """生成NDT检验响应"""
    ndt_requests = inspection_query.search_ndt_requests(limit=5)
    response = "🔍 NDT检验信息：\n"
    for i, ndt in enumerate(ndt_requests, 1):
        response += f"{i}. {ndt['component_id']} - {ndt['technique']} - {ndt['status']}\n"
    return response + "需要查看特定NDT检验的详细记录吗？"

def generate_pending_response(pending: dict) -> str:
    """生成待处理任务响应"""
    return f"""📋 待处理任务：
• 待检验: {pending['pending_inspections']} 条
• 待NDT: {pending['pending_ndt']} 条
• 过期检验: {pending['overdue_inspections']} 条
• 过期NDT: {pending['overdue_ndt']} 条

建议优先处理过期任务！"""

def generate_recent_response() -> str:
    """生成最近记录响应"""
    inspections = inspection_query.search_inspections(limit=3)
    ndt_requests = inspection_query.search_ndt_requests(limit=2)
    
    response = "🕒 最近活动：\n"
    response += "最近检验记录：\n"
    for i, insp in enumerate(inspections, 1):
        response += f"  {i}. {insp['inspection_type']} - {insp['component_id']} - {insp['status']}\n"
    
    response += "最近NDT请求：\n"
    for i, ndt in enumerate(ndt_requests, 1):
        response += f"  {i}. {ndt['technique']} - {ndt['component_id']} - {ndt['status']}\n"
    
    return response

def generate_general_response(stats: dict, pending: dict) -> str:
    """生成通用响应"""
    return f"""🤖 您好！我是制造检验AI助手。

当前系统状态：
• 总检验记录: {stats['total_inspections']}
• 待处理任务: {pending['pending_inspections'] + pending['pending_ndt']}
• 过期任务: {pending['overdue_inspections'] + pending['overdue_ndt']}

我可以帮您查询：
• 检验统计信息
• 材料/装配/焊接/最终/尺寸检验
• NDT无损检测
• 待处理任务
• 最近活动记录

请告诉我您想了解什么？"""

@router.post("/chat", response_model=ChatResponse, summary="与AI助手聊天")
async def chat_with_agent(request: ChatRequest):
    """
    与AI助手进行智能聊天对话，基于真实检验数据
    """
    # 生成会话ID（如果未提供）
    session_id = request.session_id or f"session_{hash(request.message) % 10000}"
    
    # 分析查询并生成智能响应
    response = analyze_query_and_generate_response(request.message)
    
    return ChatResponse(
        response=response,
        session_id=session_id
    )
