from mongoengine import Document, QuerySet, connect, DoesNotExist, ValidationError
from typeguard import typechecked
from typing import Any, Dict, Optional, Type

from backend.database_manager.generic_database_manager import GenericDatabaseManager
from backend.utilities import print_log

@typechecked
class DatabaseManager(GenericDatabaseManager):
    """ a database manager for an in-memory dictionary acting as a database
    """
    def __init__(self, connection_string: str, database_name: str):
        # Connect to MongoDB
        connect(host=connection_string, db=database_name)

    def create(self, model: Type[Document], **data: Any) -> Optional[Document]:
        """Create and save a new document"""
        try:
            obj = model(**data)
            obj.save()
            print_log(f"Created document in {model.__name__}: {obj.to_json()}")
            return obj
        except (Exception, ValidationError) as e:
            print_log(f"Error creating document in {model.__name__}: {str(e)}")
            return None

    def get(self, model: Type[Document], **filters: Any) -> QuerySet:
        """Retrieve documents based on filters"""
        try:
            results = model.objects(**filters)
            print_log(f"Fetched {len(results)} documents from {model.__name__}")
            return results
        except Exception as e:
            print_log(f"Error fetching data from {model.__name__}: {str(e)}")
            return model.objects.none()  # Return an empty QuerySet

    def get_one(self, model: Type[Document], **filters: Any) -> Optional[Document]:
        """Retrieve a single document"""
        try:
            result = model.objects(**filters)
            print_log(f"Fetched single document from {model.__name__}: {result.to_json()}")
            return result
        except DoesNotExist:
            print_log(f"No document found in {model.__name__} with filters: {filters}")
            return None
        except Exception as e:
            print_log(f"Error fetching single document from {model.__name__}: {str(e)}")
            return None

    def update(self, model: Type[Document], filters: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """Update documents matching the filter"""
        try:
            result = model.objects(**filters).update(**update_data)
            if result:
                print_log(f"Updated {result} document(s) in {model.__name__}")
            else:
                print_log(f"No matching document found for update in {model.__name__}")
            return result
        except Exception as e:
            print_log(f"Error updating document in {model.__name__}: {str(e)}")
            return 0

    def delete(self, model: Type[Document], **filters: Any) -> int:
        """Delete documents matching the filter"""
        try:
            result = model.objects(**filters).delete()
            if result:
                print_log(f"Deleted {result} document(s) from {model.__name__}")
            else:
                print_log(f"No matching document found for deletion in {model.__name__}")
            return result
        except Exception as e:
            print_log(f"Error deleting document from {model.__name__}: {str(e)}")
            return 0