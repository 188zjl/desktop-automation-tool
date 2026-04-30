param(
    [string]$Python = ""
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

if (-not $Python) {
    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        $Python = "py -3"
    } else {
        $pythonExe = Get-Command python -ErrorAction SilentlyContinue
        if (-not $pythonExe) {
            throw "未找到 Python。请先安装 Python 3，并勾选 Add Python to PATH。"
        }
        $Python = "python"
    }
}

Write-Host "[1/4] 创建打包环境..."
if (-not (Test-Path -LiteralPath ".venv-build\Scripts\python.exe")) {
    Invoke-Expression "$Python -m venv .venv-build"
}

$BuildPython = Join-Path $RepoRoot ".venv-build\Scripts\python.exe"

Write-Host "[2/4] 安装依赖和 PyInstaller..."
& $BuildPython -m pip install --upgrade pip
& $BuildPython -m pip install -r requirements.txt pyinstaller

Write-Host "[3/4] 清理旧产物..."
Remove-Item -LiteralPath "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath "dist" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "[4/4] 打包 Windows EXE..."
& $BuildPython -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name "多重解压与MP4提取工具" `
    --collect-all py7zr `
    --collect-all rarfile `
    "src\main.py"

$ExePath = Join-Path $RepoRoot "dist\多重解压与MP4提取工具.exe"
if (-not (Test-Path -LiteralPath $ExePath)) {
    throw "打包失败：未找到 $ExePath"
}

Write-Host ""
Write-Host "[完成] EXE 已生成：$ExePath"
Write-Host "提示：如需处理 RAR/分卷包，建议用户安装 7-Zip。"
