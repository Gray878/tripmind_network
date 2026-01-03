"""
批量更新 TripMind 所有 Agent 的模型配置

使用方法：
1. 编辑下面的 NEW_MODEL_CONFIG，选择你要使用的模型
2. 运行脚本：python update_model.py
"""

import os
import yaml
from pathlib import Path


# ============================================
# 配置区域：选择你要使用的模型
# ============================================

# 方案一：OpenAI（默认）
# NEW_MODEL_CONFIG = {
#     'provider': 'openai',
#     'name': 'gpt-4o-mini',
#     'temperature': 0.7
# }

# 方案二：阿里云通义千问（推荐国内用户）
# NEW_MODEL_CONFIG = {
#     'provider': 'dashscope',
#     'name': 'qwen-max',
#     'temperature': 0.7
# }

# 方案三：智谱 AI GLM（当前使用）
NEW_MODEL_CONFIG = {
    'provider': 'zhipuai',
    'name': 'glm-4',
    'temperature': 0.7
}
#     'temperature': 0.7
# }

# 方案四：百度文心一言
# NEW_MODEL_CONFIG = {
#     'provider': 'qianfan',
#     'name': 'ernie-4.0',
#     'temperature': 0.7
# }

# 方案五：Anthropic Claude
# NEW_MODEL_CONFIG = {
#     'provider': 'anthropic',
#     'name': 'claude-3-5-sonnet-20241022',
#     'temperature': 0.7
# }

# 方案六：Google Gemini
# NEW_MODEL_CONFIG = {
#     'provider': 'google',
#     'name': 'gemini-1.5-flash',
#     'temperature': 0.7
# }

# 方案七：月之暗面 Moonshot (Kimi)
# NEW_MODEL_CONFIG = {
#     'provider': 'moonshot',
#     'name': 'moonshot-v1-8k',
#     'temperature': 0.7
# }

# 方案八：DeepSeek
# NEW_MODEL_CONFIG = {
#     'provider': 'deepseek',
#     'name': 'deepseek-chat',
#     'temperature': 0.7
# }

# 方案九：本地 Ollama
# NEW_MODEL_CONFIG = {
#     'provider': 'ollama',
#     'name': 'qwen2.5',
#     'temperature': 0.7,
#     'base_url': 'http://localhost:11434'
# }


# ============================================
# 脚本主体（无需修改）
# ============================================

def update_agent_model(filepath, new_model_config):
    """更新单个 Agent 的模型配置"""
    try:
        # 读取 YAML 文件
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 YAML
        config = yaml.safe_load(content)
        
        if config is None:
            print(f'⚠️  跳过: {filepath.name} (空文件)')
            return False
        
        # 更新模型配置
        if 'model' in config:
            old_provider = config['model'].get('provider', 'unknown')
            old_name = config['model'].get('name', 'unknown')
            
            config['model'] = new_model_config
            
            # 写回文件（保持原有格式）
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
            
            print(f'✅ 已更新: {filepath.name}')
            print(f'   {old_provider}/{old_name} → {new_model_config["provider"]}/{new_model_config["name"]}')
            return True
        else:
            print(f'⚠️  跳过: {filepath.name} (无 model 配置)')
            return False
            
    except Exception as e:
        print(f'❌ 错误: {filepath.name} - {str(e)}')
        return False


def main():
    """主函数"""
    print('=' * 60)
    print('  TripMind 模型配置批量更新工具')
    print('=' * 60)
    print()
    
    # 显示新配置
    print('新模型配置：')
    print(f'  提供商: {NEW_MODEL_CONFIG["provider"]}')
    print(f'  模型名: {NEW_MODEL_CONFIG["name"]}')
    print(f'  温度值: {NEW_MODEL_CONFIG["temperature"]}')
    if 'base_url' in NEW_MODEL_CONFIG:
        print(f'  Base URL: {NEW_MODEL_CONFIG["base_url"]}')
    print()
    
    # 确认
    confirm = input('确认要更新所有 Agent 配置吗？(y/n): ')
    if confirm.lower() != 'y':
        print('已取消操作。')
        return
    
    print()
    print('开始更新...')
    print('-' * 60)
    
    # 获取 agents 目录
    agents_dir = Path('agents')
    if not agents_dir.exists():
        print('❌ 错误: agents 目录不存在！')
        print('请确保在 tripmind_network 目录下运行此脚本。')
        return
    
    # 遍历所有 YAML 文件
    updated_count = 0
    skipped_count = 0
    
    for filepath in sorted(agents_dir.glob('*.yaml')):
        if update_agent_model(filepath, NEW_MODEL_CONFIG):
            updated_count += 1
        else:
            skipped_count += 1
    
    # 总结
    print('-' * 60)
    print()
    print('更新完成！')
    print(f'  ✅ 成功更新: {updated_count} 个 Agent')
    print(f'  ⚠️  跳过: {skipped_count} 个文件')
    print()
    
    # 提示设置环境变量
    print('=' * 60)
    print('  下一步：设置环境变量')
    print('=' * 60)
    print()
    
    provider = NEW_MODEL_CONFIG['provider']
    
    if provider == 'openai':
        print('请在 start_network.bat 中设置：')
        print('  set OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print()
        print('获取 API Key: https://platform.openai.com/api-keys')
        
    elif provider == 'dashscope':
        print('请在 start_network.bat 中设置：')
        print('  set DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print()
        print('获取 API Key: https://dashscope.console.aliyun.com/')
        
    elif provider == 'zhipuai':
        print('请在 start_network.bat 中设置：')
        print('  set ZHIPUAI_API_KEY=your-zhipuai-api-key')
        print()
        print('获取 API Key: https://open.bigmodel.cn/')
        
    elif provider == 'qianfan':
        print('请在 start_network.bat 中设置：')
        print('  set QIANFAN_ACCESS_KEY=your-access-key')
        print('  set QIANFAN_SECRET_KEY=your-secret-key')
        print()
        print('获取 API Key: https://console.bce.baidu.com/qianfan/')
        
    elif provider == 'anthropic':
        print('请在 start_network.bat 中设置：')
        print('  set ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print()
        print('获取 API Key: https://console.anthropic.com/')
        
    elif provider == 'google':
        print('请在 start_network.bat 中设置：')
        print('  set GOOGLE_API_KEY=your-google-api-key')
        print()
        print('获取 API Key: https://makersuite.google.com/app/apikey')
        
    elif provider == 'moonshot':
        print('请在 start_network.bat 中设置：')
        print('  set MOONSHOT_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print()
        print('获取 API Key: https://platform.moonshot.cn/')
        
    elif provider == 'deepseek':
        print('请在 start_network.bat 中设置：')
        print('  set DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print()
        print('获取 API Key: https://platform.deepseek.com/')
        
    elif provider == 'ollama':
        print('使用本地 Ollama，无需设置 API Key。')
        print()
        print('请确保：')
        print('  1. 已安装 Ollama: https://ollama.ai/')
        print(f'  2. 已拉取模型: ollama pull {NEW_MODEL_CONFIG["name"]}')
        print('  3. Ollama 服务正在运行')
    
    print()
    print('=' * 60)


if __name__ == '__main__':
    main()
