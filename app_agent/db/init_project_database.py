import sqlite3
from app_agent.core.config_simple import settings

def init_project_database():
    """初始化项目数据库表结构"""
    conn = sqlite3.connect(settings.sqlite_db_path)
    cursor = conn.cursor()

    # 创建检验记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inspection_records (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        component_id TEXT NOT NULL,
        inspection_type TEXT NOT NULL,
        status TEXT NOT NULL,
        inspector TEXT NOT NULL,
        scheduled_date TEXT NOT NULL,
        actual_date TEXT,
        findings TEXT,
        notes TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')

    # 创建NDT请求表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ndt_requests (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        component_id TEXT NOT NULL,
        technique TEXT NOT NULL,
        requested_by TEXT NOT NULL,
        requested_date TEXT NOT NULL,
        scheduled_date TEXT,
        completed_date TEXT,
        results TEXT,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')

    # 创建索引以提高查询性能
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_inspection_project ON inspection_records(project_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_inspection_type ON inspection_records(inspection_type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_inspection_status ON inspection_records(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ndt_project ON ndt_requests(project_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ndt_status ON ndt_requests(status)')

    conn.commit()
    conn.close()
    print("项目数据库初始化完成。")
