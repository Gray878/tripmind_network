# TripMind - 群体旅行智能协调与情境感知系统

基于 OpenAgents 框架的智能旅行规划系统，解决群体旅行中的偏好冲突、预算协调、决策困难等核心痛点。

## 核心创新点

### 1. 群体旅行智能协调
- **偏好平衡**：自动分析群体成员偏好，找到最大公约数
- **预算分层**：设计经济/标准/豪华三层方案，满足不同预算需求
- **民主决策**：关键决策点自动发起投票

### 2. 情境感知个性化
- **疲劳追踪**：实时监测疲劳值，自动建议休息
- **健康关怀**：考虑饮食限制、身体状况等健康因素
- **动态调整**：根据实时情况自动调整行程

## 快速开始

### 前置要求
- Python 3.10+
- OpenAgents 已安装
- LLM API Key（支持多种提供商）

### 支持的模型提供商

TripMind 支持多种 LLM 提供商，你可以根据自己的情况选择：

| 提供商 | 推荐模型 | 价格 | 推荐指数 | 适合人群 |
|--------|---------|------|---------|---------|
| **阿里云通义千问** 🇨🇳 | qwen-max | ¥0.3/M tokens | ⭐⭐⭐⭐⭐ | 国内用户 |
| **智谱 AI GLM** 🇨🇳 | glm-4 | ¥0.1/K tokens | ⭐⭐⭐⭐⭐ | 国内用户 |
| **OpenAI** | gpt-4o-mini | $0.15/M tokens | ⭐⭐⭐⭐ | 追求效果 |
| **DeepSeek** 🇨🇳 | deepseek-chat | ¥0.001/K tokens | ⭐⭐⭐⭐ | 极致性价比 |
| **Ollama** 🆓 | qwen2.5 | 免费 | ⭐⭐⭐⭐ | 有 GPU |

详细对比请查看 [MODEL_COMPARISON.md](MODEL_COMPARISON.md)  
配置指南请查看 [MODEL_CONFIG.md](MODEL_CONFIG.md)

### 安装步骤

1. **选择并配置模型**
   
   TripMind 支持多种 LLM 提供商。推荐国内用户使用**阿里云通义千问**。
   
   **方式一：使用默认配置（OpenAI）**
   ```bash
   # 复制启动脚本模板
   copy start_network.bat.example start_network.bat
   
   # 编辑 start_network.bat，设置 API Key
   set OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   
   **方式二：切换到其他模型（推荐）**
   ```bash
   # 1. 编辑 update_model.py，选择你要使用的模型
   # 例如使用通义千问，取消注释：
   # NEW_MODEL_CONFIG = {
   #     'provider': 'dashscope',
   #     'name': 'qwen-max',
   #     'temperature': 0.7
   # }
   
   # 2. 运行更新脚本
   python update_model.py
   
   # 3. 复制启动脚本并设置对应的 API Key
   copy start_network.bat.example start_network.bat
   # 编辑 start_network.bat，设置：
   set DASHSCOPE_API_KEY=your-api-key-here
   ```
   
   详细配置说明：
   - [MODEL_COMPARISON.md](MODEL_COMPARISON.md) - 模型对比与选择
   - [MODEL_CONFIG.md](MODEL_CONFIG.md) - 详细配置指南

2. **启动 Network 和 Studio**
   
   双击运行 `start_network.bat` 或在命令行执行：
   ```bash
   conda activate openagents
   openagents network start tripmind_network
   ```
   
   在另一个终端启动 Studio：
   ```bash
   conda activate openagents
   openagents studio -s
   ```

3. **启动所有 Agent**
   
   双击运行 `start_agents.bat` 或手动启动每个 Agent：
   ```bash
   conda activate openagents
   # 核心协调层
   openagents agent start tripmind_network/agents/coordinator.yaml
   
   # 用户意图层
   openagents agent start tripmind_network/agents/user_intent_agent.yaml
   openagents agent start tripmind_network/agents/group_preference_agent.yaml
   openagents agent start tripmind_network/agents/budget_balancer_agent.yaml
   openagents agent start tripmind_network/agents/health_care_agent.yaml
   
   # 规划执行层
   openagents agent start tripmind_network/agents/route_planning_agent.yaml
   openagents agent start tripmind_network/agents/fatigue_tracker_agent.yaml
   openagents agent start tripmind_network/agents/voting_manager_agent.yaml
   
   # 监控调整层
   openagents agent start tripmind_network/agents/mood_adapter_agent.yaml
   openagents agent start tripmind_network/agents/dynamic_adjuster_agent.yaml
   ```

4. **访问 Studio**
   
   打开浏览器访问：http://localhost:8050

## Agent 架构

```
                    Coordinator Agent (协调中心)
                            ↓
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
  用户意图层          规划执行层            监控调整层
        ↓                   ↓                   ↓
User Intent Agent   Route Planning Agent   Dynamic Adjuster Agent
        ↓                   ↓                   ↓
        ├─→ Group Preference Agent      ├─→ Mood Adapter Agent
        ├─→ Budget Balancer Agent       └─→ Voting Manager Agent
        ├─→ Fatigue Tracker Agent
        └─→ Health Care Agent
