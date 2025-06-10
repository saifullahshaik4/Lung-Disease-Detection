from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..models.schemas import (
    SymptomAnalysisRequest, 
    SymptomAnalysisResponse, 
    SymptomMatch,
    Disease
)
from ..services.disease_service import DiseaseService

router = APIRouter()

# Dependency to get disease service
def get_disease_service() -> DiseaseService:
    return DiseaseService()

@router.post("/match", response_model=SymptomAnalysisResponse)
async def match_symptoms_to_diseases(
    request: SymptomAnalysisRequest,
    disease_service: DiseaseService = Depends(get_disease_service)
):
    """
    Match patient symptoms to possible diseases
    """
    if not request.symptoms:
        raise HTTPException(status_code=400, detail="At least one symptom is required")
    
    # Get symptom matches
    symptom_matches_data = await disease_service.match_symptoms_to_diseases(request.symptoms)
    
    # Convert to SymptomMatch objects
    symptom_matches = []
    all_matching_diseases = set()
    
    for match_data in symptom_matches_data:
        symptom_match = SymptomMatch(
            symptom=match_data["symptom"],
            diseases=match_data["matching_diseases"],
            match_score=min(1.0, match_data["match_count"] / 4.0)  # Normalize to 0-1 scale
        )
        symptom_matches.append(symptom_match)
        all_matching_diseases.update(match_data["matching_diseases"])
    
    # Get disease details for matched diseases
    suggested_diseases = []
    for disease_name in all_matching_diseases:
        disease = await disease_service.get_disease_by_name(disease_name)
        if disease:
            suggested_diseases.append(disease)
    
    # Sort diseases by how many symptoms they match
    disease_match_scores = {}
    for disease in suggested_diseases:
        score = 0
        for symptom in request.symptoms:
            for disease_symptom in disease.symptoms:
                if symptom.lower() in disease_symptom.lower() or disease_symptom.lower() in symptom.lower():
                    score += 1
                    break
        disease_match_scores[disease.name] = score
    
    # Sort by match score
    suggested_diseases.sort(key=lambda d: disease_match_scores.get(d.name, 0), reverse=True)
    
    # Generate recommendations
    recommendations = _generate_symptom_recommendations(request.symptoms, suggested_diseases, request.age)
    
    return SymptomAnalysisResponse(
        matches=symptom_matches,
        suggested_diseases=suggested_diseases,
        recommendations=recommendations
    )

@router.get("/common-symptoms")
async def get_common_symptoms():
    """
    Get list of common lung disease symptoms
    """
    common_symptoms = [
        "Chest pain",
        "Shortness of breath",
        "Persistent cough",
        "Coughing up blood",
        "Fatigue",
        "Fever",
        "Night sweats",
        "Unexplained weight loss",
        "Wheezing",
        "Difficulty breathing",
        "Chest tightness",
        "Loss of appetite",
        "Chills",
        "Hoarseness",
        "Rapid breathing"
    ]
    
    return {
        "common_symptoms": common_symptoms,
        "total_count": len(common_symptoms),
        "note": "These are common symptoms associated with lung diseases. Always consult a healthcare professional for proper diagnosis."
    }

@router.get("/symptom-categories")
async def get_symptom_categories():
    """
    Get symptoms organized by categories
    """
    categories = {
        "respiratory": [
            "Shortness of breath",
            "Persistent cough",
            "Wheezing",
            "Rapid breathing",
            "Difficulty breathing"
        ],
        "pain_discomfort": [
            "Chest pain",
            "Chest tightness",
            "Pain when breathing",
            "Pain when coughing"
        ],
        "systemic": [
            "Fever",
            "Fatigue",
            "Night sweats",
            "Chills",
            "Unexplained weight loss",
            "Loss of appetite"
        ],
        "concerning": [
            "Coughing up blood",
            "Severe chest pain",
            "Extreme shortness of breath",
            "High fever with breathing difficulty"
        ]
    }
    
    return {
        "symptom_categories": categories,
        "emergency_note": "If experiencing 'concerning' symptoms, seek immediate medical attention"
    }

def _generate_symptom_recommendations(symptoms: List[str], diseases: List[Disease], age: int = None) -> List[str]:
    """Generate recommendations based on symptoms and matched diseases"""
    recommendations = []
    
    # Check for emergency symptoms
    emergency_symptoms = [
        "coughing up blood", "severe chest pain", "extreme shortness of breath",
        "high fever", "difficulty breathing", "blood in cough"
    ]
    
    has_emergency = any(
        any(emergency in symptom.lower() for emergency in emergency_symptoms)
        for symptom in symptoms
    )
    
    if has_emergency:
        recommendations.append("⚠️ URGENT: Seek immediate medical attention due to concerning symptoms")
        recommendations.append("Visit emergency room or call emergency services")
    
    # General recommendations
    if len(symptoms) >= 3:
        recommendations.append("Multiple symptoms detected - schedule appointment with healthcare provider")
    
    if diseases:
        top_disease = diseases[0]
        if top_disease.severity.value in ["high", "critical"]:
            recommendations.append(f"Symptoms may indicate {top_disease.name} - requires medical evaluation")
    
    # Age-specific recommendations
    if age:
        if age >= 65:
            recommendations.append("Age 65+ increases risk - prioritize medical consultation")
        elif age <= 5:
            recommendations.append("Young children require immediate pediatric evaluation")
    
    # General health advice
    recommendations.extend([
        "Monitor symptoms and track any changes",
        "Maintain good hygiene practices",
        "Get adequate rest and stay hydrated",
        "Avoid smoking and secondhand smoke"
    ])
    
    return recommendations 