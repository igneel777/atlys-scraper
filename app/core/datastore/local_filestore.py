import os
import urllib.request

from app.core.config import settings
from app.core.datastore.base_filestore import BaseFilestore


class LocalFileStore(BaseFilestore):
    def __init__(self):
        self.image_bucket_name = settings.LOCAL_FILESTORE_PATH
        if not os.path.exists(os.getcwd() + "/" + self.image_bucket_name):
            os.mkdir(self.image_bucket_name)

    def save_file_from_url(self, source_url: str, file_key: str):
        obj_key = self.image_bucket_name + file_key
        try:
            urllib.request.urlretrieve(source_url, obj_key)
        except:
            obj_key = ""
        finally:
            return obj_key
