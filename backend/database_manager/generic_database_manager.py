from abc import ABC as AbstractClass, abstractmethod
from typing import Any, Dict

class GenericDatabaseManager(AbstractClass):
    """An interface for database managers.
    """
    
    @abstractmethod
    def __init__(self, connection_string: str, database_name: str):
        pass

    @abstractmethod
    def get(self, document: Any, **filters: Any) -> Any:
        pass

    @abstractmethod
    def get_one(self, document: Any, **filters: Any) -> Any:
        pass

    @abstractmethod
    def create(self, document: Any, **data: Any) -> Any:
        pass
    
    @abstractmethod
    def update(self, document: Any, filters: Dict[str, Any], update_data: Dict[str, Any]) -> Any:
        pass
    
    @abstractmethod
    def delete(self, document: Any, **filters: Any) -> Any:
        pass