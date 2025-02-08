import pandas as pd
import numpy as np
from backend.database_manager.generic_database_manager import GenericDatabaseManager
from backend.utilities.api_exception import APIException
from database_models import WeatherData
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, Any, Type

class TabularProcessor:
    """Processes weather data and provides statistics & visualizations."""

    def __init__(self, database_manager: GenericDatabaseManager):
        self.__database_manager = database_manager

    def load_weather_data(self, weather_data_model: WeatherData, user_id: str) -> pd.DataFrame:
        """Fetches weather data and loads it into a DataFrame."""
        data = self.__database_manager.get(weather_data_model, user_id=user_id)
        return pd.DataFrame(data)

    def compute_statistics(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Returns basic statistics: mean, median, mode, quartiles, outliers."""
        df = self.load_weather_data(WeatherData, user_id=payload.get("sub"))
        if df.empty:
            raise APIException("No weather data available.", status_code=404)

        stats = {
            "temperature": {
                "mean": df["temperature"].mean(),
                "median": df["temperature"].median(),
                "mode": df["temperature"].mode().tolist(),
                "quartiles": df["temperature"].quantile([0.25, 0.5, 0.75]).tolist(),
            },
            "humidity": {
                "mean": df["humidity"].mean(),
                "median": df["humidity"].median(),
                "mode": df["humidity"].mode().tolist(),
                "quartiles": df["humidity"].quantile([0.25, 0.5, 0.75]).tolist(),
            },
        }
        return stats

    def detect_outliers(self, payload: Dict[str, Any]):
        """Detect outliers using the IQR (Interquartile Range) method."""
        df = self.load_weather_data(WeatherData, user_id=payload.get("sub"))
        if df.empty:
            raise APIException("No weather data available.", status_code=404)

        outliers = {}
        for column in df.select_dtypes(include=[np.number]):  # Numeric columns only
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outlier_values = df[(self.data[column] < lower_bound) | (self.data[column] > upper_bound)][column].tolist()
            outliers[column] = outlier_values
        
        return outliers

    def generate_chart(self, payload: Dict[str, Any]) -> str:
        """Generates a histogram of temperature and returns a base64 image."""
        df = self.load_weather_data(WeatherData, user_id=payload.get("sub"))
        if df.empty:
            raise APIException("No weather data available.", status_code=404)

        plt.figure(figsize=(6, 4))
        self.df["temperature"].hist()
        plt.title("Temperature Distribution")
        plt.xlabel("Temperature (°C)")
        plt.ylabel("Frequency")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        encoded = base64.b64encode(buf.read()).decode("utf-8")
        return encoded