#!/usr/bin/env powershell
# 直接使用Git完整路径的上传脚本

# 定义Git完整路径
$gitExe = "C:\Program Files\Git\cmd\git.exe"
$username = "xyhx0202-gif"
$repo_name = "m3u8-search-tool"
$remote_url = "https://github.com/$username/$repo_name.git"

Write-Output "使用Git完整路径上传文件到GitHub"
Write-Output "=================================="
Write-Output "Git路径: $gitExe"
Write-Output "目标仓库: $remote_url"

# 检查Git是否存在
if (-not (Test-Path $gitExe)) {
    Write-Output "错误: 找不到Git可执行文件"
    exit 1
}

# 定义执行Git命令的函数
function Run-GitCommand($command) {
    Write-Output "\n执行: git $command"
    $process = Start-Process -FilePath $gitExe -ArgumentList $command -NoNewWindow -PassThru -RedirectStandardOutput "git_output.txt" -RedirectStandardError "git_error.txt"
    $process.WaitForExit()
    
    # 读取输出
    $output = Get-Content "git_output.txt" -ErrorAction SilentlyContinue
    $errorOutput = Get-Content "git_error.txt" -ErrorAction SilentlyContinue
    
    # 显示输出
    if ($output) {
        Write-Output $output
    }
    if ($errorOutput) {
        Write-Output "错误: $errorOutput"
    }
    
    # 清理临时文件
    Remove-Item "git_output.txt" -ErrorAction SilentlyContinue
    Remove-Item "git_error.txt" -ErrorAction SilentlyContinue
    
    return $process.ExitCode
}

# 检查是否是Git仓库
if (-not (Test-Path ".git")) {
    Write-Output "\n检测到这不是Git仓库，正在初始化..."
    $exitCode = Run-GitCommand "init"
    if ($exitCode -ne 0) {
        Write-Output "初始化Git仓库失败"
        exit 1
    }
    
    # 配置用户信息
    Run-GitCommand "config user.name '$username'"
    Run-GitCommand "config user.email '$username@example.com'"
    
    # 添加远程仓库
    Write-Output "\n添加远程仓库..."
    $exitCode = Run-GitCommand "remote add origin $remote_url"
    if ($exitCode -ne 0) {
        Write-Output "添加远程仓库失败，尝试使用HTTPS而不是SSH..."
        Run-GitCommand "remote remove origin" -ErrorAction SilentlyContinue
        $exitCode = Run-GitCommand "remote add origin $remote_url"
        if ($exitCode -ne 0) {
            Write-Output "无法添加远程仓库，请检查仓库URL是否正确"
        }
    }
} else {
    Write-Output "\n已检测到Git仓库"
    # 确保远程仓库设置正确
    $exitCode = Run-GitCommand "remote -v"
    if ($exitCode -ne 0) {
        Write-Output "\n设置远程仓库..."
        Run-GitCommand "remote add origin $remote_url"
    }
}

# 添加所有文件
Write-Output "\n添加所有文件..."
Run-GitCommand "add ."

# 提交更改
Write-Output "\n提交更改..."
$exitCode = Run-GitCommand "commit -m '修复路由规则和配置文件，解决重定向循环问题'"
if ($exitCode -ne 0) {
    Write-Output "提交失败，可能没有新的更改"
}

# 推送代码
Write-Output "\n推送到GitHub..."
# 先尝试直接推送
$exitCode = Run-GitCommand "push origin main"
if ($exitCode -ne 0) {
    Write-Output "推送失败，尝试创建main分支..."
    Run-GitCommand "checkout -b main"
    $exitCode = Run-GitCommand "push -u origin main"
    if ($exitCode -ne 0) {
        Write-Output "\n推送失败! 这可能是因为需要身份验证。"
        Write-Output "\n手动推送指南:"
        Write-Output "1. 打开命令提示符或PowerShell"
        Write-Output "2. 进入目录: cd d:\1\m3u8-search-tool"
        Write-Output "3. 使用以下命令:"
        Write-Output "   '$gitExe push -u origin main'"
        Write-Output "4. 系统会提示您输入GitHub凭据"
    } else {
        Write-Output "\n推送成功!"
    }
}

Write-Output "\n操作完成!"
Write-Output "注意: 如果遇到认证问题，请尝试手动推送并提供GitHub凭据"