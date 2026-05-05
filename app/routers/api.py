"""
主要 API 路由
"""
import time
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import (
    ChatRequest,
    ChatResponse,
    Message,
)
from app.db.connection import get_db
from app.db.crud import log_request, add_message
from app.providers import get_provider


router = APIRouter(prefix="/v1", tags=["API"])


@router.get("/models")
async def list_models():
    """列出所有可用模型"""
    available_models = []
    
    # 检查 DeepSeek
    if settings.deepseek_api_key:
        available_models.extend([
            {"id": "deepseek-chat", "object": "model", "created": 1714512000, "owned_by": "deepseek"},
            {"id": "deepseek-reasoner", "object": "model", "created": 1714512000, "owned_by": "deepseek"},
        ])
    
    # 检查 OpenAI
    if settings.openai_api_key:
        available_models.extend([
            {"id": "gpt-3.5-turbo", "object": "model", "created": 1714512000, "owned_by": "openai"},
            {"id": "gpt-4", "object": "model", "created": 1714512000, "owned_by": "openai"},
        ])
    
    if not available_models:
        available_models = [
            {"id": "deepseek-chat", "object": "model", "created": 1714512000, "owned_by": "deepseek"},
        ]
    
    return {"object": "list", "data": available_models}


@router.post("/chat/completions", response_model=ChatResponse)
async def chat_completions(request: Request, chat_request: ChatRequest):
    """处理对话请求"""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        provider = get_provider(chat_request.model, settings)
        
        if not provider.is_available():
            raise HTTPException(
                status_code=400,
                detail="Provider not available. Check API key configuration."
            )
        
        if chat_request.stream:
            # 流式响应
            async def generate():
                async for chunk in provider.chat_stream(chat_request):
                    yield chunk
            
            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            # 非流式响应
            response = await provider.chat(chat_request)
            
            # 记录日志
            prompt_tokens = response.usage.prompt_tokens if response.usage else 0
            completion_tokens = response.usage.completion_tokens if response.usage else 0
            duration = time.time() - start_time
            
            async for db in get_db():
                await log_request(
                    db=db,
                    request_id=request_id,
                    model=chat_request.model,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    duration=duration,
                    success=True,
                )
            
            return response
            
    except Exception as e:
        # 记录失败
        duration = time.time() - start_time
        try:
            async for db in get_db():
                await log_request(
                    db=db,
                    request_id=request_id,
                    model=chat_request.model,
                    prompt_tokens=0,
                    completion_tokens=0,
                    duration=duration,
                    success=False,
                    error_message=str(e),
                )
        except:
            pass
        
        raise HTTPException(status_code=500, detail=str(e))
