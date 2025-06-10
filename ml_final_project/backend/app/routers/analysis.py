from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
import aiofiles
import os
import uuid
from datetime import datetime

from ..models.schemas import (
    AnalysisResponse, 
    AnalysisRequest, 
    AnalysisResult,
    FileUploadResponse,
    ErrorResponse
)
from ..services.ml_service import MLService
from ..services.firebase_service import firebase_service
from ..core.config import settings

router = APIRouter()

# Dependency to get ML service
async def get_ml_service() -> MLService:
    from ..main import ml_service
    if ml_service is None:
        raise HTTPException(status_code=503, detail="ML service not available")
    return ml_service

@router.post("/upload-xray", response_model=AnalysisResponse)
async def analyze_xray(
    file: UploadFile = File(...),
    patient_age: Optional[int] = Form(None),
    patient_gender: Optional[str] = Form(None),
    symptoms: Optional[str] = Form(None),
    medical_history: Optional[str] = Form(None),
    ml_service: MLService = Depends(get_ml_service)
):
    """
    Upload and analyze chest X-ray image for lung disease detection
    """
    try:
        # Validate file type
        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
            )
        
        # Validate file size
        file_content = await file.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        # Reset file pointer
        await file.seek(0)
        
        # Prepare patient info
        patient_info = {}
        if patient_age:
            patient_info["age"] = patient_age
        if patient_gender:
            patient_info["gender"] = patient_gender
        if symptoms:
            patient_info["symptoms"] = [s.strip() for s in symptoms.split(",")]
        if medical_history:
            patient_info["medical_history"] = [h.strip() for h in medical_history.split(",")]
        
        # Perform ML analysis
        analysis_result = await ml_service.predict_lung_disease(file_content, patient_info)
        
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        saved_filename = f"{file_id}.{file_extension}"
        file_path = f"uploads/{saved_filename}"
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # Update analysis result with file path
        analysis_result.image_path = file_path
        
        # Save analysis to Firebase
        try:
            await firebase_service.save_analysis(analysis_result)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Warning: Failed to save analysis to Firebase: {e}")
        
        return AnalysisResponse(
            success=True,
            analysis=analysis_result,
            message="X-ray analysis completed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/batch-analyze", response_model=List[AnalysisResponse])
async def batch_analyze_xrays(
    files: List[UploadFile] = File(...),
    ml_service: MLService = Depends(get_ml_service)
):
    """
    Analyze multiple X-ray images in batch
    """
    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed per batch")
    
    results = []
    
    for file in files:
        try:
            # Validate each file
            if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
                results.append(AnalysisResponse(
                    success=False,
                    analysis=None,
                    message=f"Invalid file type for {file.filename}"
                ))
                continue
            
            file_content = await file.read()
            if len(file_content) > settings.MAX_FILE_SIZE:
                results.append(AnalysisResponse(
                    success=False,
                    analysis=None,
                    message=f"File {file.filename} too large"
                ))
                continue
            
            # Analyze image
            analysis_result = await ml_service.predict_lung_disease(file_content)
            
            # Save to Firebase (optional for batch)
            try:
                await firebase_service.save_analysis(analysis_result)
            except Exception as e:
                print(f"Warning: Failed to save batch analysis to Firebase: {e}")
            
            results.append(AnalysisResponse(
                success=True,
                analysis=analysis_result,
                message=f"Analysis completed for {file.filename}"
            ))
            
        except Exception as e:
            results.append(AnalysisResponse(
                success=False,
                analysis=None,
                message=f"Failed to analyze {file.filename}: {str(e)}"
            ))
    
    return results

@router.get("/history/{analysis_id}")
async def get_analysis_history(analysis_id: str):
    """
    Get analysis history by ID from Firebase
    """
    try:
        analysis_data = await firebase_service.get_analysis(analysis_id)
        if analysis_data:
            return {
                "success": True,
                "analysis": analysis_data,
                "message": "Analysis retrieved successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Analysis not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analysis: {str(e)}")

@router.get("/supported-formats")
async def get_supported_formats():
    """
    Get supported image formats and file size limits
    """
    return {
        "supported_formats": settings.ALLOWED_IMAGE_TYPES,
        "max_file_size_mb": settings.MAX_FILE_SIZE / (1024 * 1024),
        "max_batch_size": 10,
        "confidence_threshold": settings.CONFIDENCE_THRESHOLD,
        "firebase_enabled": True
    } 