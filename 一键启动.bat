@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"
title 多重解压与 MP4 提取工具

echo ========================================
echo   多重解压与 MP4 提取工具 - 一键启动
echo ========================================
echo.

set "PYTHON_CMD=py -3"
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    set "PYTHON_CMD=python"
    python --version >nul 2>&1
)

%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python 3。
    echo 请先安装 Python，并在安装时勾选 "Add Python to PATH"。
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] 首次运行：创建本地运行环境 .venv ...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败。
        pause
        exit /b 1
    )
)

set "VENV_PY=.venv\Scripts\python.exe"

echo [2/3] 检查依赖...
"%VENV_PY%" -m pip install --upgrade pip >nul
"%VENV_PY%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败。可以稍后重试，或检查网络/Python 环境。
    pause
    exit /b 1
)

where 7z >nul 2>&1
if errorlevel 1 (
    if not exist "%ProgramFiles%\7-Zip\7z.exe" (
        if not exist "%ProgramFiles(x86)%\7-Zip\7z.exe" (
            echo.
            echo [提示] 未检测到 7-Zip。普通 ZIP/7Z 可继续尝试；
            echo        如需更稳定处理 RAR/分卷压缩包，建议安装 7-Zip：
            echo        https://www.7-zip.org/download.html
            echo.
        )
    )
)

echo [3/3] 启动图形界面...
"%VENV_PY%" src\main.py

if errorlevel 1 (
    echo.
    echo [错误] 程序异常退出，请把上方错误信息截图反馈。
    pause
)
