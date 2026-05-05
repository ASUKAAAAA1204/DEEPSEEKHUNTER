#!/usr/bin/env python3
"""DeepSeek 中转站 API 测试脚本"""

import sys
from openai import OpenAI

def test_api(base_url: str = "http://localhost:8080/v1"):
    print(f"🚀 测试 DeepSeek 中转站 API")
    print(f"📍 Base URL: {base_url}")
    print("=" * 50)
    
    try:
        client = OpenAI(
            base_url=base_url,
            api_key="test-key"  # 任意字符串
        )
        
        # 测试获取模型列表
        print("📋 获取模型列表...")
        models = client.models.list()
        model_names = [m.id for m in models.data]
        print(f"✅ 可用模型: {model_names}")
        
        # 测试流式对话
        print("\n💬 测试流式对话...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "你好，介绍一下你自己"}],
            stream=True,
            max_tokens=100
        )
        
        print("📝 响应内容:")
        print("-" * 30)
        for chunk in response:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="")
        print("\n" + "-" * 30)
        print("✅ 测试成功！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print("\n🔍 常见问题排查:")
        print("  1. 确认中转站服务正在运行")
        print("  2. 检查端口是否正确（默认8080）")
        print("  3. 检查防火墙设置")
        print("  4. 确认 Token 已正确配置")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="测试 DeepSeek 中转站 API")
    parser.add_argument("--url", default="http://localhost:8080/v1", help="中转站 API 地址")
    args = parser.parse_args()
    test_api(args.url)
