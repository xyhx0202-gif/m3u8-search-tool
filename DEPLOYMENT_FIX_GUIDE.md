# M3U8搜索工具部署修复指南

本文档提供了修复Cloudflare Pages部署访问问题的详细步骤，针对之前部署后无法访问`https://m3u8-search-tool.pages.dev/index_simple`的问题。

## 问题分析

经过检查，发现以下问题需要修复：

1. `_redirects`文件中的API请求重定向规则使用了占位符URL，导致API请求无法正确路由到Cloudflare Worker
2. 页面路径访问配置可能不正确

## 已修复的配置

### 1. _redirects文件修复

已将`_redirects`文件中的占位符URL修改为正确的Cloudflare Pages内部路由格式：

```
# Cloudflare Pages 路由规则

# 将所有API请求重定向到Cloudflare Worker
/api/* /api/:splat 200
/v1/* /api/v1/:splat 200

# 单页应用路由
/* /index_simple.html 200
```

### 2. 前端配置检查

`index_simple.html`中的API配置已经正确设置：

```javascript
// Cloudflare Pages部署配置
const API_BASE_URL = ''; // 在Cloudflare Pages上，API请求将通过_redirects文件处理
const USE_CLOUDFLARE_WORKER = true; // 是否使用Cloudflare Worker处理API请求
```

## 重新部署步骤

### 1. 推送更新到GitHub仓库

```bash
# 确保在项目根目录
cd d:\3

# 添加修改的文件
git add _redirects

# 提交更改
git commit -m "修复Cloudflare Pages路由配置"

# 推送更改到GitHub
git push origin main
```

### 2. 在Cloudflare Pages中重新部署

1. 登录到[Cloudflare Pages](https://dash.cloudflare.com/?to=/:account/pages)
2. 找到`m3u8-search-tool`项目
3. 点击右上角的"重新部署"按钮
4. 选择"使用最新代码"选项
5. 点击"重新部署"开始部署过程

### 3. 配置Cloudflare Worker

确保已在Cloudflare Pages项目中正确配置了Worker：

1. 在项目设置中，找到"Functions"或"Workers"部分
2. 确保`worker.js`文件被正确识别和部署
3. 检查Worker的API路径是否与前端请求匹配（`/api/*`和`/v1/*`）

## 验证部署

部署完成后，按照以下步骤验证：

1. 访问应用主页：`https://m3u8-search-tool.pages.dev/`
2. 测试搜索功能是否正常工作
3. 检查浏览器开发者工具的控制台是否有错误信息
4. 验证API请求是否正确路由到Worker

## 常见问题排查

### 1. API请求失败

如果API请求仍然失败：
- 检查Worker是否正确部署和运行
- 验证Worker日志中是否有错误信息
- 确认`_redirects`规则是否生效

### 2. 页面无法加载

如果页面无法加载：
- 确认`index_simple.html`文件存在且内容正确
- 检查部署日志是否有错误
- 验证`/* /index_simple.html 200`规则是否正确配置

### 3. 播放器功能异常

如果播放器功能异常：
- 确认HLS.js库是否正确加载
- 检查M3U8链接是否有效
- 验证浏览器是否支持HLS播放

## 额外提示

1. 部署后，建议清除浏览器缓存再访问网站
2. 如果使用自定义域名，确保DNS设置正确
3. 定期检查Cloudflare Pages和Worker的日志，及时发现并解决问题

按照以上步骤操作后，应用应该能够正常访问和使用。如果仍然遇到问题，请联系Cloudflare支持获取进一步帮助。