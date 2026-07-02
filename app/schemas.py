from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    max_image_mb: int = 10
    max_image_side: int = 4096
    rembg_model: str = "u2net"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
