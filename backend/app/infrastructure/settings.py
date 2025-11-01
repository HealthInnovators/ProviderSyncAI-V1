from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")
    
    environment: str = Field(default="local")
    api_prefix: str = Field(default="/api")

    # External services
    nppes_base_url: str = Field(default="https://npiregistry.cms.hhs.gov/api")
    searxng_url: str = Field(default="https://searxng.site")

    # AI keys (optional depending on provider)
    openai_api_key: Optional[str] = Field(default=None)
    hf_token: Optional[str] = Field(default=None)

    # Server config
    request_timeout_seconds: float = Field(default=10.0)
    http_max_retries: int = Field(default=2)
    cache_ttl_seconds: int = Field(default=300)
    rate_limit_per_minute: int = Field(default=60)


settings = Settings()


