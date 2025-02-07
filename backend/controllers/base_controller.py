from typeguard import typechecked
from backend.database_manager.generic_database_manager import GenericDatabaseManager
from backend.utilities import SingletonMeta

@typechecked
class BaseController(metaclass=SingletonMeta):
    _database_manager: GenericDatabaseManager

    def __init__(self, database_manager: GenericDatabaseManager) -> None:
        self._database_manager = database_manager
        