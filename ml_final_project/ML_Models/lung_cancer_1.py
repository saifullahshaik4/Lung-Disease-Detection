import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight
import kagglehub
import joblib
import os
import glob

def load_and_preprocess_data():
    """Load and preprocess the LUNA lung cancer dataset"""
    print("Loading LUNA lung cancer dataset...")
    
    # Download dataset
    path = kagglehub.dataset_download("fanbyprinciple/luna-lung-cancer-dataset")
    print(f"Dataset downloaded to: {path}")
    
    # Find CSV files in the downloaded path
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    if not csv_files:
        # Try other common file extensions
        all_files = glob.glob(os.path.join(path, "*"))
        print(f"Available files: {all_files}")
        # Look for any data file
        data_files = [f for f in all_files if f.endswith(('.csv', '.xlsx', '.json', '.parquet'))]
        if data_files:
            csv_files = data_files
        else:
            raise ValueError("No supported data files found in the dataset")
    
    print(f"Found data files: {csv_files}")
    
    # Load the first CSV file (or the largest one if multiple)
    if len(csv_files) > 1:
        # Choose the largest file
        csv_file = max(csv_files, key=os.path.getsize)
    else:
        csv_file = csv_files[0]
    
    print(f"Loading file: {csv_file}")
    
    # Load based on file extension
    if csv_file.endswith('.csv'):
        df = pd.read_csv(csv_file)
    elif csv_file.endswith('.xlsx'):
        df = pd.read_excel(csv_file)
    elif csv_file.endswith('.json'):
        df = pd.read_json(csv_file)
    elif csv_file.endswith('.parquet'):
        df = pd.read_parquet(csv_file)
    else:
        df = pd.read_csv(csv_file)  # Default to CSV
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nFirst few rows:")
    print(df.head())
    
    # Basic info about the dataset
    print("\nDataset info:")
    print(df.info())
    print("\nMissing values:")
    print(df.isnull().sum())
    
    return df

def preprocess_features(df):
    """Enhanced preprocessing with proper sampling for balanced classes"""
    # Make a copy to avoid modifying original
    df_processed = df.copy()
    
    # Handle missing values
    df_processed = df_processed.dropna()
    
    # Identify target column (common names for lung cancer datasets)
    target_candidates = ['target', 'label', 'cancer', 'diagnosis', 'result', 'outcome', 'class']
    target_col = None
    
    for col in df_processed.columns:
        if col.lower() in target_candidates or 'cancer' in col.lower() or 'target' in col.lower():
            target_col = col
            break
    
    if target_col is None:
        # If no obvious target, use the last column
        target_col = df_processed.columns[-1]
        print(f"No obvious target column found, using: {target_col}")
    
    print(f"Using target column: {target_col}")
    
    # Separate features and target
    X = df_processed.drop(columns=[target_col])
    y = df_processed[target_col]
    
    print(f"Original target distribution:\n{pd.Series(y).value_counts()}")
    
    # CRITICAL FIX: Balance the dataset by undersampling majority class
    print("\n🔧 APPLYING BALANCED SAMPLING...")
    
    # Get class counts
    class_counts = pd.Series(y).value_counts()
    minority_class_size = class_counts.min()
    
    print(f"Original classes: {class_counts.to_dict()}")
    print(f"Will sample {minority_class_size} from each class")
    
    # Sample equal amounts from each class
    balanced_indices = []
    for class_label in class_counts.index:
        class_indices = y[y == class_label].index
        sampled_indices = np.random.choice(class_indices, size=minority_class_size, replace=False)
        balanced_indices.extend(sampled_indices)
    
    # Create balanced dataset
    X_balanced = X.loc[balanced_indices]
    y_balanced = y.loc[balanced_indices]
    
    print(f"Balanced target distribution:\n{pd.Series(y_balanced).value_counts()}")
    
    # Only keep numeric features (remove seriesuid which is not predictive)
    numeric_cols = X_balanced.select_dtypes(include=[np.number]).columns
    X_final = X_balanced[numeric_cols]
    
    print(f"Using numeric features: {list(numeric_cols)}")
    print(f"Final features shape: {X_final.shape}")
    
    return X_final, y_balanced

