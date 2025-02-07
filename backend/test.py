from media_storage_manager.media_storage_manager import MediaStorageManager

media_storage_manager:MediaStorageManager = MediaStorageManager(name="deup5xdtj", api_key="184557967622589", api_secret="rZc7qfD0XjKrbZr3kYLo-rEjQWE")
# media_storage_manager.upload_file(image_path="./Screenshot 2025-02-01 at 6.16.39 PM.png", public_id="shoes")

media_storage_manager.get_file(public_id="shoes")