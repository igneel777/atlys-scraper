from app.core.config import settings
from _io import TextIOWrapper
from app.core.datastore.base_database import BaseDatabase
import os
import json

class LocalDatabase(BaseDatabase):

    connection: TextIOWrapper
    
    def __init__(self):
        # Since this is local db, we will just make the connection as true
        folder_path = os.path.dirname(settings.LOCAL_DB_FILE)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if not LocalDatabase.connection or LocalDatabase.connection.closed:
            
            
            if not os.path.exists(os.getcwd() + "/" + settings.LOCAL_DB_FILE):
                with open(settings.LOCAL_DB_FILE, 'w') as f:
                    json.dump({}, f)
            LocalDatabase.connection = open(settings.LOCAL_DB_FILE, 'r+', encoding='utf-8')

    def get_connection(self):
        return LocalDatabase.connection
    
    def refresh_connection(self):
        if not LocalDatabase.connection or LocalDatabase.connection.closed:
            LocalDatabase.connection = open(settings.LOCAL_DB_FILE, 'r+', encoding='utf-8')
