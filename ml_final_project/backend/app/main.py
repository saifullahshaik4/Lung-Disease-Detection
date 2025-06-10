from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from contextlib import asynccontextmanager

from .routers import analysis, diseases, symptoms, users
from .core.config import settings
from .services.ml_service import MLService
from .services.firebase_service import firebase_service

# Global service instances
ml_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global ml_service
    
    # Initialize Firebase
    await firebase_service.initialize()
    print("🔥 Firebase connected successfully!")
    
    # Initialize ML service
    ml_service = MLService()
    await ml_service.load_models()
    print("🚀 ML models loaded successfully!")
    
    yield
    
    # Shutdown
    print("🔄 Shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Lung Disease Detection API",
    description="AI-powered lung disease detection and analysis system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(diseases.router, prefix="/api/diseases", tags=["diseases"])
app.include_router(symptoms.router, prefix="/api/symptoms", tags=["symptoms"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/")
async def root():
    return {
        "message": "Lung Disease Detection API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ml_service": ml_service is not None} 