from flask import Blueprint, jsonify
from services.tabular_processor import TabularProcessor

class TabularController:
    """Flask Controller for handling tabular data processing requests."""
    
    def __init__(self):
        self.processor = TabularProcessor()
        self.blueprint = Blueprint("api/tabular", __name__)
        
        # Register routes
        self.blueprint.add_url_rule("/stats", "get_statistics", self.get_statistics, methods=["GET"])
        self.blueprint.add_url_rule("/chart", "get_chart", self.get_chart, methods=["GET"])

    @protected
    def get_statistics(self):
        """Returns computed statistics of weather data."""
        return jsonify(self.processor.compute_statistics())

    @protected
    def get_chart(self):
        """Returns a temperature distribution chart in base64 format."""
        image = self.processor.generate_chart()
        return jsonify({"chart": image})

# Create an instance to be used in `app.py`
tabular_controller = TabularController()
tabular_bp = tabular_controller.blueprint
