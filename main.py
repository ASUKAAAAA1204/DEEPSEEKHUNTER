#!/usr/bin/env python3
"""
DeepSeek 网页端免费对话中转站（反向代理）
支持 OpenAI 兼容 API 协议
"""

import os
import asyncio
import json
import random
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI(title="DeepSeek Free API Proxy", version="1.0")

# 配置
USER_TOKENS = os.environ.get("USER_TOKENS", "").split(",")
if not USER_TOKENS or USER_TOKENS == [""]:
    USER_TOKENS = ["your_token_here"]

DEEPSEEK_API_URL = "https://chat.deepseek.com/api/chat/completions"
MODEL_MAPPING = {
    "deepseek-chat": "deepseek-chat",
    "deepseek-reasoner": "deepseek-reasoner",
    "deepseek-r1": "deepseek-r1",
}

async def get_random_token():
    """获取随机 Token"""
    return random.choice([t for t in USER_TOKENS if t.strip()])

@app.get("/v1/models")
async def list_models():
    """列出可用模型"""
    models = [
        {
            "id": model_id,
            "object": "model",
            "created": 1714512000,
            "owned_by": "deepseek-free",
        }
        for model_id in MODEL_MAPPING.keys()
    ]
    return {"object": "list", "data": models}

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """处理对话请求"""
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    model = body.get("model", "deepseek-chat")
    if model not in MODEL_MAPPING:
        raise HTTPException(status_code=400, detail=f"Model {model} not supported")

    messages = body.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="Messages required")

    stream = body.get("stream", False)
    
    # 构建 DeepSeek 请求
    token = await get_random_token()
    
    deepseek_body = {
        "model": MODEL_MAPPING[model],
        "messages": messages,
        "stream": stream,
        "max_tokens": body.get("max_tokens", 2048),
        "temperature": body.get("temperature", 0.7),
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    async def stream_response():
        """流式响应"""
        async with httpx.AsyncClient(timeout=300) as client:
            async with client.post(
                DEEPSEEK_API_URL,
                json=deepseek_body,
                headers=headers,
                timeout=300,
            ) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes():
                    if chunk:
                        yield chunk

    async def non_stream_response():
        """非流式响应"""
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                DEEPSEEK_API_URL,
                json=deepseek_body,
                headers=headers,
                timeout=300,
            )
            response.raise_for_status()
            return response.json()

    if stream:
        return StreamingResponse(stream_response(), media_type="text/event-stream")
    else:
        return await non_stream_response()

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"🚀 DeepSeek Free API Proxy starting on http://{host}:{port}")
    print(f"📋 Available models: {list(MODEL_MAPPING.keys())}")
    print(f"🔑 Tokens configured: {len([t for t in USER_TOKENS if t.strip() and t != 'your_token_here'])}")
    uvicorn.run(app, host=host, port=port)
