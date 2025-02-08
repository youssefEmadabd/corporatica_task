import cv2, os
import numpy as np
import base64
from typing import Tuple, Dict, List
from werkzeug.datastructures import FileStorage

from backend.utilities.api_exception import APIException

class ImageProcessor:
    """Handles image processing tasks such as resizing, cropping, and segmentation."""

    def resize_image(self, image: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
        """Resizes an image to the given size."""
        return cv2.resize(image, size)

    def crop_image(self, image: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
        """Crops an image given x, y, width, and height."""
        return image[y:y+h, x:x+w]

    def generate_histogram(self, image: FileStorage) -> Dict[str, List[int]]:
        """Generate a color histogram for an image."""
        image = cv2.imread(image)
        if image is None:
            raise APIException("Invalid image", status_code=400)
        
        colors = ('b', 'g', 'r')  # OpenCV uses BGR format
        histogram_data = {}

        for i, color in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256]).flatten()
            histogram_data[color] = hist.tolist()

        return {"histogram": histogram_data}

    def generate_segmentation_mask(self, image: FileStorage, threshold: int = 128):
        """Generate a segmentation mask using thresholding."""
        image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
        if image is None:
            raise APIException("Invalid image", status_code=400)
        
        _, mask = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        mask_path = os.path.join(os.getcwd(), "mask.png")
        cv2.imwrite(mask_path, mask)

        return {"mask_url": f"/{mask_path}"}