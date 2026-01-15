@echo off
REM Set console encoding to UTF-8
chcp 65001 > nul

echo ========================================
echo   Starting TripMind All Agents
echo ========================================
echo.

REM Ensure in openagents environment
call conda activate openagents

REM Read API Key from start_network.bat (need to run start_network.bat first)
if "%ZHIPUAI_API_KEY%"=="" (
    echo Warning: ZHIPUAI_API_KEY environment variable not detected
    echo    Please run start_network.bat first or set API Key manually
    echo.
    set /p ZHIPUAI_API_KEY="Enter ZhipuAI API Key: "
)

echo Using ZhipuAI API Key: %ZHIPUAI_API_KEY:~0,8%...
echo Default Model: glm-4.5
echo API Endpoint: https://open.bigmodel.cn/api/paas/v4/
echo.

echo [Core Coordination Layer]
echo [1/9] Starting Coordinator Agent...
start "Coordinator" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4.5&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/coordinator.yaml"
timeout /t 2 /nobreak > nul

echo.
echo [User Intent Layer]
echo [2/9] Starting User Intent Agent...
start "User Intent" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4.5&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/user_intent_agent.yaml"
timeout /t 2 /nobreak > nul

echo [3/9] Starting Group Preference Agent...
start "Group Preference" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4.5&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/group_preference_agent.yaml"
timeout /t 2 /nobreak > nul

echo [4/9] Starting Budget Balancer Agent...
start "Budget Balancer" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4.5&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/budget_balancer_agent.yaml"
timeout /t 2 /nobreak > nul

echo [5/9] Starting Health Care Agent...
start "Health Care" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4.5&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/health_care_agent.yaml"
timeout /t 2 /nobreak > nul

echo.
echo [Information Layer]
echo [6/9] Starting Web Scraper Agent...
start "Web Scraper" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4.5&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/web_scraper_agent.yaml"
timeout /t 2 /nobreak > nul

echo [7/9] Starting Information Analyzer Agent...
start "Information Analyzer" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4.5&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/information_analyzer_agent.yaml"
timeout /t 2 /nobreak > nul

echo.
echo [Planning Execution Layer]
echo [8/9] Starting Route Planning Agent...
start "Route Planning" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4.5&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/route_planning_agent.yaml"
timeout /t 2 /nobreak > nul

echo [9/9] Starting Dynamic Adjuster Agent...
start "Dynamic Adjuster" cmd /k "chcp 65001 > nul && conda activate openagents && set PYTHONIOENCODING=utf-8&& set DEFAULT_LLM_PROVIDER=openai&& set DEFAULT_LLM_MODEL_NAME=glm-4.5&& set DEFAULT_LLM_API_KEY=%ZHIPUAI_API_KEY%&& set DEFAULT_LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& set OPENAI_API_KEY=%ZHIPUAI_API_KEY%&& set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/&& openagents agent start agents/dynamic_adjuster_agent.yaml"

echo.
echo ========================================
echo   All 9 Agents Started!
echo ========================================
echo.
echo Agent Architecture:
echo   Core Coordination: Coordinator
echo   User Intent: User Intent, Group Preference, Budget Balancer, Health Care
echo   Information: Web Scraper, Information Analyzer
echo   Planning: Route Planning, Dynamic Adjuster
echo.
echo Press any key to close this window...
pause > nul
