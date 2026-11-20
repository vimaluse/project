from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    app_name: str = "WebIntel AI"
    llm_provider: str = ""
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    request_timeout: float = 15.0
    max_html_bytes: int = 2_000_000
    max_text_chars: int = 18_000
    cache_ttl_hours: int = 24
    cache_db: str = "data/cache.sqlite3"
    max_redirects: int = 4
    model_input_usd_per_million: float = 0.10
    model_output_usd_per_million: float = 0.40
    model_display_name: str = "Gemini 3.8 Flash-Lite"

model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore"
)
settings = Settings()
