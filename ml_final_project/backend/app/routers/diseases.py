from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional

from ..models.schemas import Disease, SeverityLevel
from ..services.disease_service import DiseaseService

router = APIRouter()

# Dependency to get disease service
def get_disease_service() -> DiseaseService:
    return DiseaseService()

@router.get("/", response_model=List[Disease])
async def get_all_diseases(
    disease_service: DiseaseService = Depends(get_disease_service)
):
    """
    Get all available diseases
    """
    return await disease_service.get_all_diseases()

@router.get("/{disease_id}", response_model=Disease)
async def get_disease_by_id(
    disease_id: int,
    disease_service: DiseaseService = Depends(get_disease_service)
):
    """
    Get disease information by ID
    """
    disease = await disease_service.get_disease_by_id(disease_id)
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease

@router.get("/name/{disease_name}", response_model=Disease)
async def get_disease_by_name(
    disease_name: str,
    disease_service: DiseaseService = Depends(get_disease_service)
):
    """
    Get disease information by name
    """
    disease = await disease_service.get_disease_by_name(disease_name)
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease

@router.get("/search/", response_model=List[Disease])
async def search_diseases(
    q: str = Query(..., description="Search query for diseases"),
    disease_service: DiseaseService = Depends(get_disease_service)
):
    """
    Search diseases by name, description, or symptoms
    """
    if len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
    
    diseases = await disease_service.search_diseases(q)
    return diseases

@router.get("/severity/{severity_level}", response_model=List[Disease])
async def get_diseases_by_severity(
    severity_level: SeverityLevel,
    disease_service: DiseaseService = Depends(get_disease_service)
):
    """
    Get diseases by severity level
    """
    diseases = await disease_service.get_diseases_by_severity(severity_level)
    return diseases

@router.get("/recommendations/{disease_name}")
async def get_disease_recommendations(
    disease_name: str,
    disease_service: DiseaseService = Depends(get_disease_service)
):
    """
    Get treatment recommendations for a specific disease
    """
    recommendations = await disease_service.get_disease_recommendations(disease_name)
    if not recommendations:
        raise HTTPException(status_code=404, detail="Disease not found")
    return recommendations

@router.get("/compare/symptoms")
async def compare_disease_symptoms(
    disease1: str = Query(..., description="First disease name"),
    disease2: str = Query(..., description="Second disease name"),
    disease_service: DiseaseService = Depends(get_disease_service)
):
    """
    Compare symptoms between two diseases
    """
    d1 = await disease_service.get_disease_by_name(disease1)
    d2 = await disease_service.get_disease_by_name(disease2)
    
    if not d1:
        raise HTTPException(status_code=404, detail=f"Disease '{disease1}' not found")
    if not d2:
        raise HTTPException(status_code=404, detail=f"Disease '{disease2}' not found")
    
    # Find common and unique symptoms
    symptoms1 = set(d1.symptoms)
    symptoms2 = set(d2.symptoms)
    
    common_symptoms = list(symptoms1.intersection(symptoms2))
    unique_to_disease1 = list(symptoms1 - symptoms2)
    unique_to_disease2 = list(symptoms2 - symptoms1)
    
    return {
        "disease1": {
            "name": d1.name,
            "total_symptoms": len(d1.symptoms),
            "unique_symptoms": unique_to_disease1
        },
        "disease2": {
            "name": d2.name,
            "total_symptoms": len(d2.symptoms),
            "unique_symptoms": unique_to_disease2
        },
        "common_symptoms": common_symptoms,
        "similarity_score": len(common_symptoms) / max(len(symptoms1), len(symptoms2))
    } 