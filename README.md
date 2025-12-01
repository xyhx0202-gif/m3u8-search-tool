# M3U8视频搜索工具

一个基于Flask和Python的M3U8视频搜索和播放工具。

## 项目功能

- 视频搜索功能
- M3U8流播放
- 多集视频支持
- 响应式界面设计

## 技术栈

- **前端**：HTML, CSS, JavaScript, HLS.js
- **后端**：Python, Flask
- **部署**：Cloudflare Pages

## 本地开发

### 环境要求

- Python 3.6+
- 依赖包：Flask, urllib3, requests

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
python web_app.py
```

然后在浏览器中访问 http://localhost:8888

## 部署指南

### 1. 创建GitHub仓库

1. 在GitHub上创建一个新的仓库
2. 初始化Git并上传代码：

```bash
# 初始化Git仓库
git init

# 配置用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 添加文件
git add .

# 提交代码
git commit -m "Initial commit"

# 关联GitHub仓库
git remote add origin https://github.com/yourusername/m3u8-search-tool.git

# 推送代码
git push -u origin main
```

### 2. Cloudflare Pages部署

1. 登录Cloudflare账户
2. 导航到Pages部分
3. 点击"Create a project"
4. 连接到GitHub仓库
5. 配置构建设置：
   - 构建命令：`None`（纯静态文件部署）
   - 发布目录：`.`
   - Python版本：3.8+
6. 点击"Save and Deploy"

## 注意事项

- 此项目使用的M3U8链接可能涉及版权问题，请确保使用合法的内容源
- 部署到Cloudflare Pages时，API功能可能需要额外的Worker配置
- 确保遵守相关法律法规使用本工具

## License

MIT
