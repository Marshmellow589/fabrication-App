import os
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).parent.parent

# SQLite数据库路径
sqlite_db_path = str(BASE_DIR / "data" / "project_database.db")

# 确保数据目录存在
data_dir = BASE_DIR / "data"
data_dir.mkdir(exist_ok=True)

# 简单的设置对象
class Settings:
    def __init__(self):
        self.sqlite_db_path = sqlite_db_path

# 创建全局设置实例
settings = Settings()
