#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TripMind Information Analyzer Tool
信息分析工具 - 对抓取的数据进行智能分析、摘要和质量评估
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import Counter, defaultdict
import re

try:
    from openagents import tool
except ImportError:
    # 如果 openagents 不可用，定义一个空的装饰器
    def tool(func=None, **kwargs):
        if func is None:
            return lambda f: f
        return func

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InformationAnalyzer:
    """信息分析器主类"""
    
    def __init__(self):
        # 质量评估权重
        self.quality_weights = {
            'completeness': 0.3,      # 完整性
            'reliability': 0.25,      # 可靠性
            'freshness': 0.2,         # 时效性
            'consistency': 0.15,      # 一致性
            'relevance': 0.1          # 相关性
        }
        
        # 推荐评分权重
        self.recommendation_weights = {
            'rating': 0.3,            # 评分
            'popularity': 0.2,        # 受欢迎程度
            'price_value': 0.2,       # 性价比
            'uniqueness': 0.15,       # 独特性
            'accessibility': 0.15     # 可达性
        }
    
    def analyze_information(self, raw_data: List[Dict[str, Any]], analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        主要分析接口
        
        Args:
            raw_data: 原始抓取数据列表
            analysis_type: 分析类型 (comprehensive|quick|detailed)
            
        Returns:
            分析结果字典
        """
        try:
            logger.info(f"开始分析 {len(raw_data)} 条数据，分析类型: {analysis_type}")
            
            if not raw_data:
                return self._create_empty_result("没有数据需要分析")
            
            # 数据预处理
            cleaned_data = self._clean_and_deduplicate(raw_data)
            logger.info(f"数据清洗完成，剩余 {len(cleaned_data)} 条有效数据")
            
            # 执行分析
            analysis_result = {
                'summary': self._generate_summary(cleaned_data),
                'top_recommendations': self._generate_recommendations(cleaned_data),
                'insights': self._extract_insights(cleaned_data),
                'categories': self._categorize_data(cleaned_data)
            }
            
            # 质量评估
            quality_metrics = self._assess_quality(cleaned_data, raw_data)
            
            # 分析元数据
            analysis_metadata = {
                'total_items_processed': len(raw_data),
                'valid_items': len(cleaned_data),
                'duplicates_removed': len(raw_data) - len(cleaned_data),
                'analysis_duration': 0,  # 实际实现中会计算
                'analysis_method': '智能分析',
                'analyzed_at': datetime.now().isoformat()
            }
            
            result = {
                'success': True,
                'processed_data': analysis_result,
                'quality_metrics': quality_metrics,
                'analysis_metadata': analysis_metadata
            }
            
            logger.info("信息分析完成")
            return result
            
        except Exception as e:
            logger.error(f"分析过程中发生错误: {str(e)}")
            return self._create_error_result(f"分析失败: {str(e)}")
    
    def _clean_and_deduplicate(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """数据清洗和去重"""
        cleaned_data = []
        seen_items = set()
        
        for item in raw_data:
            # 基础数据验证
            if not self._is_valid_item(item):
                continue
            
            # 生成唯一标识符用于去重
            item_key = self._generate_item_key(item)
            if item_key in seen_items:
                continue
            
            # 数据清洗
            cleaned_item = self._clean_item(item)
            cleaned_data.append(cleaned_item)
            seen_items.add(item_key)
        
        return cleaned_data
    
    def _is_valid_item(self, item: Dict[str, Any]) -> bool:
        """验证数据项是否有效"""
        required_fields = ['name']
        return all(field in item and item[field] for field in required_fields)
    
    def _generate_item_key(self, item: Dict[str, Any]) -> str:
        """生成项目的唯一标识符"""
        name = item.get('name', '').lower().strip()
        location = ''
        
        if 'location' in item and isinstance(item['location'], dict):
            location = item['location'].get('address', '').lower().strip()
        
        return f"{name}|{location}"
    
    def _clean_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """清洗单个数据项"""
        cleaned = item.copy()
        
        # 清洗文本字段
        text_fields = ['name', 'description', 'type']
        for field in text_fields:
            if field in cleaned and isinstance(cleaned[field], str):
                cleaned[field] = self._clean_text(cleaned[field])
        
        # 标准化评分
        if 'rating' in cleaned:
            cleaned['rating'] = self._normalize_rating(cleaned['rating'])
        
        # 标准化价格
        if 'price' in cleaned:
            cleaned['price'] = self._normalize_price(cleaned['price'])
        
        return cleaned
    
    def _clean_text(self, text: str) -> str:
        """清洗文本内容"""
        if not text:
            return ""
        
        # 移除多余空白字符
        text = ' '.join(text.split())
        
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?()（），。！？]', '', text)
        
        return text.strip()
    
    def _normalize_rating(self, rating: Any) -> float:
        """标准化评分到 0-5 范围"""
        if isinstance(rating, (int, float)):
            return max(0.0, min(5.0, float(rating)))
        elif isinstance(rating, str):
            # 尝试从字符串中提取数字
            match = re.search(r'(\d+(?:\.\d+)?)', rating)
            if match:
                return max(0.0, min(5.0, float(match.group(1))))
        return 0.0
    
    def _normalize_price(self, price: Any) -> Dict[str, Any]:
        """标准化价格信息"""
        if isinstance(price, dict):
            return price
        elif isinstance(price, str):
            # 解析价格字符串
            if '免费' in price or 'free' in price.lower():
                return {'amount': 0, 'currency': 'CNY', 'text': '免费'}
            
            # 提取数字
            match = re.search(r'(\d+(?:\.\d+)?)', price)
            if match:
                amount = float(match.group(1))
                currency = 'CNY'
                if '$' in price:
                    currency = 'USD'
                elif '€' in price:
                    currency = 'EUR'
                return {'amount': amount, 'currency': currency$' in price:
                    currency = 'USD'
                elif '€' in price:
                    currency = 'EUR'
                return {'amount': amount, 'currency': currency, 'text': price}
        
        return {'amount': 0, 'currency': 'CNY', 'text': '价格未知'}
    
    def _generate_summary(self, data: List[Dict[str, Any]]) -> str:
        """生成数据摘要"""
        if not data:
            return "没有找到相关信息。"
        
        total_count = len(data)
        
        # 统计类型分布
        types = [item.get('type', '未知') for item in data]
        type_counts = Counter(types)
        
        # 统计价格分布
        free_count = sum(1 for item in data 
                        if isinstance(item.get('price'), dict) and item['price'].get('amount', 0) == 0)
        
        # 统计评分分布
        ratings = [item.get('rating', 0) for item in data if item.get('rating', 0) > 0]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # 生成摘要文本
        summary_parts = [
            f"共找到 {total_count} 个相关项目。"
        ]
        
        if type_counts:
            top_types = type_counts.most_common(3)
            type_text = "、".join([f"{t}({c}个)" for t, c in top_types])
            summary_parts.append(f"主要类型包括：{type_text}。")
        
        if free_count > 0:
            summary_parts.append(f"其中 {free_count} 个为免费项目。")
        
        if avg_rating > 0:
            summary_parts.append(f"平均评分 {avg_rating:.1f} 分。")
        
        return " ".join(summary_parts)
    
    def _generate_recommendations(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """生成推荐列表"""
        if not data:
            return []
        
        # 为每个项目计算推荐分数
        scored_items = []
        for item in data:
            score = self._calculate_recommendation_score(item)
            recommendation = {
                'name': item.get('name', ''),
                'type': item.get('type', ''),
                'score': score,
                'reasons': self._generate_recommendation_reasons(item),
                'highlights': self._extract_highlights(item),
                'practical_info': self._generate_practical_info(item)
            }
            scored_items.append(recommendation)
        
        # 按分数排序，返回前10个
        scored_items.sort(key=lambda x: x['score'], reverse=True)
        return scored_items[:10]
    
    def _calculate_recommendation_score(self, item: Dict[str, Any]) -> float:
        """计算推荐分数"""
        score = 0.0
        
        # 评分因子
        rating = item.get('rating', 0)
        if rating > 0:
            score += (rating / 5.0) * self.recommendation_weights['rating']
        
        # 受欢迎程度因子（基于评论数量）
        review_count = item.get('review_count', 0)
        if review_count > 0:
            popularity_score = min(1.0, review_count / 1000)  # 标准化到0-1
            score += popularity_score * self.recommendation_weights['popularity']
        
        # 性价比因子
        price_info = item.get('price', {})
        if isinstance(price_info, dict):
            amount = price_info.get('amount', 0)
            if amount == 0:  # 免费项目加分
                score += 1.0 * self.recommendation_weights['price_value']
            elif amount < 100:  # 低价项目加分
                score += 0.8 * self.recommendation_weights['price_value']
            elif amount < 300:  # 中价项目
                score += 0.6 * self.recommendation_weights['price_value']
        
        # 独特性因子（基于标签和描述）
        tags = item.get('tags', [])
        unique_tags = ['独特', '特色', '罕见', '隐藏', '秘密']
        if any(tag in ' '.join(tags) for tag in unique_tags):
            score += 1.0 * self.recommendation_weights['uniqueness']
        
        # 可达性因子（基于开放时间等）
        opening_hours = item.get('opening_hours', '')
        if opening_hours and '24小时' in opening_hours:
            score += 1.0 * self.recommendation_weights['accessibility']
        elif opening_hours:
            score += 0.7 * self.recommendation_weights['accessibility']
        
        return min(1.0, score)  # 限制在0-1范围内
    
    def _generate_recommendation_reasons(self, item: Dict[str, Any]) -> List[str]:
        """生成推荐理由"""
        reasons = []
        
        # 基于评分
        rating = item.get('rating', 0)
        if rating >= 4.5:
            reasons.append("评分极高")
        elif rating >= 4.0:
            reasons.append("评分很好")
        
        # 基于价格
        price_info = item.get('price', {})
        if isinstance(price_info, dict) and price_info.get('amount', 0) == 0:
            reasons.append("免费参观")
        
        # 基于类型和标签
        tags = item.get('tags', [])
        if '文化' in tags:
            reasons.append("文化价值高")
        if '历史' in tags:
            reasons.append("历史意义重大")
        if '自然' in tags:
            reasons.append("自然风光优美")
        
        # 基于设施
        facilities = item.get('facilities', [])
        if '停车场' in facilities:
            reasons.append("交通便利")
        if '无障碍通道' in facilities:
            reasons.append("设施完善")
        
        return reasons[:3]  # 最多返回3个理由
    
    def _extract_highlights(self, item: Dict[str, Any]) -> List[str]:
        """提取亮点信息"""
        highlights = []
        
        # 从现有的 highlights 字段获取
        if 'highlights' in item and isinstance(item['highlights'], list):
            highlights.extend(item['highlights'])
        
        # 从描述中提取关键信息
        description = item.get('description', '')
        if description:
            # 简单的关键词提取
            keywords = ['最大', '最古老', '最著名', '独特', '罕见', '珍贵']
            for keyword in keywords:
                if keyword in description:
                    # 提取包含关键词的句子片段
                    sentences = description.split('。')
                    for sentence in sentences:
                        if keyword in sentence:
                            highlights.append(sentence.strip())
                            break
        
        return highlights[:3]  # 最多返回3个亮点
    
    def _generate_practical_info(self, item: Dict[str, Any]) -> str:
        """生成实用信息"""
        info_parts = []
        
        # 开放时间
        opening_hours = item.get('opening_hours', '')
        if opening_hours:
            info_parts.append(f"开放时间：{opening_hours}")
        
        # 建议游览时间
        duration = item.get('duration', '')
        if duration:
            info_parts.append(f"建议游览时间：{duration}")
        
        # 最佳游览时间
        best_time = item.get('best_time', '')
        if best_time:
            info_parts.append(f"最佳时间：{best_time}")
        
        # 人流情况
        crowd_level = item.get('crowd_level', '')
        if crowd_level:
            info_parts.append(f"人流：{crowd_level}")
        
        return " | ".join(info_parts)
    
    def _extract_insights(self, data: List[Dict[str, Any]]) -> List[str]:
        """提取关键洞察"""
        insights = []
        
        if not data:
            return insights
        
        # 价格洞察
        free_items = [item for item in data 
                     if isinstance(item.get('price'), dict) and item['price'].get('amount', 0) == 0]
        if len(free_items) >= len(data) * 0.3:  # 30%以上免费
            insights.append(f"发现 {len(free_items)} 个免费景点，适合预算有限的旅行者")
        
        # 类型分布洞察
        types = [item.get('type', '') for item in data]
        type_counts = Counter(types)
        if type_counts:
            most_common_type = type_counts.most_common(1)[0]
            if most_common_type[1] >= len(data) * 0.4:  # 40%以上同类型
                insights.append(f"{most_common_type[0]}类景点较多，建议合理安排时间")
        
        # 评分洞察
        high_rated = [item for item in data if item.get('rating', 0) >= 4.5]
        if len(high_rated) >= 3:
            insights.append(f"发现 {len(high_rated)} 个高评分景点（4.5分以上），质量有保障")
        
        # 设施洞察
        parking_available = [item for item in data 
                           if 'facilities' in item and '停车场' in item['facilities']]
        if len(parking_available) >= len(data) * 0.5:
            insights.append("大部分景点提供停车场，适合自驾游")
        
        # 时间洞察
        all_day_open = [item for item in data 
                       if '24小时' in item.get('opening_hours', '')]
        if all_day_open:
            insights.append(f"有 {len(all_day_open)} 个景点24小时开放，时间安排更灵活")
        
        return insights[:5]  # 最多返回5个洞察
    
    def _categorize_data(self, data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """数据分类"""
        categories = defaultdict(list)
        
        for item in data:
            # 按价格分类
            price_info = item.get('price', {})
            if isinstance(price_info, dict) and price_info.get('amount', 0) == 0:
                categories['免费景点'].append(item)
            
            # 按类型分类
            item_type = item.get('type', '其他')
            categories[f"{item_type}类"].append(item)
            
            # 按标签分类
            tags = item.get('tags', [])
            for tag in tags:
                if tag in ['文化', '历史', '自然', '艺术', '娱乐']:
                    categories[f"{tag}景点"].append(item)
        
        # 只返回有内容的分类，并限制每个分类的项目数量
        result = {}
        for category, items in categories.items():
            if len(items) >= 2:  # 至少2个项目才成为一个分类
                result[category] = items[:5]  # 每个分类最多5个项目
        
        return result
    
    def _assess_quality(self, cleaned_data: List[Dict[str, Any]], raw_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """评估数据质量"""
        if not raw_data:
            return {
                'data_completeness': 0.0,
                'source_reliability': 0.0,
                'information_freshness': 0.0,
                'overall_quality': 0.0
            }
        
        # 数据完整性
        completeness = len(cleaned_data) / len(raw_data) if raw_data else 0.0
        
        # 来源可靠性（基于数据源）
        reliability = 0.9  # 模拟值，实际实现中会根据数据源评估
        
        # 信息时效性（基于抓取时间）
        freshness = 0.85  # 模拟值，实际实现中会根据时间戳计算
        
        # 整体质量
        overall = (
            completeness * self.quality_weights['completeness'] +
            reliability * self.quality_weights['reliability'] +
            freshness * self.quality_weights['freshness']
        )
        
        return {
            'data_completeness': round(completeness, 2),
            'source_reliability': round(reliability, 2),
            'information_freshness': round(freshness, 2),
            'overall_quality': round(overall, 2)
        }
    
    def _create_empty_result(self, message: str) -> Dict[str, Any]:
        """创建空结果"""
        return {
            'success': True,
            'processed_data': {
                'summary': message,
                'top_recommendations': [],
                'insights': [],
                'categories': {}
            },
            'quality_metrics': {
                'data_completeness': 0.0,
                'source_reliability': 0.0,
                'information_freshness': 0.0,
                'overall_quality': 0.0
            },
            'analysis_metadata': {
                'total_items_processed': 0,
                'valid_items': 0,
                'duplicates_removed': 0,
                'analysis_duration': 0,
                'analysis_method': '智能分析',
                'analyzed_at': datetime.now().isoformat()
            }
        }
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """创建错误结果"""
        return {
            'success': False,
            'error': error_message,
            'processed_data': {
                'summary': '分析失败',
                'top_recommendations': [],
                'insights': [],
                'categories': {}
            },
            'quality_metrics': {
                'data_completeness': 0.0,
                'source_reliability': 0.0,
                'information_freshness': 0.0,
                'overall_quality': 0.0
            },
            'analysis_metadata': {
                'total_items_processed': 0,
                'valid_items': 0,
                'duplicates_removed': 0,
                'analysis_duration': 0,
                'analysis_method': '智能分析',
                'analyzed_at': datetime.now().isoformat()
            }
        }

# 全局分析器实例
analyzer = InformationAnalyzer()

@tool(
    name="analyze_information",
    description="分析抓取的旅行信息，提供结构化分析结果，包括摘要、推荐列表和洞察信息"
)
def analyze_information(raw_data: List[Dict[str, Any]], analysis_type: str = "comprehensive") -> str:
    """
    OpenAgents 工具接口
    
    Args:
        raw_data: 原始数据列表
        analysis_type: 分析类型
        
    Returns:
        JSON 格式的分析结果
    """
    result = analyzer.analyze_information(raw_data, analysis_type)
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 测试代码
    test_data = [
        {
            'name': '测试博物馆',
            'type': '博物馆',
            'rating': 4.5,
            'price': {'amount': 0, 'currency': 'CNY', 'text': '免费'},
            'tags': ['文化', '历史'],
            'description': '这是一个展示历史文化的博物馆'
        }
    ]
    
    result = analyze_information(test_data)
    print("测试结果:")
    print(result)