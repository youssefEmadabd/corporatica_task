from flask import Blueprint, request, jsonify
from services.text_processor import TextProcessor
from decorators.authentication_decorator import protected

class TextController:
    """Flask Controller for handling text processing requests."""
    
    def __init__(self):
        self.processor = TextProcessor()
        self.blueprint = Blueprint("api/text", __name__)
        
        # Register routes
        self.blueprint.add_url_rule("/summarize", "summarize", self.summarize, methods=["POST"])
        self.blueprint.add_url_rule("/sentiment", "sentiment", self.sentiment, methods=["POST"])
        self.blueprint.add_url_rule("/keywords", "keywords", self.keywords, methods=["POST"])
    
    @protected
    def summarize(self):
        """Returns a summary of the provided text."""
        text = request.json.get("text", "")
        return jsonify({"summary": self.processor.summarize_text(text)})
    
    @protected
    def sentiment(self):
        """Returns sentiment analysis of the provided text."""
        text = request.json.get("text", "")
        return jsonify(self.processor.analyze_sentiment(text))

    @protected
    def keywords(self):
        """Extracts keywords from the provided text."""
        text = request.json.get("text", "")
        return jsonify(self.processor.extract_keywords(text))

# Create an instance to be used in `app.py`
text_controller = TextController()
text_bp = text_controller.blueprint
