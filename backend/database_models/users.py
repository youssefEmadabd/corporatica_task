from datetime import datetime, timezone
from mongoengine import Document, StringField, DateTimeField, ListField

# Define the User model
class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)  # Hash the password before storing
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))
    roles = ListField(StringField(), default=["user"])

    meta = {
        "collection": "users",
        "indexes": ["username", "email"]  # Add indexes for faster queries
    }