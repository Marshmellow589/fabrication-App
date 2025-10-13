import sqlite3
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

# 直接设置数据库路径，避免模块导入问题
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "project_database.db")

class InspectionDataQuery:
    """数据查询类，用于查询检验记录和NDT请求"""
    
    def __init__(self):
        self.db_path = SQLITE_DB_PATH
    
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def get_inspection_stats(self) -> Dict[str, Any]:
        """获取检验统计信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # 获取检验记录总数
        cursor.execute("SELECT COUNT(*) FROM inspection_records")
        stats['total_inspections'] = cursor.fetchone()[0]
        
        # 按检验类型统计
        cursor.execute("""
            SELECT inspection_type, COUNT(*) 
            FROM inspection_records 
            GROUP BY inspection_type
        """)
        stats['inspections_by_type'] = dict(cursor.fetchall())
        
        # 按状态统计
        cursor.execute("""
            SELECT status, COUNT(*) 
            FROM inspection_records 
            GROUP BY status
        """)
        stats['inspections_by_status'] = dict(cursor.fetchall())
        
        # 获取NDT请求统计
        cursor.execute("SELECT COUNT(*) FROM ndt_requests")
        stats['total_ndt_requests'] = cursor.fetchone()[0]
        
        # NDT请求按状态统计
        cursor.execute("""
            SELECT status, COUNT(*) 
            FROM ndt_requests 
            GROUP BY status
        """)
        stats['ndt_by_status'] = dict(cursor.fetchall())
        
        conn.close()
        return stats
    
    def search_inspections(self, 
                          project_id: Optional[str] = None,
                          component_id: Optional[str] = None,
                          inspection_type: Optional[str] = None,
                          status: Optional[str] = None,
                          inspector: Optional[str] = None,
                          limit: int = 10) -> List[Dict[str, Any]]:
        """搜索检验记录"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM inspection_records WHERE 1=1"
        params = []
        
        if project_id:
            query += " AND project_id LIKE ?"
            params.append(f"%{project_id}%")
        
        if component_id:
            query += " AND component_id LIKE ?"
            params.append(f"%{component_id}%")
        
        if inspection_type:
            query += " AND inspection_type = ?"
            params.append(inspection_type)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if inspector:
            query += " AND inspector LIKE ?"
            params.append(f"%{inspector}%")
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def search_ndt_requests(self,
                           project_id: Optional[str] = None,
                           component_id: Optional[str] = None,
                           technique: Optional[str] = None,
                           status: Optional[str] = None,
                           requested_by: Optional[str] = None,
                           limit: int = 10) -> List[Dict[str, Any]]:
        """搜索NDT请求"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM ndt_requests WHERE 1=1"
        params = []
        
        if project_id:
            query += " AND project_id LIKE ?"
            params.append(f"%{project_id}%")
        
        if component_id:
            query += " AND component_id LIKE ?"
            params.append(f"%{component_id}%")
        
        if technique:
            query += " AND technique = ?"
            params.append(technique)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if requested_by:
            query += " AND requested_by LIKE ?"
            params.append(f"%{requested_by}%")
        
        query += " ORDER BY requested_date DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_recent_inspections(self, days: int = 7) -> List[Dict[str, Any]]:
        """获取最近N天的检验记录"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM inspection_records 
            WHERE date(created_at) >= date('now', ?) 
            ORDER BY created_at DESC
        """, (f"-{days} days",))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_pending_actions(self) -> Dict[str, Any]:
        """获取待处理的操作（待检验、待NDT等）"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        pending = {}
        
        # 待检验的记录
        cursor.execute("""
            SELECT COUNT(*) FROM inspection_records 
            WHERE status IN ('pending', 'scheduled')
        """)
        pending['pending_inspections'] = cursor.fetchone()[0]
        
        # 待处理的NDT请求
        cursor.execute("""
            SELECT COUNT(*) FROM ndt_requests 
            WHERE status IN ('pending', 'scheduled')
        """)
        pending['pending_ndt'] = cursor.fetchone()[0]
        
        # 过期的检验
        cursor.execute("""
            SELECT COUNT(*) FROM inspection_records 
            WHERE status = 'scheduled' 
            AND date(scheduled_date) < date('now')
        """)
        pending['overdue_inspections'] = cursor.fetchone()[0]
        
        # 过期的NDT
        cursor.execute("""
            SELECT COUNT(*) FROM ndt_requests 
            WHERE status = 'scheduled' 
            AND date(scheduled_date) < date('now')
        """)
        pending['overdue_ndt'] = cursor.fetchone()[0]
        
        conn.close()
        return pending

# 创建全局实例
inspection_query = InspectionDataQuery()
