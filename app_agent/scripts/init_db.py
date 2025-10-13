import sqlite3
from app_agent.core.config import settings

def init_database():
    conn = sqlite3.connect(settings.sqlite_db_path)
    cursor = conn.cursor()

    # 创建检验记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inspection_records (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
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

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("数据库初始化完成。")