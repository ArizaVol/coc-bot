"""
Profile Manager - Save and load bot configurations/strategies
"""

import logging
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class BotProfile:
    """Represents a complete bot configuration profile"""
    
    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        
        # Strategy settings
        self.attack_strategy = "BARCHING"
        self.farm_strategy = "GOBLINS"
        
        # Resource filters
        self.min_gold = 50000
        self.min_elixir = 50000
        self.min_dark_elixir = 0
        self.target_gold = 200000
        self.target_elixir = 200000
        self.target_dark_elixir = 0
        
        # Difficulty settings
        self.max_difficulty = 80
        self.skip_multiplayer = False
        self.skip_league = False
        
        # Timing
        self.attack_delay = 5  # seconds
        self.screenshot_interval = 2  # seconds
        
        # Advanced
        self.enable_spell_usage = True
        self.enable_hero_usage = True
        self.use_clan_castle = True
        self.max_attacks_per_session = 100
        
        # Farming mode
        self.farming_enabled = True
        self.farming_hours = "18-23"  # 18:00 to 23:00
        
        # Statistics
        self.total_attacks = 0
        self.total_gold_looted = 0
        self.total_elixir_looted = 0
        self.success_rate = 0.0
    
    def to_dict(self) -> dict:
        """Convert profile to dictionary"""
        return {
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "strategy": {
                "attack": self.attack_strategy,
                "farm": self.farm_strategy
            },
            "resources": {
                "min_gold": self.min_gold,
                "min_elixir": self.min_elixir,
                "min_dark_elixir": self.min_dark_elixir,
                "target_gold": self.target_gold,
                "target_elixir": self.target_elixir,
                "target_dark_elixir": self.target_dark_elixir
            },
            "difficulty": {
                "max_difficulty": self.max_difficulty,
                "skip_multiplayer": self.skip_multiplayer,
                "skip_league": self.skip_league
            },
            "timing": {
                "attack_delay": self.attack_delay,
                "screenshot_interval": self.screenshot_interval
            },
            "advanced": {
                "enable_spell_usage": self.enable_spell_usage,
                "enable_hero_usage": self.enable_hero_usage,
                "use_clan_castle": self.use_clan_castle,
                "max_attacks_per_session": self.max_attacks_per_session
            },
            "farming": {
                "enabled": self.farming_enabled,
                "hours": self.farming_hours
            },
            "statistics": {
                "total_attacks": self.total_attacks,
                "total_gold_looted": self.total_gold_looted,
                "total_elixir_looted": self.total_elixir_looted,
                "success_rate": self.success_rate
            }
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'BotProfile':
        """Create profile from dictionary"""
        profile = BotProfile(data.get("name", "Unknown"))
        profile.created_at = data.get("created_at", profile.created_at)
        profile.updated_at = data.get("updated_at", profile.updated_at)
        
        # Strategy
        strategy = data.get("strategy", {})
        profile.attack_strategy = strategy.get("attack", "BARCHING")
        profile.farm_strategy = strategy.get("farm", "GOBLINS")
        
        # Resources
        resources = data.get("resources", {})
        profile.min_gold = resources.get("min_gold", 50000)
        profile.min_elixir = resources.get("min_elixir", 50000)
        profile.target_gold = resources.get("target_gold", 200000)
        profile.target_elixir = resources.get("target_elixir", 200000)
        
        # Difficulty
        difficulty = data.get("difficulty", {})
        profile.max_difficulty = difficulty.get("max_difficulty", 80)
        profile.skip_multiplayer = difficulty.get("skip_multiplayer", False)
        profile.skip_league = difficulty.get("skip_league", False)
        
        # Timing
        timing = data.get("timing", {})
        profile.attack_delay = timing.get("attack_delay", 5)
        profile.screenshot_interval = timing.get("screenshot_interval", 2)
        
        # Advanced
        advanced = data.get("advanced", {})
        profile.enable_spell_usage = advanced.get("enable_spell_usage", True)
        profile.enable_hero_usage = advanced.get("enable_hero_usage", True)
        profile.use_clan_castle = advanced.get("use_clan_castle", True)
        profile.max_attacks_per_session = advanced.get("max_attacks_per_session", 100)
        
        # Farming
        farming = data.get("farming", {})
        profile.farming_enabled = farming.get("enabled", True)
        profile.farming_hours = farming.get("hours", "18-23")
        
        # Statistics
        stats = data.get("statistics", {})
        profile.total_attacks = stats.get("total_attacks", 0)
        profile.total_gold_looted = stats.get("total_gold_looted", 0)
        profile.total_elixir_looted = stats.get("total_elixir_looted", 0)
        profile.success_rate = stats.get("success_rate", 0.0)
        
        return profile


class ProfileManager:
    """Manage bot profiles"""
    
    def __init__(self, profiles_dir: str = "profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
        self.profiles: Dict[str, BotProfile] = {}
        self.current_profile: Optional[BotProfile] = None
        self.load_all_profiles()
    
    def create_profile(self, name: str) -> BotProfile:
        """Create new profile"""
        try:
            if name in self.profiles:
                logger.warning(f"Profile already exists: {name}")
                return self.profiles[name]
            
            profile = BotProfile(name)
            self.profiles[name] = profile
            self.save_profile(profile)
            logger.info(f"Profile created: {name}")
            return profile
            
        except Exception as e:
            logger.error(f"Profile creation error: {e}")
            return None
    
    def load_profile(self, name: str) -> Optional[BotProfile]:
        """Load profile from file"""
        try:
            profile_path = self.profiles_dir / f"{name}.json"
            
            if not profile_path.exists():
                logger.warning(f"Profile file not found: {profile_path}")
                return None
            
            with open(profile_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            profile = BotProfile.from_dict(data)
            self.profiles[name] = profile
            logger.info(f"Profile loaded: {name}")
            return profile
            
        except Exception as e:
            logger.error(f"Profile load error: {e}")
            return None
    
    def save_profile(self, profile: BotProfile):
        """Save profile to file"""
        try:
            profile.updated_at = datetime.now().isoformat()
            profile_path = self.profiles_dir / f"{profile.name}.json"
            
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile.to_dict(), f, indent=2)
            
            logger.info(f"Profile saved: {profile.name}")
            
        except Exception as e:
            logger.error(f"Profile save error: {e}")
    
    def delete_profile(self, name: str) -> bool:
        """Delete profile"""
        try:
            profile_path = self.profiles_dir / f"{name}.json"
            
            if profile_path.exists():
                profile_path.unlink()
                if name in self.profiles:
                    del self.profiles[name]
                logger.info(f"Profile deleted: {name}")
                return True
            
            logger.warning(f"Profile file not found: {profile_path}")
            return False
            
        except Exception as e:
            logger.error(f"Profile deletion error: {e}")
            return False
    
    def set_current_profile(self, name: str) -> bool:
        """Set current active profile"""
        try:
            if name not in self.profiles:
                logger.warning(f"Profile not found: {name}")
                return False
            
            self.current_profile = self.profiles[name]
            logger.info(f"Current profile set to: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Profile selection error: {e}")
            return False
    
    def get_current_profile(self) -> Optional[BotProfile]:
        """Get currently active profile"""
        return self.current_profile
    
    def list_profiles(self) -> List[str]:
        """List all profile names"""
        return list(self.profiles.keys())
    
    def load_all_profiles(self):
        """Load all profiles from disk"""
        try:
            for profile_file in self.profiles_dir.glob("*.json"):
                profile_name = profile_file.stem
                self.load_profile(profile_name)
            
            logger.info(f"Loaded {len(self.profiles)} profiles")
            
        except Exception as e:
            logger.error(f"Load all profiles error: {e}")
    
    def export_profile(self, name: str, export_path: str) -> bool:
        """Export profile to external file"""
        try:
            if name not in self.profiles:
                return False
            
            profile = self.profiles[name]
            export_file = Path(export_path)
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(profile.to_dict(), f, indent=2)
            
            logger.info(f"Profile exported: {export_file}")
            return True
            
        except Exception as e:
            logger.error(f"Profile export error: {e}")
            return False
    
    def import_profile(self, import_path: str, name: str = None) -> Optional[BotProfile]:
        """Import profile from external file"""
        try:
            import_file = Path(import_path)
            
            if not import_file.exists():
                logger.error(f"Import file not found: {import_file}")
                return None
            
            with open(import_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            profile_name = name or data.get("name", "Imported")
            profile = BotProfile.from_dict(data)
            profile.name = profile_name
            
            self.profiles[profile_name] = profile
            self.save_profile(profile)
            
            logger.info(f"Profile imported: {profile_name}")
            return profile
            
        except Exception as e:
            logger.error(f"Profile import error: {e}")
            return None
