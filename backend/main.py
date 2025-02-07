
import os
from typing import Dict, Any
from flask import Flask, request
from dotenv import load_dotenv
import os, sys

sys.path.insert(0, os.getcwd())

from backend.utilities.api_exception import APIException
from backend.controllers.user_controller import UserController
from backend.media_storage_manager.media_storage_manager import MediaStorageManager
from backend.database_manager.database_manager import DatabaseManager
from decorators.authentication_decorator import protected

app = Flask(__name__)
@app.errorhandler(APIException)
def handle_api_exception(error):
    return error.to_response()

@app.route("/register", methods=["POST"])
def register():
    """_summary_

    Raises:
        APIException: _description_
        APIException: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    data:Dict[str, Any] = request.json

    return UserController().register(data)

@app.route("/login", methods=["POST"])
def login():
    """
    Login endpoint to get a jwt token.
    => Test payload: {
            "username": "generic_username",
            "password": "test"
        }
    Args:
        data (dict): Dictionary with username and password.

    Returns:
        dict: A dictionary with the jwt token.

    Raises:
        HTTPException: 401 if username or password is invalid.
    """
    data:Dict[str, Any] = request.json
    return UserController().login(data)

def main():
    dotenv_loading_status = load_dotenv()
    if not dotenv_loading_status:
        raise FileNotFoundError("Error loading .env file, check if it exists")

    mongo_db_connection_string = os.environ.get("MONGO_DB_CONNECTION_STRING")
    mongo_db_database_name = os.environ.get("MONGO_DB_DATABASE_NAME")
    cloudinary_cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key = os.environ.get("CLOUDINARY_API_KEY")
    cloudinary_api_secret = os.environ.get("CLOUDINARY_API_SECRET")
    
    global database_manager
    global file_storage_manager
    
    database_manager = DatabaseManager(connection_string=mongo_db_connection_string, database_name=mongo_db_database_name)
    file_storage_manager = MediaStorageManager(name=cloudinary_cloud_name, api_key=cloudinary_api_key, api_secret=cloudinary_api_secret)
    UserController(database_manager=database_manager)
    app.run(debug=True)

if __name__ == "__main__":
    main()