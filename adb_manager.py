"""
ADB Manager - Handle Android Device Bridge connections
"""

import subprocess
import logging
import time
from typing import Optional
from PIL import Image
import io

logger = logging.getLogger(__name__)


class ADBManager:
    """Manages ADB connection and commands"""

    def __init__(self, device_ip: str, device_port: int = 5555, timeout: int = 10):
        """
        Initialize ADB Manager

        Args:
            device_ip: IP address of Android device/emulator
            device_port: ADB port (default 5555)
            timeout: Command timeout in seconds
        """
        self.device_ip = device_ip
        self.device_port = device_port
        self.timeout = timeout
        self.device_id = f"{device_ip}:{device_port}"
        self.connected = False

    def connect(self) -> bool:
        """Connect to Android device via ADB"""
        try:
            logger.info(f"Connecting to device: {self.device_id}")
            result = subprocess.run(
                ["adb", "connect", self.device_id],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )

            if "connected" in result.stdout.lower():
                self.connected = True
                logger.info("✓ Successfully connected to device")
                return True
            else:
                logger.error(f"Failed to connect: {result.stdout}")
                return False

        except FileNotFoundError:
            logger.error("ADB not found. Please ensure Android SDK is installed.")
            return False
        except subprocess.TimeoutExpired:
            logger.error("Connection timeout")
            return False

    def disconnect(self) -> bool:
        """Disconnect from device"""
        try:
            subprocess.run(
                ["adb", "disconnect", self.device_id],
                capture_output=True,
                timeout=self.timeout,
            )
            self.connected = False
            logger.info("Disconnected from device")
            return True
        except Exception as e:
            logger.error(f"Disconnect error: {e}")
            return False

    def get_screenshot(self) -> Optional[Image.Image]:
        """Capture screenshot from device"""
        try:
            # Capture screenshot on device
            subprocess.run(
                ["adb", "-s", self.device_id, "shell", "screencap", "-p", "/sdcard/screenshot.png"],
                capture_output=True,
                timeout=self.timeout,
            )

            # Pull screenshot to local machine
            result = subprocess.run(
                ["adb", "-s", self.device_id, "pull", "/sdcard/screenshot.png", "-"],
                capture_output=True,
                timeout=self.timeout,
            )

            if result.returncode == 0:
                # Convert bytes to PIL Image
                image = Image.open(io.BytesIO(result.stdout))
                return image
            else:
                logger.error("Failed to capture screenshot")
                return None

        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return None

    def tap(self, x: int, y: int) -> bool:
        """Tap on screen at coordinates"""
        try:
            subprocess.run(
                ["adb", "-s", self.device_id, "shell", "input", "tap", str(x), str(y)],
                capture_output=True,
                timeout=self.timeout,
            )
            logger.debug(f"Tapped at ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"Tap error: {e}")
            return False

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 500) -> bool:
        """Swipe from (x1, y1) to (x2, y2)"""
        try:
            subprocess.run(
                [
                    "adb",
                    "-s",
                    self.device_id,
                    "shell",
                    "input",
                    "swipe",
                    str(x1),
                    str(y1),
                    str(x2),
                    str(y2),
                    str(duration),
                ],
                capture_output=True,
                timeout=self.timeout,
            )
            logger.debug(f"Swiped from ({x1}, {y1}) to ({x2}, {y2})")
            return True
        except Exception as e:
            logger.error(f"Swipe error: {e}")
            return False

    def type_text(self, text: str) -> bool:
        """Type text on device"""
        try:
            # Escape special characters
            text = text.replace(" ", "%s")
            subprocess.run(
                ["adb", "-s", self.device_id, "shell", "input", "text", text],
                capture_output=True,
                timeout=self.timeout,
            )
            logger.debug(f"Typed: {text}")
            return True
        except Exception as e:
            logger.error(f"Type error: {e}")
            return False

    def wait_for_device(self, max_attempts: int = 5) -> bool:
        """Wait for device to be ready"""
        for attempt in range(max_attempts):
            if self.connected:
                return True
            logger.info(f"Waiting for device... (attempt {attempt + 1}/{max_attempts})")
            time.sleep(2)
        return False
