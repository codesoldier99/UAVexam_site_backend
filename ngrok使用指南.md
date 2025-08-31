# 🚀 ngrok设置和使用完整指南

## ✅ 第一步：ngrok已安装完成

**恭喜！ngrok已经通过winget成功安装到您的系统中！**
- 版本：3.3.1
- 已添加到系统PATH
- 可以直接使用 `ngrok` 命令

**重要提醒**：请重启PowerShell窗口以使PATH环境变量生效！

## 第二步：注册账号

1. 访问：https://ngrok.com/signup
2. 注册免费账号（可以用GitHub/Google登录）
3. 登录后进入Dashboard
4. 复制你的authtoken（类似：`2abc123def456ghi789jkl`）

## 第三步：配置ngrok

**重要：请先重启PowerShell窗口，然后运行以下命令：**

```bash
# ngrok已安装到系统PATH，直接使用
ngrok config add-authtoken YOUR_TOKEN_HERE
```

**替换 YOUR_TOKEN_HERE 为您从ngrok Dashboard获取的实际token**

## 第四步：启动后端服务

```bash
# 在backend目录下启动
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 第五步：启动ngrok

**重要：请重启PowerShell窗口后再执行以下命令**

```bash
# 新开一个PowerShell窗口，直接运行
ngrok http 8000
```

## 第六步：获取公网地址

ngrok启动后会显示类似信息：
```
ngrok                                                          

Session Status                online                           
Account                       your-email@example.com (Plan: Free)
Version                       3.3.1                            
Region                        United States (us)               
Latency                       45ms                             
Web Interface                 http://127.0.0.1:4040           
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90  
                              0       0       0.00    0.00    0.00    0.00 
```

**你的API公网地址就是：`https://abc123.ngrok.io`**

## 第七步：测试API

```bash
# 测试健康检查接口
curl https://abc123.ngrok.io/api/v1/health

# 测试其他接口
curl https://abc123.ngrok.io/api/v1/system/info
```

## 📋 常用命令

```bash
# 启动ngrok映射8000端口
ngrok http 8000

# 启动ngrok并指定域名前缀（付费功能）
ngrok http 8000 --subdomain=myapp

# 查看ngrok配置
ngrok config check

# 查看ngrok版本
ngrok version

# 停止ngrok
Ctrl + C
```

## 🔧 Web界面监控

ngrok启动后，访问 http://127.0.0.1:4040 可以看到：
- 实时请求日志
- 请求/响应详情
- 流量统计
- 重放请求功能

## ⚠️ 注意事项

1. **免费版限制**：
   - 每次启动域名会变化
   - 同时只能有1个隧道
   - 有流量限制

2. **安全提醒**：
   - 不要在生产环境使用
   - 注意保护敏感数据
   - 及时关闭不需要的隧道

3. **网络要求**：
   - 需要稳定的网络连接
   - 防火墙可能需要配置

## 🎯 完整使用流程

1. **下载并解压ngrok** ✅
2. **注册账号获取token** ✅
3. **配置authtoken** ✅
4. **启动后端服务**（端口8000）
5. **启动ngrok映射**
6. **获取公网地址**
7. **测试API接口**

## 📞 如果遇到问题

1. **ngrok启动失败**：检查token是否正确配置
2. **无法访问**：检查后端服务是否正常运行
3. **连接超时**：检查网络连接和防火墙设置
4. **域名变化**：免费版每次重启域名都会变化，这是正常的

---

**准备好后，按以下顺序操作：**
1. 启动后端：`cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. 启动ngrok：`ngrok http 8000`
3. 复制显示的https地址，这就是你的公网API地址！