from app.core.datastore.base_filestore import BaseFilestore
import urllib.request
import os

class LocalFileStore(BaseFilestore):
    
    def __init__(self, image_bucket_name:str):
        self.image_bucket_name = image_bucket_name
        if not os.path.exists(os.getcwd() + "/" +image_bucket_name):
            os.mkdir(image_bucket_name)
    def save_file_from_url(self, source_url:str, file_key:str):
        obj_key = self.image_bucket_name + file_key
        try:
            urllib.request.urlretrieve(source_url, obj_key)
        except:
            obj_key = ""
        finally:
            return obj_key