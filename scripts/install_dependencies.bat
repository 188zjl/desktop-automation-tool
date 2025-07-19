@echo off
chcp 65001 >nul
title 桌面自动化脚本 - 依赖库安装器

echo ========================================
echo    桌面自动化脚本 - 依赖库安装器
echo ========================================
echo.

:: 检查Python是否安装
echo [1/5] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python环境！
    echo.
    echo 请先安装Python 3.7或更高版本：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载最新版本的Python
    echo 3. 安装时请勾选 "Add Python to PATH"
    echo 4. 安装时请勾选 "Install tkinter"
    echo.
    pause
    exit /b 1
)

python --version
echo [成功] Python环境检测正常
echo.

:: 升级pip
echo [2/5] 升级pip包管理器...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [警告] pip升级失败，继续使用当前版本
) else (
    echo [成功] pip升级完成
)
echo.

:: 安装py7zr库
echo [3/5] 安装py7zr库（7z文件支持）...
pip install py7zr
if %errorlevel% neq 0 (
    echo [错误] py7zr库安装失败
    echo 尝试使用国内镜像源...
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple py7zr
    if %errorlevel% neq 0 (
        echo [错误] py7zr库安装失败，7z文件可能无法处理
    ) else (
        echo [成功] py7zr库安装完成（使用镜像源）
    )
) else (
    echo [成功] py7zr库安装完成
)
echo.

:: 安装rarfile库
echo [4/5] 安装rarfile库（RAR文件支持）...
pip install rarfile
if %errorlevel% neq 0 (
    echo [错误] rarfile库安装失败
    echo 尝试使用国内镜像源...
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple rarfile
    if %errorlevel% neq 0 (
        echo [错误] rarfile库安装失败，RAR文件可能无法处理
    ) else (
        echo [成功] rarfile库安装完成（使用镜像源）
    )
) else (
    echo [成功] rarfile库安装完成
)
echo.

:: 检查tkinter
echo [5/5] 检查tkinter库（GUI界面支持）...
python -c "import tkinter; print('tkinter版本检查通过')" 2>nul
if %errorlevel% neq 0 (
    echo [错误] tkinter库不可用
    echo tkinter通常包含在Python标准安装中
    echo 如果您使用的是精简版Python，请重新安装完整版Python
    echo.
    pause
    exit /b 1
) else (
    echo [成功] tkinter库检查通过
)
echo.

:: 验证所有依赖
echo ========================================
echo 验证依赖库安装状态：
echo ========================================

python -c "
import sys
print(f'Python版本: {sys.version}')
print()

modules = {
    'tkinter': 'GUI界面支持',
    'py7zr': '7z文件解压支持', 
    'rarfile': 'RAR文件解压支持',
    'tarfile': 'tar.gz文件解压支持（内置）',
    'zipfile': 'ZIP文件解压支持（内置）',
    'shutil': '文件操作支持（内置）',
    'threading': '多线程支持（内置）',
    'logging': '日志记录支持（内置）'
}

success_count = 0
total_count = len(modules)

for module, description in modules.items():
    try:
        __import__(module)
        print(f'✓ {module:<12} - {description}')
        success_count += 1
    except ImportError as e:
        print(f'✗ {module:<12} - {description} [安装失败]')

print()
print(f'依赖库状态: {success_count}/{total_count} 个库可用')

if success_count == total_count:
    print('🎉 所有依赖库安装成功！脚本已准备就绪。')
else:
    print('⚠️  部分依赖库安装失败，脚本功能可能受限。')
"

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 现在您可以：
echo 1. 双击 "运行桌面自动化脚本.bat" 启动程序
echo 2. 或者直接运行 "python desktop_automation_script.py"
echo.

pause