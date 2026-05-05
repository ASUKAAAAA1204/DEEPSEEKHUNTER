# DeepSeek 网页端免费对话中转站（反向代理）

> **2026年最新可用** - 利用 DeepSeek 网页端免费对话建立中转站（反向代理）

---

## 📁 项目结构

```
D:\programss\fandai\
├── main.py          # 核心中转服务
├── start.py         # 启动脚本
├── config.toml      # 配置文件
├── test_api.py      # 测试脚本
└── README.md        # 本说明文档
```

---

## 🚀 快速开始

### 第一步：安装依赖

```bash
cd D:\programss\fandai
pip install fastapi uvicorn httpx -q
```

### 第二步：获取 userToken

1. 打开浏览器访问 `https://chat.deepseek.com` 并登录
2. 发起一次对话
3. 按 F12 打开开发者工具 → **Application** → **Local Storage** → `https://chat.deepseek.com`
4. 找到 `userToken` 并复制其值

### 第三步：配置 Token

**方法1：编辑配置文件**

编辑 `config.toml`：
```toml
user_tokens = [
    "你的_token_1",
    "你的_token_2",
    # 更多...
]
```

**方法2：环境变量**
```bash
set USER_TOKENS=你的_token_1,你的_token_2
python start.py
```

### 第四步：启动服务

```bash
python start.py
```

服务启动后访问：`http://localhost:8080/v1`

---

## 📡 API 使用

### 基础配置

| 配置项 | 值 |
|--------|----|
| Base URL | `http://localhost:8080/v1` |
| API Key | 任意字符串（如 `sk-123456`） |
| Model | `deepseek-chat` / `deepseek-reasoner` / `deepseek-r1` |

### Python 示例

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="anything"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

---

## 🔧 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/models` | GET | 列出可用模型 |
| `/v1/chat/completions` | POST | 对话补全 |
| `/health` | GET | 健康检查 |

---

## 🐛 测试服务

```bash
python test_api.py --url http://localhost:8080/v1
```

---

## ⚠️ 注意事项

1. **并发限制**：单个 Token 通常只能一路对话，建议准备 5-20 个 Token
2. **稳定性**：网页端逆向容易被检测，Token 可能失效，需定期更新
3. **使用建议**：仅限个人、小团队、低频使用
4. **生产环境**：建议转向官方 API（https://platform.deepseek.com）

---

## 🌐 支持的客户端

- Open WebUI
- SillyTavern
- Cursor / Continue.dev
- LM Studio
- Python OpenAI SDK
