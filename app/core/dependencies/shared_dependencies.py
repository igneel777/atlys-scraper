from app.core.datastore import LocalDatabase, LocalFileStore, RedisAdapter


def get_cache_store():
    return RedisAdapter()


def get_database():
    return LocalDatabase()


def get_filestore():
    return LocalFileStore()
