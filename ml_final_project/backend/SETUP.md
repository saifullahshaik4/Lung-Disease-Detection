# 🔥 Firebase Backend Setup

## Quick Setup (5 minutes)

### 1. Get Firebase Credentials
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: **lungdiseasedetection-19b4f**
3. Go to Settings → Project settings → Service accounts
4. Click "Generate new private key"
5. Download the JSON file as `firebase-credentials.json`
6. Place it in the `backend/` folder

### 2. Setup Environment
```bash
cd backend
cp env.firebase .env
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Backend
```bash
python start.py
```

You should see:
```
🔥 Firebase connected successfully!
🚀 ML models loaded successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 5. Test It Works
```bash
python test_api.py
```

## What Changed?

✅ **Removed**: SQLite, JWT auth, password hashing (unnecessary)  
✅ **Added**: Firebase Firestore integration  
✅ **Kept**: ML service, file uploads, disease data, symptoms matching  

## File Structure
```
backend/
├── firebase-credentials.json  # ← Add this file
├── .env                      # ← Rename from env.firebase
├── app/
│   ├── services/
│   │   ├── firebase_service.py  # ← New Firebase integration
│   │   ├── ml_service.py        # ← Unchanged
│   │   └── disease_service.py   # ← Now uses Firebase
│   └── core/config.py           # ← Updated for Firebase
└── requirements.txt             # ← Updated dependencies
```

## Firebase Collections Created
- `diseases` - Disease information
- `analyses` - X-ray analysis results

The backend will automatically create sample data when you first run it!

## Security Note
Add to your `.gitignore`:
```
firebase-credentials.json
.env
``` 