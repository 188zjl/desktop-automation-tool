@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0.."
title 多重解压与 MP4 提取工具 - 依赖安装

set "PYTHON_CMD=py -3"
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    set "PYTHON_CMD=python"
)

%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python 3，请先安装 Python：
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [信息] 创建虚拟环境 .venv ...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo [错误] 虚拟环境创建失败。
        pause
        exit /b 1
    )
)

echo [信息] 安装依赖...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败。
    pause
    exit /b 1
)

echo [完成] 依赖安装成功。之后可双击根目录“一键启动.bat”。
pause
