"""
Strategy Module - Attack strategies and troop deployments
"""

import logging
from enum import Enum
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class TroopType(Enum):
    """Available troop types"""
    BARBARIAN = "barbarian"
    ARCHER = "archer"
    GIANT = "giant"
    GOBLIN = "goblin"
    WALL_BREAKER = "wall_breaker"
    BALLOON = "balloon"
    WIZARD = "wizard"
    HEALER = "healer"
    DRAGON = "dragon"
    P_E_K_K_A = "pekka"
    HOG_RIDER = "hog_rider"
    VALKYRIE = "valkyrie"
    GOLEM = "golem"
    WITCH = "witch"
    LAVA_HOUND = "lava_hound"


class SpellType(Enum):
    """Available spell types"""
    LIGHTNING = "lightning"
    HEAL = "heal"
    RAGE = "rage"
    FREEZE = "freeze"
    CLONE = "clone"
    POISON = "poison"
    EARTHQUAKE = "earthquake"
    HASTE = "haste"


@dataclass
class TroopComposition:
    """Troop composition for an attack"""
    strategy_name: str
    troops: Dict[TroopType, int]
    spells: Dict[SpellType, int]
    heroes_to_use: List[str]  # e.g., ["barbarian_king", "archer_queen"]
    clan_castle_troops: str = "dragons"
    deployment_pattern: str = "balanced"  # "spread", "concentrated", "balanced"


class AttackStrategy:
    """Base class for attack strategies"""
    
    def __init__(self, name: str):
        self.name = name
        self.troop_composition = None
        self.deployment_points = []
    
    def get_composition(self) -> TroopComposition:
        """Get troop composition for this strategy"""
        return self.troop_composition
    
    def get_deployment_points(self, base_layout: Dict) -> List[Tuple[int, int]]:
        """Get deployment points for troops"""
        return self.deployment_points


class BarchingStrategy(AttackStrategy):
    """Barbarians + Archers strategy - Good for farming"""
    
    def __init__(self):
        super().__init__("BARCHING")
        self.troop_composition = TroopComposition(
            strategy_name="BARCHING",
            troops={
                TroopType.BARBARIAN: 30,
                TroopType.ARCHER: 30,
                TroopType.GIANT: 5,
                TroopType.WALL_BREAKER: 5
            },
            spells={
                SpellType.RAGE: 1,
                SpellType.HEAL: 1
            },
            heroes_to_use=["barbarian_king"],
            deployment_pattern="spread"
        )


class DragonStrategy(AttackStrategy):
    """Dragon heavy strategy - Good for lower town halls"""
    
    def __init__(self):
        super().__init__("DRAGS")
        self.troop_composition = TroopComposition(
            strategy_name="DRAGS",
            troops={
                TroopType.DRAGON: 10,
                TroopType.BALLOON: 3,
                TroopType.WIZARD: 2
            },
            spells={
                SpellType.RAGE: 2,
                SpellType.LIGHTNING: 1
            },
            heroes_to_use=["barbarian_king", "archer_queen"],
            deployment_pattern="balanced"
        )


class HogRiderStrategy(AttackStrategy):
    """Hog riders + support strategy - Good for mid town halls"""
    
    def __init__(self):
        super().__init__("HOG_RIDERS")
        self.troop_composition = TroopComposition(
            strategy_name="HOG_RIDERS",
            troops={
                TroopType.HOG_RIDER: 20,
                TroopType.WIZARD: 8,
                TroopType.GIANT: 3,
                TroopType.WALL_BREAKER: 2
            },
            spells={
                SpellType.HEAL: 3,
                SpellType.RAGE: 1
            },
            heroes_to_use=["barbarian_king", "archer_queen"],
            deployment_pattern="concentrated"
        )


