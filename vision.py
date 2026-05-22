"""
Vision Module - Screen analysis and OCR
"""

import cv2
import numpy as np
import logging
from typing import Tuple, Optional, List
from PIL import Image

logger = logging.getLogger(__name__)


class VisionAnalyzer:
    """Analyzes game screenshots for game state"""

    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode

    @staticmethod
    def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
        """Convert PIL Image to OpenCV format"""
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    @staticmethod
    def cv2_to_pil(cv2_image: np.ndarray) -> Image.Image:
        """Convert OpenCV image to PIL Image"""
        return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))

    def find_template(
        self, screenshot: Image.Image, template: Image.Image, threshold: float = 0.8
    ) -> Optional[Tuple[int, int]]:
        """
        Find template in screenshot using template matching

        Args:
            screenshot: Full screenshot
            template: Template image to find
            threshold: Matching threshold (0-1)

        Returns:
            (x, y) coordinates of center if found, else None
        """
        try:
            img_cv = self.pil_to_cv2(screenshot)
            template_cv = self.pil_to_cv2(template)

            # Convert to grayscale
            img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template_cv, cv2.COLOR_BGR2GRAY)

            # Template matching
            result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                # Get center of template
                template_h, template_w = template_gray.shape
                x = max_loc[0] + template_w // 2
                y = max_loc[1] + template_h // 2
                logger.info(f"✓ Template found at ({x}, {y}) with confidence {max_val:.2f}")
                return (x, y)
            else:
                logger.debug(f"Template not found (confidence: {max_val:.2f})")
                return None

        except Exception as e:
            logger.error(f"Template matching error: {e}")
            return None

    def detect_color_range(
        self,
        screenshot: Image.Image,
        lower_hsv: Tuple[int, int, int],
        upper_hsv: Tuple[int, int, int],
    ) -> List[Tuple[int, int]]:
        """
        Detect objects by color range (HSV)

        Args:
            screenshot: Screenshot image
            lower_hsv: Lower HSV bounds
            upper_hsv: Upper HSV bounds

        Returns:
            List of (x, y) coordinates of detected objects
        """
        try:
            img_cv = self.pil_to_cv2(screenshot)
            hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

            # Create mask
            mask = cv2.inRange(hsv, np.array(lower_hsv), np.array(upper_hsv))

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            results = []
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    results.append((cx, cy))

            logger.info(f"Found {len(results)} objects with color range")
            return results

        except Exception as e:
            logger.error(f"Color detection error: {e}")
            return []

    def extract_region(
        self, screenshot: Image.Image, x1: int, y1: int, x2: int, y2: int
    ) -> Image.Image:
        """Extract specific region from screenshot"""
        return screenshot.crop((x1, y1, x2, y2))

    def detect_text_region(
        self, screenshot: Image.Image, region: Tuple[int, int, int, int]
    ) -> Image.Image:
        """Extract text region for OCR"""
        try:
            x1, y1, x2, y2 = region
            text_region = self.extract_region(screenshot, x1, y1, x2, y2)

            # Enhance image for OCR
            img_cv = self.pil_to_cv2(text_region)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

            # Thresholding
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

            return self.cv2_to_pil(thresh)

        except Exception as e:
            logger.error(f"Text region detection error: {e}")
            return screenshot

    def get_image_stats(self, screenshot: Image.Image) -> dict:
        """Get basic image statistics"""
        img_array = np.array(screenshot)
        return {
            "shape": img_array.shape,
            "mean": img_array.mean(),
            "std": img_array.std(),
        }
