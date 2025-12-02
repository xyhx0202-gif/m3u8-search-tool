#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3U8搜索工具 - 简化Web版（使用内置http.server）
"""

import http.server
import socketserver
import socket
import urllib.request
import urllib.parse
import re
import ssl
import json
import os
import base64
from urllib.parse import parse_qs, urlparse

# 全局变量用于API请求频率限制
api_requests = {}

# 端口配置
PORT = 8888
# API密钥用于验证请求
API_SECRET_KEY = "Xm3U8V1d30p1D"

def generate_api_token():
    """生成API调用的临时token"""
    import time
    timestamp = str(int(time.time()))
    # 简单的token生成：时间戳 + 密钥的部分字符拼接
    token = timestamp + "_" + API_SECRET_KEY[2:8]
    return token

def validate_api_token(token):
    """验证API token是否有效"""
    try:
        import time
        if not token or '_' not in token:
            return False
        
        timestamp_str, secret_part = token.split('_')
        timestamp = int(timestamp_str)
        current_time = int(time.time())
        
        # 验证时间戳是否在5分钟内
        if abs(current_time - timestamp) > 300:
            return False
        
        # 验证密钥部分
        return secret_part == API_SECRET_KEY[2:8]
    except Exception:
        return False

def check_rate_limit(client_ip):
    """检查API请求频率限制"""
    import time
    current_time = time.time()
    
    if client_ip not in api_requests:
        api_requests[client_ip] = []
    
    # 清理5分钟前的请求记录
    api_requests[client_ip] = [t for t in api_requests[client_ip] if current_time - t < 300]
    
    # 检查是否超过频率限制（每分钟最多30次请求）
    recent_requests = [t for t in api_requests[client_ip] if current_time - t < 60]
    if len(recent_requests) >= 30:
        return False
    
    # 记录本次请求
    api_requests[client_ip].append(current_time)
    return True

def encrypt_m3u8_url(url):
    """加密M3U8地址（简单实现）"""
    # 这里只是一个简单的演示，实际项目中可以使用更复杂的加密算法
    import base64
    return base64.b64encode(url.encode()).decode()

def decrypt_m3u8_url(encrypted_url):
    """简化的M3U8地址处理"""
    # 不再进行解密，直接返回原始URL
    return encrypted_url

class M3U8SearchHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/' or self.path == '/index.html':
            # 返回主页
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # 读取现有的HTML文件
            try:
                with open('index_simple.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                self.wfile.write(html_content.encode('utf-8'))
            except FileNotFoundError:
                # 如果文件不存在，创建基础文件
                create_simple_html()
                with open('index_simple.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path.startswith('/api/') or self.path.startswith('/v1/'):
            # 处理API请求（支持原始路径和混淆路径）
            self.handle_api_request()
        else:
            # 静态文件服务
            super().do_GET()
    
    def do_POST(self):
        """处理POST请求"""
        if self.path.startswith('/api/') or self.path.startswith('/v1/'):
            self.handle_api_request()
        else:
            self.send_error(404, "File not found")
    
    def handle_api_request(self):
        """处理API请求（添加混淆和验证）"""
        # 1. 验证请求头中的特殊标识（支持前端使用的X-API-Key）
        x_api_key = self.headers.get('X-API-Key')
        
        # 支持两种请求头验证方式
        if not x_api_key or x_api_key != 'm3u8_viewer_key':
            self.send_response(403)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Forbidden: Invalid API key'}).encode('utf-8'))
            return
        
        # 2. 验证API token
        api_token = self.headers.get('X-API-Token')
        if not validate_api_token(api_token):
            # 返回新的token
            new_token = generate_api_token()
            self.send_response(401)
            self.send_header('X-New-Token', new_token)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Token expired', 'new_token': new_token}).encode('utf-8'))
            return
        
        # 3. 检查请求频率限制
        client_ip = self.client_address[0]
        if not check_rate_limit(client_ip):
            self.send_response(429)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Rate limit exceeded'}).encode('utf-8'))
            return
        
        # 4. 读取请求数据（支持GET和POST）
        data = {}
        
        if self.command == 'GET':
            # 处理GET请求的查询参数
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # 转换为普通字典
            for key, values in query_params.items():
                data[key] = values[0] if len(values) == 1 else values
                
            # 针对/v1/query路径，将q参数转换为video_name
            if self.path.startswith('/v1/query') and 'q' in data:
                data['video_name'] = data['q']
            # 针对/v1/stream路径，将id参数转换为video_id
            elif self.path.startswith('/v1/stream') and 'id' in data:
                data['video_id'] = data['id']
            # 针对/v1/episodes路径，将episode参数转换为episode_url
            elif self.path.startswith('/v1/episodes') and 'episode' in data:
                data['episode_url'] = data['episode']
        else:  # POST请求
            # 处理POST请求的JSON数据
            if 'Content-Length' in self.headers:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                
                try:
                    data = json.loads(post_data)
                except:
                    data = {}
        
        # 5. 处理混淆的API路径
        # 支持混淆路径和原始路径，增加爬虫难度
        api_paths = {
            # 原始路径
            '/api/search': self.api_search,
            '/api/get_m3u8': self.api_get_m3u8,
            '/api/get_episode_m3u8': self.api_get_episode_m3u8,
            # 混淆路径
            '/v1/query': self.api_search,
            '/v1/stream': self.api_get_m3u8,
            '/v1/episodes': self.api_get_episode_m3u8
        }
        
        # 提取路径部分（忽略查询参数）
        path_without_query = urlparse(self.path).path
        if path_without_query in api_paths:
            response = api_paths[path_without_query](data)
        else:
            response = {'error': 'API not found'}
        
        # 添加响应头，防止简单的爬虫检测
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('X-Powered-By', 'Unknown-Server')
        self.send_header('Server', 'Custom-HTTP/1.1')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-Token, X-Client-ID, X-App-Version')
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def setup_proxy(self):
        """设置代理"""
        try:
            # 尝试多种代理配置
            proxy_configs = [
                {'http': 'http://127.0.0.1:7897', 'https': 'https://127.0.0.1:7897'},
                {'http': 'http://127.0.0.1:7890', 'https': 'https://127.0.0.1:7890'},
                {'http': 'http://127.0.0.1:1080', 'https': 'https://127.0.0.1:1080'},
                {}  # 无代理
            ]
            
            for proxy_config in proxy_configs:
                try:
                    proxy_handler = urllib.request.ProxyHandler(proxy_config)
                    opener = urllib.request.build_opener(proxy_handler)
                    urllib.request.install_opener(opener)
                    
                    # 测试连接
                    test_url = "https://www.baidu.com"
                    response = urllib.request.urlopen(test_url, timeout=5)
                    print(f"代理设置成功: {proxy_config}")
                    return
                except Exception as e:
                    print(f"代理测试失败 {proxy_config}: {e}")
                    continue
            
            print("所有代理配置都失败，使用无代理模式")
            
        except Exception as e:
            print(f"代理设置异常: {e}")
            # 使用无代理
            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)
    
    def fetch_page_content(self, url):
        """获取页面内容"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req, timeout=30)
            return response.read().decode('utf-8')
        except Exception as e:
            print(f"获取页面失败: {e}")
            return None
    
    def search_video(self, video_name):
        """搜索视频并返回播放页面URL"""
        encoded_name = urllib.parse.quote_plus(video_name, safe='')
        search_url = f"https://xiaoxintv.cc/index.php/vod/search.html?wd={encoded_name}&submit="
        
        html_content = self.fetch_page_content(search_url)
        if not html_content:
            return None
        
        pattern = r'<a[^>]*href="(/index\.php/vod/detail/id/(\d+)\.html)"[^>]*title="([^"]+)"[^>]*>'
        matches = re.findall(pattern, html_content)
        
        results = []
        for match in matches:
            href, video_id, title = match
            if video_name.lower() in title.lower():
                play_url = f"https://xiaoxintv.cc/index.php/vod/play/id/{video_id}/sid/1/nid/1.html"
                results.append({
                    'title': title.strip(),
                    'video_id': video_id,
                    'play_url': play_url
                })
        
        return results
    
    def extract_m3u8_from_play_page(self, play_url):
        """从播放页面提取M3U8地址"""
        print(f"开始提取M3U8地址，播放页面: {play_url}")
        
        html_content = self.fetch_page_content(play_url)
        if not html_content:
            print(f"无法获取页面内容: {play_url}")
            return []
        
        print(f"页面内容长度: {len(html_content)} 字符")
        
        # 更全面的M3U8地址匹配模式
        patterns = [
            # 基础URL匹配
            r'"(https?://[^"]+\.m3u8[^"]*)"',
            r"'(https?://[^']+\.m3u8[^']*)'",
            r'(https?://[^\s"\'<>]+\.m3u8)',
            
            # 属性匹配
            r'url\s*[:=]\s*["\'](https?://[^"\']+\.m3u8)["\']',
            r'videoUrl\s*[:=]\s*["\'](https?://[^"\']+\.m3u8)["\']',
            r'src\s*[:=]\s*["\'](https?://[^"\']+\.m3u8)["\']',
            r'file\s*[:=]\s*["\'](https?://[^"\']+\.m3u8)["\']',
            r'video\s*[:=]\s*["\'](https?://[^"\']+\.m3u8)["\']',
            
            # 播放器配置
            r'player\.setup\s*\([^)]*url\s*[:=]\s*["\'](https?://[^"\']+\.m3u8)["\']',
            r'new\s+Player\s*\([^)]*url\s*[:=]\s*["\'](https?://[^"\']+\.m3u8)["\']',
            
            # JSON格式
            r'"url"\s*:\s*["\'](https?://[^"\']+\.m3u8)["\']',
            r'"src"\s*:\s*["\'](https?://[^"\']+\.m3u8)["\']',
            r'"file"\s*:\s*["\'](https?://[^"\']+\.m3u8)["\']',
            
            # 相对路径（需要拼接完整URL）
            r'"(//[^"]+\.m3u8[^"]*)"',
            r"'(//[^']+\.m3u8[^']*)'",
            r'(//[^\s"\'<>]+\.m3u8)',
            
            # 更宽松的匹配模式
            r'[\"\'](https?://[^\"\']*?\.m3u8[^\"\']*?)[\"\']',
            r'(https?://[^\s<>]*?\.m3u8[^\s<>]*)',
            
            # 包含特殊字符的URL
            r'[\"\'](https?://[^\"\']*?m3u8[^\"\']*?)[\"\']',
            r'(https?://[^\s<>]*?m3u8[^\s<>]*)',
            
            # 针对该网站的特殊模式：JavaScript变量中的JSON格式
            r'var\s+player_[^=]*=\s*{[^}]*"url"\s*:\s*"([^"]+\.m3u8[^"]*)"',
            r'var\s+player_[^=]*=\s*{[^}]*"url"\s*:\s*\'([^\']+\.m3u8[^\']*)\'',
            r'"url"\s*:\s*"([^"]+\.m3u8[^"]*)"[^}]*}',
            r'"url"\s*:\s*\'([^\']+\.m3u8[^\']*)\'[^}]*}'
        ]
        
        m3u8_urls = []
        for i, pattern in enumerate(patterns):
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                print(f"模式{i+1}匹配到M3U8地址: {matches}")
                # 处理转义字符
                processed_matches = []
                for match in matches:
                    # 处理JavaScript中的转义字符
                    processed_url = match.replace('\\/', '/').replace('\\"', '"')
                    processed_matches.append(processed_url)
                m3u8_urls.extend(processed_matches)
        
        # 如果没有找到，尝试查找JavaScript中的M3U8地址
        if not m3u8_urls:
            print("尝试在JavaScript中查找M3U8地址...")
            js_patterns = [
                r'var\s+[^=]*\s*=\s*["\'](https?://[^"\']+\.m3u8)["\']',
                r'let\s+[^=]*\s*=\s*["\'](https?://[^"\']+\.m3u8)["\']',
                r'const\s+[^=]*\s*=\s*["\'](https?://[^"\']+\.m3u8)["\']',
                r'window\.[^=]*\s*=\s*["\'](https?://[^"\']+\.m3u8)["\']',
                
                # 更宽松的JavaScript匹配
                r'var\s+[^=]*\s*=\s*["\'](https?://[^"\']*?\.m3u8)["\']',
                r'=[\s]*["\'](https?://[^"\']*?\.m3u8)["\']',
                r'url[\s]*[=:][\s]*["\'](https?://[^"\']*?\.m3u8)["\']'
            ]
            for pattern in js_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    print(f"JavaScript模式匹配到M3U8地址: {matches}")
                    m3u8_urls.extend(matches)
        
        # 处理相对路径
        processed_urls = []
        for url in m3u8_urls:
            if url.startswith('//'):
                # 将相对路径转换为完整URL
                full_url = 'https:' + url
                processed_urls.append(full_url)
                print(f"相对路径转换为完整URL: {url} -> {full_url}")
            else:
                processed_urls.append(url)
        
        # 去重并过滤无效地址
        m3u8_urls = list(set(processed_urls))
        m3u8_urls = [url for url in m3u8_urls if 'm3u8' in url.lower()]
        
        print(f"最终找到的M3U8地址数量: {len(m3u8_urls)}")
        if m3u8_urls:
            print(f"M3U8地址列表: {m3u8_urls}")
        else:
            print("未找到M3U8地址，尝试查找其他视频格式...")
            # 查找其他可能的视频格式
            video_patterns = [
                r'"(https?://[^"]+\.mp4[^"]*)"',
                r'"(https?://[^"]+\.ts[^"]*)"',
                r'"(https?://[^"]+\.flv[^"]*)"'
            ]
            for pattern in video_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    print(f"找到其他视频格式: {matches}")
        
        return m3u8_urls
    
    def get_video_info(self, video_id):
        """获取视频的详细信息（封面、简介等）"""
        detail_url = f"https://xiaoxintv.cc/index.php/vod/detail/id/{video_id}.html"
        html_content = self.fetch_page_content(detail_url)
        
        if not html_content:
            print(f"无法获取详情页面内容: {detail_url}")
            return {'cover': '', 'description': '', 'episodes': []}
        
        print(f"详情页面内容长度: {len(html_content)} 字符")
        
        # 提取封面图片（优先JPG格式）
        cover_url = ''
        cover_patterns = [
            # 优先匹配JPG格式的图片
            r'<img[^>]*src="([^"]+\.jpg)"[^>]*alt="[^"]*"[^>]*>',
            r'<img[^>]*src="([^"]+\.jpeg)"[^>]*alt="[^"]*"[^>]*>',
            r'<img[^>]*data-original="([^"]+\.jpg)"[^>]*>',
            r'<img[^>]*data-original="([^"]+\.jpeg)"[^>]*>',
            r'background-image:\s*url\(["\']?([^"\']+\.jpg)["\']?\)',
            r'background-image:\s*url\(["\']?([^"\']+\.jpeg)["\']?\)',
            
            # 其他格式的图片（作为备选）
            r'<img[^>]*src="([^"]+\.png)"[^>]*alt="[^"]*"[^>]*>',
            r'<img[^>]*src="([^"]+)"[^>]*class="stui-vodlist__thumb[^>]*>',
            r'<img[^>]*src="([^"]+)"[^>]*class="vod-pic[^>]*>',
            r'<img[^>]*src="([^"]+)"[^>]*alt="[^"]*"[^>]*class="[^"]*thumb[^"]*"[^>]*>',
            r'<img[^>]*src="([^"]+)"[^>]*alt="[^"]*"[^>]*class="[^"]*cover[^"]*"[^>]*>',
            r'<img[^>]*src="([^"]+)"[^>]*data-original="([^"]+)"[^>]*>',
            r'<img[^>]*data-original="([^"]+)"[^>]*>',
            r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)',
            r'<img[^>]*src="([^"]+)"[^>]*style="[^"]*background[^"]*"[^>]*>',
            r'<img[^>]*src="([^"]+)"[^>]*width="[0-9]+"[^>]*height="[0-9]+"[^>]*>',
            r'<img[^>]*src="([^"]+)"[^>]*title="[^"]*"[^>]*>',
        ]
        
        for pattern in cover_patterns:
            cover_match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if cover_match:
                # 获取第一个匹配到的组
                cover_url = cover_match.group(1)
                if not cover_url.startswith('http'):
                    # 处理相对路径
                    if cover_url.startswith('//'):
                        cover_url = 'https:' + cover_url
                    else:
                        cover_url = f"https://xiaoxintv.cc{cover_url}"
                print(f"找到封面图片: {cover_url}")
                
                # 如果是JPG格式，优先使用
                if cover_url.lower().endswith(('.jpg', '.jpeg')):
                    break
        
        # 提取完整的视频信息（主演、导演、简介等）
        description = ''
        
        # 提取导演信息
        director = ''
        director_patterns = [
            r'导演[：:]([^<]+)',
            r'<span[^>]*>导演[：:]<[^>]*>([^<]+)</',
            r'导演[：:]<[^>]*>([^<]+)</',
            r'<p[^>]*>导演[：:]([^<]+)</p>',
        ]
        
        for pattern in director_patterns:
            director_match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if director_match:
                director = re.sub(r'<[^>]+>', '', director_match.group(1)).strip()
                if director:
                    print(f"找到导演信息: {director}")
                    break
        
        # 提取主演信息
        actors = ''
        actor_patterns = [
            r'主演[：:]([^<]+)',
            r'<span[^>]*>主演[：:]<[^>]*>([^<]+)</',
            r'主演[：:]<[^>]*>([^<]+)</',
            r'<p[^>]*>主演[：:]([^<]+)</p>',
        ]
        
        for pattern in actor_patterns:
            actor_match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if actor_match:
                actors = re.sub(r'<[^>]+>', '', actor_match.group(1)).strip()
                if actors:
                    print(f"找到主演信息: {actors}")
                    break
        
        # 提取详细简介
        detail_desc = ''
        desc_patterns = [
            r'<div[^>]*class="stui-content__detail[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<div[^>]*class="vod-content[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<div[^>]*class="content[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<p[^>]*class="data[^>]*>(.*?)</p>',
            r'<div[^>]*class="detail[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<div[^>]*class="intro[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<div[^>]*class="description[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<div[^>]*class="summary[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<div[^>]*id="detail[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<div[^>]*id="intro[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<div[^>]*id="description[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<div[^>]*id="summary[^>]*>.*?<p[^>]*>(.*?)</p>',
            r'<p[^>]*class="intro[^>]*>(.*?)</p>',
            r'<p[^>]*class="description[^>]*>(.*?)</p>',
            r'<p[^>]*class="summary[^>]*>(.*?)</p>',
        ]
        
        for pattern in desc_patterns:
            desc_match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if desc_match:
                detail_desc = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()
                if len(detail_desc) > 0:
                    print(f"找到详细简介: {detail_desc[:100]}...")
                    break
        
        # 组合完整的简介信息
        description_parts = []
        if director:
            description_parts.append(f"导演: {director}")
        if actors:
            description_parts.append(f"主演: {actors}")
        if detail_desc:
            description_parts.append(f"简介: {detail_desc}")
        
        if not description_parts:
            # 如果没有找到详细信息，使用原来的简介提取方式
            for pattern in desc_patterns:
                desc_match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
                if desc_match:
                    description = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()
                    if len(description) > 0:
                        print(f"找到视频简介: {description[:100]}...")
                        break
        else:
            description = '\\n'.join(description_parts)
        
        episodes = []
        
        # 多种集数列表匹配模式
        play_list_patterns = [
            r'<ul[^>]*class="stui-content__playlist[^>]*>(.*?)</ul>',
            r'<ul[^>]*class="playlist[^>]*>(.*?)</ul>',
            r'<div[^>]*class="playlist[^>]*>(.*?)</div>',
            r'<div[^>]*class="stui-content__playlist[^>]*>(.*?)</div>'
        ]
        
        play_list_html = None
        for pattern in play_list_patterns:
            play_list_match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if play_list_match:
                play_list_html = play_list_match.group(1)
                print(f"找到集数列表，使用模式: {pattern[:50]}...")
                break
        
        if not play_list_html:
            print("未找到集数列表，尝试直接在整个页面中查找集数链接")
            play_list_html = html_content
        
        # 多种集数链接匹配模式
        episode_patterns = [
            r'<a[^>]*href="(/index\.php/vod/play/id/\d+/sid/(\d+)/nid/(\d+)\.html)"[^>]*>(.*?)</a>',
            r'<a[^>]*href="(/vod/play/id/\d+/sid/(\d+)/nid/(\d+)\.html)"[^>]*>(.*?)</a>',
            r'<a[^>]*href="(/play/\d+/\d+/\d+)"[^>]*>(.*?)</a>',
            r'<a[^>]*href="(https?://[^"]+/index\.php/vod/play/id/\d+/sid/(\d+)/nid/(\d+)\.html)"[^>]*>(.*?)</a>'
        ]
        
        for pattern in episode_patterns:
            episode_matches = re.findall(pattern, play_list_html, re.DOTALL | re.IGNORECASE)
            if episode_matches:
                print(f"找到 {len(episode_matches)} 个集数，使用模式: {pattern[:50]}...")
                
                for match in episode_matches:
                    if len(match) == 4:
                        href, sid, nid, title = match
                        # 从HTML中提取纯文本标题
                        clean_title = re.sub(r'<[^>]+>', '', title).strip()
                        if not clean_title:
                            clean_title = f"第{nid}集"
                        
                        if not href.startswith('http'):
                            full_url = f"https://xiaoxintv.cc{href}"
                        else:
                            full_url = href
                        episodes.append({
                            'sid': sid,
                            'nid': nid,
                            'title': clean_title,
                            'url': full_url
                        })
                    elif len(match) == 2:
                        href, title = match
                        # 从HTML中提取纯文本标题
                        clean_title = re.sub(r'<[^>]+>', '', title).strip()
                        if not clean_title:
                            # 从URL中提取sid和nid
                            sid_nid_match = re.search(r'/sid/(\d+)/nid/(\d+)', href)
                            if sid_nid_match:
                                sid, nid = sid_nid_match.groups()
                                clean_title = f"第{nid}集"
                        
                        # 从URL中提取sid和nid
                        sid_nid_match = re.search(r'/sid/(\d+)/nid/(\d+)', href)
                        if sid_nid_match:
                            sid, nid = sid_nid_match.groups()
                            if not href.startswith('http'):
                                full_url = f"https://xiaoxintv.cc{href}"
                            else:
                                full_url = href
                            episodes.append({
                                'sid': sid,
                                'nid': nid,
                                'title': clean_title,
                                'url': full_url
                            })
                
                if episodes:
                    break
        
        # 去重
        unique_episodes = []
        seen_urls = set()
        for episode in episodes:
            if episode['url'] not in seen_urls:
                unique_episodes.append(episode)
                seen_urls.add(episode['url'])
        
        print(f"最终提取到 {len(unique_episodes)} 个集数")
        
        return {
            'cover': cover_url,
            'description': description,
            'episodes': unique_episodes
        }
    
    def api_search(self, data):
        """搜索视频API"""
        video_name = data.get('video_name', '').strip()
        
        if not video_name:
            return {'error': '请输入视频名称'}
        
        self.setup_proxy()
        ssl._create_default_https_context = ssl._create_unverified_context
        
        results = self.search_video(video_name)
        
        if not results:
            return {'error': '未找到相关视频'}
        
        return {'success': True, 'results': results}
    
    def api_get_m3u8(self, data):
        """获取M3U8地址API"""
        video_id = data.get('video_id')
        play_url = data.get('play_url')
        
        if not play_url:
            return {'error': '缺少播放页面URL'}
        
        self.setup_proxy()
        ssl._create_default_https_context = ssl._create_unverified_context
        
        m3u8_urls = self.extract_m3u8_from_play_page(play_url)
        
        if not m3u8_urls:
            return {'error': '未找到M3U8地址'}
        
        video_info = {'cover': '', 'description': '', 'episodes': []}
        if video_id:
            video_info = self.get_video_info(video_id)
        
        # 加密M3U8地址
        encrypted_m3u8_url = encrypt_m3u8_url(m3u8_urls[0])
        
        return {
            'success': True,
            'm3u8_url': encrypted_m3u8_url,
            'cover': video_info['cover'],
            'description': video_info['description'],
            'episodes': video_info['episodes']
        }
    
    def api_get_episode_m3u8(self, data):
        """获取指定集数的M3U8地址"""
        episode_url = data.get('episode_url')
        
        if not episode_url:
            return {'error': '缺少集数URL'}
        
        self.setup_proxy()
        ssl._create_default_https_context = ssl._create_unverified_context
        
        m3u8_urls = self.extract_m3u8_from_play_page(episode_url)
        
        if not m3u8_urls:
            return {'error': '未找到M3U8地址'}
        
        # 加密M3U8地址
        encrypted_m3u8_url = encrypt_m3u8_url(m3u8_urls[0])
        return {'success': True, 'm3u8_url': encrypted_m3u8_url}

