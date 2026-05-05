#!/usr/bin/env python3
"""
AI API Proxy Service 启动脚本
版本 2.0.0
"""
import os
import sys
import uvicorn


def main():
    print("=" * 60)
    print("   AI API Proxy Service (v2.0.0)")
    print("=" * 60)
    
    # 检查 .env 文件
    if not os.path.exists(".env"):
        print("\n⚠️  配置文件 .env 不存在")
        print("📋 从 .env.example 复制...")
        
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ 已创建 .env 文件")
            print("🔧 请编辑 .env 配置你的 API 密钥")
            print("\n启动命令：python run.py")
            return
        else:
            print("❌ .env.example 也不存在，已跳过")
    
    # 导入环境变量
    from dotenv import load_dotenv
    load_dotenv()
    
    print("\n📊 配置状态：")
    
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    
    print(f"   DeepSeek: {'✅ 已配置' if deepseek_key and not deepseek_key.startswith('your_') else '❌ 未配置'}")
    print(f"   OpenAI:    {'✅ 已配置' if openai_key and not openai_key.startswith('your_') else '❌ 未配置'}")
    
    print("\n🚀 启动服务...")
    print("📍 服务地址: http://localhost:8080")
    print("📖 API 文档: http://localhost:8080/docs")
    print("=" * 60)
    print()
    
    # 启动 uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "8080")),
        reload=os.environ.get("DEBUG", "true").lower() == "true",
        log_level=os.environ.get("LOG_LEVEL", "info").lower(),
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已停止服务")
        sys.exit(0)
