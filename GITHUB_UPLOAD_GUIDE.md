# GitHub 上传指南

## 准备工作

### 1. 安装 Git
如果还没有安装 Git，请从 [https://git-scm.com/](https://git-scm.com/) 下载并安装。

### 2. 配置 Git（首次使用）
```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱@example.com"
```

## 创建 GitHub 仓库

### 1. 登录 GitHub
访问 [https://github.com](https://github.com) 并登录你的账户。

### 2. 创建新仓库
1. 点击右上角的 "+" 按钮
2. 选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `desktop-automation-tool`
   - **Description**: `🚀 一个功能强大的桌面自动化工具，专门用于批量处理压缩文件并提取MP4视频文件`
   - **Public/Private**: 选择 Public（开源项目）
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了）
4. 点击 "Create repository"

## 上传代码到 GitHub

### 方法一：使用命令行（推荐）

1. **打开命令提示符或 PowerShell**
   ```bash
   cd C:\Users\gopal\Documents\desktop-automation-tool
   ```

2. **初始化 Git 仓库**
   ```bash
   git init
   ```

3. **添加所有文件**
   ```bash
   git add .
   ```

4. **创建首次提交**
   ```bash
   git commit -m "🎉 Initial commit: Desktop Automation Tool v1.0

   ✨ Features:
   - 批量压缩文件处理
   - 智能格式检测和转换
   - 个性化输出目录配置
   - 多密码重试机制
   - 失败文件交互式处理
   - 支持多种压缩格式 (.7z, .rar, .zip, .tar.gz, .666z等)
   - MP4视频文件自动提取
   - 图形化用户界面"
   ```

5. **添加远程仓库**
   ```bash
   git remote add origin https://github.com/你的用户名/desktop-automation-tool.git
   ```

6. **推送到 GitHub**
   ```bash
   git branch -M main
   git push -u origin main
   ```

### 方法二：使用 GitHub Desktop

1. 下载并安装 [GitHub Desktop](https://desktop.github.com/)
2. 登录你的 GitHub 账户
3. 点击 "Add an Existing Repository from your Hard Drive"
4. 选择 `C:\Users\gopal\Documents\desktop-automation-tool` 文件夹
5. 填写提交信息并点击 "Commit to main"
6. 点击 "Publish repository"

## 完善仓库信息

### 1. 添加 Topics（标签）
在 GitHub 仓库页面右侧点击设置图标，添加以下标签：
- `python`
- `automation`
- `desktop-tool`
- `file-extraction`
- `compression`
- `gui`
- `tkinter`
- `batch-processing`
- `video-extraction`
- `mp4`

### 2. 设置仓库描述
确保仓库描述清晰明了：
```
🚀 一个功能强大的桌面自动化工具，专门用于批量处理压缩文件并提取MP4视频文件。支持智能格式检测、个性化输出配置和交互式错误处理。
```

### 3. 启用 Issues 和 Discussions
在仓库设置中启用：
- Issues（用于bug报告和功能请求）
- Discussions（用于社区讨论）

## 后续维护

### 更新代码
```bash
# 添加更改
git add .

# 提交更改
git commit -m "✨ Add new feature: 描述你的更改"

# 推送到 GitHub
git push
```

### 创建 Release
1. 在 GitHub 仓库页面点击 "Releases"
2. 点击 "Create a new release"
3. 填写版本信息：
   - **Tag version**: `v1.0.0`
   - **Release title**: `Desktop Automation Tool v1.0.0`
   - **Description**: 详细描述功能和更新内容

## 推广项目

### 1. 完善 README
确保 README.md 包含：
- ✅ 清晰的项目描述
- ✅ 安装说明
- ✅ 使用示例
- ✅ 功能截图（如果有的话）
- ✅ 贡献指南

### 2. 添加徽章
README 中已经包含了状态徽章，这些会让项目看起来更专业。

### 3. 社区推广
- 在相关的 Reddit 社区分享
- 在技术博客上写文章介绍
- 在 Twitter 等社交媒体分享

## 常见问题

### Q: 推送时要求输入用户名和密码
A: GitHub 现在要求使用 Personal Access Token 而不是密码。
1. 访问 GitHub Settings > Developer settings > Personal access tokens
2. 生成新的 token
3. 使用 token 作为密码

### Q: 文件太大无法上传
A: GitHub 单个文件限制 100MB，仓库建议不超过 1GB。
- 使用 `.gitignore` 排除大文件
- 考虑使用 Git LFS 处理大文件

### Q: 如何处理敏感信息
A: 
- 永远不要提交密码、API密钥等敏感信息
- 使用环境变量或配置文件（并加入 .gitignore）
- 如果意外提交了敏感信息，立即更改密钥并清理 Git 历史

## 完成检查清单

- [ ] Git 已安装并配置
- [ ] GitHub 仓库已创建
- [ ] 代码已推送到 GitHub
- [ ] README.md 显示正常
- [ ] LICENSE 文件存在
- [ ] .gitignore 配置正确
- [ ] 仓库描述和标签已设置
- [ ] 第一个 Release 已创建

---

🎉 恭喜！你的开源项目现在已经在 GitHub 上了！