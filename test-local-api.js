// 本地API接口测试脚本
const https = require('https');
const http = require('http');

// 测试API接口连通性
function testAPI(url, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const isHttps = url.startsWith('https://');
    const client = isHttps ? https : http;
    
    const options = {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'WeChat-MiniProgram-Test'
      },
      timeout: 10000
    };

    if (data && method !== 'GET') {
      options.headers['Content-Length'] = Buffer.byteLength(JSON.stringify(data));
    }

    const req = client.request(url, options, (res) => {
      let responseData = '';
      
      res.on('data', (chunk) => {
        responseData += chunk;
      });
      
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          data: responseData,
          success: res.statusCode >= 200 && res.statusCode < 300
        });
      });
    });

    req.on('error', (error) => {
      reject({
        error: error.message,
        success: false
      });
    });

    req.on('timeout', () => {
      req.destroy();
      reject({
        error: 'Request timeout',
        success: false
      });
    });

    if (data && method !== 'GET') {
      req.write(JSON.stringify(data));
    }
    
    req.end();
  });
}

// 测试本地API端点
async function runLocalAPITests() {
  const baseURL = 'http://10.20.175.146:3000';
  const testEndpoints = [
    '/realtime/status',
    '/realtime/public-board', 
    '/realtime/venue-status',
    '/realtime/system-status',
    '/wx-miniprogram/candidate-info?id_number=test',
    '/institutions',
    '/venues',
    '/schedules'
  ];

  console.log('开始测试本地API接口连通性...\n');
  console.log(`基础URL: ${baseURL}\n`);

  // 首先测试服务器基本连通性
  console.log('测试服务器基本连通性...');
  try {
    const result = await testAPI(baseURL);
    console.log(`✅ 服务器响应: ${result.statusCode}`);
    console.log(`📄 响应内容预览: ${result.data.substring(0, 200)}...`);
  } catch (error) {
    console.log(`❌ 服务器无法连接: ${error.error}`);
    console.log('请确认：');
    console.log('1. 本地API服务器是否已启动');
    console.log('2. 端口3000是否正确');
    console.log('3. 防火墙是否阻止了连接');
    return;
  }

  console.log('\n测试具体API端点...\n');

  for (const endpoint of testEndpoints) {
    const fullURL = `${baseURL}${endpoint}`;
    console.log(`测试: ${endpoint}`);
    
    try {
      const result = await testAPI(fullURL);
      console.log(`✅ 状态码: ${result.statusCode}`);
      console.log(`📄 响应长度: ${result.data.length} 字符`);
      
      // 尝试解析JSON
      try {
        const jsonData = JSON.parse(result.data);
        console.log(`📊 JSON数据: ${Object.keys(jsonData).length} 个字段`);
        if (jsonData.data) {
          console.log(`📋 数据内容: ${Array.isArray(jsonData.data) ? jsonData.data.length + ' 条记录' : '对象数据'}`);
        }
      } catch (e) {
        console.log(`📄 非JSON响应或HTML页面`);
      }
      
    } catch (error) {
      console.log(`❌ 错误: ${error.error}`);
    }
    
    console.log('---');
  }
}

// 运行测试
runLocalAPITests().catch(console.error);