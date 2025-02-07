import pandas as pd
from database_models import WeatherData
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, Any

class TabularProcessor:
    """Processes weather data and provides statistics & visualizations."""

    def __init__(self):
        self.df = self.load_weather_data()

    def load_weather_data(self) -> pd.DataFrame:
        """Fetches weather data and loads it into a DataFrame."""
        data = WeatherData.objects().as_pymongo()
        return pd.DataFrame(data)

    def compute_statistics(self) -> Dict[str, Any]:
        """Returns basic statistics: mean, median, mode, quartiles, outliers."""
        if self.df.empty:
            return {"error": "No weather data available."}

        stats = {
            "temperature": {
                "mean": self.df["temperature"].mean(),
                "median": self.df["temperature"].median(),
                "mode": self.df["temperature"].mode().tolist(),
            },
            "humidity": {
                "mean": self.df["humidity"].mean(),
                "median": self.df["humidity"].median(),
                "mode": self.df["humidity"].mode().tolist(),
            },
        }
        return stats

    def generate_chart(self) -> str:
        """Generates a histogram of temperature and returns a base64 image."""
        if self.df.empty:
            return None

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