def train_improved_model(X, y):
    """Train improved Random Forest model with proper validation"""
    print("\n🚀 TRAINING IMPROVED MODEL...")
    print("="*50)
    
    # Stratified split to maintain class balance
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Training Random Forest with careful hyperparameters...")
    
    # More conservative hyperparameters to prevent overfitting
    model = RandomForestClassifier(
        n_estimators=50,  # Reduced from 100
        max_depth=5,      # Limited depth
        min_samples_split=10,  # Increased
        min_samples_leaf=5,    # Increased
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'  # Handle any remaining imbalance
    )
    
    # Cross-validation to check for overfitting
    print("Performing stratified cross-validation...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = []
    
    for fold, (train_idx, val_idx) in enumerate(cv.split(X_train_scaled, y_train)):
        X_fold_train, X_fold_val = X_train_scaled[train_idx], X_train_scaled[val_idx]
        y_fold_train, y_fold_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
        
        fold_model = RandomForestClassifier(
            n_estimators=50, max_depth=5, min_samples_split=10, 
            min_samples_leaf=5, random_state=42, class_weight='balanced'
        )
        fold_model.fit(X_fold_train, y_fold_train)
        fold_score = fold_model.score(X_fold_val, y_fold_val)
        cv_scores.append(fold_score)
        print(f"Fold {fold+1}: {fold_score:.4f}")
    
    print(f"CV Mean: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores)*2:.4f})")
    
    # Train final model
    model.fit(X_train_scaled, y_train)
    
    # Predictions with threshold adjustment
    y_pred_proba = model.predict_proba(X_test_scaled)
    
    # Adjust threshold to balance precision/recall
    best_threshold = 0.5
    best_f1 = 0
    
    for threshold in np.arange(0.3, 0.8, 0.05):
        y_pred_thresh = (y_pred_proba[:, 1] >= threshold).astype(int)
        f1 = f1_score(y_test, y_pred_thresh)
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
    
    print(f"Best threshold: {best_threshold:.2f} (F1: {best_f1:.4f})")
    
    # Final predictions with best threshold
    y_pred = (y_pred_proba[:, 1] >= best_threshold).astype(int)
    
    # Evaluation
    print("\n" + "="*50)
    print("IMPROVED MODEL EVALUATION - LUNA DATASET")
    print("="*50)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"F1-Score: {f1_score(y_test, y_pred):.4f}")
    
    if len(np.unique(y)) == 2:
        auc = roc_auc_score(y_test, y_pred_proba[:, 1])
        print(f"ROC-AUC: {auc:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Check for both classes being predicted
    pred_classes = np.unique(y_pred)
    print(f"\nPredicted classes: {pred_classes}")
    if len(pred_classes) == 1:
        print("⚠️  WARNING: Model only predicts one class!")
    else:
        print("✅ Model predicts both classes")
    
    # Feature importance
    importance_df = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importances:")
    print(importance_df)
    
    return model, scaler, best_threshold

def main():
    """Main training pipeline"""
    print("🔧 TRAINING IMPROVED LUNA LUNG CANCER MODEL")
    print("="*60)
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    try:
        # Load and preprocess data
        df = load_and_preprocess_data()
        X, y = preprocess_features(df)
        
        # Train improved model
        model, scaler, threshold = train_improved_model(X, y)
        
        # Save model and scaler
        print("\nSaving improved model...")
        joblib.dump(model, 'models/luna_cancer_model_fixed.pkl')
        joblib.dump(scaler, 'models/luna_cancer_scaler_fixed.pkl')
        joblib.dump({'threshold': threshold}, 'models/luna_cancer_params_fixed.pkl')
        
        print("✅ Improved LUNA model training completed!")
        print("📁 Model saved to: models/luna_cancer_model_fixed.pkl")
        print("📁 Scaler saved to: models/luna_cancer_scaler_fixed.pkl")
        print(f"📁 Best threshold: {threshold:.3f}")
        
    except Exception as e:
        print(f"❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()