```

### Agent 说明

#### 核心协调层
| Agent | 功能 | 监听事件 | 发布事件 |
|-------|------|---------|---------|
| **Coordinator** | 任务调度、结果汇总、冲突检测 | `project.notification.started` | `task_assigned`, `planning_complete` |

#### 用户意图层
| Agent | 功能 | 监听事件 | 发布事件 |
|-------|------|---------|---------|
| **User Intent** | 解析用户需求、提取约束条件 | `user_input` | `intent_parsed`, `clarification_needed` |
| **Group Preference** | 分析群体偏好、识别冲突 | `intent_parsed` | `preference_analyzed`, `preference_conflict` |
| **Budget Balancer** | 预算分层、费用分摊 | `intent_parsed` | `budget_analyzed`, `budget_exceeded` |
| **Health Care** | 健康档案、风险预警 | `intent_parsed` | `health_checked`, `health_alert` |

#### 规划执行层
| Agent | 功能 | 监听事件 | 发布事件 |
|-------|------|---------|---------|
| **Route Planning** | 生成行程路线、优化交通 | `intent_parsed`, `replanning_triggered` | `route_planned`, `itinerary_generated` |
| **Fatigue Tracker** | 疲劳监测、休息建议 | `itinerary_generated`, `activity_completed` | `fatigue_analyzed`, `fatigue_alert` |
| **Voting Manager** | 组织投票、解决冲突 | `voting_request`, `preference_conflict` | `voting_completed`, `consensus_reached` |

#### 监控调整层
| Agent | 功能 | 监听事件 | 发布事件 |
|-------|------|---------|---------|
| **Mood Adapter** | 心情适配、活动推荐 | `mood_update`, `itinerary_generated` | `mood_analysis_complete`, `mood_adjustment_needed` |
| **Dynamic Adjuster** | 约束检测、触发重规划 | `constraint_violation`, `budget_exceeded`, `fatigue_alert` | `adjustment_needed`, `replanning_triggered` |

## 使用示例

### 场景：5人日本7日游

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

系统将自动：
1. 分析群体偏好，找到"美食"和"文化"作为共同兴趣
2. 生成三层预算方案（8000/11000/14000元）
3. 为Carol（孕妇）和Eve（素食）过滤不适合的活动
4. 实时监测疲劳度并建议休息时间

## 项目结构

```
tripmind_network/
├── network.yaml                    # 网络配置
├── agents/                         # Agent 配置文件
│   ├── coordinator.yaml
│   ├── group_preference_agent.yaml
│   ├── budget_balancer_agent.yaml
│   ├── fatigue_tracker_agent.yaml
│   └── health_care_agent.yaml
├── start_network.bat               # 启动网络脚本
├── start_agents.bat                # 启动所有Agent脚本
└── README.md                       # 本文档
```

## 技术特性

### OpenAgents 特性应用

1. **事件驱动架构**
   - 使用 `triggers` 实现事件监听
   - 通过 `send_event()` 实现 Agent 间通信
   - 事件可见性控制（PUBLIC/NETWORK/CHANNEL/DIRECT）

2. **持久化社区**
   - 使用 `workspace.project` Mod 管理旅行项目
   - Agent 状态持久化保存用户偏好
   - 支持多轮对话和方案调整

3. **可视化协作**
   - OpenAgents Studio 实时展示 Agent 协作过程
   - 事件日志提供完整决策追踪链
   - 透明化 AI 决策过程

## 故障排除

### Network 启动失败
- 检查端口 8700 和 8600 是否被占用
- 确认 OpenAgents 已正确安装：`pip install openagents`

### Agent 无法连接
- 确保 Network 已经启动
- 检查 `connection.host` 和 `connection.port` 配置

### API 调用失败
- 确认 OPENAI_API_KEY 已正确设置
- 检查 API Key 是否有效且有余额

## 测试工作流程

运行测试脚本查看完整的多 Agent 协作流程：

```bash
cd tripmind_network
python test_workflow.py
```

测试场景包括：
1. **基础工作流程**：家庭旅行规划（成都5天）
2. **约束冲突处理**：预算超标触发重规划
3. **群体协调**：6人云南游的偏好平衡与投票决策
4. **动态适应**：疲劳状态触发行程调整

## 示例事件

在 `events/` 目录下提供了多个示例事件文件：
- `example_user_input.json`：用户输入示例
- `example_group_travel.json`：群体旅行示例
- `example_constraint_violation.json`：约束冲突示例
- `example_voting_request.json`：投票请求示例
- `example_mood_update.json`：心情更新示例

## 下一步计划

- [x] 添加 User Intent Agent（意图解析）
- [x] 添加 Route Planning Agent（路线规划）
- [x] 添加 Mood Adapter Agent（心情适配）
- [x] 添加 Voting Manager Agent（投票决策）
- [x] 添加 Dynamic Adjuster Agent（动态调整）
- [x] 创建测试工作流程和示例事件
- [ ] 实现完整的约束传播重规划机制
- [ ] 接入实时天气、交通、价格数据 API
- [ ] 添加持久化学习功能（记录用户偏好）
- [ ] 开发 Web 前端界面
- [ ] 录制演示视频

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
