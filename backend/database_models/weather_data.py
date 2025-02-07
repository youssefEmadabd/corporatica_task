from mongoengine import Document, ReferenceField, CASCADE, DateTimeField, StringField, IntField, FloatField
from datetime import datetime, timezone

from backend.database_models.users import User

class WeatherData(Document):
    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))
    temperature = FloatField(required=True)  # In Celsius
    humidity = IntField(required=True)  # Percentage
    weather_condition = StringField(required=True)  # e.g., "Sunny", "Rainy"
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'weather_data'}