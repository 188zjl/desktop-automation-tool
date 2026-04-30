# 多重解压与 MP4 提取工具

面向普通 Windows 用户的懒人版压缩包处理工具：批量选择压缩包后，自动识别格式、递归解压内部压缩包，并把 MP4 视频提取到指定目录。

## 懒人使用

### 方式 1：下载发布版 EXE（推荐）

打开 Releases 页面，下载 `desktop-automation-tool-windows.zip`，解压后双击：

```text
多重解压与MP4提取工具.exe
```

Releases 地址：

```text
https://github.com/188zjl/desktop-automation-tool/releases
```

> 说明：RAR、分卷包等复杂格式建议同时安装 7-Zip。程序会自动识别常见 7-Zip 安装位置。

### 方式 2：下载源码后双击启动

如果没有发布版，或者想直接运行源码：

1. 下载本仓库 ZIP 并解压。
2. 双击根目录：

```text
一键启动.bat
```

脚本会自动创建 `.venv`、安装依赖并启动图形界面。

可选：双击 `安装到桌面.bat`，会创建桌面快捷方式。

## 支持格式

- `.zip`
- `.rar`
- `.7z`
- `.666z`
- `.001`
- `.part1.rar`
- `.tar.gz`
- `.tgz`
- `.tar.bz2`
- `.tar.xz`
- `.tar`

程序会结合扩展名和文件头识别真实格式，尽量兼容“后缀写错/非标准后缀”的压缩包。

## 主要功能

- 批量选择多个压缩包。
- 自动递归解压内部压缩包。
- 自动提取所有 `.mp4` 文件。
- 统一输出或每个源文件独立输出。
- 支持手动填写默认密码和备用密码。
- 无需记命令，根目录双击即可运行。
- 窗口支持“紧凑 / 标准 / 宽屏 / 最大化”快捷切换。
- 处理完成后一键打开输出目录。

## 密码说明

公开上传版默认不内置任何站点或个人解压密码。

如遇加密压缩包，请在界面里填写：

- 默认密码
- 备用密码，多个密码用英文逗号分隔

## 安装要求

### 使用 EXE

- Windows 10/11
- 建议安装 7-Zip：<https://www.7-zip.org/download.html>

### 使用源码

- Windows 10/11
- Python 3.7+
- 建议安装 7-Zip

依赖会由 `一键启动.bat` 自动安装。

## 开发/打包

安装依赖：

```bat
scripts\install_dependencies.bat
```

源码运行：

```bat
scripts\run.bat
```

本地打包 EXE：

```bat
打包EXE.bat
```

GitHub Actions 会在推送到 `main` 或推送 `v*` 标签时自动构建 Windows 便携 ZIP。推送标签时会自动发布 Release。

## 项目结构

```text
desktop-automation-tool/
├── src/main.py
├── scripts/
│   ├── run.bat
│   ├── install_dependencies.bat
│   └── build_windows_exe.ps1
├── docs/
├── tests/
├── 一键启动.bat
├── 安装到桌面.bat
├── 打包EXE.bat
├── requirements.txt
└── README.md
```

## License

MIT
