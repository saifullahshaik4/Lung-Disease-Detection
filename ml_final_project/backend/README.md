# Lung Disease Detection API Backend

FastAPI backend for AI-powered lung disease detection and analysis system.

## Features

- 🧠 **ML-Powered Analysis**: AI-based X-ray image analysis for lung disease detection
- 📋 **Disease Information**: Comprehensive database of lung diseases and symptoms  
- 🔍 **Symptom Matching**: Match patient symptoms to possible conditions
- 📤 **File Upload**: Support for multiple image formats with validation
- 🔄 **Batch Processing**: Analyze multiple X-ray images simultaneously
- 📊 **Detailed Results**: Confidence scores, recommendations, and severity assessment
- 🌐 **CORS Enabled**: Ready for frontend integration
- 📚 **Auto Documentation**: Interactive API docs with Swagger UI

## Supported Diseases

- Pneumonia
- Tuberculosis (TB)
- Lung Cancer
- COVID-19
- Normal (healthy lungs)

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configurations
   ```

4. **Start the server:**
   ```bash
   python start.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API:**
   - **API Server**: http://localhost:8000
   - **Interactive Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

6. **Test the API:**
   ```bash
   python test_api.py
   ```

## API Endpoints

### Analysis Endpoints
- `POST /api/analysis/upload-xray` - Analyze single X-ray image
- `POST /api/analysis/batch-analyze` - Analyze multiple X-ray images
- `GET /api/analysis/history/{analysis_id}` - Get analysis history
- `GET /api/analysis/supported-formats` - Get supported file formats

### Disease Endpoints
- `GET /api/diseases/` - Get all diseases
- `GET /api/diseases/{disease_id}` - Get disease by ID
- `GET /api/diseases/name/{disease_name}` - Get disease by name
- `GET /api/diseases/search/?q={query}` - Search diseases
- `GET /api/diseases/severity/{severity_level}` - Get diseases by severity
- `GET /api/diseases/recommendations/{disease_name}` - Get treatment recommendations

### Symptom Endpoints
- `POST /api/symptoms/match` - Match symptoms to diseases
- `GET /api/symptoms/common-symptoms` - Get common lung disease symptoms
- `GET /api/symptoms/symptom-categories` - Get symptoms by categories

### User Endpoints (Basic)
- `POST /api/users/register` - Register new user
- `GET /api/users/profile/{user_id}` - Get user profile
- `GET /api/users/history/{user_id}` - Get user analysis history

## Usage Examples

### Analyze X-ray Image

```bash
curl -X POST "http://localhost:8000/api/analysis/upload-xray" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@chest_xray.jpg" \
  -F "patient_age=45" \
  -F "patient_gender=male" \
  -F "symptoms=chest pain,shortness of breath"
```

### Match Symptoms

```bash
curl -X POST "http://localhost:8000/api/symptoms/match" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["chest pain", "persistent cough", "fever"],
    "age": 45,
    "gender": "male"
  }'
```

### Search Diseases

```bash
curl "http://localhost:8000/api/diseases/search/?q=cough"
```

## Configuration Options

Environment variables can be set in `.env` file:

```env
# API Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# CORS Settings  
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=uploads

# ML Model Settings
MODEL_PATH=app/models
CONFIDENCE_THRESHOLD=0.7

# Database
DATABASE_URL=sqlite:///./lung_disease.db
```

## File Upload Specifications

- **Supported Formats**: JPEG, JPG, PNG, BMP, TIFF
- **Maximum File Size**: 10MB per file
- **Batch Limit**: 10 files per batch request
- **Image Requirements**: Chest X-ray images for best results

## Response Format

### Analysis Response
```json
{
  "success": true,
  "analysis": {
    "id": "uuid-string",
    "predictions": [
      {
        "disease_type": "pneumonia",
        "confidence": 0.85,
        "probability": 0.85
      }
    ],
    "top_prediction": {
      "disease_type": "pneumonia", 
      "confidence": 0.85,
      "probability": 0.85
    },
    "confidence_score": 0.85,
    "recommendations": [
      "Possible pneumonia detected. Seek immediate medical attention.",
      "Complete rest and increased fluid intake recommended."
    ],
    "severity_assessment": "high",
    "requires_immediate_attention": true,
    "analysis_timestamp": "2024-01-01T00:00:00Z"
  },
  "message": "X-ray analysis completed successfully"
}
```

## Development

### Project Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/
│   │   └── config.py        # Configuration settings
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── routers/
│   │   ├── analysis.py      # X-ray analysis endpoints
│   │   ├── diseases.py      # Disease information endpoints
│   │   ├── symptoms.py      # Symptom matching endpoints
│   │   └── users.py         # User management endpoints
│   └── services/
│       ├── ml_service.py    # ML model integration
│       └── disease_service.py # Disease data service
├── uploads/                 # File upload directory
├── requirements.txt         # Python dependencies
├── start.py                # Server startup script
├── test_api.py             # API testing script
└── README.md               # This file
```

### Adding Real ML Models

To integrate actual ML models:

1. **Save your trained model** in `app/models/` directory
2. **Update `ml_service.py`**:
   ```python
   async def load_models(self):
       self.model = tf.keras.models.load_model("app/models/your_model.h5")
       self.is_loaded = True
   ```
3. **Replace mock predictions** with actual inference

### Database Integration

For production, replace mock data with actual database:

1. **Install database dependencies** (PostgreSQL, MySQL, etc.)
2. **Update `DATABASE_URL`** in configuration
3. **Create database models** using SQLAlchemy
4. **Implement CRUD operations** in services

## Health & Monitoring

- **Health Check**: `GET /health`
- **API Documentation**: `GET /docs`
- **Server Logs**: Structured logging with timestamp and level

## Security Considerations

- File upload validation and size limits
- CORS configuration for frontend integration
- Input validation using Pydantic models
- Environment-based configuration
- Secure file storage practices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Disclaimer

This is a demonstration/educational project. For production medical applications:
- Use validated ML models
- Implement proper security measures
- Follow medical data privacy regulations (HIPAA, GDPR)
- Get appropriate medical certifications
- Include proper medical disclaimers 