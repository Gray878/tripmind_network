#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础抓取器类 - 提供通用的抓取功能和接口
"""

import time
import random
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """抓取器基类"""
    
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.session = requests.Session()
        
        # 设置通用请求头
        self.session.headers.update({
            'User-Agent': self._get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # 抓取配置
        self.config = {
            'timeout': 30,
            'max_retries': 3,
            'retry_delay': 2,
            'min_delay': 1.0,
            'max_delay': 3.0
        }
    
    @abstractmethod
    def scrape(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        抓取数据的抽象方法，子类必须实现
        
        Args:
            query: 查询参数
            
        Returns:
            抓取结果列表
        """
        pass
    
    def fetch_page(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        """
        获取网页内容
        
        Args:
            url: 目标URL
            params: 查询参数
            
        Returns:
            BeautifulSoup 对象或 None
        """
        for attempt in range(self.config['max_retries']):
            try:
                # 添加延时
                self._add_delay()
                
                response = self.session.get(
                    url, 
                    params=params,
                    timeout=self.config['timeout']
                )
                response.raise_for_status()
                
                # 检测编码
                response.encoding = response.apparent_encoding
                
                soup = BeautifulSoup(response.text, 'html.parser')
                logger.info(f"成功获取页面: {url}")
                return soup
                
            except requests.RequestException as e:
                logger.warning(f"获取页面失败 (尝试 {attempt + 1}/{self.config['max_retries']}): {e}")
                if attempt < self.config['max_retries'] - 1:
                    time.sleep(self.config['retry_delay'] * (attempt + 1))
                else:
                    logger.error(f"最终获取页面失败: {url}")
                    return None
    
    def extract_text(self, element, selector: str, default: str = "") -> str:
        """
        从元素中提取文本
        
        Args:
            element: BeautifulSoup 元素
            selector: CSS 选择器
            default: 默认值
            
        Returns:
            提取的文本
        """
        try:
            found = element.select_one(selector)
            return found.get_text(strip=True) if found else default
        except Exception as e:
            logger.warning(f"提取文本失败 ({selector}): {e}")
            return default
    
    def extract_attribute(self, element, selector: str, attr: str, default: str = "") -> str:
        """
        从元素中提取属性值
        
        Args:
            element: BeautifulSoup 元素
            selector: CSS 选择器
            attr: 属性名
            default: 默认值
            
        Returns:
            属性值
        """
        try:
            found = element.select_one(selector)
            return found.get(attr, default) if found else default
        except Exception as e:
            logger.warning(f"提取属性失败 ({selector}.{attr}): {e}")
            return default
    
    def clean_text(self, text: str) -> str:
        """
        清理文本内容
        
        Args:
            text: 原始文本
            
        Returns:
            清理后的文本
        """
        if not text:
            return ""
        
        # 移除多余空白字符
        text = ' '.join(text.split())
        
        # 移除特殊字符
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        
        return text.strip()
    
    def parse_price(self, price_text: str) -> Dict[str, Any]:
        """
        解析价格文本
        
        Args:
            price_text: 价格文本
            
        Returns:
            价格信息字典
        """
        import re
        
        if not price_text:
            return {'amount': 0, 'currency': 'CNY', 'text': '价格未知'}
        
        # 清理价格文本
        price_text = self.clean_text(price_text)
        
        # 检查是否免费
        if any(word in price_text.lower() for word in ['免费', 'free', '不收费']):
            return {'amount': 0, 'currency': 'CNY', 'text': '免费'}
        
        # 提取数字和货币符号
        price_pattern = r'[¥$€£]?(\d+(?:\.\d+)?)'
        matches = re.findall(price_pattern, price_text)
        
        if matches:
            amount = float(matches[0])
            currency = 'CNY'  # 默认人民币
            
            if '$' in price_text:
                currency = 'USD'
            elif '€' in price_text:
                currency = 'EUR'
            elif '£' in price_text:
                currency = 'GBP'
            
            return {'amount': amount, 'currency': currency, 'text': price_text}
        
        return {'amount': 0, 'currency': 'CNY', 'text': price_text}
    
    def parse_rating(self, rating_text: str) -> float:
        """
        解析评分文本
        
        Args:
            rating_text: 评分文本
            
        Returns:
            评分数值
        """
        import re
        
        if not rating_text:
            return 0.0
        
        # 提取数字
        rating_pattern = r'(\d+(?:\.\d+)?)'
        matches = re.findall(rating_pattern, rating_text)
        
        if matches:
            return float(matches[0])
        
        return 0.0
    
    def _get_random_user_agent(self) -> str:
        """获取随机 User-Agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        return random.choice(user_agents)
    
    def _add_delay(self):
        """添加随机延时"""
        delay = random.uniform(self.config['min_delay'], self.config['max_delay'])
        time.sleep(delay)
    
    def validate_query(self, query: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        验证查询参数
        
        Args:
            query: 查询参数
            required_fields: 必需字段列表
            
        Returns:
            验证结果
        """
        for field in required_fields:
            if field not in query or not query[field]:
                logger.error(f"缺少必需参数: {field}")
                return False
        return True