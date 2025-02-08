from typing import Any, Dict
from flask import Blueprint, jsonify
from backend.controllers.base_controller import BaseController
from backend.database_manager.generic_database_manager import GenericDatabaseManager
from backend.decorators.authentication_decorator import protected
from tabular_data_module.tabular_data_processor import TabularProcessor

class TabularController(BaseController):
    """Flask Controller for handling tabular data processing requests."""
    
    def __init__(self, database_manager: GenericDatabaseManager):
        super().__init__(database_manager=database_manager)
        self.processor = TabularProcessor(database_manager=database_manager, )
        self.blueprint = Blueprint("api/tabular", __name__)
        
        # Register routes
        self.blueprint.add_url_rule("/stats", "get_statistics", self.get_statistics, methods=["GET"])
        self.blueprint.add_url_rule("/chart", "get_chart", self.get_chart, methods=["GET"])
        self.blueprint.add_url_rule("/outliers", "get_outliers", self.get_outliers, methods=["GET"])

    @protected
    def get_statistics(self, payload: Dict[str, Any]):
        """Returns computed statistics of weather data."""
        return jsonify(self.processor.compute_statistics(payload=payload))

    @protected
    def get_chart(self, payload: Dict[str, Any]):
        """Returns a temperature distribution chart in base64 format."""
        image = self.processor.generate_chart(payload=payload)
        return jsonify({"chart": image})

    @protected
    def get_outliers(self, payload: Dict[str, Any]):
        """Returns detected outliers."""
        return jsonify(self.processor.detect_outliers(payload=payload))
