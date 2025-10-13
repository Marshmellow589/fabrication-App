from langchain_core.tools import tool
from datetime import datetime

@tool
def get_project_inspections(project_id: str, inspection_type: str = None, status: str = None) -> str:
    """获取项目的检验记录。可以按检验类型（material, fit_up, final, ndt）和状态（pending, in_progress, completed, rejected）过滤。"""
    return f"项目 {project_id} 的检验记录查询功能暂时不可用。数据库连接需要配置。"

@tool
def get_project_ndt_requests(project_id: str, status: str = None) -> str:
    """获取项目的无损检测（NDT）请求。可以按状态（pending, in_progress, completed, rejected）过滤。"""
    return f"项目 {project_id} 的NDT请求查询功能暂时不可用。数据库连接需要配置。"

@tool
def get_project_status_summary(project_id: str) -> str:
    """获取项目的总体状态摘要，包括各种检验的计数和下一个计划中的检验。"""
    return f"项目 {project_id} 的状态摘要功能暂时不可用。数据库连接需要配置。"

@tool
def check_inspection_compliance(project_id: str, inspection_type: str) -> str:
    """检查特定类型检验的合规性状态。"""
    return f"项目 {project_id} 的 {inspection_type} 检验合规性检查功能暂时不可用。数据库连接需要配置。"

# 将工具添加到列表
project_tools = [get_project_inspections, get_project_ndt_requests, 
                 get_project_status_summary, check_inspection_compliance]
