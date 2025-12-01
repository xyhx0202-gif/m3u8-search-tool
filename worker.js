// Cloudflare Worker 代码
// 用于处理API请求并代理到后端服务

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

// API密钥验证
const API_SECRET_KEY = 'Xm3U8V1d30p1D'; // 与web_app.py中的密钥保持一致
const API_KEY = 'm3u8_viewer_key'; // 与前端使用的API密钥保持一致

// 模拟API响应（实际部署时应替换为真实的后端逻辑）
async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname;
  
  // 检查API密钥
  const apiKey = request.headers.get('X-API-Key');
  if (!apiKey || apiKey !== API_KEY) {
    return new Response(JSON.stringify({ error: 'Forbidden: Invalid API key' }), {
      status: 403,
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  // 处理API请求
  if (path.startsWith('/api/search') || path.startsWith('/v1/query')) {
    // 搜索API处理
    const query = url.searchParams.get('q') || url.searchParams.get('video_name') || '';
    if (!query) {
      return new Response(JSON.stringify({ error: 'Missing search query' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // 模拟搜索结果（实际部署时应替换为真实的搜索逻辑）
    return new Response(JSON.stringify({
      status: 'success',
      results: [
        {
          id: '1',
          title: `搜索结果: ${query}`,
          cover: 'https://example.com/cover1.jpg',
          play_url: '/api/stream?id=1'
        },
        {
          id: '2',
          title: `相关视频: ${query}`,
          cover: 'https://example.com/cover2.jpg',
          play_url: '/api/stream?id=2'
        }
      ]
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (path.startsWith('/api/get_m3u8') || path.startsWith('/v1/stream')) {
    // 获取M3U8链接API处理
    const videoId = url.searchParams.get('video_id') || url.searchParams.get('id') || '';
    if (!videoId) {
      return new Response(JSON.stringify({ error: 'Missing video ID' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // 模拟M3U8链接（实际部署时应替换为真实的链接获取逻辑）
    return new Response(JSON.stringify({
      status: 'success',
      m3u8_url: 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8',
      title: `视频ID: ${videoId}`,
      cover: 'https://example.com/cover.jpg',
      episodes: [
        { id: '1', title: '第1集', episode_url: `/api/episodes?episode=1` },
        { id: '2', title: '第2集', episode_url: `/api/episodes?episode=2` }
      ]
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  if (path.startsWith('/api/get_episode_m3u8') || path.startsWith('/v1/episodes')) {
    // 获取剧集M3U8链接API处理
    const episodeUrl = url.searchParams.get('episode_url') || url.searchParams.get('episode') || '';
    
    // 模拟剧集M3U8链接
    return new Response(JSON.stringify({
      status: 'success',
      m3u8_url: 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  // 默认返回404
  return new Response(JSON.stringify({ error: 'Not found' }), {
    status: 404,
    headers: { 'Content-Type': 'application/json' }
  });
}

// 生成API token的辅助函数
function generateApiToken() {
  const timestamp = Math.floor(Date.now() / 1000);
  return `${timestamp}_${API_SECRET_KEY.substring(2, 8)}`;
}
