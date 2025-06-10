# Firebase Setup Instructions

## Step 1: Get Firebase Service Account Key

1. Go to your Firebase Console: https://console.firebase.google.com/
2. Select your project: **lungdiseasedetection-19b4f**
3. Click on the gear icon (Settings) → **Project settings**
4. Go to the **Service accounts** tab
5. Click **Generate new private key**
6. Download the JSON file and rename it to `firebase-credentials.json`
7. Place it in your `backend/` directory

## Step 2: Set Up Environment File

1. Rename `env.firebase` to `.env`:
   ```bash
   cd backend
   mv env.firebase .env
   ```

2. Update the `.env` file with your actual values:
   ```env
   # Firebase Configuration
   FIREBASE_PROJECT_ID=lungdiseasedetection-19b4f
   FIREBASE_CREDENTIALS_PATH=firebase-credentials.json

   # API Settings
   SECRET_KEY=your-actual-secret-key-here
   DEBUG=True

   # CORS Settings (for Next.js frontend)
   ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

   # File Upload Settings
   MAX_FILE_SIZE=10485760  # 10MB in bytes

   # ML Model Settings
   CONFIDENCE_THRESHOLD=0.7

   # Logging
   LOG_LEVEL=INFO
   ```

## Step 3: Install Firebase Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Test Firebase Connection

Run the backend server:
```bash
python start.py
```

The server will automatically:
- Connect to your Firestore database
- Create sample disease data if the database is empty
- Initialize all necessary collections

## Security Notes

- **NEVER** commit `firebase-credentials.json` to version control
- Add `firebase-credentials.json` to your `.gitignore` file
- For production deployment, use environment variables or cloud secret management

## Firestore Collections Structure

The backend will create these collections:

### `diseases` collection
```json
{
  "id": 1,
  "name": "Pneumonia",
  "description": "...",
  "severity": "high",
  "symptoms": [...],
  "treatment": "...",
  "risk_factors": [...],
  "prevention": [...],
  "created_at": "timestamp"
}
```

### `analyses` collection
```json
{
  "id": "uuid",
  "predictions": [...],
  "top_prediction": {...},
  "confidence_score": 0.85,
  "recommendations": [...],
  "severity_assessment": "high",
  "requires_immediate_attention": true,
  "analysis_timestamp": "timestamp",
  "image_path": "uploads/...",
  "created_at": "timestamp"
}
``` 