#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TripMind Information Analyzer Tool
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime
from collections import Counter, defaultdict
import re

try:
    from openagents import tool
except ImportError:
    def tool(func=None, **kwargs):
        if func is None:
            return lambda f: f
        return func

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InformationAnalyzer:
    def __init__(self):
        self.quality_weights = {
            'completeness': 0.3,
            'reliability': 0.25,
            'freshness': 0.2,
            'consistency': 0.15,
            'relevance': 0.1
        }
        self.recommendation_weights = {
            'rating': 0.3,
            'popularity': 0.2,
            'price_value': 0.2,
            'uniqueness': 0.15,
            'accessibility': 0.15
        }
    
    def analyze_information(self, raw_data: List[Dict[str, Any]], analysis_type: str = "comprehensive") -> Dict[str, Any]:
        try:
            logger.info(f"Analyzing {len(raw_data)} items")
            if not raw_data:
                return self._create_empty_result("No data to analyze")
            
            cleaned_data = self._clean_and_deduplicate(raw_data)
            
            analysis_result = {
                'summary': self._generate_summary(cleaned_data),
                'top_recommendations': self._generate_recommendations(cleaned_data),
                'insights': self._extract_insights(cleaned_data),
                'categories': self._categorize_data(cleaned_data)
            }
            
            quality_metrics = self._assess_quality(cleaned_data, raw_data)
            
            analysis_metadata = {
                'total_items_processed': len(raw_data),
                'valid_items': len(cleaned_data),
                'duplicates_removed': len(raw_data) - len(cleaned_data),
                'analyzed_at': datetime.now().isoformat()
            }
            
            return {
                'success': True,
                'processed_data': analysis_result,
                'quality_metrics': quality_metrics,
                'analysis_metadata': analysis_metadata
            }
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return self._create_error_result(f"Analysis failed: {str(e)}")
    
    def _clean_and_deduplicate(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned_data = []
        seen_items = set()
        for item in raw_data:
            if not self._is_valid_item(item):
                continue
            item_key = self._generate_item_key(item)
            if item_key in seen_items:
                continue
            cleaned_item = self._clean_item(item)
            cleaned_data.append(cleaned_item)
            seen_items.add(item_key)
        return cleaned_data
    
    def _is_valid_item(self, item: Dict[str, Any]) -> bool:
        return 'name' in item and item['name']
    
    def _generate_item_key(self, item: Dict[str, Any]) -> str:
        name = item.get('name', '').lower().strip()
        location = ''
        if 'location' in item and isinstance(item['location'], dict):
            location = item['location'].get('address', '').lower().strip()
        return f"{name}|{location}"
    
    def _clean_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = item.copy()
        if 'rating' in cleaned:
            cleaned['rating'] = self._normalize_rating(cleaned['rating'])
        if 'price' in cleaned:
            cleaned['price'] = self._normalize_price(cleaned['price'])
        return cleaned
    
    def _normalize_rating(self, rating: Any) -> float:
        if isinstance(rating, (int, float)):
            return max(0.0, min(5.0, float(rating)))
        elif isinstance(rating, str):
            match = re.search(r'(\d+(?:\.\d+)?)', rating)
            if match:
                return max(0.0, min(5.0, float(match.group(1))))
        return 0.0
    
    def _normalize_price(self, price: Any) -> Dict[str, Any]:
        if isinstance(price, dict):
            return price
        elif isinstance(price, str):
            if 'free' in price.lower():
                return {'amount': 0, 'currency': 'CNY', 'text': 'Free'}
            match = re.search(r'(\d+(?:\.\d+)?)', price)
            if match:
                amount = float(match.group(1))
                currency = 'CNY'
                if '$' in price:
                    currency = 'USD'
                return {'amount': amount, 'currency': currency, 'text': price}
        return {'amount': 0, 'currency': 'CNY', 'text': 'Unknown'}
    
    def _generate_summary(self, data: List[Dict[str, Any]]) -> str:
        if not data:
            return "No items found."
        total_count = len(data)
        types = [item.get('type', 'Unknown') for item in data]
        type_counts = Counter(types)
        free_count = sum(1 for item in data 
                        if isinstance(item.get('price'), dict) and item['price'].get('amount', 0) == 0)
        ratings = [item.get('rating', 0) for item in data if item.get('rating', 0) > 0]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        summary_parts = [f"Found {total_count} items."]
        if type_counts:
            top_types = type_counts.most_common(3)
            type_text = ", ".join([f"{t}({c})" for t, c in top_types])
            summary_parts.append(f"Types: {type_text}.")
        if free_count > 0:
            summary_parts.append(f"{free_count} free items.")
        if avg_rating > 0:
            summary_parts.append(f"Average rating: {avg_rating:.1f}.")
        return " ".join(summary_parts)
    
    def _generate_recommendations(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not data:
            return []
        scored_items = []
        for item in data:
            score = self._calculate_recommendation_score(item)
            recommendation = {
                'name': item.get('name', ''),
                'type': item.get('type', ''),
                'score': score,
                'reasons': self._generate_recommendation_reasons(item),
                'highlights': item.get('tags', [])[:3],
                'practical_info': item.get('opening_hours', '')
            }
            scored_items.append(recommendation)
        scored_items.sort(key=lambda x: x['score'], reverse=True)
        return scored_items[:10]
    
    def _calculate_recommendation_score(self, item: Dict[str, Any]) -> float:
        score = 0.0
        rating = item.get('rating', 0)
        if rating > 0:
            score += (rating / 5.0) * self.recommendation_weights['rating']
        price_info = item.get('price', {})
        if isinstance(price_info, dict):
            amount = price_info.get('amount', 0)
            if amount == 0:
                score += 1.0 * self.recommendation_weights['price_value']
            elif amount < 100:
                score += 0.8 * self.recommendation_weights['price_value']
        opening_hours = item.get('opening_hours', '')
        if opening_hours:
            score += 0.7 * self.recommendation_weights['accessibility']
        return min(1.0, score)
    
    def _generate_recommendation_reasons(self, item: Dict[str, Any]) -> List[str]:
        reasons = []
        rating = item.get('rating', 0)
        if rating >= 4.5:
            reasons.append("Highly rated")
        elif rating >= 4.0:
            reasons.append("Good rating")
        price_info = item.get('price', {})
        if isinstance(price_info, dict) and price_info.get('amount', 0) == 0:
            reasons.append("Free admission")
        tags = item.get('tags', [])
        if 'culture' in [t.lower() for t in tags]:
            reasons.append("Cultural value")
        return reasons[:3]
    
    def _extract_insights(self, data: List[Dict[str, Any]]) -> List[str]:
        insights = []
        if not data:
            return insights
        free_items = [item for item in data 
                     if isinstance(item.get('price'), dict) and item['price'].get('amount', 0) == 0]
        if len(free_items) >= len(data) * 0.3:
            insights.append(f"Found {len(free_items)} free attractions")
        high_rated = [item for item in data if item.get('rating', 0) >= 4.5]
        if len(high_rated) >= 3:
            insights.append(f"Found {len(high_rated)} highly rated spots (4.5+)")
        return insights[:5]
    
    def _categorize_data(self, data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        categories = defaultdict(list)
        for item in data:
            item_type = item.get('type', 'Other')
            categories[item_type].append(item)
        result = {}
        for category, items in categories.items():
            if len(items) >= 1:
                result[category] = items[:5]
        return result
    
    def _assess_quality(self, cleaned_data: List[Dict[str, Any]], raw_data: List[Dict[str, Any]]) -> Dict[str, float]:
        if not raw_data:
            return {'data_completeness': 0.0, 'source_reliability': 0.0, 'information_freshness': 0.0, 'overall_quality': 0.0}
        completeness = len(cleaned_data) / len(raw_data) if raw_data else 0.0
        reliability = 0.9
        freshness = 0.85
        overall = completeness * 0.3 + reliability * 0.25 + freshness * 0.2
        return {
            'data_completeness': round(completeness, 2),
            'source_reliability': round(reliability, 2),
            'information_freshness': round(freshness, 2),
            'overall_quality': round(overall, 2)
        }
    
    def _create_empty_result(self, message: str) -> Dict[str, Any]:
        return {
            'success': True,
            'processed_data': {'summary': message, 'top_recommendations': [], 'insights': [], 'categories': {}},
            'quality_metrics': {'data_completeness': 0.0, 'source_reliability': 0.0, 'information_freshness': 0.0, 'overall_quality': 0.0},
            'analysis_metadata': {'total_items_processed': 0, 'valid_items': 0, 'duplicates_removed': 0, 'analyzed_at': datetime.now().isoformat()}
        }
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        return {
            'success': False,
            'error': error_message,
            'processed_data': {'summary': 'Analysis failed', 'top_recommendations': [], 'insights': [], 'categories': {}},
            'quality_metrics': {'data_completeness': 0.0, 'source_reliability': 0.0, 'information_freshness': 0.0, 'overall_quality': 0.0},
            'analysis_metadata': {'total_items_processed': 0, 'valid_items': 0, 'duplicates_removed': 0, 'analyzed_at': datetime.now().isoformat()}
        }

analyzer = InformationAnalyzer()

@tool(name="analyze_information", description="Analyze scraped travel information")
def analyze_information(raw_data: List[Dict[str, Any]], analysis_type: str = "comprehensive") -> str:
    result = analyzer.analyze_information(raw_data, analysis_type)
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    test_data = [{'name': 'Test Museum', 'type': 'Museum', 'rating': 4.5, 'price': {'amount': 0, 'currency': 'CNY', 'text': 'Free'}, 'tags': ['culture', 'history']}]
    result = analyze_information(test_data)
    print(result)
