"""
请求日志中间件
"""
import time
import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import StreamingResponse


logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next: Callable) -> Response:
    """请求日志中间件"""
    start_time = time.time()
    
    # 记录请求
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # 处理请求
    response = await call_next(request)
    
    # 计算耗时
    process_time = time.time() - start_time
    
    # 记录响应
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    # 添加响应头
    response.headers["X-Process-Time"] = str(process_time)
    
    return response
