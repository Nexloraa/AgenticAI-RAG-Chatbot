from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# load env variables from .env file
load_dotenv()


class AgentSettings(BaseSettings):
    GROQ_API_KEY: str
    DOCUMENTS_DIR: str
    VECTOR_STORE_DIR: str
    COLLECTION_NAME: str

    MODEL_NAME: str = "llama-3.1-8b-instant"
    MODEL_TEMPERATURE: float = 0.2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
