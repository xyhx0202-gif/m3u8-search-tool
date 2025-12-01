#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用gitpython初始化Git仓库
"""

import git
import os
import sys

# 获取当前目录
repo_path = os.path.dirname(os.path.abspath(__file__))

try:
    # 初始化Git仓库
    print(f"正在初始化Git仓库在: {repo_path}")
    repo = git.Repo.init(repo_path)
    print("Git仓库初始化成功！")
    
    # 创建.gitignore文件（如果不存在）
    gitignore_path = os.path.join(repo_path, '.gitignore')
    if os.path.exists(gitignore_path):
        print(".gitignore文件已存在")
    else:
        print("警告：.gitignore文件不存在")
    
    # 配置用户名和邮箱（临时配置）
    git_config = repo.git.config
    git_config('--local', 'user.name', 'M3U8 Search Tool')
    git_config('--local', 'user.email', 'm3u8-search@example.com')
    print("Git用户名和邮箱已配置")
    
    # 查看仓库状态
    print("\n仓库状态:")
    print(repo.git.status())
    
    print("\nGit仓库初始化完成！")
    
except Exception as e:
    print(f"初始化Git仓库时出错: {str(e)}")
    sys.exit(1)
