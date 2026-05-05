"""
模型提供商基类
"""
from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional
from app.models import ChatRequest, ChatResponse, Message


class BaseProvider(ABC):
    """模型提供商基类"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.initialized = False
    
    @abstractmethod
    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """非流式对话"""
        pass
    
    @abstractmethod
    async def chat_stream(
        self,
        request: ChatRequest,
    ) -> AsyncGenerator[str, None]:
        """流式对话"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查提供商是否可用"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """获取可用模型列表"""
        pass
