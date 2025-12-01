# M3U8视频搜索工具 - GitHub上传指南

## 方法一：使用Git命令行（推荐）

### 步骤1：安装Git

如果您还没有安装Git，可以从官网下载：
[https://git-scm.com/download/win](https://git-scm.com/download/win)

安装时，请确保选择允许在命令行中使用Git的选项。

### 步骤2：准备上传

1. 打开PowerShell或命令提示符（CMD）
2. 进入项目目录：
   ```bash
   cd d:\3
   ```

### 步骤3：初始化Git仓库

```bash
# 初始化本地仓库
git init

# 配置Git用户名和邮箱（替换为您的信息）
git config --global user.name "您的GitHub用户名"
git config --global user.email "您的邮箱@example.com"

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit"
```

### 步骤4：创建GitHub仓库

1. 登录GitHub：[https://github.com](https://github.com)
2. 点击右上角的"+"图标，选择"New repository"
3. 填写仓库名称（建议使用"m3u8-search-tool"）
4. 不要勾选"Initialize this repository with a README"
5. 点击"Create repository"

### 步骤5：连接并推送

在创建仓库后，复制GitHub提供的命令，然后在PowerShell中执行：

```bash
# 添加远程仓库（替换为您的GitHub用户名和仓库名）
git remote add origin https://github.com/您的用户名/m3u8-search-tool.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

## 方法二：使用GitHub Desktop（简单）

### 步骤1：下载GitHub Desktop

[https://desktop.github.com/](https://desktop.github.com/)

### 步骤2：安装并登录

安装完成后，使用您的GitHub账号登录。

### 步骤3：添加项目

1. 点击"File" > "Add Local Repository"
2. 选择"d:\3"文件夹
3. 点击"Add Repository"

### 步骤4：发布到GitHub

1. 点击顶部的"Publish repository"
2. 填写仓库名称（建议使用"m3u8-search-tool"）
3. 选择是否公开或私有
4. 点击"Publish Repository"

## 方法三：使用VS Code的Git集成

### 步骤1：打开项目

使用VS Code打开"d:\3"文件夹。

### 步骤2：初始化仓库

1. 点击左侧的源代码管理图标（Git图标）
2. 点击"Initialize Repository"
3. 输入提交信息（如"Initial commit"）
4. 点击"√"提交

### 步骤3：发布到GitHub

1. 点击"Publish to GitHub"
2. 填写仓库信息
3. 点击"Publish Repository"

## 完成后继续部署

代码上传到GitHub后，您可以继续进行Cloudflare Pages部署：

1. 登录Cloudflare：[https://dash.cloudflare.com](https://dash.cloudflare.com)
2. 进入Pages
3. 点击"Connect to Git"
4. 选择您的GitHub仓库
5. 配置构建设置：
   - 构建命令：留空
   - 发布目录：/（根目录）
   - 环境变量：无需特殊设置
6. 点击"Save and Deploy"

## 遇到问题？

如果在上传过程中遇到问题，请参考以下常见解决方案：

1. **Git未找到错误**：重新安装Git，确保添加到系统PATH
2. **权限错误**：确保您的GitHub账号有正确的权限
3. **网络问题**：检查您的网络连接，可能需要配置代理

详细的部署指南请参考：`d:\3\DEPLOYMENT_GUIDE.md`

祝您部署顺利！