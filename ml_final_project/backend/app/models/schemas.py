from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class DiseaseType(str, Enum):
    PNEUMONIA = "pneumonia"
    TUBERCULOSIS = "tuberculosis"
    LUNG_CANCER = "lung_cancer"
    COVID19 = "covid19"
    NORMAL = "normal"

# Base schemas
class DiseaseBase(BaseModel):
    name: str
    description: str
    severity: SeverityLevel
    symptoms: List[str]
    treatment: Optional[str] = None
    
class Disease(DiseaseBase):
    id: int
    image_url: Optional[str] = None
    risk_factors: List[str] = []
    prevention: List[str] = []
    created_at: datetime

class DiseaseCreate(DiseaseBase):
    pass

# Analysis schemas
class AnalysisRequest(BaseModel):
    patient_age: Optional[int] = Field(None, ge=0, le=120)
    patient_gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    symptoms: Optional[List[str]] = []
    medical_history: Optional[List[str]] = []

class PredictionResult(BaseModel):
    disease_type: DiseaseType
    confidence: float = Field(..., ge=0.0, le=1.0)
    probability: float = Field(..., ge=0.0, le=1.0)

class AnalysisResult(BaseModel):
    id: str
    predictions: List[PredictionResult]
    top_prediction: PredictionResult
    confidence_score: float
    recommendations: List[str]
    severity_assessment: SeverityLevel
    requires_immediate_attention: bool
    analysis_timestamp: datetime
    image_path: Optional[str] = None

class AnalysisResponse(BaseModel):
    success: bool
    analysis: AnalysisResult
    message: str

# Symptom schemas
class SymptomMatch(BaseModel):
    symptom: str
    diseases: List[str]
    match_score: float = Field(..., ge=0.0, le=1.0)

class SymptomAnalysisRequest(BaseModel):
    symptoms: List[str]
    age: Optional[int] = None
    gender: Optional[str] = None

class SymptomAnalysisResponse(BaseModel):
    matches: List[SymptomMatch]
    suggested_diseases: List[Disease]
    recommendations: List[str]

# User schemas
class UserBase(BaseModel):
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

class UserAnalysisHistory(BaseModel):
    user_id: int
    analyses: List[AnalysisResult]
    total_analyses: int

# File upload schema
class FileUploadResponse(BaseModel):
    filename: str
    file_path: str
    file_size: int
    content_type: str
    upload_timestamp: datetime

# Error schemas
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None

# Health check schema
class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    ml_service_status: bool
    database_status: bool
    version: str 