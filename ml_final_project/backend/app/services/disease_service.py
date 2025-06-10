from typing import List, Optional, Dict
from datetime import datetime

from ..models.schemas import Disease, DiseaseCreate, DiseaseType, SeverityLevel
from .firebase_service import firebase_service

class DiseaseService:
    def __init__(self):
        pass
    
    def _convert_firestore_to_disease(self, firestore_data: Dict) -> Disease:
        """Convert Firestore document to Disease model"""
        return Disease(
            id=firestore_data.get('id', 0),
            name=firestore_data.get('name', ''),
            description=firestore_data.get('description', ''),
            severity=SeverityLevel(firestore_data.get('severity', 'moderate')),
            symptoms=firestore_data.get('symptoms', []),
            treatment=firestore_data.get('treatment'),
            image_url=firestore_data.get('image_url'),
            risk_factors=firestore_data.get('risk_factors', []),
            prevention=firestore_data.get('prevention', []),
            created_at=datetime.now()  # Firestore timestamp conversion would be more complex
        )
    
    async def get_all_diseases(self) -> List[Disease]:
        """Get all diseases from Firebase"""
        firestore_diseases = await firebase_service.get_all_diseases()
        return [self._convert_firestore_to_disease(disease_data) for disease_data in firestore_diseases]
    
    async def get_disease_by_id(self, disease_id: int) -> Optional[Disease]:
        """Get disease by ID from Firebase"""
        firestore_diseases = await firebase_service.get_all_diseases()
        for disease_data in firestore_diseases:
            if disease_data.get('id') == disease_id:
                return self._convert_firestore_to_disease(disease_data)
        return None
    
    async def get_disease_by_name(self, name: str) -> Optional[Disease]:
        """Get disease by name from Firebase"""
        disease_data = await firebase_service.get_disease_by_name(name)
        if disease_data:
            return self._convert_firestore_to_disease(disease_data)
        return None
    
    async def search_diseases(self, query: str) -> List[Disease]:
        """Search diseases by name or symptoms in Firebase"""
        firestore_diseases = await firebase_service.search_diseases(query)
        return [self._convert_firestore_to_disease(disease_data) for disease_data in firestore_diseases]
    
    async def get_diseases_by_severity(self, severity: SeverityLevel) -> List[Disease]:
        """Get diseases by severity level from Firebase"""
        all_diseases = await self.get_all_diseases()
        return [disease for disease in all_diseases if disease.severity == severity]
    
    async def match_symptoms_to_diseases(self, symptoms: List[str]) -> List[Dict]:
        """Match symptoms to possible diseases using Firebase data"""
        all_diseases = await self.get_all_diseases()
        symptom_matches = []
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            matching_diseases = []
            
            for disease in all_diseases:
                for disease_symptom in disease.symptoms:
                    if symptom_lower in disease_symptom.lower() or disease_symptom.lower() in symptom_lower:
                        matching_diseases.append(disease.name)
                        break
            
            if matching_diseases:
                symptom_matches.append({
                    "symptom": symptom,
                    "matching_diseases": matching_diseases,
                    "match_count": len(matching_diseases)
                })
        
        return symptom_matches
    
    async def get_disease_recommendations(self, disease_name: str) -> Dict:
        """Get treatment recommendations for a disease from Firebase"""
        disease = await self.get_disease_by_name(disease_name)
        if not disease:
            return {}
        
        return {
            "disease": disease.name,
            "treatment": disease.treatment,
            "prevention": disease.prevention,
            "risk_factors": disease.risk_factors,
            "severity": disease.severity.value,
            "urgent_care_needed": disease.severity in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]
        } 