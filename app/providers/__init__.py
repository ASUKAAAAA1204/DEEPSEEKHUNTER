"""
模型提供商模块
"""
from app.providers.base import BaseProvider
from app.providers.deepseek import DeepSeekProvider
from app.providers.openai import OpenAIProvider


def get_provider(model_name: str, config):
    """根据模型名称获取合适的提供商"""
    model_name = model_name.lower()
    
    if model_name.startswith("deepseek"):
        return DeepSeekProvider(config.deepseek_api_key)
    elif model_name.startswith("gpt"):
        return OpenAIProvider(config.openai_api_key)
    else:
        return DeepSeekProvider(config.deepseek_api_key)


__all__ = [
    "BaseProvider",
    "DeepSeekProvider",
    "OpenAIProvider",
    "get_provider",
]
