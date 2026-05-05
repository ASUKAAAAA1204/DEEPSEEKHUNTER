#!/usr/bin/env python3
"""DeepSeek 中转站启动器"""

import os
import subprocess

def main():
    print("=" * 50)
    print("  DeepSeek 网页端中转站 - 快速启动器")
    print("=" * 50)
    
    # 优先从环境变量获取 Token
    tokens = os.environ.get("USER_TOKENS", "").strip()
    
    # 如果环境变量没有，尝试从配置文件读取
    if not tokens:
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("user_tokens"):
                        # 提取 tokens
                        import re
                        match = re.search(r'\[(.*?)\]', line)
                        if match:
                            tokens = match.group(1).replace('"', '').replace("'", "")
    
    if not tokens or tokens == "your_token_here":
        print("⚠️  未配置 userToken，请按以下步骤获取：")
        print("")
        print("📌 获取方式：")
        print("  1. 登录 https://chat.deepseek.com")
        print("  2. 发起一次对话")
        print("  3. 按 F12 打开开发者工具")
        print("  4. 切换到 Application（应用）标签")
        print("  5. 左侧选择 Local Storage → https://chat.deepseek.com")
        print("  6. 找到 userToken 并复制其值")
        print("")
        print("🔧 配置方式：")
        print("  方法1: 设置环境变量 USER_TOKENS=token1,token2")
        print("  方法2: 编辑 config.toml 文件")
        print("  方法3: 使用命令行: USER_TOKENS=your_token python start.py")
        print("")
        return
    
    os.environ["USER_TOKENS"] = tokens
    os.environ["PORT"] = "8080"
    
    token_count = len([t for t in tokens.split(',') if t.strip()])
    print(f"✅ 已配置 {token_count} 个 Token")
    print("🚀 启动服务...")
    print("📍 服务地址: http://localhost:8080/v1")
    print("🔄 按 Ctrl+C 停止服务")
    print("-" * 50)
    
    subprocess.run([
        "python", "-m", "uvicorn", "main:app", 
        "--host", "0.0.0.0", 
        "--port", "8080",
        "--reload"
    ])

if __name__ == "__main__":
    main()
