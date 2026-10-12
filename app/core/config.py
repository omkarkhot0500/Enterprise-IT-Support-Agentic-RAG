# Reason of this file is: to store all the configuration variables in a single place
# which will make it easier to manage and modify the configuration

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    app_name: str = "Enterprise IT Support Agentic RAG Copilot"
    app_env: str = "development"
    groq_api_key: str = ""  # Nothing here because it is a secret key and should not be shared
    openai_api_key: str = ""
    tavily_api_key: str = ""
    pinecone_api_key: str = ""
    pinecone_index_name: str = "fde-it-support-rag" # Name of the pinecone index
    pinecone_namespace: str = "company-it-kb" # Namespace of the pinecone index
    embedding_model: str = "all-MiniLM-L6-v2" # This is the model used for embedding the text
    groq_model: str = "openai/gpt-oss-20b" # This is the model used for the agent
    openai_model: str = "gpt-4o-mini" 
    top_k: int = 4 # Number of similar chunks to retrieve from the pinecone index
    max_retries: int = 1 # Maximum number of retries for failed requests
    admin_api_key: str = "change-me" # Admin API key for authentication
    # Below are Sqllite database and paths for storing the data
    audit_db_path: str = str(BASE_DIR / "data" / "audit.db") # Path to the audit database, audit means keeping track of all the requests and responses (this db will be used for tracking the user queries and the bot responses)
    upload_dir: str = str(BASE_DIR / "uploads") # Path to the upload directory where all the user uploaded pdfs are stored (This is where user uploaded pdfs are temporarily stored, later they are moved to the pinecone index)
    sample_kb_dir: str = str(BASE_DIR / "data" / "sample_kb") # Path to the sample knowledge base directory (it stores a few pdf files for testing and demo purposes in local storage)    

    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), extra="ignore")




@lru_cache
def get_settings() -> Settings:
    return Settings()
