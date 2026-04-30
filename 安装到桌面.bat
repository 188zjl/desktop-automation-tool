@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo 正在创建桌面快捷方式...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$desktop=[Environment]::GetFolderPath('Desktop');" ^
  "$shortcut=(New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $desktop '多重解压与MP4提取工具.lnk'));" ^
  "$shortcut.TargetPath=(Join-Path '%~dp0' '一键启动.bat');" ^
  "$shortcut.WorkingDirectory='%~dp0';" ^
  "$shortcut.IconLocation=\"$env:SystemRoot\System32\shell32.dll,46\";" ^
  "$shortcut.Save();"

if errorlevel 1 (
    echo [错误] 创建快捷方式失败。
    pause
    exit /b 1
)

echo [完成] 已在桌面创建快捷方式：多重解压与MP4提取工具
pause
