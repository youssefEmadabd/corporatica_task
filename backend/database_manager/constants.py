from enum import Enum
    
class UserKeys(Enum):
    NAME = "name"
    USERNAME = "username"
    PASSWORD = "password"
    ID = "id"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value