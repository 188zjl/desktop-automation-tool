# 🚀 Desktop Automation Tool

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

一个功能强大的桌面自动化工具，专门用于批量处理压缩文件并提取MP4视频文件。支持多种压缩格式，具备智能格式检测、个性化输出目录配置和交互式错误处理等高级功能。

## ✨ 主要特性

### 🎯 核心功能
- **批量文件处理**: 支持同时选择和处理多个压缩文件
- **多格式支持**: 支持 `.tar.gz`, `.zip`, `.rar`, `.7z`, `.666z`, `.001`, `.tar.bz2`, `.tar.xz` 等格式
- **智能格式检测**: 自动检测文件真实格式，智能转换非标准格式（如 `.666z` → `.7z`）
- **MP4视频提取**: 递归搜索并提取所有MP4视频文件到指定目录

### 🛠️ 高级功能
- **个性化输出目录**: 为每个文件单独选择输出目录
- **多密码重试机制**: 支持多个密码尝试，密码失败时提供交互式输入
- **失败文件处理**: 批量处理完成后交互式处理失败文件
- **智能清理**: 自动清理中间临时文件
- **进度显示**: 实时显示处理进度和详细日志

### 🎨 用户界面
- **图形化界面**: 基于Tkinter的直观GUI界面
- **输出模式选择**: 支持统一输出和个性化输出两种模式
- **高级配置**: 密码设置、目录配置等高级选项
- **实时反馈**: 处理状态和错误信息实时显示

## 📦 安装

### 系统要求
- Windows 10/11
- Python 3.7 或更高版本
- 7-Zip (用于处理7z和rar文件)

### 快速安装

1. **克隆仓库**
```bash
git clone https://github.com/yourusername/desktop-automation-tool.git
cd desktop-automation-tool
```

2. **安装依赖**
```bash
# 使用脚本自动安装
scripts/install_dependencies.bat

# 或手动安装
pip install -r requirements.txt
```

3. **安装7-Zip**
- 下载并安装 [7-Zip](https://www.7-zip.org/download.html)
- 确保7z.exe在系统PATH中或位于默认安装路径

## 🚀 使用方法

### 快速启动
```bash
# 使用启动脚本
scripts/run.bat

# 或直接运行Python脚本
python src/main.py
```

### 基本使用流程

1. **启动程序**: 运行脚本后会打开图形化界面
2. **选择文件**: 点击"选择文件"按钮，支持多选压缩文件
3. **配置输出**: 选择输出模式（统一输出/个性化输出）
4. **设置密码**: 配置默认密码和备用密码（可选）
5. **开始处理**: 点击"开始处理"按钮开始批量处理
6. **处理失败文件**: 处理完成后可交互式处理失败的文件

### 高级功能使用

#### 个性化输出目录
```python
# 在GUI中选择"个性化输出"模式
# 为每个文件单独配置输出目录
```

#### 智能格式检测
```python
# 程序自动检测文件格式
# 自动转换 .666z → .7z
# 支持文件头分析
```

#### 多密码重试
```python
# 配置多个密码
passwords = ["password1", "password2", "123456"]
# 程序会依次尝试所有密码
```

## 📁 项目结构

```
desktop-automation-tool/
├── src/
│   └── main.py                 # 主程序文件
├── scripts/
│   ├── run.bat                 # 启动脚本
│   └── install_dependencies.bat # 依赖安装脚本
├── tests/
│   └── test_main.py           # 测试文件
├── docs/
│   ├── usage.md               # 使用说明
│   ├── project_summary.md     # 项目总结
│   └── test_report.md         # 测试报告
├── README.md                  # 项目说明
├── requirements.txt           # 依赖列表
└── LICENSE                    # 开源许可证
```

## 🧪 测试

运行测试套件：
```bash
python tests/test_main.py
```

测试覆盖的功能：
- ✅ 智能格式检测
- ✅ 个性化输出目录设置
- ✅ 失败文件跟踪
- ✅ 多密码重试机制

## 📋 支持的文件格式

| 格式 | 扩展名 | 支持状态 | 备注 |
|------|--------|----------|------|
| TAR.GZ | `.tar.gz` | ✅ | 完全支持 |
| ZIP | `.zip` | ✅ | 完全支持 |
| RAR | `.rar` | ✅ | 需要7-Zip |
| 7Z | `.7z` | ✅ | 支持密码 |
| 非标准7Z | `.666z` | ✅ | 自动转换 |
| 分卷压缩 | `.001` | ✅ | 自动识别 |
| TAR.BZ2 | `.tar.bz2` | ✅ | 完全支持 |
| TAR.XZ | `.tar.xz` | ✅ | 完全支持 |

## 🔧 配置选项

### 密码配置
```python
# 默认密码列表
default_passwords = [
    "123456", "password", "123", "000000",
    "111111", "666666", "888888", "999999"
]
```

### 输出目录配置
```python
# 统一输出模式
unified_output = True
output_directory = "C:/Users/Desktop/extracted_videos"

# 个性化输出模式
individual_outputs = {
    "file1.7z": "C:/Output1/",
    "file2.rar": "C:/Output2/"
}
```

## 🐛 故障排除

### 常见问题

**Q: 7z文件解压失败**
- A: 确保安装了7-Zip并且在系统PATH中

**Q: 密码错误导致解压失败**
- A: 使用高级密码设置功能，添加更多密码选项

**Q: 找不到MP4文件**
- A: 检查压缩文件是否包含MP4文件，程序会递归搜索所有子目录

**Q: 程序运行缓慢**
- A: 大文件处理需要时间，请耐心等待，可查看日志了解进度

### 日志文件
程序运行时会生成详细日志，包含：
- 文件处理状态
- 错误信息
- 密码尝试记录
- 提取文件列表

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 开发指南
- 遵循PEP 8代码规范
- 添加适当的注释和文档
- 编写测试用例
- 更新README文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [7-Zip](https://www.7-zip.org/) - 强大的压缩工具
- [Python](https://www.python.org/) - 优秀的编程语言
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI框架

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/desktop-automation-tool/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/desktop-automation-tool/discussions)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！