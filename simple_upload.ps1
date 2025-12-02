#!/usr/bin/env powershell
# 简化版GitHub上传脚本 - 使用Git完整路径

# 配置
$gitExe = "C:\Program Files\Git\cmd\git.exe"
$username = "xyhx0202-gif"
$repo_name = "m3u8-search-tool"
$remote_url = "https://github.com/$username/$repo_name.git"

Write-Output "=== GitHub 上传工具 ==="
Write-Output "Git路径: $gitExe"
Write-Output "仓库: $remote_url"

# 检查Git可执行文件
if (-not (Test-Path $gitExe)) {
    Write-Output "错误: 找不到Git可执行文件"
    pause
    exit 1
}

# 执行Git命令的函数
function Execute-Git($cmd) {
    Write-Output "\n执行: git $cmd"
    & $gitExe $cmd.Split(' ')
    return $LASTEXITCODE
}

# 初始化Git仓库（如果需要）
if (-not (Test-Path ".git")) {
    Write-Output "\n初始化Git仓库..."
    Execute-Git "init"
    Execute-Git "config user.name '$username'"
    Execute-Git "config user.email '$username@example.com'"
    Execute-Git "remote add origin $remote_url"
}

# 添加所有文件
Write-Output "\n添加文件到暂存区..."
Execute-Git "add ."

# 提交更改
Write-Output "\n提交更改..."
Execute-Git "commit -m '上传m3u8-search-tool项目'"

# 创建并推送分支
Write-Output "\n创建main分支..."
Execute-Git "checkout -b main"

Write-Output "\n推送代码到GitHub..."
Write-Output "注意: 如果需要认证，请在弹出的窗口中输入GitHub凭据"
Execute-Git "push -u origin main"

Write-Output "\n=== 操作完成 ==="
Write-Output "如果遇到认证问题，请手动运行Git推送命令并输入凭据"