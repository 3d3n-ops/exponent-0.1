# Modal Training Script for Plant Disease Classification
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# Set matplotlib backend for non-interactive environments
plt.switch_backend('Agg')

def load_dataset():
    """Load the plant disease dataset."""
    try:
        df = pd.read_csv('plant_disease_dataset.csv')
        print(f"✅ Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print("❌ Error: plant_disease_dataset.csv not found!")
        print("💡 Make sure the dataset file is in the current directory")
        raise
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        raise

def preprocess_data(df):
    """Preprocess the data for training."""
    print("🔧 Preprocessing data...")
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        print(f"⚠️ Found missing values: {missing_values[missing_values > 0]}")
        df = df.dropna()
    
    # Separate features and target
    feature_columns = ['temperature', 'humidity', 'rainfall', 'soil_pH']
    target_column = 'disease_present'
    
    # Verify columns exist
    missing_cols = [col for col in feature_columns + [target_column] if col not in df.columns]
    if missing_cols:
        print(f"❌ Missing columns: {missing_cols}")
        print(f"Available columns: {list(df.columns)}")
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    X = df[feature_columns]
    y = df[target_column]
    
    print(f"✅ Features: {X.shape[1]} columns")
    print(f"✅ Target: {y.value_counts().to_dict()}")
    
    return X, y

def train_model(X_train, X_test, y_train, y_test):
    """Train the Random Forest model."""
    print("🤖 Training Random Forest model...")
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create and train the model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    
    # Print classification report
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return model, scaler, y_pred

def save_model(model, scaler):
    """Save the trained model and scaler."""
    print("💾 Saving model artifacts...")
    
    try:
        joblib.dump(model, 'plant_disease_model.joblib')
        joblib.dump(scaler, 'scaler.joblib')
        print("✅ Model saved: plant_disease_model.joblib")
        print("✅ Scaler saved: scaler.joblib")
    except Exception as e:
        print(f"❌ Error saving model: {e}")
        raise

def create_visualizations(y_test, y_pred, model, X_train):
    """Create training visualizations."""
    print("📈 Creating visualizations...")
    
    # Confusion matrix
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Confusion matrix saved: confusion_matrix.png")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': model.feature_importances_
    })
    feature_importance = feature_importance.sort_values('importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feature_importance)
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Feature importance saved: feature_importance.png")

def main():
    """Main training function."""
    print("🚀 Starting Plant Disease Classification Training")
    print("=" * 50)
    
    try:
        # Load dataset
        df = load_dataset()
        
        # Preprocess data
        X, y = preprocess_data(df)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"✅ Training set: {X_train.shape[0]} samples")
        print(f"✅ Test set: {X_test.shape[0]} samples")
        
        # Train model
        model, scaler, y_pred = train_model(X_train, X_test, y_train, y_test)
        
        # Save model
        save_model(model, scaler)
        
        # Create visualizations
        create_visualizations(y_test, y_pred, model, X_train)
        
        print("\n🎉 Training completed successfully!")
        print("📁 Generated files:")
        print("  - plant_disease_model.joblib")
        print("  - scaler.joblib")
        print("  - confusion_matrix.png")
        print("  - feature_importance.png")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        raise

if __name__ == "__main__":
    main()