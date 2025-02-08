from typing import Any, Dict
from flask import Blueprint, request, jsonify

from backend.controllers.base_controller import BaseController
from backend.database_manager.generic_database_manager import GenericDatabaseManager
from text_processor.text_processor import TextProcessor
from decorators.authentication_decorator import protected

class TextController(BaseController):
    """Flask Controller for handling text processing requests."""
    
    def __init__(self, database_manager: GenericDatabaseManager):
        super().__init__(database_manager=database_manager)
        self.blueprint = Blueprint("api/text", __name__)
        self.processor = TextProcessor()
        
        # Register routes
        self.blueprint.add_url_rule("/summarize", "summarize", self.summarize, methods=["POST"])
        self.blueprint.add_url_rule("/sentiment", "sentiment", self.sentiment, methods=["POST"])
        self.blueprint.add_url_rule("/keywords", "keywords", self.keywords, methods=["POST"])
        self.blueprint.add_url_rule("/embed", "embed", self.embed, methods=["POST"])
    
    @protected
    def summarize(self, payload: Dict[str, Any]):
        """Returns a summary of the provided text."""
        text = request.json.get("text", "")
        return jsonify({"summary": self.processor.summarize_text(text)})
    
    @protected
    def sentiment(self, payload: Dict[str, Any]):
        """Returns sentiment analysis of the provided text."""
        text = request.json.get("text", "")
        return jsonify(self.processor.analyze_sentiment(text))

    @protected
    def keywords(self, payload: Dict[str, Any]):
        """Extracts keywords from the provided text."""
        text = request.json.get("text", "")
        return jsonify(self.processor.extract_keywords(text))

    @protected
    def embed(self, payload: Dict[str, Any]):
        """Performs T-SNE dimensionality reduction on text input."""
        text_list = request.json.get("text_list", [])
        return jsonify(self.processor.embed_text(text_list))
