import cv2
import numpy as np
import base64
from typing import Tuple, Dict
from flask import request

class ImageProcessor:
    """Handles image processing tasks such as resizing, cropping, and segmentation."""

    def resize_image(self, image: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
        """Resizes an image to the given size."""
        return cv2.resize(image, size)

    def crop_image(self, image: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
        """Crops an image given x, y, width, and height."""
        return image[y:y+h, x:x+w]

    def process_uploaded_image(self) -> Dict[str, str]:
        """Processes an uploaded image and returns the modified version."""
        file = request.files.get("image")
        if not file:
            return {"error": "No image uploaded."}

        image = np.frombuffer(file.read(), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        resized = self.resize_image(image, (100, 100))

        _, buffer = cv2.imencode(".jpg", resized)
        encoded = base64.b64encode(buffer).decode("utf-8")
        return {"resized_image": encoded}
