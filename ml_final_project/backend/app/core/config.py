from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "Lung Disease Detection API"
    DEBUG: bool = True
    
    # Firebase Settings
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "lungdiseasedetection-19b4f")
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # Next.js frontend
        "http://127.0.0.1:3000",
        "http://localhost:8000",  # FastAPI docs
    ]
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = [
        "image/jpeg",
        "image/jpg", 
        "image/png",
        "image/bmp",
        "image/tiff"
    ]
    
    # ML Model Settings
    MODEL_PATH: str = "app/models"
    CONFIDENCE_THRESHOLD: float = 0.7
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings() 