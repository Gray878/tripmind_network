#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
景点信息抓取器 - 专门抓取旅游景点相关信息
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class AttractionScraper(BaseScraper):
    """景点抓取器"""
    
    def __init__(self):
        super().__init__("attraction_scraper", "https://example.com")
        
        # 景点类型映射
        self.attraction_types = {
            '博物馆': ['museum', '博物馆', '展览馆'],
            '公园': ['park', '公园', '花园', '植物园'],
            '寺庙': ['temple', '寺庙', '教堂', '清真寺'],
            '景点': ['attraction', '景点', '名胜', '古迹'],
            '娱乐': ['entertainment', '娱乐', '游乐园', '主题公园'],
            '购物': ['shopping', '购物', '商场', '市场'],
            '文化': ['culture', '文化', '艺术', '画廊']
        }
    
    def scrape(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        抓取景点信息
        
        Args:
            query: 查询参数，包含 location, keywords, budget_range 等
            
        Returns:
            景点信息列表
        """
        if not self.validate_query(query, ['location']):
            return []
        
        location = query.get('location', '')
        keywords = query.get('keywords', [])
        budget_range = query.get('budget_range', [0, 10000])
        
        logger.info(f"开始抓取 {location} 的景点信息，关键词: {keywords}")
        
        # 在实际实现中，这里会调用真实的网站API或抓取网页
        # 目前使用模拟数据进行演示
        attractions = self._generate_mock_attractions(location, keywords, budget_range)
        
        logger.info(f"成功抓取到 {len(attractions)} 个景点")
        return attractions
    
    def _generate_mock_attractions(self, location: str, keywords: List[str], budget_range: List[int]) -> List[Dict[str, Any]]:
        """生成模拟景点数据"""
        
        # 基础景点模板
        base_attractions = [
            {
                'name': f'{location}历史博物馆',
                'type': '博物馆',
                'category': 'culture',
                'rating': 4.5,
                'review_count': 1250,
                'price': {'amount': 0, 'currency': 'CNY', 'text': '免费'},
                'opening_hours': '9:00-17:00 (周一闭馆)',
                'duration': '2-3小时',
                'description': f'展示{location}丰富历史文化的综合性博物馆，收藏了大量珍贵文物和历史资料。',
                'highlights': ['古代文物展', '历史文献', '互动体验区'],
                'location': {
                    'address': f'{location}市中心区文化街1号',
                    'district': '中心区',
                    'lat': 35.7148 + self._random_offset(),
                    'lng': 139.7967 + self._random_offset()
                },
                'tags': ['历史', '文化', '教育', '免费'],
                'facilities': ['停车场', '无障碍通道', '纪念品店', '咖啡厅'],
                'best_time': '上午',
                'crowd_level': '中等',
                'photo_spots': ['大厅雕塑', '历史长廊', '屋顶花园']
            },
            {
                'name': f'{location}中央公园',
                'type': '公园',
                'category': 'nature',
                'rating': 4.2,
                'review_count': 890,
                'price': {'amount': 0, 'currency': 'CNY', 'text': '免费'},
                'opening_hours': '24小时开放',
                'duration': '1-4小时',
                'description': f'{location}最大的城市公园，绿树成荫，湖光山色，是市民休闲娱乐的好去处。',
                'highlights': ['人工湖', '樱花大道', '儿童游乐区'],
                'location': {
                    'address': f'{location}中央区公园路88号',
                    'district': '中央区',
                    'lat': 35.7058 + self._random_offset(),
                    'lng': 139.7958 + self._random_offset()
                },
                'tags': ['自然', '休闲', '运动', '免费', '家庭'],
                'facilities': ['公共厕所', '休息亭', '健身器材', '自行车租赁'],
                'best_time': '早晨或傍晚',
                'crowd_level': '较高',
                'photo_spots': ['湖心亭', '樱花树下', '日落观景台']
            },
            {
                'name': f'{location}艺术画廊',
                'type': '画廊',
                'category': 'culture',
                'rating': 4.3,
                'review_count': 456,
                'price': {'amount': 50, 'currency': 'CNY', 'text': '¥50'},
                'opening_hours': '10:00-18:00 (周二闭馆)',
                'duration': '1-2小时',
                'description': f'展示当代艺术作品的现代画廊，定期举办各种艺术展览和文化活动。',
                'highlights': ['当代艺术展', '雕塑花园', '艺术工作坊'],
                'location': {
                    'address': f'{location}艺术区创意大道15号',
                    'district': '艺术区',
                    'lat': 35.7248 + self._random_offset(),
                    'lng': 139.8067 + self._random_offset()
                },
                'tags': ['艺术', '文化', '现代', '创意'],
                'facilities': ['艺术品商店', '咖啡厅', '讲座厅'],
                'best_time': '下午',
                'crowd_level': '较低',
                'photo_spots': ['主展厅', '雕塑花园', '创意角落']
            },
            {
                'name': f'{location}古城墙遗址',
                'type': '古迹',
                'category': 'history',
                'rating': 4.0,
                'review_count': 678,
                'price': {'amount': 30, 'currency': 'CNY', 'text': '¥30'},
                'opening_hours': '8:00-18:00',
                'duration': '1-2小时',
                'description': f'{location}保存完好的古代城墙遗址，见证了城市的历史变迁。',
                'highlights': ['古城墙', '瞭望塔', '历史展示区'],
                'location': {
                    'address': f'{location}老城区古城路',
                    'district': '老城区',
                    'lat': 35.6948 + self._random_offset(),
                    'lng': 139.7767 + self._random_offset()
                },
                'tags': ['历史', '古迹', '文化', '摄影'],
                'facilities': ['导览服务', '休息区', '纪念品店'],
                'best_time': '上午或下午',
                'crowd_level': '中等',
                'photo_spots': ['城墙顶部', '古门楼', '护城河']
            },
            {
                'name': f'{location}科技馆',
                'type': '科技馆',
                'category': 'education',
                'rating': 4.4,
                'review_count': 1100,
                'price': {'amount': 80, 'currency': 'CNY', 'text': '¥80'},
                'opening_hours': '9:00-17:00 (周一闭馆)',
                'duration': '3-4小时',
                'description': f'现代化的科技展览馆，通过互动体验展示最新科技成果。',
                'highlights': ['VR体验区', '机器人展示', '天文馆'],
                'location': {
                    'address': f'{location}新区科技大道100号',
                    'district': '新区',
                    'lat': 35.7348 + self._random_offset(),
                    'lng': 139.8167 + self._random_offset()
                },
                'tags': ['科技', '教育', '互动', '家庭', '现代'],
                'facilities': ['停车场', '餐厅', '纪念品店', '休息区'],
                'best_time': '全天',
                'crowd_level': '较高',
                'photo_spots': ['VR体验区', '机器人展厅', '天文馆穹顶']
            }
        ]
        
        # 根据关键词过滤景点
        filtered_attractions = []
        for attraction in base_attractions:
            if self._matches_keywords(attraction, keywords):
                # 检查价格是否在预算范围内
                price_amount = attraction['price']['amount']
                if budget_range[0] <= price_amount <= budget_range[1]:
                    # 添加抓取元数据
                    attraction.update({
                        'source': 'mock_attraction_scraper',
                        'scraped_at': datetime.now().isoformat(),
                        'data_quality': self._calculate_data_quality(attraction)
                    })
                    filtered_attractions.append(attraction)
        
        return filtered_attractions
    
    def _matches_keywords(self, attraction: Dict[str, Any], keywords: List[str]) -> bool:
        """检查景点是否匹配关键词"""
        if not keywords:
            return True
        
        # 搜索字段
        search_fields = [
            attraction.get('name', ''),
            attraction.get('description', ''),
            attraction.get('type', ''),
            attraction.get('category', ''),
            ' '.join(attraction.get('tags', [])),
            ' '.join(attraction.get('highlights', []))
        ]
        
        search_text = ' '.join(search_fields).lower()
        
        # 检查是否有任何关键词匹配
        for keyword in keywords:
            if keyword.lower() in search_text:
                return True
        
        return False
    
    def _calculate_data_quality(self, attraction: Dict[str, Any]) -> float:
        """计算数据质量分数"""
        score = 0.0
        total_fields = 0
        
        # 检查必需字段
        required_fields = ['name', 'type', 'rating', 'description', 'location']
        for field in required_fields:
            total_fields += 1
            if field in attraction and attraction[field]:
                score += 1.0
        
        # 检查可选字段
        optional_fields = ['opening_hours', 'price', 'highlights', 'tags', 'facilities']
        for field in optional_fields:
            total_fields += 1
            if field in attraction and attraction[field]:
                score += 0.5
        
        return min(score / total_fields, 1.0)
    
    def _random_offset(self) -> float:
        """生成随机坐标偏移"""
        import random
        return random.uniform(-0.01, 0.01)

# 创建全局实例
attraction_scraper = AttractionScraper()