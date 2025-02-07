import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from backend.utilities import SingletonMeta

class MediaStorageManager(metaclass=SingletonMeta):
    def __init__(self, name: str, api_key: str, api_secret: str):
        # Configuration       
        cloudinary.config( 
            cloud_name = name, 
            api_key = api_key, 
            api_secret = api_secret,
            secure=True
        )

    def upload_file(self,image_path: str, public_id: str) -> str:
        # Upload an image
        upload_result = cloudinary.uploader.upload(image_path,
                                                public_id=public_id)
        print(upload_result["secure_url"])
        return upload_result["secure_url"]

    def get_file(self, public_id: str) -> str:
        optimize_url, _ = cloudinary_url(public_id, fetch_format="auto", quality="auto")
        print(optimize_url)
        return optimize_url
