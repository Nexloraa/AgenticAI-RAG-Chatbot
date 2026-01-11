from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Compute project root (folder that contains .env)
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class DocIngestionSettings(BaseSettings):
    DOCUMENTS_DIR: str
    VECTOR_STORE_DIR: str
    COLLECTION_NAME: str
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Pydantic v2 settings config
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )
