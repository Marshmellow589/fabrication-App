#!/usr/bin/env python3
"""
Create test projects for the project selector
"""

import os
import sys
from datetime import datetime, timedelta

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import SessionLocal
from backend.app.models.project import Project
from backend.app.models.user import User

def create_test_projects():
    """Create test projects for the project selector"""
    db = SessionLocal()
    
    try:
        # Get the first user to use as created_by
        user = db.query(User).first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return
        
        # Create test projects
        projects_data = [
            {
                "project_number": "PROJ-001",
                "project_name": "炼油厂管道安装项目",
                "client": "中国石油化工集团",
                "start_date": datetime.now().date(),
                "end_date": (datetime.now() + timedelta(days=90)).date(),
                "status": "active",
                "project_manager": "张三",
                "description": "炼油厂主要管道系统安装和检验项目",
                "budget": 5000000.00,
                "created_by": user.id
            },
            {
                "project_number": "PROJ-002",
                "project_name": "化工厂设备检验项目",
                "client": "中国化工集团",
                "start_date": datetime.now().date(),
                "end_date": (datetime.now() + timedelta(days=60)).date(),
                "status": "active",
                "project_manager": "李四",
                "description": "化工厂压力容器和管道系统定期检验",
                "budget": 3000000.00,
                "created_by": user.id
            },
            {
                "project_number": "PROJ-003",
                "project_name": "发电厂锅炉检验项目",
                "client": "国家电网公司",
                "start_date": datetime.now().date(),
                "end_date": (datetime.now() + timedelta(days=120)).date(),
                "status": "active",
                "project_manager": "王五",
                "description": "发电厂锅炉系统全面检验和维护",
                "budget": 8000000.00,
                "created_by": user.id
            }
        ]
        
        for project_data in projects_data:
            project = Project(**project_data)
            db.add(project)
        
        db.commit()
        print(f"✅ Created {len(projects_data)} test projects successfully!")
        
    except Exception as e:
        print(f"❌ Error creating test projects: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_projects()
