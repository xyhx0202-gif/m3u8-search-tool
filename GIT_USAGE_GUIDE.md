# Git 使用指南

我们已经确认您的系统上安装了Git，位于 `C:\Program Files\Git\cmd\git.exe`。以下是几种使用Git的方法：

## 临时解决方案

在当前PowerShell会话中，您可以：

1. **直接使用完整路径**运行Git命令：
   ```powershell
   & "C:\Program Files\Git\cmd\git.exe" --version
   ```

2. **临时添加到当前会话**的环境变量（重启终端后失效）：
   ```powershell
   $env:PATH = "$env:PATH;C:\Program Files\Git\cmd"
   git --version
   ```

## 永久设置环境变量的方法

### 方法一：通过系统属性设置（推荐）

1. 右键点击「此电脑」或「计算机」→ 选择「属性」
2. 点击「高级系统设置」→ 「环境变量」
3. 在「系统变量」部分找到「Path」变量，点击「编辑」
4. 点击「新建」，添加路径：`C:\Program Files\Git\cmd`
5. 点击「确定」保存所有更改
6. 重启所有打开的命令提示符或PowerShell窗口

### 方法二：使用管理员权限运行批处理文件

我们创建了一个批处理文件 `add_git_to_path.bat`，您可以：

1. 右键点击该文件 → 选择「以管理员身份运行」
2. 按照屏幕提示操作
3. 重启命令提示符或PowerShell窗口

## 验证Git是否正常工作

设置完成后，打开新的命令提示符或PowerShell窗口，运行：

```powershell
git --version
```

如果看到Git版本信息（如 `git version 2.52.0.windows.1`），则表示设置成功。

## 使用Git上传文件到GitHub

一旦Git可用，您可以使用以下命令上传文件：

```powershell
# 进入项目目录
cd d:\1\m3u8-search-tool

# 设置Git用户名和邮箱
git config --global user.name "您的GitHub用户名"
git config --global user.email "您的GitHub邮箱"

# 初始化仓库（如果尚未初始化）
git init

# 添加远程仓库
git remote add origin https://github.com/xyhx0202-gif/m3u8-search-tool.git

# 添加所有文件
git add .

# 提交更改
git commit -m "修复路由规则和配置文件，解决重定向循环问题"

# 推送代码
git push -u origin main
```

如果在推送时遇到权限问题，您可能需要使用GitHub Personal Access Token进行认证。

## 注意事项

- 环境变量更改需要管理员权限
- 修改环境变量后需要重启所有命令提示符或PowerShell窗口
- 如果您使用VPN或公司网络，可能需要额外的配置

祝您使用Git愉快！