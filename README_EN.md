# TripMind - Group Travel Intelligent Coordination System

English | [中文](README.md)

A multi-agent travel planning system based on the OpenAgents framework.

📄 [Documentation](https://oxb708x94fk.feishu.cn/wiki/UTxwwxE3uifqmFkvgwUcjzOtnXl) | 🎬 [Demo Video](https://b23.tv/pbaMt6y)

## Project Introduction

TripMind is a multi-agent group travel planning system based on the OpenAgents framework.

**Problem We Solve**: When a group of people want to travel together, everyone has different preferences, budgets, and physical conditions. How do you coordinate all these needs and generate an itinerary that satisfies everyone?

**Three Major Pain Points**:
- **Preference Conflicts**: Some people love food, some love adventure, some love shopping
- **Budget Differences**: Member budgets range from ¥8,000 to ¥15,000
- **Special Needs**: Pregnant women need relaxed itineraries, vegetarians need specific restaurants

**Core Innovation**: Through collaboration of 9 specialized agents, we achieve a complete pipeline of "Intent Parsing → Information Collection → Intelligent Planning". Each agent focuses on a single responsibility, collaborating through event-driven mechanisms to generate personalized itineraries that balance all members' needs.

**OpenAgents Key Features Used**:
- Event-Driven Architecture: Agents communicate asynchronously via send_event, enabling loose coupling
- Triggers Mechanism: Each agent listens for specific events and automatically triggers processing logic
- Progress Visualization: Designed progress.update events so users can see the agent call chain in real-time
- workspace.project Mod: Manages travel project lifecycle
- Studio Visualization: Real-time display of agent collaboration process

## Agent Architecture

The system contains 9 agents in four layers:

| Layer | Agent | Responsibility |
|-------|-------|----------------|
| Core Coordination | Coordinator | Receive requests, dispatch tasks, aggregate results |
| User Intent | User Intent | Parse natural language, extract structured information |
| | Group Preference | Analyze group preferences, identify conflicts |
| | Budget Balancer | Balance budgets, design tiered solutions |
| | Health Care | Health considerations, filter unsuitable activities |
| Information | Web Scraper | Scrape real-time travel information |
| | Information Analyzer | Data analysis and recommendation ranking |
| Planning | Route Planning | Generate detailed itineraries |
| | Dynamic Adjuster | Dynamic adjustment and optimization |

## Requirements

- Python 3.10+
- Conda (recommended)
- ZhipuAI API Key (get from https://open.bigmodel.cn/)

## Quick Start

### 1. Create Python Environment

```bash
conda create -n openagents python=3.10
conda activate openagents
```

### 2. Install OpenAgents

```bash
pip install openagents
```

### 3. Configure API Key

Copy the example file and set your API Key:
```batch
copy start_network.bat.example start_network.bat
```

Edit `start_network.bat` and set your ZhipuAI API Key:
```batch
set ZHIPUAI_API_KEY=your-api-key-here
```

### 4. Start Network

```bash
start_network.bat
```

### 5. Start Agents

```bash
start_agents.bat
```

### 6. Access Studio

Open browser: http://localhost:8700

## Usage Example

Create a new project in Studio and input:

```
We are 5 people planning a 7-day trip to Japan:

Members:
- Alice (25F): Likes culture and food, budget ¥12,000, average stamina
- Bob (28M): Likes nature and adventure, budget ¥15,000, good stamina
- Carol (30F): Likes shopping and food, budget ¥10,000, pregnant
- David (26M): Likes anime and tech, budget ¥8,000, budget-sensitive
- Eve (27F): Likes art and photography, budget ¥13,000, vegetarian

Please help us plan a trip that balances everyone's needs.
```

## Agent Call Chain

The system displays the currently active agent:
```
[Agent Call Chain]
-> coordinator -> user-intent-agent (task.parse_intent)
-> user-intent-agent -> route-planning-agent (intent.parsed)
-> route-planning-agent -> coordinator (route.planned)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Encoding error `'gbk' codec can't decode` | Ensure `chcp 65001` is in startup scripts |
| API call failed | Check if ZHIPUAI_API_KEY is correct |

## License

MIT License
