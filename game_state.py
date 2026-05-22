"""
Game State Module - Track game status and resources
"""

import logging
from dataclasses import dataclass
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)


class GameState(Enum):
    """Possible game states"""

    HOME = "home"
    ATTACKING = "attacking"
    SEARCHING = "searching"
    IN_BATTLE = "in_battle"
    LOOTING = "looting"
    UNKNOWN = "unknown"


@dataclass
class Resources:
    """Player resources"""

    gold: int = 0
    elixir: int = 0
    dark_elixir: int = 0

    def __str__(self):
        return f"Gold: {self.gold} | Elixir: {self.elixir} | Dark: {self.dark_elixir}"


@dataclass
class EnemyInfo:
    """Enemy base information"""

    name: str = "Unknown"
    gold: int = 0
    elixir: int = 0
    dark_elixir: int = 0
    level: int = 0
    trophy_change: int = 0

    def meets_criteria(self, min_gold: int, min_elixir: int) -> bool:
        """Check if enemy meets attack criteria"""
        return self.gold >= min_gold and self.elixir >= min_elixir

    def __str__(self):
        return f"{self.name} (Lvl {self.level}) - Gold: {self.gold} | Elixir: {self.elixir}"


class GameStateManager:
    """Manages and tracks game state"""

    def __init__(self):
        self.current_state = GameState.UNKNOWN
        self.player_resources = Resources()
        self.target_enemy: Optional[EnemyInfo] = None
        self.attack_count = 0
        self.total_gold_looted = 0
        self.total_elixir_looted = 0

    def update_state(self, new_state: GameState):
        """Update current game state"""
        if self.current_state != new_state:
            logger.info(f"State change: {self.current_state.value} → {new_state.value}")
            self.current_state = new_state

    def update_resources(self, gold: int, elixir: int, dark_elixir: int = 0):
        """Update player resources"""
        self.player_resources.gold = gold
        self.player_resources.elixir = elixir
        self.player_resources.dark_elixir = dark_elixir
        logger.debug(f"Resources updated: {self.player_resources}")

    def set_target(self, enemy: EnemyInfo):
        """Set current target enemy"""
        self.target_enemy = enemy
        logger.info(f"Target set: {enemy}")

    def record_attack(self, gold_looted: int, elixir_looted: int):
        """Record completed attack"""
        self.attack_count += 1
        self.total_gold_looted += gold_looted
        self.total_elixir_looted += elixir_looted
        logger.info(
            f"Attack #{self.attack_count} completed. "
            f"Looted: {gold_looted} gold, {elixir_looted} elixir"
        )

    def should_continue_attacking(
        self, target_gold: int, target_elixir: int
    ) -> bool:
        """Check if should continue attacking based on resource targets"""
        should_continue = (
            self.player_resources.gold < target_gold
            and self.player_resources.elixir < target_elixir
        )

        if not should_continue:
            logger.info(
                f"Stopping attacks - Resource targets reached. "
                f"Gold: {self.player_resources.gold}/{target_gold} | "
                f"Elixir: {self.player_resources.elixir}/{target_elixir}"
            )

        return should_continue

    def get_stats(self) -> dict:
        """Get current bot statistics"""
        return {
            "state": self.current_state.value,
            "attacks_completed": self.attack_count,
            "total_gold_looted": self.total_gold_looted,
            "total_elixir_looted": self.total_elixir_looted,
            "current_resources": {
                "gold": self.player_resources.gold,
                "elixir": self.player_resources.elixir,
                "dark_elixir": self.player_resources.dark_elixir,
            },
            "target": (
                str(self.target_enemy) if self.target_enemy else "None"
            ),
        }
