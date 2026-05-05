#!/usr/bin/env python3
"""
快速启动测试
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """测试模块导入"""
    print("📋 测试模块导入...")
    try:
        from app.config import settings
        print("  ✅ 配置模块导入成功")
        
        from app.models import ChatRequest, Message
        print("  ✅ 数据模型导入成功")
        
        from app.providers import DeepSeekProvider, OpenAIProvider
        print("  ✅ 提供商模块导入成功")
        
        from app.db.connection import get_db, Base
        print("  ✅ 数据库模块导入成功")
        
        print("\n✅ 所有模块导入成功！")
        return True
    except Exception as e:
        print(f"\n❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """测试配置"""
    print("\n📋 测试配置...")
    from app.config import settings
    print(f"  Host: {settings.host}")
    print(f"  Port: {settings.port}")
    print(f"  Debug: {settings.debug}")
    print(f"  Default Model: {settings.default_model}")
    print("  ✅ 配置加载成功")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("  AI API Proxy Service 启动测试")
    print("=" * 60)
    
    all_ok = True
    all_ok &= test_imports()
    all_ok &= test_config()
    
    print("\n" + "=" * 60)
    if all_ok:
        print("  ✅ 所有测试通过！项目可以正常运行")
        print("\n📝 下一步：")
        print("  1. 复制 .env.example 为 .env")
        print("  2. 编辑 .env 填入 API 密钥")
        print("  3. 运行: python run.py")
        print("=" * 60)
        sys.exit(0)
    else:
        print("  ❌ 存在问题，请检查")
        print("=" * 60)
        sys.exit(1)
