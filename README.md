# TripMind - 群体旅行智能协调系统

基于 OpenAgents 框架的多 Agent 旅行规划系统。

## 快速启动

### 1. 配置 API Key

复制示例文件并设置 API Key：
```batch
copy start_network.bat.example start_network.bat
```

编辑 `start_network.bat`，设置智谱 AI API Key：
```batch
set ZHIPUAI_API_KEY=your-api-key-here
```

### 2. 启动 Network

```bash
start_network.bat
```

### 3. 启动 Agent

```bash
start_agents.bat
```

### 4. 访问 Studio

打开浏览器：http://localhost:8700

## 使用示例

在 Studio 中创建新项目，输入：

```
我们5个人计划去日本旅行7天：

成员信息：
- Alice（25岁女）：喜欢文化和美食，预算12000元，体力一般
- Bob（28岁男）：喜欢自然和冒险，预算15000元，体力好
- Carol（30岁女）：喜欢购物和美食，预算10000元，孕妇
- David（26岁男）：喜欢动漫和科技，预算8000元，预算敏感
- Eve（27岁女）：喜欢艺术和摄影，预算13000元，素食主义者

请帮我们规划一个平衡所有人需求的旅行方案。
```

## Agent 调用链

```
[用户请求]
     |
     v
Coordinator (协调器)
     |
     v
User Intent Agent (意图解析)
     |
     v
Route Planning Agent (行程规划)
     |
     v
Coordinator (返回结果)
```

系统会显示当前调用的 Agent：
```
[Agent Call Chain]
-> coordinator -> user-intent-agent (task.parse_intent)
-> user-intent-agent -> route-planning-agent (intent.parsed)
-> route-planning-agent -> coordinator (route.planned)
```

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| 编码错误 `'gbk' codec can't decode` | 确保启动脚本中有 `chcp 65001` |
| API 调用失败 | 检查 ZHIPUAI_API_KEY 是否正确 |

## 许可证

MIT License
