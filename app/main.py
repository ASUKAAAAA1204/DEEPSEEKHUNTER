"""
FastAPI 主应用
"""
import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.connection import init_db
from app.routers import api, admin
from app.middleware.logging import log_requests


# 配置日志
def setup_logging():
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(settings.log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ]
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动前
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting AI Proxy Service...")
    
    # 确保目录存在
    os.makedirs("./data", exist_ok=True)
    os.makedirs("./logs", exist_ok=True)
    
    # 初始化数据库
    await init_db()
    logger.info("Database initialized")
    
    logger.info("Service started successfully!")
    
    yield
    
    # 关闭前
    logger.info("Shutting down...")


def create_app() -> FastAPI:
    """创建应用实例"""
    app = FastAPI(
        title="AI API Proxy Service",
        description="专业的 AI API 代理服务，支持 DeepSeek 和 OpenAI",
        version="2.0.0",
        lifespan=lifespan,
    )
    
    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 添加中间件
    app.middleware("http")(log_requests)
    
    # 注册路由
    app.include_router(api.router)
    app.include_router(admin.router)
    
    # 根路径
    @app.get("/")
    async def root():
        return {
            "service": "AI API Proxy Service",
            "version": "2.0.0",
            "status": "running",
            "docs": "/docs",
        }
    
    return app


app = create_app()
