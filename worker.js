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
  
  // 暂时禁用API验证，确保基本功能可用
  // 生产环境应恢复验证逻辑
  /*
  // 检查API密钥（简化版）
  const apiKey = request.headers.get('X-API-Key');
  if (!apiKey || apiKey !== API_KEY) {
    return new Response(JSON.stringify({ error: 'Forbidden: Invalid API key' }), {
      status: 403,
      headers: corsHeaders
    });
  }
  */
  
  try {
    // 简单的测试端点
    if (path === '/api/test' || path === '/v1/test') {
      return new Response(JSON.stringify({
        success: true,
        message: 'API is working!',
        timestamp: new Date().toISOString()
      }), {
        headers: corsHeaders,
        status: 200
      });
    }
    
        // 处理所有API路由 - 确保任何路径都能被正确处理
    else if (path.startsWith('/api/') || path.startsWith('/v1/')) {
      console.log('API请求到达:', { path, method: request.method });
      
      // 特殊处理测试端点
      if (path === '/api/test' || path === '/v1/test') {
        return new Response(JSON.stringify({
          success: true,
          message: 'API服务正常运行',
          timestamp: new Date().toISOString(),
          endpoint: path
        }), {
          headers: corsHeaders,
          status: 200
        });
      }
      
      // 处理搜索相关端点
      if (path.includes('search') || path.includes('query')) {
        // 获取搜索关键词
        const searchTerm = url.searchParams.get('q') || '';
        console.log('搜索请求:', { searchTerm });
        
        // 简单的搜索逻辑
        let searchResults = mockM3U8Data.movies;
        if (searchTerm) {
          searchResults = mockM3U8Data.movies.filter(movie => 
            movie.title.toLowerCase().includes(searchTerm.toLowerCase())
          );
        }
        
        // 转换数据格式
        const formattedResults = searchResults.map((movie, index) => ({
          video_id: `video_${index + 1}`,
          title: movie.title,
          play_url: movie.url,
          quality: movie.quality,
          size: movie.size
        }));
        
        const responseData = {
          success: true,
          query: searchTerm,
          results: formattedResults,
          total: formattedResults.length,
          endpoint: path
        };
        
        console.log('返回搜索结果:', { total: responseData.total });
        return new Response(JSON.stringify(responseData), {
          headers: corsHeaders,
          status: 200
        });
      }
      
      // 处理流播放端点
      if (path.includes('stream')) {
        const videoId = url.searchParams.get('id') || '';
        return new Response(JSON.stringify({
          success: true,
          video_id: videoId,
          stream_url: `https://example.com/stream/${videoId}.m3u8`,
          timestamp: new Date().toISOString(),
          endpoint: path
        }), {
          headers: corsHeaders,
          status: 200
        });
      }
      
      // 对于其他未明确处理的API端点，返回404错误
      return new Response(JSON.stringify({
        success: false,
        error: 'Endpoint not found',
        endpoint: path,
        available_endpoints: ['/api/test', '/v1/test', '/api/search', '/v1/query', '/v1/search', '/v1/stream']
      }), {
        headers: corsHeaders,
        status: 404
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

// 生成API token的辅助函数（暂时注释）
/*
function generateApiToken() {
  const timestamp = Math.floor(Date.now() / 1000);
  return `${timestamp}_${API_SECRET_KEY.substring(2, 8)}`;
}

// 验证API token的辅助函数（暂时注释）
function validateApiToken(token) {
  if (!token || typeof token !== 'string') {
    return false;
  }
  
  const parts = token.split('_');
  if (parts.length !== 2) {
    return false;
  }
  
  const [timestampStr, secretPart] = parts;
  const timestamp = parseInt(timestampStr, 10);
  
  // 检查时间戳是否有效且未过期（24小时有效期）
  const currentTime = Math.floor(Date.now() / 1000);
  const tokenAge = currentTime - timestamp;
  
  // 允许token在24小时内有效
  if (isNaN(timestamp) || tokenAge > 86400 || tokenAge < 0) {
    return false;
  }
  
  // 验证密钥部分
  return secretPart === API_SECRET_KEY.substring(2, 8);
}
*/
