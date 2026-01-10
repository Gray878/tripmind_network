@echo off
REM 启动 5 个核心 Agent
chcp 65001 > nul

echo ========================================
echo   启动 TripMind 5 个核心 Agent
echo ========================================
echo.

call conda activate openagents

if "%ZHIPUAI_API_KEY%"=="" (
    echo ⚠️  警告：未检测到 ZHIPUAI_API_KEY 环境变量
    set /p ZHIPUAI_API_KEY="请输入智谱 AI API Key: "
)

echo ✅ 使用智谱 AI API Key: %ZHIPUAI_API_KEY:~0,8%...
echo ✅ 默认模型: glm-4-flash
echo.

echo [1/5] 启动 Coordinator Agent...
start "Coordinator" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/coordinator.yaml"
timeout /t 3 /nobreak > nul

echo [2/5] 启动 User Intent Agent...
start "User Intent" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/user_intent_agent.yaml"
timeout /t 3 /nobreak > nul

echo [3/5] 启动 Route Planning Agent...
start "Route Planning" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/route_planning_agent.yaml"
timeout /t 3 /nobreak > nul

echo [4/5] 启动 Budget Balancer Agent...
start "Budget Balancer" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/budget_balancer_agent.yaml"
timeout /t 3 /nobreak > nul

echo [5/5] 启动 Health Care Agent...
start "Health Care" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/health_care_agent.yaml"

echo.
echo ========================================
echo   5 个核心 Agent 启动完成！
echo ========================================
echo.
echo 工作流：
echo   用户消息 → Coordinator → User Intent Agent
echo   → Coordinator → Route Planning Agent
echo   → Coordinator → Budget Balancer Agent
echo   → Coordinator → Health Care Agent
echo   → Coordinator → 发送完整计划（行程+预算+健康）
echo.
echo 测试消息示例：
echo   "I want to travel to Tokyo for 5 days with $2000 budget"
echo.
echo 按任意键关闭此窗口...
pause > nul
