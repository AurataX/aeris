from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    supabase_db_url_api: str = ""
    api_cors_origins: str = "http://localhost:3000"
    api_admin_key: str = ""
    run_now_cooldown_seconds: int = 600
    databricks_host: str = ""
    databricks_client_id: str = ""
    databricks_client_secret: str = ""
    databricks_job_id: str = ""


settings = Settings()
