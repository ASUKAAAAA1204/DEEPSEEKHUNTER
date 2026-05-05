@echo off
chcp 65001 >nul
echo ==============================================
echo   DeepSeek 中转站快速启动脚本
echo ==============================================
echo.

set "BASE_DIR=%~dp0"
set "API_PORT=8080"

echo 请选择启动方式:
echo 1. 使用 Docker Compose 启动（推荐）
echo 2. 使用本地二进制启动
echo 3. 测试 API 连接
echo 4. 退出
echo.

set /p "choice=请输入选择 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🚀 启动 Docker Compose...
    cd /d "%BASE_DIR%"
    docker-compose up -d
    echo.
    echo ✅ 服务已启动！
    echo 访问地址: http://localhost:%API_PORT%/v1
    pause
) else if "%choice%"=="2" (
    echo.
    echo ⚠️  请先下载并解压 ds-free-api 二进制文件到当前目录
    echo 下载地址: https://github.com/NIyueeE/ds-free-api/releases
    echo.
    set /p "token=请输入 userToken（多个用逗号分隔）: "
    set "USER_TOKENS=%token%"
    echo 启动本地服务...
    ds-free-api.exe
    pause
) else if "%choice%"=="3" (
    echo.
    echo 🧪 测试 API 连接...
    python test_api.py
    pause
) else if "%choice%"=="4" (
    echo 👋 退出...
    exit /b
) else (
    echo ❌ 无效选择，请重新运行脚本
    pause
)
