#!/usr/bin/env python3
"""
样本数据填充脚本 - 修复版本
"""

import sqlite3
import uuid
from datetime import datetime, timedelta

def populate_sample_data():
    """填充样本检验数据"""
    db_path = "app_agent/data/project_database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("开始填充样本数据...")
    
    # 清空现有数据
    cursor.execute("DELETE FROM inspection_records")
    cursor.execute("DELETE FROM ndt_requests")
    
    # 样本项目ID
    projects = ["PROJ-2024-001", "PROJ-2024-002", "PROJ-2024-003"]
    
    # 样本组件ID
    components = ["COMP-001", "COMP-002", "COMP-003", "COMP-004", "COMP-005"]
    
    # 检验类型
    inspection_types = ["material", "fitup", "final", "weld", "dimensional"]
    
    # NDT技术
    ndt_techniques = ["UT", "RT", "PT", "MT", "VT"]
    
    # 状态
    statuses = ["pending", "scheduled", "in_progress", "completed", "rejected"]
    
    # 检验员
    inspectors = ["张三", "李四", "王五", "赵六", "钱七"]
    
    # 填充检验记录
    inspection_records = []
    for i in range(50):
        record_id = str(uuid.uuid4())
        project_id = projects[i % len(projects)]
        component_id = components[i % len(components)]
        inspection_type = inspection_types[i % len(inspection_types)]
        status = statuses[i % len(statuses)]
        inspector = inspectors[i % len(inspectors)]
        
        # 生成日期
        base_date = datetime.now() - timedelta(days=30)
        scheduled_date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        actual_date = (base_date + timedelta(days=i + 1)).strftime("%Y-%m-%d") if status in ["completed", "in_progress"] else None
        created_at = (base_date + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
        updated_at = (base_date + timedelta(days=i + 1)).strftime("%Y-%m-%d %H:%M:%S")
        
        findings = f"检验发现 #{i+1}: 组件{component_id}的{inspection_type}检验结果"
        notes = f"备注: 这是{inspector}执行的{inspection_type}检验"
        
        inspection_records.append((
            record_id, project_id, component_id, inspection_type, status,
            inspector, scheduled_date, actual_date, findings, notes,
            created_at, updated_at
        ))
    
    # 插入检验记录
    cursor.executemany("""
        INSERT INTO inspection_records 
        (id, project_id, component_id, inspection_type, status, inspector, 
         scheduled_date, actual_date, findings, notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, inspection_records)
    
    print(f"已插入 {len(inspection_records)} 条检验记录")
    
    # 填充NDT请求
    ndt_requests = []
    for i in range(20):
        request_id = str(uuid.uuid4())
        project_id = projects[i % len(projects)]
        component_id = components[i % len(components)]
        technique = ndt_techniques[i % len(ndt_techniques)]
        requested_by = inspectors[i % len(inspectors)]
        status = statuses[i % len(statuses)]
        
        # 生成日期
        base_date = datetime.now() - timedelta(days=20)
        requested_date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        scheduled_date = (base_date + timedelta(days=i + 2)).strftime("%Y-%m-%d") if status in ["scheduled", "in_progress", "completed"] else None
        completed_date = (base_date + timedelta(days=i + 3)).strftime("%Y-%m-%d") if status == "completed" else None
        created_at = (base_date + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
        updated_at = (base_date + timedelta(days=i + 1)).strftime("%Y-%m-%d %H:%M:%S")
        
        results = f"NDT结果 #{i+1}: 使用{technique}技术检测组件{component_id}"
        
        ndt_requests.append((
            request_id, project_id, component_id, technique, requested_by,
            requested_date, scheduled_date, completed_date, results, status,
            created_at, updated_at
        ))
    
    # 插入NDT请求
    cursor.executemany("""
        INSERT INTO ndt_requests 
        (id, project_id, component_id, technique, requested_by, 
         requested_date, scheduled_date, completed_date, results, status, 
         created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ndt_requests)
    
    print(f"已插入 {len(ndt_requests)} 条NDT请求")
    
    conn.commit()
    conn.close()
    print("样本数据填充完成!")

if __name__ == "__main__":
    populate_sample_data()
