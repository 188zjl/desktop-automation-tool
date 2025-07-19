@echo off
chcp 65001 >nul
title 桌面自动化脚本启动器

echo ========================================
echo    桌面自动化脚本 - 压缩包处理工具
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python环境！
    echo 请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [信息] Python环境检测正常
echo.

:: 检查并安装必要的依赖库
echo [信息] 检查依赖库...
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] tkinter库未安装，这通常包含在Python标准库中
    echo 请重新安装Python并确保包含tkinter
    pause
    exit /b 1
)

:: 安装其他必要的库
echo [信息] 安装必要的依赖库...
pip install py7zr rarfile >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 部分依赖库安装可能失败，脚本会尝试自动安装
)

echo [信息] 依赖库检查完成
echo.

:: 运行主脚本
echo [信息] 启动桌面自动化脚本...
echo.
cd /d "%~dp0.."
python src/main.py

:: 检查脚本运行结果
if %errorlevel% neq 0 (
    echo.
    echo [错误] 脚本运行出现问题
    echo 请检查错误信息或联系技术支持
    echo.
    pause
) else (
    echo.
    echo [信息] 脚本运行完成
)

pause