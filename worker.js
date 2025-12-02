// Cloudflare Worker 脚本用于 M3U8 搜索工具

// API密钥验证
const API_SECRET_KEY = 'Xm3U8V1d30p1D'; // 与web_app.py中的密钥保持一致
const API_KEY = 'm3u8_viewer_key'; // 与前端使用的API密钥保持一致

// 模拟M3U8数据
const mockM3U8Data = {
  "movies": [
    {
      "title": "示例视频1",
      "url": "https://example.com/playlist1.m3u8",
      "quality": "高清",
      "size": "1.2GB"
    },
    {
      "title": "示例视频2",
      "url": "https://example.com/playlist2.m3u8",
      "quality": "超清",
      "size": "2.5GB"
    },
    {
      "title": "示例视频3",
      "url": "https://example.com/playlist3.m3u8",
      "quality": "蓝光",
      "size": "4.8GB"
    }
  ]
};

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
    // 处理API路由 - 支持前端使用的/v1/query路径和标准的/api/search路径
    if (path.startsWith('/api/search') || path.startsWith('/v1/query')) {
      // 获取搜索关键词
      const searchTerm = url.searchParams.get('q') || '';
      
      // 简单的搜索逻辑（实际应用中可能需要更复杂的处理）
      let results = mockM3U8Data.movies;
      if (searchTerm) {
        results = mockM3U8Data.movies.filter(movie => 
          movie.title.toLowerCase().includes(searchTerm.toLowerCase())
        );
      }
      
      // 返回搜索结果 - 格式匹配前端预期
      return new Response(JSON.stringify({
        success: true,
        query: searchTerm,
        results: results,
        total: results.length
      }), {
        headers: corsHeaders,
        status: 200
      });
    }
    
    // 处理流媒体请求
    else if (path.startsWith('/api/get_m3u8') || path.startsWith('/v1/stream')) {
      return new Response(JSON.stringify({
        success: true,
        message: 'Stream API is working!',
        mock_url: 'https://example.com/sample-playlist.m3u8'
      }), {
        headers: corsHeaders,
        status: 200
      });
    }
    
    // 处理集数请求
    else if (path.startsWith('/api/get_episode_m3u8') || path.startsWith('/v1/episodes')) {
      return new Response(JSON.stringify({
        success: true,
        message: 'Episodes API is working!',
        episodes: [{ title: '第1集', url: 'https://example.com/episode1.m3u8' }]
      }), {
        headers: corsHeaders,
        status: 200
      });
    }
    
    // 其他API路由
    else if (path.startsWith('/api/') || path.startsWith('/v1/')) {
      return new Response(JSON.stringify({
        success: true,
        message: 'API is working!',
        endpoint: path
      }), {
        headers: corsHeaders,
        status: 200
      });
    }
    
    // 未找到的路由
    else {
      return new Response(JSON.stringify({
        error: 'Not Found',
        path: path
      }), {
        headers: corsHeaders,
        status: 404
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
