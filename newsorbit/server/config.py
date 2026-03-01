from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NewsOrbit AI"
    environment: str = "development"
    debug: bool = False

    mongo_uri: str = Field(..., alias="MONGO_URI")
    mongo_db_name: str = Field("newsorbit", alias="MONGO_DB_NAME")

    firebase_credentials_path: str = Field(..., alias="FIREBASE_CREDENTIALS_PATH")

    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")
    gemini_model: str = Field("gemini-1.5-flash", alias="GEMINI_MODEL")

    gnews_api_key: str = Field(..., alias="GNEWS_API_KEY")

    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_algorithm: str = Field("HS256", alias="JWT_ALGORITHM")
    jwt_exp_minutes: int = Field(60 * 24, alias="JWT_EXP_MINUTES")

    cors_origins: str = Field("*", alias="CORS_ORIGINS")
    rate_limit: str = Field("100/minute", alias="RATE_LIMIT")

    scheduler_enabled: bool = Field(True, alias="SCHEDULER_ENABLED")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
