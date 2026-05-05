"""
配置管理模块
"""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """应用配置"""
    
    # 服务配置
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = True
    
    # API 密钥
    deepseek_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # 数据库配置
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    
    # 缓存配置
    redis_url: Optional[str] = None
    cache_ttl: int = 3600
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    # 安全配置
    secret_key: str = "your-secret-key-change-this-in-production"
    allowed_hosts: str = "*"
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 30
    
    # 模型配置
    default_model: str = "deepseek-chat"
    available_models: List[str] = [
        "deepseek-chat",
        "deepseek-reasoner",
        "gpt-4",
        "gpt-3.5-turbo",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
