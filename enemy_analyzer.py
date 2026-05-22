"""
Enemy Analyzer - Analyze enemy bases and decide attack strategy
"""

import logging
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum
import json

logger = logging.getLogger(__name__)


class BaseType(Enum):
    """Types of enemy bases"""
    NORMAL = "normal"
    WAR = "war"
    LEAGUE = "league"
    UNKNOWN = "unknown"


class DefenseLevel(Enum):
    """Defense strength estimation"""
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


@dataclass
class BuildingInfo:
    """Information about a single building"""
    name: str
    level: int
    is_upgrading: bool = False
    building_type: str = "defense"  # defense, resource, trap, etc.


@dataclass
class BaseAnalysis:
    """Complete analysis of an enemy base"""
    name: str
    town_hall_level: int
    base_type: BaseType
    defense_level: DefenseLevel
    
    # Resources
    gold_available: int
    elixir_available: int
    dark_elixir_available: int
    
    # Defense Info
    air_defenses: int
    ground_defenses: int
    air_traps: int
    ground_traps: int
    
    # Heroes
    barbarian_king_level: int
    archer_queen_level: int
    giant_golem_level: int
    electro_dragon_level: int
    
    # Recommendations
    recommended_strategy: str
    predicted_star_count: int  # 0-3 stars
    difficulty_score: float  # 0-100
    
    buildings: List[BuildingInfo] = None
    
    def to_dict(self):
        return {
            "name": self.name,
            "town_hall_level": self.town_hall_level,
            "base_type": self.base_type.value,
            "defense_level": self.defense_level.value,
            "gold": self.gold_available,
            "elixir": self.elixir_available,
            "dark_elixir": self.dark_elixir_available,
            "air_defenses": self.air_defenses,
            "ground_defenses": self.ground_defenses,
            "strategy": self.recommended_strategy,
            "predicted_stars": self.predicted_star_count,
            "difficulty": self.difficulty_score
        }


