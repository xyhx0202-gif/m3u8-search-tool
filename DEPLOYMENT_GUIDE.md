# Cloudflare部署详细指南

## 步骤1：创建GitHub仓库

1. 登录您的GitHub账户
2. 点击右上角的 "+" 图标，选择 "New repository"
3. 填写仓库信息：
   - 仓库名称：`m3u8-search-tool`
   - 描述：M3U8视频搜索工具
   - 选择公开或私有
   - 不要初始化README.md（因为我们已有）
4. 点击 "Create repository"

## 步骤2：上传本地代码到GitHub

（如果系统中Git已正确安装）在项目目录中执行以下命令：

```bash
# 初始化Git仓库（如果尚未初始化）
git init

# 配置Git用户信息
git config --global user.name "您的GitHub用户名"
git config --global user.email "您的GitHub邮箱"

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit"

# 关联GitHub仓库（替换为您的仓库URL）
git remote add origin https://github.com/您的用户名/m3u8-search-tool.git

# 推送到GitHub
git push -u origin main
```

## 步骤3：部署到Cloudflare Pages

1. 登录您的Cloudflare账户
2. 在侧边栏中选择 "Pages"
3. 点击 "Create a project"
4. 选择 "Connect to Git"
5. 选择 "GitHub" 并授权Cloudflare访问您的仓库
6. 从仓库列表中选择 `m3u8-search-tool`
7. 配置构建和部署设置：
   - **项目名称**：可以保持默认或自定义
   - **生产分支**：`main`
   - **构建命令**：留空（这是一个静态网站）
   - **发布目录**：`.`
   - **环境变量**：无需设置特殊环境变量
8. 点击 "Save and Deploy"
9. Cloudflare将开始构建和部署您的网站

## 步骤4：部署Cloudflare Worker（用于API功能）

1. 在Cloudflare仪表板中，导航到 "Workers & Pages"
2. 点击 "Create application"，然后选择 "Worker"
3. 命名您的Worker（例如：`m3u8-api-worker`）
4. 点击 "Create worker"
5. 在编辑器中，复制粘贴 `worker.js` 文件的内容
6. 点击 "Deploy"

## 步骤5：更新重定向规则

1. 在Cloudflare Pages项目设置中，导航到 "Settings > Functions > Redirect Rules"
2. 点击 "Add rule"
3. 添加以下重定向规则：
   - **规则名称**：`API Redirect`
   - **路径模式**：`/api/*` 和 `/v1/*`
   - **目标URL**：`https://您的worker名称.您的子域.workers.dev/:splat`
   - **状态码**：200（重写）
4. 保存规则

## 步骤6：验证部署

1. 部署完成后，Cloudflare会提供一个预览URL
2. 点击预览URL访问您的网站
3. 测试搜索功能和视频播放功能
4. 确保API请求能够正确转发到Worker

## 步骤7：（可选）设置自定义域名

1. 在Cloudflare Pages项目设置中，导航到 "Custom domains"
2. 点击 "Set up a custom domain"
3. 按照提示添加您的自定义域名
4. 确保您的域名DNS已正确配置为指向Cloudflare

## 故障排除

### 常见问题及解决方案

1. **API请求失败**
   - 检查Worker是否部署成功
   - 验证_redirects文件配置是否正确
   - 确认API密钥在前端和Worker中保持一致

2. **视频无法播放**
   - 检查M3U8链接是否有效
   - 确保HLS.js已正确加载
   - 检查浏览器控制台是否有错误信息

3. **部署构建失败**
   - 确保没有语法错误
   - 验证发布目录设置是否正确
   - 检查Cloudflare日志获取详细错误信息

## 注意事项

- 此项目的API功能在Cloudflare上可能受到一些限制
- 对于高流量场景，考虑升级Cloudflare计划
- 定期更新代码和依赖包以确保安全性
