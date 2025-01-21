from app.core.config import settings
from _io import TextIOWrapper
from app.core.datastore.base_database import BaseDatabase

class LocalDatabase(BaseDatabase):

    connection: TextIOWrapper
    
    def __init__(self):
        # Since this is local db, we will just make the connection as true
        if not LocalDatabase.connection or LocalDatabase.connection.closed:
            LocalDatabase.connection = open(settings.LOCAL_DB_FILE, 'r+', encoding='utf-8')

    def get_connection(self):
        return LocalDatabase.connection
    
    def refresh_connection(self):
        if not LocalDatabase.connection or LocalDatabase.connection.closed:
            LocalDatabase.connection = open(settings.LOCAL_DB_FILE, 'r+', encoding='utf-8')
