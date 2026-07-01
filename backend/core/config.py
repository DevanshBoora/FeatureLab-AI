from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FeatureLab AI"
    API_V1_STR: str = "/api/v1"
    
    # Supabase / Database
    SUPABASE_URL: str
    SUPABASE_KEY: str
    DATABASE_URL: str
    
    # JWT Auth
    SECRET_KEY: str = "supersecretkey" # In production, use a strong key
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
