# TripMind - 群体旅行智能协调系统

[English](README_EN.md) | 中文

基于 OpenAgents 框架的多 Agent 旅行规划系统。

📄 [项目说明文档](https://oxb708x94fk.feishu.cn/wiki/UTxwwxE3uifqmFkvgwUcjzOtnXl) | 🎬 [演示视频](https://b23.tv/pbaMt6y)

## 项目简介

TripMind 是基于 OpenAgents 框架的多 Agent 群体旅行规划系统。

**解决的问题**：当一群人想一起旅行时，每个人的偏好、预算、身体状况都不一样，如何协调这些需求，生成一个让所有人都满意的行程方案？

**三大痛点**：
- **偏好冲突**：有人爱美食，有人爱冒险，有人爱购物
- **预算差异**：成员预算从 8000 到 15000 不等
- **特殊需求**：孕妇需要轻松行程，素食者需要特定餐厅

**核心创新**：通过 9 个专业 Agent 协作，实现"意图解析 → 信息采集 → 智能规划"的完整链路。每个 Agent 专注单一职责，通过事件驱动机制协同工作，最终生成平衡所有成员需求的个性化行程方案。

**OpenAgents 关键特性应用**：
- 事件驱动架构：Agent 间通过 send_event 异步通信，松耦合协作
- Triggers 机制：每个 Agent 监听特定事件，自动触发处理逻辑
- 进度可视化：设计 progress.update 事件，用户可实时看到 Agent 调用链
- workspace.project Mod：管理旅行项目生命周期
- Studio 可视化：实时展示 Agent 协作过程

## Agent 架构

系统包含 9 个 Agent，分为四层：

| 层级 | Agent | 职责 |
|------|-------|------|
| 核心协调层 | Coordinator | 接收请求、调度任务、汇总结果 |
| 用户意图层 | User Intent | 解析自然语言，提取结构化信息 |
| | Group Preference | 分析群体偏好，识别冲突 |
| | Budget Balancer | 预算平衡，设计分层方案 |
| | Health Care | 健康关怀，过滤不适合的活动 |
| 信息采集层 | Web Scraper | 抓取实时旅行信息 |
| | Information Analyzer | 数据分析和推荐排序 |
| 规划执行层 | Route Planning | 生成详细行程表 |
| | Dynamic Adjuster | 动态调整优化 |

## 环境要求

- Python 3.10+
- Conda（推荐）
- 智谱 AI API Key（从 https://open.bigmodel.cn/ 获取）

## 快速启动

### 1. 创建 Python 环境

```bash
conda create -n openagents python=3.10
conda activate openagents
```

### 2. 安装 OpenAgents

```bash
pip install openagents
```

### 3. 配置 API Key

复制示例文件并设置 API Key：
```batch
copy start_network.bat.example start_network.bat
```

编辑 `start_network.bat`，设置智谱 AI API Key：
```batch
set ZHIPUAI_API_KEY=your-api-key-here
```

### 4. 启动 Network

```bash
start_network.bat
```

### 5. 启动 Agent

```bash
start_agents.bat
```

### 6. 访问 Studio

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
