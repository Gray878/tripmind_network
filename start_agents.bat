@echo off
REM 设置控制台编码为 UTF-8，解决中文乱码问题
chcp 65001 > nul

echo ========================================
echo   启动 TripMind 所有 Agent
echo ========================================
echo.

REM 确保在 openagents 环境中
call conda activate openagents

REM 从 start_network.bat 读取 API Key（需要先运行 start_network.bat）
if "%ZHIPUAI_API_KEY%"=="" (
    echo ⚠️  警告：未检测到 ZHIPUAI_API_KEY 环境变量
    echo    请先运行 start_network.bat 或手动设置 API Key
    echo.
    set /p ZHIPUAI_API_KEY="请输入智谱 AI API Key: "
)

echo ✅ 使用智谱 AI API Key: %ZHIPUAI_API_KEY:~0,8%...
echo ✅ 默认模型: glm-4-flash
echo ✅ API 端点: https://open.bigmodel.cn/api/paas/v4/
echo.

echo [核心协调层]
echo [1/10] 启动 Coordinator Agent...
start "Coordinator" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/coordinator.yaml"
timeout /t 2 /nobreak > nul

echo.
echo [用户意图层]
echo [2/10] 启动 User Intent Agent...
start "User Intent" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/user_intent_agent.yaml"
timeout /t 2 /nobreak > nul

echo [3/10] 启动 Group Preference Agent...
start "Group Preference" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/group_preference_agent.yaml"
timeout /t 2 /nobreak > nul

echo [4/10] 启动 Budget Balancer Agent...
start "Budget Balancer" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/budget_balancer_agent.yaml"
timeout /t 2 /nobreak > nul

echo [5/10] 启动 Health Care Agent...
start "Health Care" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/health_care_agent.yaml"
timeout /t 2 /nobreak > nul

echo.
echo [规划执行层]
echo [6/10] 启动 Route Planning Agent...
start "Route Planning" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/route_planning_agent.yaml"
timeout /t 2 /nobreak > nul

echo [7/10] 启动 Fatigue Tracker Agent...
start "Fatigue Tracker" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/fatigue_tracker_agent.yaml"
timeout /t 2 /nobreak > nul

echo [8/10] 启动 Voting Manager Agent...
start "Voting Manager" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/voting_manager_agent.yaml"
timeout /t 2 /nobreak > nul

echo.
echo [监控调整层]
echo [9/10] 启动 Mood Adapter Agent...
start "Mood Adapter" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/mood_adapter_agent.yaml"
timeout /t 2 /nobreak > nul

echo [10/10] 启动 Dynamic Adjuster Agent...
start "Dynamic Adjuster" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4-flash&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/dynamic_adjuster_agent.yaml"

echo.
echo ========================================
echo   所有 10 个 Agent 启动完成！
echo ========================================
echo.
echo Agent 架构：
echo   核心协调层：Coordinator
echo   用户意图层：User Intent, Group Preference, Budget Balancer, Health Care
echo   规划执行层：Route Planning, Fatigue Tracker, Voting Manager
echo   监控调整层：Mood Adapter, Dynamic Adjuster
echo.
echo 按任意键关闭此窗口...
pause > nul