def main():
    """主函数"""
    print("正在初始化服务器...")
    # 创建简化的HTML页面
    create_simple_html()
    
    # 获取端口配置，支持环境变量配置（用于Cloudflare Pages部署环境）
    port = int(os.environ.get('PORT', PORT))
    print(f"使用端口: {port}")
    
    try:
        # 创建一个可以重用地址的服务器类
        socketserver.TCPServer.allow_reuse_address = True
        
        server_address = ("", port)
        print(f"准备创建服务器实例，地址: {server_address}")
        
        # 创建服务器实例
        with socketserver.TCPServer(server_address, M3U8SearchHandler) as httpd:
            # 设置请求超时（提高稳定性）
            httpd.timeout = 60
            
            print(f"🚀 M3U8搜索工具已启动")
            print(f"📱 访问地址: http://localhost:{port}")
            print(f"🌐 Cloudflare Pages 部署地址: https://m3u8-search-tool.pages.dev/")
            print(f"💡 按 Ctrl+C 停止服务器")
            print("服务器开始监听请求...")
            
            # 启动服务器
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n👋 服务器已停止")
            except Exception as e:
                print(f"服务器运行错误: {str(e)}")
                httpd.server_close()
    except Exception as e:
        print(f"服务器初始化错误: {str(e)}")
        import traceback
        traceback.print_exc()

def create_simple_html():
    """创建简化的HTML页面（如果不存在）"""
    # 检查文件是否已存在，如果存在则不再覆盖
    if os.path.exists('index_simple.html'):
        print("index_simple.html 文件已存在，跳过创建")
        return
    
    # 如果文件不存在，创建基础HTML结构
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>M3U8视频搜索工具</title>
    <script>
        // 全局配置
        const API_BASE_URL = 'http://localhost:{PORT}';
    </script>
</head>
<body>
    <h1>M3U8视频搜索工具</h1>
    <p>请确保 index_simple.html 文件存在</p>
</body>
</html>'''
    
    with open('index_simple.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("已创建基础的 index_simple.html 文件")

if __name__ == "__main__":
    main()