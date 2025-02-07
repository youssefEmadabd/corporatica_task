
import os
from typing import Dict, Any
from flask import Flask, request
from dotenv import load_dotenv
import os, sys

sys.path.insert(0, os.getcwd())

from backend.utilities.api_exception import APIException
from backend.controllers.user_controller import user_bp
from backend.controllers.image_processing_controller import image_bp
from backend.controllers.tabular_data_processing_contoller import tabular_bp
from backend.controllers.text_processing_controller import text_bp
from backend.media_storage_manager.media_storage_manager import MediaStorageManager
from backend.database_manager.database_manager import DatabaseManager

app = Flask(__name__)
@app.errorhandler(APIException)
def handle_api_exception(error):
    return error.to_response()

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
    # Register blueprints from class-based controllers
    app.register_blueprint(tabular_bp, url_prefix="/tabular")
    app.register_blueprint(image_bp, url_prefix="/image")
    app.register_blueprint(text_bp, url_prefix="/text")
    app.register_blueprint(user_bp, url_prefix="/users")

    UserController(database_manager=database_manager)
    app.run(debug=True)

if __name__ == "__main__":
    main()