class EnemyAnalyzer:
    """Analyze enemy bases and make attack recommendations"""
    
    def __init__(self):
        self.analysis_history = []
        
    def analyze_base(self, screenshot_data: dict) -> BaseAnalysis:
        """
        Analyze enemy base from screenshot data
        
        Args:
            screenshot_data: Dictionary with extracted game data
            
        Returns:
            BaseAnalysis object with detailed analysis
        """
        try:
            logger.info("Starting base analysis...")
            
            # Extract basic info
            name = screenshot_data.get("enemy_name", "Unknown")
            town_hall_level = screenshot_data.get("town_hall_level", 1)
            
            # Estimate defense level
            defense_level = self._estimate_defense_level(screenshot_data)
            
            # Extract resources
            gold = screenshot_data.get("gold_available", 0)
            elixir = screenshot_data.get("elixir_available", 0)
            dark_elixir = screenshot_data.get("dark_elixir_available", 0)
            
            # Count defenses
            air_defenses = screenshot_data.get("air_defenses", 0)
            ground_defenses = screenshot_data.get("ground_defenses", 0)
            air_traps = screenshot_data.get("air_traps", 0)
            ground_traps = screenshot_data.get("ground_traps", 0)
            
            # Hero levels
            bk_level = screenshot_data.get("barbarian_king_level", 0)\n            aq_level = screenshot_data.get("archer_queen_level", 0)\n            golem_level = screenshot_data.get("giant_golem_level", 0)\n            edrag_level = screenshot_data.get("electro_dragon_level", 0)\n            \n            # Recommend strategy\n            strategy = self._recommend_strategy(\n                town_hall_level, defense_level, gold, elixir\n            )\n            \n            # Predict stars\n            predicted_stars = self._predict_stars(\n                town_hall_level, defense_level, gold, elixir\n            )\n            \n            # Calculate difficulty\n            difficulty = self._calculate_difficulty(\n                town_hall_level, defense_level, gold, elixir, \n                air_defenses, ground_defenses\n            )\n            \n            analysis = BaseAnalysis(\n                name=name,\n                town_hall_level=town_hall_level,\n                base_type=BaseType.NORMAL,\n                defense_level=defense_level,\n                gold_available=gold,\n                elixir_available=elixir,\n                dark_elixir_available=dark_elixir,\n                air_defenses=air_defenses,\n                ground_defenses=ground_defenses,\n                air_traps=air_traps,\n                ground_traps=ground_traps,\n                barbarian_king_level=bk_level,\n                archer_queen_level=aq_level,\n                giant_golem_level=golem_level,\n                electro_dragon_level=edrag_level,\n                recommended_strategy=strategy,\n                predicted_star_count=predicted_stars,\n                difficulty_score=difficulty\n            )\n            \n            self.analysis_history.append(analysis)\n            logger.info(f\"Base analysis complete: {analysis.name} (TH{town_hall_level})\")\n            \n            return analysis\n            \n        except Exception as e:\n            logger.error(f\"Base analysis error: {e}\")\n            return None\n    
    def _estimate_defense_level(self, data: dict) -> DefenseLevel:\n        \"\"\"\n        Estimate overall defense level\n        \"\"\"\n        try:\n            air_defenses = data.get(\"air_defenses\", 0)\n            ground_defenses = data.get(\"ground_defenses\", 0)\n            total_defenses = air_defenses + ground_defenses\n            \n            if total_defenses < 10:\n                return DefenseLevel.WEAK\n            elif total_defenses < 20:\n                return DefenseLevel.MODERATE\n            elif total_defenses < 30:\n                return DefenseLevel.STRONG\n            else:\n                return DefenseLevel.VERY_STRONG\n                \n        except Exception as e:\n            logger.error(f\"Defense estimation error: {e}\")\n            return DefenseLevel.MODERATE\n    
    def _recommend_strategy(self, town_hall: int, defense: DefenseLevel, gold: int, elixir: int) -> str:\n        \"\"\"\n        Recommend attack strategy based on base characteristics\n        \"\"\"\n        try:\n            if defense == DefenseLevel.WEAK:\n                if gold > 200000 or elixir > 200000:\n                    return \"BARCHING\"  # Barbarians + Archers\n                else:\n                    return \"GOBLINS\"   # Goblins for minimal loot\n            \n            elif defense == DefenseLevel.MODERATE:\n                if town_hall <= 7:\n                    return \"DRAGS\"     # Dragons\n                else:\n                    return \"HOG_RIDERS\" # Hog riders\n            \n            elif defense == DefenseLevel.STRONG:\n                if town_hall <= 9:\n                    return \"LAVA_LOON\"\n                else:\n                    return \"ELECTRO_DRAG\"\n            \n            else:  # VERY_STRONG\n                return \"SKIP\"  # Too strong, skip\n                \n        except Exception as e:\n            logger.error(f\"Strategy recommendation error: {e}\")\n            return \"SKIP\"\n    \n    def _predict_stars(self, town_hall: int, defense: DefenseLevel, gold: int, elixir: int) -> int:\n        \"\"\"\n        Predict number of stars likely to achieve\n        \"\"\"\n        try:\n            if defense == DefenseLevel.VERY_STRONG:\n                return 0\n            elif defense == DefenseLevel.STRONG:\n                return 1\n            elif defense == DefenseLevel.MODERATE:\n                return 2\n            else:\n                return 3\n                \n        except Exception as e:\n            logger.error(f\"Stars prediction error: {e}\")\n            return 0\n    \n    def _calculate_difficulty(self, town_hall: int, defense: DefenseLevel, \n                             gold: int, elixir: int, air_def: int, ground_def: int) -> float:\n        \"\"\"\n        Calculate base difficulty score (0-100)\n        \"\"\"\n        try:\n            base_score = town_hall * 5  # TH level contributes 5 points each\n            \n            # Add defense contributions\n            defense_score = {\n                DefenseLevel.WEAK: 10,\n                DefenseLevel.MODERATE: 30,\n                DefenseLevel.STRONG: 60,\n                DefenseLevel.VERY_STRONG: 90\n            }\n            base_score += defense_score[defense]\n            \n            # Add troop count factor\n            total_troops = air_def + ground_def\n            base_score += min(total_troops * 0.5, 20)\n            \n            # Clamp to 0-100\n            return min(max(base_score, 0), 100)\n            \n        except Exception as e:\n            logger.error(f\"Difficulty calculation error: {e}\")\n            return 50\n    \n    def should_attack(self, analysis: BaseAnalysis, min_gold: int = 50000, \n                     min_elixir: int = 50000, max_difficulty: float = 80) -> bool:\n        \"\"\"\n        Decide whether to attack this base\n        \n        Args:\n            analysis: BaseAnalysis object\n            min_gold: Minimum gold required\n            min_elixir: Minimum elixir required\n            max_difficulty: Maximum difficulty to attack\n            \n        Returns:\n            True if should attack, False otherwise\n        \"\"\"\n        try:\n            reasons = []\n            \n            # Check resources\n            if analysis.gold_available < min_gold:\n                reasons.append(f\"Insufficient gold ({analysis.gold_available} < {min_gold})\")\n            \n            if analysis.elixir_available < min_elixir:\n                reasons.append(f\"Insufficient elixir ({analysis.elixir_available} < {min_elixir})\")\n            \n            # Check difficulty\n            if analysis.difficulty_score > max_difficulty:\n                reasons.append(f\"Too difficult ({analysis.difficulty_score} > {max_difficulty})\")\n            \n            # Check strategy\n            if analysis.recommended_strategy == \"SKIP\":\n                reasons.append(\"Strategy recommends skipping\")\n            \n            should_attack = len(reasons) == 0\n            \n            if should_attack:\n                logger.info(f\"✓ Should attack {analysis.name}\")\n            else:\n                logger.info(f\"✗ Skip {analysis.name}: {', '.join(reasons)}\")\n            \n            return should_attack\n            \n        except Exception as e:\n            logger.error(f\"Attack decision error: {e}\")\n            return False\n    \n    def get_analysis_history(self) -> List[dict]:\n        \"\"\"\n        Get analysis history as dictionaries\n        \"\"\"\n        return [analysis.to_dict() for analysis in self.analysis_history]\n