class LavaLoonStrategy(AttackStrategy):
    """Lava Hound + Balloon strategy - Good for air based defenses"""
    
    def __init__(self):
        super().__init__("LAVA_LOON")
        self.troop_composition = TroopComposition(
            strategy_name="LAVA_LOON",
            troops={
                TroopType.LAVA_HOUND: 2,
                TroopType.BALLOON: 15,
                TroopType.WIZARD: 5,
                TroopType.MINION: 10
            },
            spells={
                SpellType.RAGE: 2,
                SpellType.FREEZE: 1,
                SpellType.HEAL: 1
            },
            heroes_to_use=["archer_queen"],
            deployment_pattern="balanced"
        )


class ElectroDragonStrategy(AttackStrategy):
    """Electro Dragon strategy - Good for higher town halls"""
    
    def __init__(self):
        super().__init__("ELECTRO_DRAG")
        self.troop_composition = TroopComposition(
            strategy_name="ELECTRO_DRAG",
            troops={
                TroopType.DRAGON: 3,
                TroopType.BALLOON: 5,
                TroopType.WIZARD: 5
            },
            spells={
                SpellType.LIGHTNING: 1,
                SpellType.RAGE: 2,
                SpellType.FREEZE: 1
            },
            heroes_to_use=["barbarian_king", "archer_queen"],
            deployment_pattern="balanced"
        )


class GobblinStrategy(AttackStrategy):
    """Goblins strategy - Fast farming with minimal loot"""
    
    def __init__(self):
        super().__init__("GOBLINS")
        self.troop_composition = TroopComposition(
            strategy_name="GOBLINS",
            troops={
                TroopType.GOBLIN: 60,
                TroopType.GIANT: 2,
                TroopType.WALL_BREAKER: 3
            },
            spells={
                SpellType.RAGE: 1
            },
            heroes_to_use=[],
            deployment_pattern="spread"
        )


class StrategyManager:
    """Manage and select attack strategies"""
    
    def __init__(self):
        self.strategies = {
            "BARCHING": BarchingStrategy(),
            "DRAGS": DragonStrategy(),
            "HOG_RIDERS": HogRiderStrategy(),
            "LAVA_LOON": LavaLoonStrategy(),
            "ELECTRO_DRAG": ElectroDragonStrategy(),
            "GOBLINS": GobblinStrategy()
        }
        self.selected_strategy = None
    
    def select_strategy(self, strategy_name: str) -> Optional[AttackStrategy]:
        """
        Select attack strategy
        
        Args:
            strategy_name: Name of strategy to select
            
        Returns:
            Selected strategy or None
        """
        try:
            if strategy_name not in self.strategies:
                logger.warning(f"Strategy not found: {strategy_name}")
                return None
            
            self.selected_strategy = self.strategies[strategy_name]
            logger.info(f"Strategy selected: {strategy_name}")
            return self.selected_strategy
            
        except Exception as e:
            logger.error(f"Strategy selection error: {e}")
            return None
    
    def get_strategy(self, strategy_name: str) -> Optional[AttackStrategy]:
        """Get specific strategy"""
        return self.strategies.get(strategy_name)
    
    def list_strategies(self) -> List[str]:
        """List all available strategies"""
        return list(self.strategies.keys())
    
    def get_current_strategy(self) -> Optional[AttackStrategy]:
        """Get currently selected strategy"""
        return self.selected_strategy
    
    def get_strategy_info(self, strategy_name: str) -> dict:
        """Get detailed information about strategy"""
        try:
            strategy = self.strategies.get(strategy_name)
            if not strategy:
                return {}
            
            composition = strategy.get_composition()
            return {
                "name": composition.strategy_name,
                "troops": {troop.value: count for troop, count in composition.troops.items()},
                "spells": {spell.value: count for spell, count in composition.spells.items()},
                "heroes": composition.heroes_to_use,
                "deployment_pattern": composition.deployment_pattern
            }
            
        except Exception as e:
            logger.error(f"Strategy info error: {e}")
            return {}
