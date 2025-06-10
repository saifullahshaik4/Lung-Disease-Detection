import numpy as np
import tensorflow as tf
from PIL import Image
import io
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import asyncio

from ..models.schemas import (
    PredictionResult, 
    AnalysisResult, 
    DiseaseType, 
    SeverityLevel
)
from ..core.config import settings

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.model = None
        self.is_loaded = False
        self.class_names = [
            DiseaseType.NORMAL,
            DiseaseType.PNEUMONIA,
            DiseaseType.TUBERCULOSIS,
            DiseaseType.LUNG_CANCER,
            DiseaseType.COVID19
        ]
        
    async def load_models(self):
        """Load ML models - For now using mock implementation"""
        try:
            # In production, you would load actual models like:
            # self.model = tf.keras.models.load_model(f"{settings.MODEL_PATH}/lung_disease_model.h5")
            
            # Mock implementation for demonstration
            logger.info("Loading ML models...")
            await asyncio.sleep(1)  # Simulate loading time
            self.is_loaded = True
            logger.info("✅ ML models loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load ML models: {str(e)}")
            raise
    
    def preprocess_image(self, image_data: bytes) -> np.ndarray:
        """Preprocess X-ray image for ML model"""
        try:
            # Open image using PIL
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to model input size (typically 224x224 for medical imaging)
            image = image.resize((224, 224))
            
            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            logger.error(f"Image preprocessing failed: {str(e)}")
            raise ValueError(f"Invalid image format: {str(e)}")
    
    async def predict_lung_disease(self, image_data: bytes, patient_info: Optional[Dict] = None) -> AnalysisResult:
        """Perform lung disease prediction on X-ray image"""
        if not self.is_loaded:
            raise RuntimeError("ML models not loaded")
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_data)
            
            # Mock prediction - In production, use actual model
            predictions = await self._mock_prediction(processed_image, patient_info)
            
            # Generate analysis result
            analysis_id = str(uuid.uuid4())
            
            return AnalysisResult(
                id=analysis_id,
                predictions=predictions,
                top_prediction=max(predictions, key=lambda x: x.confidence),
                confidence_score=max(pred.confidence for pred in predictions),
                recommendations=self._generate_recommendations(predictions, patient_info),
                severity_assessment=self._assess_severity(predictions),
                requires_immediate_attention=self._check_urgent_care(predictions),
                analysis_timestamp=datetime.now(),
                image_path=None  # Would be set after saving image
            )
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
    
    async def _mock_prediction(self, image_array: np.ndarray, patient_info: Optional[Dict] = None) -> List[PredictionResult]:
        """Mock prediction for demonstration - Replace with actual model inference"""
        # Simulate inference time
        await asyncio.sleep(0.5)
        
        # Generate realistic mock predictions
        np.random.seed(42)  # For consistent results
        raw_predictions = np.random.dirichlet([1, 2, 1, 1, 1.5])  # Slightly favor pneumonia
        
        predictions = []
        for i, (class_name, prob) in enumerate(zip(self.class_names, raw_predictions)):
            predictions.append(PredictionResult(
                disease_type=class_name,
                confidence=float(prob),
                probability=float(prob)
            ))
        
        # Sort by confidence
        predictions.sort(key=lambda x: x.confidence, reverse=True)
        return predictions
    
    def _generate_recommendations(self, predictions: List[PredictionResult], patient_info: Optional[Dict] = None) -> List[str]:
        """Generate medical recommendations based on predictions"""
        top_prediction = max(predictions, key=lambda x: x.confidence)
        recommendations = []
        
        if top_prediction.disease_type == DiseaseType.NORMAL:
            recommendations = [
                "Your chest X-ray appears normal.",
                "Continue regular health checkups.",
                "Maintain a healthy lifestyle with regular exercise."
            ]
        elif top_prediction.disease_type == DiseaseType.PNEUMONIA:
            recommendations = [
                "Possible pneumonia detected. Seek immediate medical attention.",
                "Complete rest and increased fluid intake recommended.",
                "Follow up with pulmonary function tests.",
                "Consider antibiotic treatment as prescribed by physician."
            ]
        elif top_prediction.disease_type == DiseaseType.TUBERCULOSIS:
            recommendations = [
                "TB screening required. Contact healthcare provider immediately.",
                "Isolate until medical clearance is obtained.",
                "Complete TB testing including sputum analysis.",
                "Follow strict medication compliance if diagnosed."
            ]
        elif top_prediction.disease_type == DiseaseType.LUNG_CANCER:
            recommendations = [
                "Abnormal findings require immediate oncology consultation.",
                "Additional imaging (CT scan) recommended.",
                "Biopsy may be necessary for definitive diagnosis.",
                "Discuss treatment options with oncology specialist."
            ]
        elif top_prediction.disease_type == DiseaseType.COVID19:
            recommendations = [
                "COVID-19 features detected. Get PCR test immediately.",
                "Self-isolate and monitor symptoms closely.",
                "Contact healthcare provider for guidance.",
                "Monitor oxygen saturation levels."
            ]
        
        # Add general recommendations
        if top_prediction.confidence < settings.CONFIDENCE_THRESHOLD:
            recommendations.append("Low confidence prediction - seek professional medical opinion.")
        
        return recommendations
    
    def _assess_severity(self, predictions: List[PredictionResult]) -> SeverityLevel:
        """Assess severity based on predictions"""
        top_prediction = max(predictions, key=lambda x: x.confidence)
        
        if top_prediction.disease_type == DiseaseType.NORMAL:
            return SeverityLevel.LOW
        elif top_prediction.disease_type in [DiseaseType.PNEUMONIA, DiseaseType.COVID19]:
            return SeverityLevel.MODERATE if top_prediction.confidence < 0.8 else SeverityLevel.HIGH
        elif top_prediction.disease_type in [DiseaseType.TUBERCULOSIS, DiseaseType.LUNG_CANCER]:
            return SeverityLevel.HIGH if top_prediction.confidence < 0.9 else SeverityLevel.CRITICAL
        
        return SeverityLevel.MODERATE
    
    def _check_urgent_care(self, predictions: List[PredictionResult]) -> bool:
        """Check if immediate medical attention is required"""
        top_prediction = max(predictions, key=lambda x: x.confidence)
        
        urgent_conditions = [
            DiseaseType.TUBERCULOSIS,
            DiseaseType.LUNG_CANCER
        ]
        
        moderate_urgent = [
            DiseaseType.PNEUMONIA,
            DiseaseType.COVID19
        ]
        
        if top_prediction.disease_type in urgent_conditions:
            return True
        elif top_prediction.disease_type in moderate_urgent and top_prediction.confidence > 0.8:
            return True
        
        return False
    
    async def batch_analyze(self, image_data_list: List[bytes]) -> List[AnalysisResult]:
        """Analyze multiple X-ray images concurrently"""
        tasks = [self.predict_lung_disease(img_data) for img_data in image_data_list]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log errors
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch analysis failed for image {i}: {str(result)}")
            else:
                valid_results.append(result)
        
        return valid_results