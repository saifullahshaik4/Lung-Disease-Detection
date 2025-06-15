import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.pipeline import Pipeline
import kagglehub
import joblib
import os
import glob

def load_and_preprocess_data():
    """Load and preprocess cancer dataset without data leakage"""
    print("Loading cancer dataset...")
    
    # Try different dataset names
    dataset_names = [
        "rishidamarla/cancer-patients-data",
        "thedevastator/cancer-patients-and-air-pollution-a-new-link",
        "rishidamarla/lung-cancer-data"
    ]
    
    path = None
    for dataset_name in dataset_names:
        try:
            print(f"Trying dataset: {dataset_name}")
            path = kagglehub.dataset_download(dataset_name)
            print(f"✅ Successfully downloaded: {dataset_name}")
            break
        except Exception as e:
            print(f"❌ Failed to download {dataset_name}: {str(e)}")
            continue
    
    if path is None:
        raise ValueError("Unable to download any of the specified datasets.")
    
    print(f"Dataset downloaded to: {path}")
    
    # Find data files
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    if not csv_files:
        all_files = glob.glob(os.path.join(path, "*"))
        print(f"Available files: {all_files}")
        data_files = [f for f in all_files if f.endswith(('.csv', '.xlsx', '.json', '.parquet'))]
        if data_files:
            csv_files = data_files
        else:
            raise ValueError("No supported data files found in the dataset")
    
    print(f"Found data files: {csv_files}")
    
    # Load the largest file
    if len(csv_files) > 1:
        data_file = max(csv_files, key=os.path.getsize)
    else:
        data_file = csv_files[0]
    
    print(f"Loading file: {data_file}")
    
    # Load with error handling
    try:
        if data_file.endswith('.csv'):
            df = pd.read_csv(data_file)
        elif data_file.endswith('.xlsx'):
            try:
                df = pd.read_excel(data_file)
            except ImportError:
                print("Installing openpyxl...")
                import subprocess
                subprocess.check_call(['pip', 'install', 'openpyxl'])
                df = pd.read_excel(data_file)
        else:
            df = pd.read_csv(data_file)
    except Exception as e:
        print(f"❌ Error loading {data_file}: {e}")
        raise e
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nFirst few rows:")
    print(df.head())
    
    return df

def preprocess_features(df):
    """Enhanced preprocessing WITHOUT data leakage"""
    print("\n🔧 PREPROCESSING WITHOUT DATA LEAKAGE...")
    print("="*50)
    
    # Make a copy
    df_processed = df.copy()
    
    # CRITICAL: Remove ID columns (data leakage!)
    id_columns = [col for col in df_processed.columns 
                  if 'id' in col.lower() or 'patient' in col.lower()]
    
    if id_columns:
        print(f"🚨 REMOVING ID COLUMNS (data leakage): {id_columns}")
        df_processed = df_processed.drop(columns=id_columns)
    
    # Handle missing values
    for col in df_processed.columns:
        if df_processed[col].dtype == 'object':
            df_processed[col] = df_processed[col].fillna(df_processed[col].mode()[0] if len(df_processed[col].mode()) > 0 else 'Unknown')
        else:
            df_processed[col] = df_processed[col].fillna(df_processed[col].median())
    
    # Identify target column
    target_candidates = ['target', 'label', 'cancer', 'diagnosis', 'result', 'outcome', 'level']
    target_col = None
    
    for col in df_processed.columns:
        col_lower = col.lower()
        if any(candidate in col_lower for candidate in target_candidates):
            target_col = col
            break
    
    if target_col is None:
        target_col = df_processed.columns[-1]
        print(f"No obvious target column found, using: {target_col}")
    
    print(f"Using target column: {target_col}")
    
    # Separate features and target
    X = df_processed.drop(columns=[target_col])
    y = df_processed[target_col]
    
    print(f"Features after ID removal: {list(X.columns)}")
    
    # Encode categorical variables in features
    label_encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le
    
    # Encode target if categorical
    target_encoder = None
    if y.dtype == 'object':
        target_encoder = LabelEncoder()
        y = target_encoder.fit_transform(y)
        print(f"Target classes: {target_encoder.classes_}")
    
    print(f"Features shape: {X.shape}")
    print(f"Target distribution:\n{pd.Series(y).value_counts()}")
    
    return X, y, label_encoders, target_encoder

