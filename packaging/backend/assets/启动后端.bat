@echo off
chcp 65001 >nul
title PersonaWeaver 后端服务
echo ============================================================
echo  PersonaWeaver 后端服务启动中...
echo ============================================================
if not exist ".env" (
    echo [警告] 未找到 .env 配置文件！
    echo 请先把 .env.example 复制为 .env 并填入你的 API key。
    echo.
    pause
    exit /b 1
)
personaweaver-backend.exe --port 8000
pause
