# M3U8搜索工具部署说明

本文档提供了将M3U8搜索工具部署到Cloudflare Pages的详细步骤。

## 前提条件

1. GitHub账号
2. Cloudflare账号

## 步骤1：创建GitHub仓库

1. 登录GitHub
2. 点击右上角"+"按钮，选择"New repository"
3. 填写仓库信息：
   - 仓库名称：`m3u8-search-tool`
   - 选择公开或私有
   - 勾选"Add a README file"
   - 点击"Create repository"

## 步骤2：上传项目代码

### 方法1：使用Git命令行

```bash
# 克隆仓库到本地
git clone https://github.com/YOUR_USERNAME/m3u8-search-tool.git

# 复制所有项目文件到克隆的仓库中
# 确保包含以下文件：
# - index_simple.html
# - worker.js
# - _redirects
# - .cloudflare/pages.toml
# - requirements.txt
# - web_app.py

# 进入仓库目录
cd m3u8-search-tool

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: M3U8搜索工具"

# 推送到GitHub
git push origin main
```

### 方法2：直接在GitHub网页上传

1. 进入创建的仓库
2. 点击"Add file" → "Upload files"
3. 拖拽或选择所有项目文件上传
4. 填写提交信息，点击"Commit changes"

## 步骤3：配置Cloudflare Pages

1. 登录Cloudflare账号
2. 在左侧菜单选择"Pages"
3. 点击"Create a project" → "Connect to Git"
4. 选择GitHub并授权访问你的仓库
5. 选择`m3u8-search-tool`仓库
6. 配置构建设置：
   - 生产分支：`main`
   - 构建命令：留空（纯静态网站）
   - 构建输出目录：`.` (根目录)
   - 环境变量：不需要特别设置
7. 点击"Save and Deploy"
8. 等待构建完成

## 步骤4：部署Cloudflare Worker

1. 在Cloudflare左侧菜单选择"Workers & Pages"
2. 点击"Create application" → "Create Worker"
3. 填写Worker名称：`m3u8-search-api`
4. 点击"Edit code"，将`worker.js`文件的内容复制粘贴进去
5. 点击"Deploy"
6. 部署完成后，记录Worker的URL

## 步骤5：配置路由规则

1. 在Cloudflare Pages项目中，选择"Settings" → "Functions"
2. 找到"Routes"部分
3. 添加以下路由规则：
   - 路径：`/api/*` → 指向Worker
   - 路径：`/v1/*` → 指向Worker

## 步骤6：验证部署

1. 打开Cloudflare Pages分配的URL
2. 测试搜索功能是否正常工作
3. 验证视频播放和M3U8链接获取功能

## 步骤7：配置自定义域名（可选）

1. 在Cloudflare Pages项目中，选择"Custom domains"
2. 点击"Setup a custom domain"
3. 输入`m3u8-search-tool.pages.dev`
4. 按照提示完成域名配置

## 常见问题排查

1. **API请求失败**：检查Worker配置和路由规则是否正确
2. **页面无法加载**：确认index_simple.html文件已正确上传
3. **CORS错误**：检查Worker中的CORS头设置是否正确
4. **M3U8播放失败**：验证后端服务是否正常运行

## 注意事项

1. 确保API密钥在前端、Worker和后端保持一致
2. 定期更新项目代码，及时修复安全漏洞
3. 监控Cloudflare Pages和Worker的使用情况和错误日志

如有其他问题，请参考DEPLOYMENT_GUIDE.md和DEPLOYMENT_FIX_GUIDE.md文件。
