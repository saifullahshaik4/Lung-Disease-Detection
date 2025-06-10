import firebase_admin
from firebase_admin import credentials, firestore
from typing import List, Optional, Dict, Any
import os
import logging
from datetime import datetime

from ..core.config import settings
from ..models.schemas import Disease, AnalysisResult, SeverityLevel

logger = logging.getLogger(__name__)

class FirebaseService:
    def __init__(self):
        self.db = None
        self.app = None
        
    async def initialize(self):
        """Initialize Firebase connection"""
        try:
            # Check if Firebase app is already initialized
            if not firebase_admin._apps:
                # Initialize Firebase
                if os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
                    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                    self.app = firebase_admin.initialize_app(cred, {
                        'projectId': settings.FIREBASE_PROJECT_ID,
                    })
                else:
                    # Use default credentials (for deployment)
                    self.app = firebase_admin.initialize_app()
                
                logger.info("✅ Firebase initialized successfully")
            else:
                self.app = firebase_admin.get_app()
                logger.info("✅ Using existing Firebase app")
            
            # Get Firestore client
            self.db = firestore.client()
            
            # Initialize collections if they don't exist
            await self._initialize_collections()
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Firebase: {str(e)}")
            raise
    
    async def _initialize_collections(self):
        """Initialize Firestore collections with sample data if empty"""
        try:
            # Check if diseases collection exists and has data
            diseases_ref = self.db.collection('diseases')
            diseases = diseases_ref.limit(1).get()
            
            if not diseases:
                logger.info("📝 Initializing diseases collection...")
                await self._create_sample_diseases()
                
        except Exception as e:
            logger.error(f"Failed to initialize collections: {str(e)}")
    
    async def _create_sample_diseases(self):
        """Create sample diseases in Firestore"""
        sample_diseases = [
            {
                'id': 1,
                'name': 'Pneumonia',
                'description': 'Pneumonia is an infection that inflames air sacs in one or both lungs. The air sacs may fill with fluid or pus, causing cough with phlegm or pus, fever, chills, and difficulty breathing.',
                'severity': 'high',
                'symptoms': [
                    'Chest pain when breathing or coughing',
                    'Confusion or changes in mental awareness',
                    'Cough with phlegm',
                    'Fatigue',
                    'Fever, sweating and shaking chills',
                    'Lower than normal body temperature',
                    'Nausea, vomiting or diarrhea',
                    'Shortness of breath'
                ],
                'treatment': 'Antibiotics, rest, fluids, and over-the-counter pain relievers. Severe cases may require hospitalization.',
                'image_url': '/images/pneumonia.jpg',
                'risk_factors': [
                    'Age under 2 or over 65',
                    'Chronic illness',
                    'Smoking',
                    'Weakened immune system',
                    'Recent respiratory infection'
                ],
                'prevention': [
                    'Get vaccinated',
                    'Practice good hygiene',
                    'Don\'t smoke',
                    'Keep your immune system strong'
                ],
                'created_at': firestore.SERVER_TIMESTAMP
            },
            {
                'id': 2,
                'name': 'Tuberculosis',
                'description': 'Tuberculosis (TB) is a potentially serious infectious disease that mainly affects your lungs. The bacteria that cause tuberculosis are spread from person to person through tiny droplets released into the air via coughs and sneezes.',
                'severity': 'critical',
                'symptoms': [
                    'Coughing for three or more weeks',
                    'Coughing up blood or mucus',
                    'Chest pain',
                    'Pain with breathing or coughing',
                    'Unintentional weight loss',
                    'Fatigue',
                    'Fever',
                    'Night sweats',
                    'Chills',
                    'Loss of appetite'
                ],
                'treatment': 'Long-term antibiotic treatment (6-9 months). Multiple drugs are used to prevent resistance.',
                'image_url': '/images/tuberculosis.jpg',
                'risk_factors': [
                    'Weakened immune system',
                    'HIV infection',
                    'Diabetes',
                    'Severe kidney disease',
                    'Certain cancers',
                    'Malnutrition',
                    'Close contact with infected person'
                ],
                'prevention': [
                    'BCG vaccine (in some countries)',
                    'Avoid close contact with TB patients',
                    'Maintain good ventilation',
                    'Treat latent TB infection'
                ],
                'created_at': firestore.SERVER_TIMESTAMP
            },
            {
                'id': 3,
                'name': 'Lung Cancer',
                'description': 'Lung cancer is a type of cancer that begins in the lungs. It\'s the leading cause of cancer deaths worldwide. Smoking is the primary risk factor, but non-smokers can also develop lung cancer.',
                'severity': 'critical',
                'symptoms': [
                    'A new cough that doesn\'t go away',
                    'Coughing up blood',
                    'Shortness of breath',
                    'Chest pain',
                    'Hoarseness',
                    'Losing weight without trying',
                    'Bone pain',
                    'Headache'
                ],
                'treatment': 'Treatment depends on type and stage. Options include surgery, chemotherapy, radiation therapy, targeted therapy, and immunotherapy.',
                'image_url': '/images/lung_cancer.jpg',
                'risk_factors': [
                    'Smoking',
                    'Secondhand smoke',
                    'Radon gas exposure',
                    'Asbestos exposure',
                    'Family history',
                    'Air pollution',
                    'Previous radiation therapy'
                ],
                'prevention': [
                    'Don\'t smoke',
                    'Avoid secondhand smoke',
                    'Test home for radon',
                    'Avoid carcinogens at work',
                    'Eat healthy diet',
                    'Exercise regularly'
                ],
                'created_at': firestore.SERVER_TIMESTAMP
            },
            {
                'id': 4,
                'name': 'COVID-19',
                'description': 'COVID-19 is a respiratory illness caused by SARS-CoV-2 virus. It can cause severe pneumonia and respiratory failure in some patients, particularly those with underlying health conditions.',
                'severity': 'moderate',
                'symptoms': [
                    'Fever or chills',
                    'Cough',
                    'Shortness of breath',
                    'Fatigue',
                    'Muscle or body aches',
                    'Headache',
                    'Loss of taste or smell',
                    'Sore throat',
                    'Congestion or runny nose',
                    'Nausea or vomiting',
                    'Diarrhea'
                ],
                'treatment': 'Supportive care including rest, fluids, and fever reducers. Severe cases may require hospitalization and oxygen therapy.',
                'image_url': '/images/covid19.jpg',
                'risk_factors': [
                    'Age 65 and older',
                    'Chronic medical conditions',
                    'Immunocompromised state',
                    'Obesity',
                    'Pregnancy',
                    'Smoking'
                ],
                'prevention': [
                    'Get vaccinated',
                    'Wear masks in crowded areas',
                    'Maintain social distance',
                    'Wash hands frequently',
                    'Avoid large gatherings'
                ],
                'created_at': firestore.SERVER_TIMESTAMP
            }
        ]
        
        for disease_data in sample_diseases:
            self.db.collection('diseases').document(f"disease_{disease_data['id']}").set(disease_data)
        
        logger.info(f"✅ Created {len(sample_diseases)} sample diseases in Firestore")
    
    # Disease operations
    async def get_all_diseases(self) -> List[Dict]:
        """Get all diseases from Firestore"""
        try:
            diseases_ref = self.db.collection('diseases')
            docs = diseases_ref.stream()
            
            diseases = []
            for doc in docs:
                disease_data = doc.to_dict()
                disease_data['firestore_id'] = doc.id
                diseases.append(disease_data)
            
            return diseases
        except Exception as e:
            logger.error(f"Failed to get diseases: {str(e)}")
            return []
    
    async def get_disease_by_name(self, name: str) -> Optional[Dict]:
        """Get disease by name from Firestore"""
        try:
            diseases_ref = self.db.collection('diseases')
            query = diseases_ref.where('name', '==', name).limit(1)
            docs = list(query.stream())
            
            if docs:
                disease_data = docs[0].to_dict()
                disease_data['firestore_id'] = docs[0].id
                return disease_data
            
            return None
        except Exception as e:
            logger.error(f"Failed to get disease by name: {str(e)}")
            return None
    
    async def search_diseases(self, query: str) -> List[Dict]:
        """Search diseases by name or symptoms"""
        try:
            diseases = await self.get_all_diseases()
            query_lower = query.lower()
            
            matching_diseases = []
            for disease in diseases:
                # Check name match
                if query_lower in disease.get('name', '').lower():
                    matching_diseases.append(disease)
                    continue
                
                # Check description match
                if query_lower in disease.get('description', '').lower():
                    matching_diseases.append(disease)
                    continue
                
                # Check symptoms match
                symptoms = disease.get('symptoms', [])
                for symptom in symptoms:
                    if query_lower in symptom.lower():
                        matching_diseases.append(disease)
                        break
            
            return matching_diseases
        except Exception as e:
            logger.error(f"Failed to search diseases: {str(e)}")
            return []
    
    # Analysis operations
    async def save_analysis(self, analysis: AnalysisResult) -> str:
        """Save analysis result to Firestore"""
        try:
            analysis_data = {
                'id': analysis.id,
                'predictions': [pred.dict() for pred in analysis.predictions],
                'top_prediction': analysis.top_prediction.dict(),
                'confidence_score': analysis.confidence_score,
                'recommendations': analysis.recommendations,
                'severity_assessment': analysis.severity_assessment.value,
                'requires_immediate_attention': analysis.requires_immediate_attention,
                'analysis_timestamp': analysis.analysis_timestamp,
                'image_path': analysis.image_path,
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = self.db.collection('analyses').document(analysis.id)
            doc_ref.set(analysis_data)
            
            logger.info(f"✅ Saved analysis {analysis.id} to Firestore")
            return analysis.id
        except Exception as e:
            logger.error(f"Failed to save analysis: {str(e)}")
            raise
    
    async def get_analysis(self, analysis_id: str) -> Optional[Dict]:
        """Get analysis by ID from Firestore"""
        try:
            doc_ref = self.db.collection('analyses').document(analysis_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            
            return None
        except Exception as e:
            logger.error(f"Failed to get analysis: {str(e)}")
            return None

# Global Firebase service instance
firebase_service = FirebaseService() 