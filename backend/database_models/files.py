from datetime import datetime, timezone
from mongoengine import Document, StringField, DateTimeField, ReferenceField, CASCADE
from backend.database_models.users import User

class FileDocument(Document):
    """
    Model to store files related to a user.
    """
    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    filename = StringField(required=True)
    uploaded_at = DateTimeField(default=datetime.now(timezone.utc))

    meta = {'collection': 'file_documents'}