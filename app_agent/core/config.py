from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    app_version: str = "1.0.0"
    environment: str = "development"
    
    # Database settings
    sqlite_db_path: str = "app_agent/data/project_data.db"
    
    # Ollama settings
    ollama_default_model: str = "llama3.2"
    ollama_base_url: str = "http://localhost:11434"
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    
    # JWT settings (should match main backend)
    jwt_secret_key: str = "dataprojecthash"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 20
    
    # CORS settings
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env.development"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()
