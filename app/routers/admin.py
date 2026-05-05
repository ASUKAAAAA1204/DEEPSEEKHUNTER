"""
管理后台路由
"""
import time
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.config import settings
from app.db.connection import get_db
from app.db.crud import get_stats
from app.models import SystemStatusResponse, ApiKeyResponse, ProviderType


router = APIRouter(prefix="/admin", tags=["Admin"])

# 服务启动时间
START_TIME = time.time()


@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status():
    """获取系统状态"""
    stats = {}
    try:
        async for db in get_db():
            stats = await get_stats(db)
    except Exception:
        pass
    
    uptime = time.time() - START_TIME
    
    active_providers = []
    if settings.deepseek_api_key:
        active_providers.append("deepseek")
    if settings.openai_api_key:
        active_providers.append("openai")
    
    return SystemStatusResponse(
        status="ok",
        uptime=uptime,
        total_requests=stats.get("total_requests", 0),
        success_requests=stats.get("success_requests", 0),
        failed_requests=stats.get("failed_requests", 0),
        active_providers=active_providers,
    )


@router.get("/api-keys", response_model=list[ApiKeyResponse])
async def get_api_keys_status():
    """获取 API 密钥状态"""
    keys = []
    
    if settings.deepseek_api_key:
        keys.append(ApiKeyResponse(
            provider=ProviderType.DEEPSEEK,
            is_configured=True,
        ))
    else:
        keys.append(ApiKeyResponse(
            provider=ProviderType.DEEPSEEK,
            is_configured=False,
        ))
    
    if settings.openai_api_key:
        keys.append(ApiKeyResponse(
            provider=ProviderType.OPENAI,
            is_configured=True,
        ))
    else:
        keys.append(ApiKeyResponse(
            provider=ProviderType.OPENAI,
            is_configured=False,
        ))
    
    return keys


@router.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
