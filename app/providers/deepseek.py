"""
DeepSeek 官方 API 提供商
使用官方 API：https://platform.deepseek.com
"""
import json
import time
from typing import AsyncGenerator, List, Optional
import httpx
from app.providers.base import BaseProvider
from app.models import ChatRequest, ChatResponse, Message, ChatChoice, Usage


class DeepSeekProvider(BaseProvider):
    """DeepSeek 官方 API 提供商"""
    
    BASE_URL = "https://api.deepseek.com"
    DEFAULT_MODEL = "deepseek-chat"
    
    AVAILABLE_MODELS = [
        "deepseek-chat",
        "deepseek-reasoner",
    ]
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.api_key = api_key
        self.initialized = api_key is not None and len(api_key.strip()) > 0
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """非流式对话"""
        if not self.initialized:
            raise RuntimeError("DeepSeek provider not initialized: API key missing")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        payload = {
            "model": request.model if request.model in self.AVAILABLE_MODELS else self.DEFAULT_MODEL,
            "messages": [m.model_dump() for m in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "top_p": request.top_p,
            "stream": False,
        }
        
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                f"{self.BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
        
        # 构造响应
        choices = [
            ChatChoice(
                index=choice["index"],
                message=Message(
                    role=choice["message"]["role"],
                    content=choice["message"]["content"],
                ),
                finish_reason=choice.get("finish_reason"),
            )
            for choice in data["choices"]
        ]
        
        usage = None
        if "usage" in data:
            usage = Usage(
                prompt_tokens=data["usage"]["prompt_tokens"],
                completion_tokens=data["usage"]["completion_tokens"],
                total_tokens=data["usage"]["total_tokens"],
            )
        
        return ChatResponse(
            id=data["id"],
            created=data["created"],
            model=data["model"],
            choices=choices,
            usage=usage,
        )
    
    async def chat_stream(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        """流式对话"""
        if not self.initialized:
            raise RuntimeError("DeepSeek provider not initialized: API key missing")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        payload = {
            "model": request.model if request.model in self.AVAILABLE_MODELS else self.DEFAULT_MODEL,
            "messages": [m.model_dump() for m in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "top_p": request.top_p,
            "stream": True,
        }
        
        async with httpx.AsyncClient(timeout=300) as client:
            async with client.stream(
                "POST",
                f"{self.BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        line = line[6:].strip()
                        if line == "[DONE]":
                            break
                        yield f"data: {line}\n\n"
    
    def is_available(self) -> bool:
        """检查提供商是否可用"""
        return self.initialized
    
    def get_available_models(self) -> List[str]:
        """获取可用模型列表"""
        return self.AVAILABLE_MODELS if self.initialized else []
