// Cloudflare Worker 脚本用于 M3U8 搜索工具

// API密钥验证
const API_SECRET_KEY = 'Xm3U8V1d30p1D'; // 与web_app.py中的密钥保持一致
const API_KEY = 'm3u8_viewer_key'; // 与前端使用的API密钥保持一致

// 后端服务器地址（在实际部署时可能需要调整）
const BACKEND_SERVER = 'http://localhost:8888'; // 或其他后端地址

// 处理请求的主函数
async function handleRequest(request) {
  // 获取请求方法和URL
  const method = request.method;
  const url = new URL(request.url);
  const path = url.pathname;
  
  // 添加 CORS 头
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-API-Key, X-API-Token',
    'Content-Type': 'application/json'
  };
  
  // 处理 OPTIONS 请求
  if (method === 'OPTIONS') {
    return new Response(null, {
      headers: corsHeaders,
      status: 204
    });
  }
  
  // 检查API密钥
  const apiKey = request.headers.get('X-API-Key');
  if (!apiKey || apiKey !== API_KEY) {
    return new Response(JSON.stringify({ error: 'Forbidden: Invalid API key' }), {
      status: 403,
      headers: corsHeaders
    });
  }
  
  try {
    // 构建后端请求URL
    const backendUrl = BACKEND_SERVER + path + url.search;
    console.log(`Forwarding request to: ${backendUrl}`);
    
    // 创建后端请求选项
    const requestHeaders = new Headers(request.headers);
    const backendRequest = new Request(backendUrl, {
      method: method,
      headers: requestHeaders,
      body: method === 'POST' ? await request.clone().text() : null
    });
    
    // 发送请求到后端
    const response = await fetch(backendRequest);
    
    // 检查后端响应状态
    if (!response.ok) {
      return new Response(JSON.stringify({
        error: `Backend error: ${response.status} ${response.statusText}`
      }), {
        status: response.status,
        headers: corsHeaders
      });
    }
    
    // 尝试解析JSON响应
    try {
      const data = await response.json();
      return new Response(JSON.stringify(data), {
        headers: corsHeaders
      });
    } catch (jsonError) {
      // 如果响应不是JSON，返回原始内容
      const text = await response.text();
      return new Response(text, {
        headers: {
          ...corsHeaders,
          'Content-Type': response.headers.get('Content-Type') || 'text/plain'
        }
      });
    }
  } catch (error) {
    // 处理错误
    console.error('Request error:', error);
    return new Response(JSON.stringify({
      error: '服务暂时不可用，请稍后再试',
      details: error.message
    }), {
      status: 500,
      headers: corsHeaders
    });
  }
}

// 监听请求事件
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

// 生成API token的辅助函数
function generateApiToken() {
  const timestamp = Math.floor(Date.now() / 1000);
  return `${timestamp}_${API_SECRET_KEY.substring(2, 8)}`;
}
