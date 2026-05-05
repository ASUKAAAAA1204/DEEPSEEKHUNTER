"""
数据模型和 Pydantic Schemas
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class ProviderType(str, Enum):
    """模型提供商类型"""
    DEEPSEEK = "deepseek"
    OPENAI = "openai"


class Role(str, Enum):
    """消息角色"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    """单条消息"""
    role: Role
    content: str
    name: Optional[str] = None


class ChatRequest(BaseModel):
    """对话请求"""
    model: str = Field(default="deepseek-chat", description="模型名称")
    messages: List[Message]
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=2048, ge=1, le=32768)
    top_p: Optional[float] = Field(default=1.0, ge=0.0, le=1.0)
    stream: bool = Field(default=False)


class ChatChoice(BaseModel):
    """对话选择项"""
    index: int
    message: Message
    finish_reason: Optional[str] = None


class Usage(BaseModel):
    """Token 使用统计"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    """对话响应"""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatChoice]
    usage: Optional[Usage] = None


class ApiKeyResponse(BaseModel):
    """API 密钥状态"""
    provider: ProviderType
    is_configured: bool
    last_used: Optional[datetime] = None


class SystemStatusResponse(BaseModel):
    """系统状态"""
    status: str = "ok"
    uptime: float
    total_requests: int
    success_requests: int
    failed_requests: int
    active_providers: List[str]
