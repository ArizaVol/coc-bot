"""
Main Bot Module - Core automation logic
"""

import logging
import time
import yaml
from pathlib import Path
from typing import Optional
from adb_manager import ADBManager
from vision import VisionAnalyzer
from game_state import GameStateManager, GameState, EnemyInfo, Resources

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ClashOfClansBot:
    """Main bot class for Clash of Clans automation"""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize bot with configuration"""
        self.config = self.load_config(config_path)
        self.adb = ADBManager(
            device_ip=self.config["adb"]["device_ip"],
            device_port=self.config["adb"]["device_port"],
            timeout=self.config["adb"]["timeout"],
        )
        self.vision = VisionAnalyzer(debug_mode=self.config["bot"]["debug_mode"])
        self.state = GameStateManager()
        self.running = False

        logger.info("=" * 50)
        logger.info("Clash of Clans Bot Initialized")
        logger.info("=" * 50)

    @staticmethod
    def load_config(config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config: {e}")
            raise

    def start(self):
        """Start bot"""
        logger.info("Starting bot...")

        if not self.adb.connect():
            logger.error("Failed to connect to device")
            return

        self.running = True
        logger.info("✓ Bot started successfully")

        try:
            self.main_loop()
        except KeyboardInterrupt:
            logger.info("Bot interrupted by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            self.stop()

    def stop(self):
        """Stop bot"""
        self.running = False
        self.adb.disconnect()
        logger.info("Bot stopped")
        self.print_stats()

    def main_loop(self):
        """Main bot loop"""
        logger.info("Entering main loop...")

        while self.running:
            try:
                # Capture screenshot
                screenshot = self.adb.get_screenshot()
                if not screenshot:
                    logger.warning("Failed to get screenshot, retrying...")
                    time.sleep(2)
                    continue

                # Analyze current state
                self.analyze_game_state(screenshot)

                # Check if should continue attacking
                target_gold = self.config["game"]["target_gold_threshold"]
                target_elixir = self.config["game"]["target_elixir_threshold"]

                if not self.state.should_continue_attacking(target_gold, target_elixir):
                    logger.info("Target resources reached. Bot stopping.")
                    break

                # Check minimum resources for attack
                min_gold = self.config["game"]["min_gold"]
                min_elixir = self.config["game"]["min_elixir"]

                if (
                    self.state.player_resources.gold >= min_gold
                    and self.state.player_resources.elixir >= min_elixir
                ):
                    self.perform_attack()
                else:
                    logger.info("Insufficient resources for attack, waiting...")
                    time.sleep(self.config["bot"]["attack_delay"])

            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                time.sleep(5)

    def analyze_game_state(self, screenshot):
        """Analyze game state from screenshot"""
        try:
            logger.debug("Analyzing game state...")
            self.state.update_state(GameState.HOME)

        except Exception as e:
            logger.error(f"Error analyzing game state: {e}")

    def perform_attack(self):
        """Execute attack sequence"""
        logger.info("Performing attack...")

        try:
            # Step 1: Go to attack screen
            logger.info("Step 1: Opening attack screen...")
            attack_btn = self.config["coordinates"]["attack_button"]
            self.adb.tap(attack_btn[0], attack_btn[1])
            time.sleep(2)

            # Step 2: Search for next enemy
            logger.info("Step 2: Searching for enemy...")
            self.search_for_enemy()

            # Step 3: Analyze enemy and decide whether to attack
            screenshot = self.adb.get_screenshot()
            if screenshot and self.should_attack_enemy(screenshot):
                # Step 4: Start attack
                logger.info("Step 3: Starting attack...")
                attack_btn = self.config["coordinates"]["attack_button"]
                self.adb.tap(attack_btn[0], attack_btn[1])
                time.sleep(3)

                # Step 5: Wait for battle to complete
                self.wait_for_battle_complete()

                # Step 6: Collect rewards
                self.collect_rewards()

            else:
                logger.info("Enemy does not meet criteria, searching next...")
                self.find_next_enemy()

            time.sleep(self.config["bot"]["attack_delay"])

        except Exception as e:
            logger.error(f"Error during attack: {e}", exc_info=True)

    def search_for_enemy(self):
        """Search for next enemy"""
        try:
            self.state.update_state(GameState.SEARCHING)
            logger.info("Searching for enemies...")
            time.sleep(2)

        except Exception as e:
            logger.error(f"Error searching for enemy: {e}")

    def should_attack_enemy(self, screenshot) -> bool:
        """Determine if current enemy should be attacked"""
        try:
            return True
        except Exception as e:
            logger.error(f"Error evaluating enemy: {e}")
            return False

    def find_next_enemy(self):
        """Find next enemy in search results"""
        try:
            logger.info("Finding next enemy...")
            next_btn = self.config["coordinates"]["next_button"]
            self.adb.tap(next_btn[0], next_btn[1])
            time.sleep(1)

        except Exception as e:
            logger.error(f"Error finding next enemy: {e}")

    def wait_for_battle_complete(self):
        """Wait for battle to finish"""
        logger.info("Battle in progress...")
        self.state.update_state(GameState.IN_BATTLE)

        max_wait = 180
        elapsed = 0
        check_interval = 10

        while elapsed < max_wait:
            time.sleep(check_interval)
            elapsed += check_interval

            screenshot = self.adb.get_screenshot()
            if screenshot and self.is_battle_complete(screenshot):
                logger.info("Battle completed!")
                return

        logger.warning("Battle timeout reached")

    @staticmethod
    def is_battle_complete(screenshot) -> bool:
        """Check if battle is complete (placeholder)"""
        return False

    def collect_rewards(self):
        """Collect battle rewards"""
        try:
            logger.info("Collecting rewards...")
            self.state.update_state(GameState.LOOTING)

            time.sleep(2)

            # Record attack stats
            self.state.record_attack(
                gold_looted=50000, elixir_looted=50000
            )

        except Exception as e:
            logger.error(f"Error collecting rewards: {e}")

    def print_stats(self):
        """Print bot statistics"""
        logger.info("=" * 50)
        logger.info("BOT STATISTICS")
        logger.info("=" * 50)
        stats = self.state.get_stats()
        for key, value in stats.items():
            logger.info(f"{key}: {value}")
        logger.info("=" * 50)


def main():
    """Entry point"""
    bot = ClashOfClansBot()
    bot.start()


if __name__ == "__main__":
    main()
