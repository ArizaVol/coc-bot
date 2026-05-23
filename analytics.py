"""
Analytics Engine - Analyze bot performance and trends
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import statistics as stats

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """Analyze bot performance and statistics"""
    
    def __init__(self):
        self.data_points = []
    
    def analyze_strategy_performance(self, stats_manager) -> Dict:
        """Analyze performance of each strategy"""
        try:
            all_stats = stats_manager.all_time_stats
            
            if not all_stats:
                return {}
            
            strategies = {}
            
            for attack in all_stats:
                if attack.strategy not in strategies:
                    strategies[attack.strategy] = {
                        "total_attacks": 0,
                        "successful_attacks": 0,
                        "total_gold": 0,
                        "total_elixir": 0,
                        "destructions": [],
                        "stars": []
                    }
                
                strategy_data = strategies[attack.strategy]
                strategy_data["total_attacks"] += 1
                if attack.success:
                    strategy_data["successful_attacks"] += 1
                strategy_data["total_gold"] += attack.gold_looted
                strategy_data["total_elixir"] += attack.elixir_looted
                strategy_data["destructions"].append(attack.destruction_percentage)\n                strategy_data["stars"].append(attack.stars_achieved)
            
            # Calculate metrics for each strategy
            results = {}
            for strategy_name, data in strategies.items():
                total = data["total_attacks"]
                success_rate = (data["successful_attacks"] / total * 100) if total > 0 else 0
                avg_gold_per_attack = data["total_gold"] / total if total > 0 else 0
                avg_elixir_per_attack = data["total_elixir"] / total if total > 0 else 0
                
                avg_destruction = stats.mean(data["destructions"]) if data["destructions"] else 0
                avg_stars = stats.mean(data["stars"]) if data["stars"] else 0
                
                results[strategy_name] = {
                    "total_uses": total,
                    "success_rate": round(success_rate, 2),
                    "average_gold": round(avg_gold_per_attack, 2),
                    "average_elixir": round(avg_elixir_per_attack, 2),
                    "average_destruction": round(avg_destruction, 2),
                    "average_stars": round(avg_stars, 2),
                    "efficiency_score": self._calculate_efficiency_score(
                        success_rate, avg_gold_per_attack, avg_destruction
                    )
                }
            
            return results
        
        except Exception as e:
            logger.error(f"Strategy analysis error: {e}")
            return {}
    
    def analyze_time_trends(self, stats_manager) -> Dict:
        """Analyze trends over time"""
        try:
            all_stats = stats_manager.all_time_stats
            
            if not all_stats:
                return {}
            
            # Group by day
            daily_data = {}
            
            for attack in all_stats:
                attack_date = datetime.fromisoformat(attack.timestamp).date()
                date_str = str(attack_date)
                
                if date_str not in daily_data:
                    daily_data[date_str] = {
                        "attacks": 0,
                        "gold": 0,
                        "elixir": 0,
                        "successful": 0
                    }
                
                daily_data[date_str]["attacks"] += 1
                daily_data[date_str]["gold"] += attack.gold_looted
                daily_data[date_str]["elixir"] += attack.elixir_looted
                if attack.success:
                    daily_data[date_str]["successful"] += 1
            
            # Calculate trends
            dates = sorted(daily_data.keys())\n            if len(dates) < 2:
                return {"trend": "insufficient_data"}
            
            # Calculate day-over-day growth
            growth_rate = []\n            for i in range(1, len(dates)):
                prev_gold = daily_data[dates[i-1]]["gold"]
                curr_gold = daily_data[dates[i]]["gold"]
                \n                if prev_gold > 0:
                    growth = ((curr_gold - prev_gold) / prev_gold) * 100
                    growth_rate.append(growth)
            
            avg_growth = stats.mean(growth_rate) if growth_rate else 0
            
            return {
                "days_tracked": len(dates),
                "average_daily_gold": round(stats.mean([d["gold"] for d in daily_data.values()]), 2),
                "average_daily_attacks": round(stats.mean([d["attacks"] for d in daily_data.values()]), 2),
                "growth_trend": round(avg_growth, 2),
                "best_day": max(daily_data.items(), key=lambda x: x[1]["gold"])[0],
                "daily_breakdown": daily_data
            }
        
        except Exception as e:
            logger.error(f"Time trend analysis error: {e}")
            return {}
    
    def analyze_attack_patterns(self, stats_manager) -> Dict:
        """Analyze attack patterns"""
        try:
            all_stats = stats_manager.all_time_stats
            
            if not all_stats:
                return {}
            
            # Group by hour
            hourly_data = {}
            
            for attack in all_stats:
                attack_time = datetime.fromisoformat(attack.timestamp)
                hour = attack_time.hour
                
                if hour not in hourly_data:
                    hourly_data[hour] = {
                        "attacks": 0,
                        "gold": 0,
                        "success": 0
                    }
                
                hourly_data[hour]["attacks"] += 1
                hourly_data[hour]["gold"] += attack.gold_looted
                if attack.success:
                    hourly_data[hour]["success"] += 1
            
            # Find peak hour
            peak_hour = max(hourly_data.items(), key=lambda x: x[1]["attacks"])[0]
            
            return {
                "hourly_distribution": hourly_data,
                "peak_hour": peak_hour,
                "most_active_time": f"{peak_hour:02d}:00",
                "attacks_by_hour": [hourly_data.get(h, {"attacks": 0})["attacks"] for h in range(24)]
            }
        
        except Exception as e:
            logger.error(f"Attack pattern analysis error: {e}")
            return {}
    
    def get_performance_score(self, stats_manager) -> float:
        """Calculate overall performance score (0-100)"""
        try:
            all_time_stats = stats_manager.get_all_time_summary()
            \n            if not all_time_stats or all_time_stats.get("total_attacks", 0) == 0:
                return 0
            
            # Factor in multiple metrics\n            success_rate = all_time_stats.get("success_rate", 0) / 100
            avg_stars = all_time_stats.get("average_stars", 0) / 3  # 3 stars max
            avg_destruction = all_time_stats.get("average_destruction", 0) / 100
            
            # Weighted score\n            score = (success_rate * 0.3 + avg_stars * 0.4 + avg_destruction * 0.3) * 100
            
            return round(score, 2)
        
        except Exception as e:
            logger.error(f"Performance score calculation error: {e}")
            return 0
    
    def get_recommendations(self, stats_manager) -> List[str]:
        """Get recommendations based on performance"""
        try:
            recommendations = []
            all_stats = stats_manager.get_all_time_summary()
            strategy_stats = self.analyze_strategy_performance(stats_manager)
            
            if not all_stats:
                return ["Start attacking to gather data"]
            
            # Low success rate\n            if all_stats.get("success_rate", 0) < 50:
                recommendations.append("⚠️ Low success rate. Consider changing strategies or increasing difficulty threshold")
            
            # Low average stars\n            if all_stats.get("average_stars", 0) < 2:
                recommendations.append("📉 Low average stars. Try more aggressive strategies")
            
            # Find best strategy\n            if strategy_stats:
                best_strategy = max(strategy_stats.items(), key=lambda x: x[1].get("efficiency_score", 0))
                if best_strategy[1].get("efficiency_score", 0) > 0:
                    recommendations.append(f"✅ Best performing strategy: {best_strategy[0]}")
            
            # Total attacks milestone\n            attacks = all_stats.get("total_attacks", 0)
            if attacks < 10:
                recommendations.append("📊 Run more attacks to gather better analytics")
            
            return recommendations
        
        except Exception as e:
            logger.error(f"Recommendations error: {e}")
            return []
    
    def _calculate_efficiency_score(self, success_rate: float, gold_per_attack: float, destruction: float) -> float:
        """Calculate efficiency score for strategy"""
        try:
            # Normalize values
n            success_norm = success_rate / 100
            gold_norm = min(gold_per_attack / 100000, 1.0)  # Normalize to 100k gold
            destruction_norm = destruction / 100
            
            # Weighted calculation
            score = (success_norm * 0.4 + gold_norm * 0.3 + destruction_norm * 0.3) * 100
            
            return round(score, 2)
        except:
            return 0