def train_robust_model(X, y):
    """Train robust model with proper validation"""
    print("\n🚀 TRAINING ROBUST MODEL...")
    print("="*50)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create pipeline with scaling
    models_to_try = {
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=50,
            max_depth=4,
            learning_rate=0.1,
            random_state=42
        ),
        'Logistic Regression': LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced'
        )
    }
    
    best_model = None
    best_score = 0
    best_name = ""
    
    print("Testing different models with cross-validation...")
    
    for name, model in models_to_try.items():
        # Create pipeline
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', model)
        ])
        
        # Cross-validation
        cv_scores = cross_val_score(
            pipeline, X_train, y_train, 
            cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
            scoring='f1_macro'
        )
        
        mean_score = cv_scores.mean()
        std_score = cv_scores.std()
        
        print(f"{name}: {mean_score:.4f} (+/- {std_score*2:.4f})")
        
        if mean_score > best_score:
            best_score = mean_score
            best_model = pipeline
            best_name = name
    
    print(f"\n🏆 Best model: {best_name} (F1: {best_score:.4f})")
    
    # Train best model on full training set
    best_model.fit(X_train, y_train)
    
    # Predictions
    y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)
    
    # Evaluation
    print("\n" + "="*50)
    print("ROBUST MODEL EVALUATION - FIXED DATASET")
    print("="*50)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"F1-Score (macro): {f1_score(y_test, y_pred, average='macro'):.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Check prediction distribution
    pred_distribution = np.bincount(y_pred)
    print(f"\nPrediction distribution: {pred_distribution}")
    
    # Check confidence levels
    max_proba = y_pred_proba.max(axis=1)
    print(f"Average confidence: {max_proba.mean():.3f}")
    print(f"High confidence (>0.9): {(max_proba > 0.9).sum()}/{len(max_proba)}")
    
    # Sanity checks
    print(f"\n--- 🔍 SANITY CHECKS ---")
    unique_preds = len(np.unique(y_pred))
    unique_actual = len(np.unique(y_test))
    
    if unique_preds == unique_actual:
        print("✅ Model predicts all classes")
    else:
        print(f"⚠️  Model predicts {unique_preds}/{unique_actual} classes")
    
    if max_proba.mean() < 0.95:
        print("✅ Reasonable confidence levels")
    else:
        print("⚠️  Very high confidence - possible overfitting")
    
    return best_model, best_name

def main():
    """Main training pipeline"""
    print("🔧 TRAINING ROBUST CANCER MODEL (NO DATA LEAKAGE)")
    print("="*60)
    
    os.makedirs('models', exist_ok=True)
    
    try:
        # Load and preprocess data
        df = load_and_preprocess_data()
        X, y, label_encoders, target_encoder = preprocess_features(df)
        
        # Train model
        model, model_name = train_robust_model(X, y)
        
        # Save everything
        print("\nSaving robust model...")
        joblib.dump(model, 'models/cancer_model_fixed.pkl')
        joblib.dump(label_encoders, 'models/cancer_label_encoders_fixed.pkl')
        if target_encoder:
            joblib.dump(target_encoder, 'models/cancer_target_encoder_fixed.pkl')
        
        # Save training info
        with open('models/cancer_training_info_fixed.txt', 'w') as f:
            f.write(f"Model Type: {model_name}\n")
            f.write(f"Features: {list(X.columns)}\n")
            f.write(f"Dataset shape: {X.shape}\n")
            f.write("Data leakage prevention: ID columns removed\n")
        
        print("✅ Robust model training completed!")
        print("📁 Model saved to: models/cancer_model_fixed.pkl")
        print(f"📁 Best model: {model_name}")
        
    except Exception as e:
        print(f"❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()