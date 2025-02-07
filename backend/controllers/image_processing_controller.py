from flask import Blueprint, request, jsonify
from services.image_processor import ImageProcessor

class ImageController:
    """Flask Controller for handling image processing requests."""
    
    def __init__(self):
        self.processor = ImageProcessor()
        self.blueprint = Blueprint("image", __name__)
        
        # Register routes
        self.blueprint.add_url_rule("/upload", "upload_image", self.upload_image, methods=["POST"])

    def upload_image(self):
        """Handles image uploads and returns the processed image."""
        return jsonify(self.processor.process_uploaded_image())

# Create an instance to be used in `app.py`
image_controller = ImageController()
image_bp = image_controller.blueprint
