
import os
from flask import Flask
from dotenv import load_dotenv
import os, sys

sys.path.insert(0, os.getcwd())

from backend.utilities import print_log
from backend.utilities.api_exception import APIException
from backend.controllers.user_controller import UserController
from backend.controllers.image_processing_controller import ImageController
from backend.controllers.tabular_data_processing_contoller import TabularController
from backend.controllers.text_processing_controller import TextController
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
        
    # Create an instance of user controller
    user_controller = UserController(database_manager=database_manager)
    user_bp = user_controller.blueprint

    # Create an instance of text controller
    text_controller = TextController(database_manager=database_manager)
    text_bp = text_controller.blueprint

    # Create an instance of tabular controller
    tabular_controller = TabularController(database_manager=database_manager)
    tabular_bp = tabular_controller.blueprint

    # Create an instance of image controller
    image_controller = ImageController(database_manager=database_manager, media_storage_manager=file_storage_manager)
    image_bp = image_controller.blueprint

    # Register blueprints from class-based controllers
    app.register_blueprint(tabular_bp, url_prefix="/tabular")
    app.register_blueprint(image_bp, url_prefix="/image")
    app.register_blueprint(text_bp, url_prefix="/text")
    app.register_blueprint(user_bp, url_prefix="/users")

    # Print all routes
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print_log(f"Route: {rule}, Methods: {', '.join(rule.methods)}")

    app.run(debug=True)

if __name__ == "__main__":
    main()