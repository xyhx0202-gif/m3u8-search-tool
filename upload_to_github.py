#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub仓库自动上传工具
"""

import os
import sys
import subprocess
import time

def run_command(cmd, cwd=None):
    """运行命令并返回输出"""
    print(f"执行命令: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True
        )
        return result
    except Exception as e:
        print(f"命令执行失败: {str(e)}")
        return None

def check_git_installed():
    """检查Git是否安装"""
    result = run_command("git --version")
    if result and result.returncode == 0:
        print(f"Git已安装: {result.stdout.strip()}")
        return True
    else:
        print("Git未安装或无法访问。正在尝试使用其他方法...")
        return False

def setup_git_config(username, email):
    """配置Git用户名和邮箱"""
    run_command(f"git config --global user.name \"{username}\"")
    run_command(f"git config --global user.email \"{email}\"")
    print(f"Git配置已设置: {username} <{email}>")

def initialize_git_repo():
    """初始化Git仓库"""
    run_command("git init")
    run_command("git add .")
    run_command("git commit -m \"Initial commit\"")
    print("Git仓库已初始化并完成首次提交")

def add_remote_repo(remote_url):
    """添加远程仓库"""
    run_command(f"git remote add origin {remote_url}")
    print(f"已添加远程仓库: {remote_url}")

def push_to_github():
    """推送到GitHub"""
    # 尝试设置上游分支并推送
    result = run_command("git push -u origin main")
    if result and result.returncode != 0:
        # 如果main分支不存在，尝试推送master分支
        print("尝试使用master分支推送...")
        run_command("git branch -M master")
        result = run_command("git push -u origin master")
        
    if result and result.returncode == 0:
        print("✅ 代码成功推送到GitHub！")
        return True
    else:
        print("❌ 推送失败，请手动处理以下问题:")
        if result:
            print(f"错误输出: {result.stderr}")
        print("\n请按照以下步骤手动完成推送:")
        print("1. 确保GitHub仓库已创建")
        print("2. 使用浏览器登录GitHub")
        print("3. 手动推送代码或使用GitHub Desktop")
        return False

def generate_manual_instructions(username, repo_name):
    """生成手动操作指南"""
    instructions = f"""
📋 手动上传指南

如果自动上传失败，请按照以下步骤手动操作：

1. 在浏览器中打开 https://github.com/new
2. 创建新仓库:
   - 仓库名称: {repo_name}
   - 不要初始化README.md
3. 使用Git命令行（如果已安装）:
   ```bash
   cd d:\3
   git init
   git config --global user.name "{username}"
   git config --global user.email "{username}@example.com"
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/{username}/{repo_name}.git
   git branch -M main
   git push -u origin main
   ```
4. 或者使用GitHub Desktop:
   - 下载并安装: https://desktop.github.com/
   - 点击"Add Existing Repository"
   - 选择"d:\3"文件夹
   - 点击"Publish repository"
   - 填写仓库信息并发布

5. 或者使用VS Code的Git集成:
   - 打开项目文件夹
   - 点击源代码管理图标
   - 初始化仓库
   - 提交更改
   - 发布到GitHub
   """
    
    # 保存指南到文件
    with open(r"d:\3\MANUAL_UPLOAD_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print(instructions)
    print("\n指南已保存到: d:\3\MANUAL_UPLOAD_GUIDE.md")

def main():
    print("🚀 M3U8视频搜索工具 - GitHub上传工具")
    print("=" * 50)
    
    # 自动填充参数，避免交互式输入
    username = "xyhx0202-gif"
    print(f"使用GitHub用户名: {username}")
    
    repo_name = "m3u8-search-tool"
    print(f"使用仓库名称: {repo_name}")
    
    email = f"{username}@example.com"
    print(f"使用邮箱: {email}")
    
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    
    print(f"\n准备上传到: {remote_url}")
    print("请确保您已经在GitHub上创建了这个仓库，或者准备使用上述用户名和仓库名创建新仓库")
    
    # 检查Git安装
    if check_git_installed():
        # 设置Git配置
        setup_git_config(username, email)
        
        # 初始化仓库
        initialize_git_repo()
        
        # 添加远程仓库
        add_remote_repo(remote_url)
        
        # 推送代码
        success = push_to_github()
        
        if not success:
            # 生成手动指南
            generate_manual_instructions(username, repo_name)
    else:
        # Git未安装，生成手动指南
        print("\n由于Git未安装，无法执行自动上传操作")
        generate_manual_instructions(username, repo_name)
    
    print("\n完成！请按照上述指南完成GitHub仓库上传")

if __name__ == "__main__":
    main()
