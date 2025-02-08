from typing import Any, Dict
from flask import Blueprint, Response, jsonify, request
from backend.controllers.base_controller import BaseController
from backend.database_manager.generic_database_manager import GenericDatabaseManager
from backend.database_models.files import FileDocument
from backend.decorators.authentication_decorator import protected
from backend.media_storage_manager.media_storage_manager import MediaStorageManager
from image_processing_module.image_processor import ImageProcessor

class ImageController(BaseController):
    """Flask Controller for handling image processing requests."""
    
    def __init__(self, database_manager: GenericDatabaseManager, media_storage_manager: MediaStorageManager):
        super().__init__(database_manager=database_manager)
        self.processor = ImageProcessor()
        self.media_storage_manager = media_storage_manager
        self.blueprint = Blueprint("api/image", __name__)
        
        # Register routes
        self.blueprint.add_url_rule("/upload", "upload_image", self.upload_image, methods=["POST"])
    
    @protected
    def upload_image(self, payload: Dict[str, Any]):
        """Handles image uploads and returns the processed image."""
        file = request.files.get("image")
        user_id = payload.get("sub")
        file_path = file.name

        file_document = FileDocument(user_id=user_id, filename=file.name)
        upload_link = self.media_storage_manager.upload_file(file_path, str(file_document.pk))
        file_document.save()
        return jsonify({"upload_link": upload_link})

    @protected
    def histogram(self, payload: Dict[str, Any]) -> Response:
        """API to generate color histograms."""
        file = request.files.get("image")
        return jsonify(self.processor.generate_histogram(file))

    @protected
    def segmentation(self, payload: Dict[str, Any]) -> Response:
        """API to generate segmentation masks."""
        file = request.files.get("image")
        data = request.json
        threshold = data.get("threshold", 128)
        return jsonify(self.processor.generate_segmentation_mask(file, threshold))
