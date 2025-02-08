from typing import Any, Dict
from mongoengine import QuerySet
from flask import Blueprint, request, jsonify

from backend.controllers.base_controller import BaseController
from backend.database_manager.database_manager import DatabaseManager
from backend.database_manager.generic_database_manager import GenericDatabaseManager
from backend.database_models.users import User
from backend.utilities import create_access_token, is_valid_password, APIException, hash_password
from database_manager.constants import UserKeys

class UserController(BaseController):

    def __init__(self, database_manager: GenericDatabaseManager):
        super().__init__(database_manager)
        self.blueprint = Blueprint("api/users", __name__)
        
        # Register routes
        self.blueprint.add_url_rule("/login", "login", self.login, methods=["POST"])
        self.blueprint.add_url_rule("/register", "register", self.login, methods=["POST"])

    def login(self) -> Dict[str, Any]:
        """
        Authenticates a user and returns a JWT token if successful.

        Args:
            payload (Dict[str, Any]): A dictionary containing 'username' and 'password' keys.

        Returns:
            Dict[str, Any]: A dictionary containing the 'access_token' if authentication is successful.

        Raises:
            APIException: If the username is invalid or the password does not match.
        """
        payload = request.json

        username = payload.get("username")
        password = payload.get("password")
        users: QuerySet = self._database_manager.get(User, username=username)
        user = users.first()
        status = users.count() > 0
        if not status or not user:
            raise APIException(status_code=401, message="Invalid username")
        
        if is_valid_password(user[UserKeys.PASSWORD.value], password):
            token = create_access_token({"sub": str(user.pk)})
            return jsonify({"access_token": token})

        raise APIException(status_code=401, message="Invalid password")

    def register(self) -> Dict[str, Any]:
        """
        Registers a new user and returns a JWT token if successful.

        Args:
            payload (Dict[str, Any]): A dictionary containing 'username', 'password', and 'email' keys.

        Returns:
            Dict[str, Any]: A dictionary containing the 'access_token' if registration is successful.

        Raises:
            APIException: If the username or email is already in use.
        """
        payload = request.json

        username = payload.get("username")
        email = payload.get("email")
        password = payload.get("password")
        users: QuerySet = self._database_manager.get(User, username=username, email=email)
        status = users.count() == 0
        if not status:
            raise APIException(status_code=409, message="Username or email already in use")
        
        hashed_password = hash_password(password)
        user = User(username=username, email=email, password=hashed_password)
        user.save()
        token = create_access_token({"sub": str(user.pk)})

        return jsonify({"access_token": token})
