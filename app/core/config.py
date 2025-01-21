from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ScrapeBotBaseSetting(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, validate_default=True)

    LOG_LEVEL: str = Field("DEBUG")
    APP_TITLE: str = Field("ScrapeBot")
    REDIS_URL: RedisDsn = Field(RedisDsn("redis://localhost:6379"))
    LOCAL_DB_FILE: str = Field("data/local_database.json")
    LOCAL_FILESTORE_PATH: str = Field("data/file_store/")
    AUTH_TOKEN: str = Field("atlys_test")


settings = ScrapeBotBaseSetting() # type: ignore
