"""
Statistics and Reporting Module
"""

import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class AttackStats:
    """Statistics for a single attack"""
    timestamp: str
    enemy_name: str
    strategy: str
    gold_looted: int
    elixir_looted: int
    dark_elixir_looted: int
    stars_achieved: int
    destruction_percentage: float
    battle_duration: int  # seconds
    success: bool
    notes: str = ""


class StatisticsManager:
    """Manage and analyze bot statistics"""
    
    def __init__(self, stats_dir: str = "statistics"):
        self.stats_dir = Path(stats_dir)
        self.stats_dir.mkdir(exist_ok=True)
        self.current_session_stats = []
        self.all_time_stats = []
        self.load_stats()
    
    def record_attack(self, stats: AttackStats):
        """Record attack statistics"""
        try:
            self.current_session_stats.append(stats)
            self.all_time_stats.append(stats)
            self.save_stats()
            
            logger.info(f"Attack recorded: {stats.enemy_name} - "
                       f"Gold: {stats.gold_looted}, Elixir: {stats.elixir_looted}")
            
        except Exception as e:
            logger.error(f"Record attack error: {e}")
    
    def get_session_summary(self) -> dict:
        """Get current session summary"""
        try:
            if not self.current_session_stats:
                return {
                    "total_attacks": 0,
                    "total_gold": 0,
                    "total_elixir": 0,
                    "average_destruction": 0,
                    "average_stars": 0,
                    "success_rate": 0
                }
            
            total_attacks = len(self.current_session_stats)
            total_gold = sum(s.gold_looted for s in self.current_session_stats)
            total_elixir = sum(s.elixir_looted for s in self.current_session_stats)
            
            avg_destruction = sum(s.destruction_percentage for s in self.current_session_stats) / total_attacks
            avg_stars = sum(s.stars_achieved for s in self.current_session_stats) / total_attacks
            successful_attacks = sum(1 for s in self.current_session_stats if s.success)
            success_rate = (successful_attacks / total_attacks * 100) if total_attacks > 0 else 0
            
            return {
                "total_attacks": total_attacks,
                "total_gold": total_gold,
                "total_elixir": total_elixir,
                "average_destruction": round(avg_destruction, 2),
                "average_stars": round(avg_stars, 2),
                "success_rate": round(success_rate, 2),
                "session_duration": self._get_session_duration()
            }
            
        except Exception as e:
            logger.error(f"Session summary error: {e}")
            return {}
    
    def get_all_time_summary(self) -> dict:
        """Get all-time statistics"""
        try:
            if not self.all_time_stats:
                return {
                    "total_attacks": 0,
                    "total_gold": 0,
                    "total_elixir": 0,
                    "average_destruction": 0,
                    "average_stars": 0,
                    "success_rate": 0
                }
            
            total_attacks = len(self.all_time_stats)
            total_gold = sum(s.gold_looted for s in self.all_time_stats)
            total_elixir = sum(s.elixir_looted for s in self.all_time_stats)
            
            avg_destruction = sum(s.destruction_percentage for s in self.all_time_stats) / total_attacks
            avg_stars = sum(s.stars_achieved for s in self.all_time_stats) / total_attacks
            successful = sum(1 for s in self.all_time_stats if s.success)
            
            return {
                "total_attacks": total_attacks,
                "total_gold": total_gold,
                "total_elixir": total_elixir,
                "average_destruction": round(avg_destruction, 2),
                "average_stars": round(avg_stars, 2),
                "success_rate": round(successful / total_attacks * 100, 2)
            }
            
        except Exception as e:
            logger.error(f"All-time summary error: {e}")
            return {}
    
    def export_report(self, filename: str = None) -> bool:
        """Export statistics report"""
        try:
            if not filename:
                filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            report = {
                "generated_at": datetime.now().isoformat(),
                "session_summary": self.get_session_summary(),
                "all_time_summary": self.get_all_time_summary(),
                "recent_attacks": [asdict(s) for s in self.all_time_stats[-100:]]
            }
            
            report_path = self.stats_dir / filename
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Report exported: {report_path}")
            return True
            
        except Exception as e:
            logger.error(f"Report export error: {e}")
            return False
    
    def save_stats(self):
        """Save statistics to disk"""
        try:
            stats_file = self.stats_dir / "all_stats.json"
            stats_data = [asdict(s) for s in self.all_time_stats]
            
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Save stats error: {e}")
    
    def load_stats(self):
        """Load statistics from disk"""
        try:
            stats_file = self.stats_dir / "all_stats.json"
            
            if not stats_file.exists():
                return
            
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats_data = json.load(f)
            
            self.all_time_stats = [AttackStats(**stat) for stat in stats_data]
            logger.info(f"Loaded {len(self.all_time_stats)} attack records")
            
        except Exception as e:
            logger.error(f"Load stats error: {e}")
    
    def _get_session_duration(self) -> str:
        """Get current session duration"""
        try:
            if not self.current_session_stats:
                return "0h 0m"
            
            first_attack = datetime.fromisoformat(self.current_session_stats[0].timestamp)
            last_attack = datetime.fromisoformat(self.current_session_stats[-1].timestamp)
            duration = last_attack - first_attack
            
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            
            return f"{hours}h {minutes}m"
            
        except:
            return "Unknown"
    
    def clear_session(self):
        """Clear current session statistics"""
        self.current_session_stats = []
        logger.info("Session statistics cleared")
