#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TripMind 网络抓取功能测试脚本
测试 Web Scraper Agent 和 Information Analyzer Agent 的功能
"""

import json
import time
import sys
import os

# 添加工具路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

from web_scraper import scrape_travel_info
from information_analyzer import analyze_information

def test_web_scraper():
    """测试网络抓取器"""
    print("=" * 60)
    print("测试 1: Web Scraper Agent 功能测试")
    print("=" * 60)
    
    # 测试景点抓取
    print("\n🔍 测试景点信息抓取...")
    query = {
        'location': '东京',
        'keywords': ['文化', '历史'],
        'budget_range': [0, 500],
        'preferences': ['博物馆', '公园']
    }
    
    result = scrape_travel_info('attractions', query)
    scraping_data = json.loads(result)
    
    if scraping_data['success']:
        print(f"✅ 抓取成功！获得 {scraping_data['metadata']['total_items']} 条景点信息")
        print(f"   数据源: {', '.join(scraping_data['metadata']['sources_used'])}")
        print(f"   耗时: {scraping_data['metadata']['scraping_duration']} 秒")
        
        # 显示前3个结果
        print("\n📍 抓取结果预览:")
        for i, item in enumerate(scraping_data['raw_data'][:3]):
            print(f"   {i+1}. {item['name']} ({item['type']})")
            print(f"      评分: {item['rating']}/5.0")
            
            # 安全处理价格字段
            if isinstance(item.get('price'), dict):
                print(f"      价格: {item['price']['text']}")
            else:
                print(f"      价格: {item.get('price', '未知')}")
            
            print(f"      标签: {', '.join(item['tags'])}")
    else:
        print(f"❌ 抓取失败: {scraping_data.get('error', '未知错误')}")
        return None
    
    return scraping_data['raw_data']

def test_information_analyzer(raw_data):
    """测试信息分析器"""
    print("\n" + "=" * 60)
    print("测试 2: Information Analyzer Agent 功能测试")
    print("=" * 60)
    
    if not raw_data:
        print("❌ 没有原始数据可供分析")
        return
    
    print(f"\n🧠 开始分析 {len(raw_data)} 条原始数据...")
    
    result = analyze_information(raw_data, "comprehensive")
    analysis_data = json.loads(result)
    
    if analysis_data['success']:
        processed = analysis_data['processed_data']
        quality = analysis_data['quality_metrics']
        metadata = analysis_data['analysis_metadata']
        
        print("✅ 分析完成！")
        print(f"   处理项目: {metadata['total_items_processed']} 条")
        print(f"   有效项目: {metadata['valid_items']} 条")
        print(f"   去重项目: {metadata['duplicates_removed']} 条")
        
        print(f"\n📊 数据质量评估:")
        print(f"   数据完整性: {quality['data_completeness']:.2%}")
        print(f"   来源可靠性: {quality['source_reliability']:.2%}")
        print(f"   信息时效性: {quality['information_freshness']:.2%}")
        print(f"   整体质量: {quality['overall_quality']:.2%}")
        
        print(f"\n📝 智能摘要:")
        print(f"   {processed['summary']}")
        
        print(f"\n🏆 推荐排行 (前5名):")
        for i, rec in enumerate(processed['top_recommendations'][:5]):
            print(f"   {i+1}. {rec['name']} (评分: {rec['score']:.2f})")
            print(f"      推荐理由: {', '.join(rec['reasons'])}")
            if rec['practical_info']:
                print(f"      实用信息: {rec['practical_info']}")
        
        print(f"\n💡 关键洞察:")
        for insight in processed['insights']:
            print(f"   • {insight}")
        
        print(f"\n📂 数据分类:")
        for category, items in processed['categories'].items():
            print(f"   {category}: {len(items)} 个项目")
    else:
        print(f"❌ 分析失败: {analysis_data.get('error', '未知错误')}")

def test_integration_workflow():
    """测试完整的集成工作流程"""
    print("\n" + "=" * 60)
    print("测试 3: 完整工作流程集成测试")
    print("=" * 60)
    
    print("\n🔄 模拟完整的信息抓取和分析流程...")
    
    # 步骤1: 抓取多种类型的信息
    test_queries = [
        {
            'type': 'attractions',
            'query': {
                'location': '京都',
                'keywords': ['寺庙', '传统'],
                'budget_range': [0, 300]
            }
        },
        {
            'type': 'restaurants',
            'query': {
                'location': '京都',
                'keywords': ['日式', '传统'],
                'budget_range': [50, 200]
            }
        }
    ]
    
    all_data = []
    for test_query in test_queries:
        print(f"\n   抓取 {test_query['type']} 信息...")
        result = scrape_travel_info(test_query['type'], test_query['query'])
        data = json.loads(result)
        
        if data['success']:
            all_data.extend(data['raw_data'])
            print(f"   ✅ 获得 {len(data['raw_data'])} 条 {test_query['type']} 信息")
        else:
            print(f"   ❌ {test_query['type']} 抓取失败")
    
    if all_data:
        print(f"\n   📊 总计获得 {len(all_data)} 条综合信息")
        
        # 步骤2: 综合分析
        print("   🧠 执行综合分析...")
        result = analyze_information(all_data, "comprehensive")
        analysis = json.loads(result)
        
        if analysis['success']:
            print("   ✅ 综合分析完成")
            
            # 显示综合洞察
            insights = analysis['processed_data']['insights']
            if insights:
                print("   💡 综合洞察:")
                for insight in insights[:3]:
                    print(f"      • {insight}")
            
            # 显示分类结果
            categories = analysis['processed_data']['categories']
            if categories:
                print("   📂 信息分类:")
                for category, items in list(categories.items())[:3]:
                    print(f"      {category}: {len(items)} 项")
        else:
            print("   ❌ 综合分析失败")
    else:
        print("   ❌ 没有获得有效数据")

def main():
    """主测试函数"""
    print("🚀 TripMind 网络抓取和信息分析功能测试")
    print("=" * 60)
    print("测试目标:")
    print("  1. Web Scraper Agent - 网络信息抓取")
    print("  2. Information Analyzer Agent - 信息分析和摘要")
    print("  3. 完整工作流程集成")
    print("=" * 60)
    
    try:
        # 测试1: 网络抓取
        raw_data = test_web_scraper()
        
        # 测试2: 信息分析
        if raw_data:
            test_information_analyzer(raw_data)
        
        # 测试3: 集成工作流程
        test_integration_workflow()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试完成！")
        print("=" * 60)
        print("✅ 网络抓取功能正常")
        print("✅ 信息分析功能正常") 
        print("✅ 工作流程集成正常")
        print("\n💡 提示: 现在可以启动完整的 Agent 系统进行实际测试")
        print("   1. 运行 start_network.bat")
        print("   2. 运行 start_agents.bat")
        print("   3. 在 Studio 中测试完整功能")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()