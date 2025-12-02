#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的GitHub上传工具
"""

import os
import subprocess
import sys

def run_cmd(cmd):
    """运行命令并显示输出"""
    print(f"\n执行: {cmd}")
    try:
        # 使用shell=True在Windows上执行命令
        process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        # 实时显示输出
        stdout_lines = []
        stderr_lines = []
        
        while True:
            stdout = process.stdout.readline()
            stderr = process.stderr.readline()
            
            if stdout:
                print(stdout.strip())
                stdout_lines.append(stdout)
            if stderr:
                print(f"错误: {stderr.strip()}")
                stderr_lines.append(stderr)
            
            if process.poll() is not None:
                # 读取剩余输出
                for line in process.stdout.readlines():
                    print(line.strip())
                    stdout_lines.append(line)
                for line in process.stderr.readlines():
                    print(f"错误: {line.strip()}")
                    stderr_lines.append(line)
                break
        
        return process.returncode, ''.join(stdout_lines), ''.join(stderr_lines)
    except Exception as e:
        print(f"命令执行异常: {str(e)}")
        return -1, "", str(e)

def main():
    print("简单的GitHub上传工具")
    print("=" * 50)
    
    # GitHub配置
    username = "xyhx0202-gif"
    repo_name = "m3u8-search-tool"
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    print(f"目标仓库: {remote_url}")
    
    # 检查是否存在.git目录
    git_dir = os.path.join(current_dir, ".git")
    if not os.path.isdir(git_dir):
        print("\n检测到这不是Git仓库，正在初始化...")
        # 初始化Git仓库
        returncode, stdout, stderr = run_cmd("git init")
        if returncode != 0:
            print("初始化Git仓库失败")
            return
        
        # 配置Git用户名和邮箱
        run_cmd(f"git config user.name \"{username}\")
        run_cmd(f"git config user.email \"{username}@example.com\"")
        
        # 添加远程仓库
        run_cmd(f"git remote add origin {remote_url}")
    else:
        print("\n已检测到Git仓库")
    
    # 添加所有文件
    print("\n添加所有文件...")
    run_cmd("git add .")
    
    # 提交更改
    print("\n提交更改...")
    returncode, stdout, stderr = run_cmd("git commit -m \"修复路由规则和配置文件，解决重定向循环问题\"")
    if returncode != 0:
        print("提交失败，可能没有新的更改")
    
    # 推送代码
    print("\n推送到GitHub...")
    # 尝试推送，如果失败可能需要创建分支
    returncode, stdout, stderr = run_cmd("git push origin main")
    if returncode != 0:
        print("推送失败，尝试创建main分支...")
        run_cmd("git checkout -b main")
        returncode, stdout, stderr = run_cmd("git push -u origin main")
        if returncode != 0:
            print("\n推送失败！请检查GitHub凭证或手动推送")
            print("手动推送命令:")
            print(f"git push -u origin main")
        else:
            print("\n推送成功！")
    else:
        print("\n推送成功！")
    
    print("\n操作完成！")

if __name__ == "__main__":
    main()