"""
数据库 CRUD 操作
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.db.connection import Base


class Conversation(Base):
    """对话历史表"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, unique=True, index=True)
    user_id = Column(String, index=True, default="anonymous")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    model = Column(String)
    message_count = Column(Integer, default=0)


class MessageHistory(Base):
    """消息历史表"""
    __tablename__ = "message_history"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    token_count = Column(Integer, default=0)


class RequestLog(Base):
    """请求日志表"""
    __tablename__ = "request_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True)
    model = Column(String)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    duration = Column(Float)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


async def create_conversation(
    db: AsyncSession,
    conversation_id: str,
    user_id: str = "anonymous",
    model: str = "deepseek-chat",
) -> Conversation:
    """创建对话"""
    conversation = Conversation(
        conversation_id=conversation_id,
        user_id=user_id,
        model=model,
    )
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation


async def add_message(
    db: AsyncSession,
    conversation_id: str,
    role: str,
    content: str,
    token_count: int = 0,
) -> MessageHistory:
    """添加消息"""
    message = MessageHistory(
        conversation_id=conversation_id,
        role=role,
        content=content,
        token_count=token_count,
    )
    db.add(message)
    
    # 更新对话的消息计数
    result = await db.execute(
        select(Conversation).where(Conversation.conversation_id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    if conversation:
        conversation.message_count += 1
        conversation.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(message)
    return message


async def log_request(
    db: AsyncSession,
    request_id: str,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    duration: float,
    success: bool = True,
    error_message: str = None,
) -> RequestLog:
    """记录请求日志"""
    log = RequestLog(
        request_id=request_id,
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens,
        duration=duration,
        success=success,
        error_message=error_message,
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


async def get_stats(db: AsyncSession) -> dict:
    """获取统计数据"""
    from sqlalchemy import func
    
    total = await db.execute(select(func.count(RequestLog.id)))
    total_count = total.scalar() or 0
    
    success = await db.execute(
        select(func.count(RequestLog.id)).where(RequestLog.success == True)
    )
    success_count = success.scalar() or 0
    
    return {
        "total_requests": total_count,
        "success_requests": success_count,
        "failed_requests": total_count - success_count,
    }
