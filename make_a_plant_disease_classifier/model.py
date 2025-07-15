# predict.py
import pandas as pd
import numpy as np
import logging
from model import PlantDiseaseClassifier
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model():
    """Load trained model and scaler"""
    try:
        MODEL_PATH = "plant_disease_model.joblib"
        SCALER_PATH = "scaler.joblib"
        
        if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
            raise FileNotFoundError("Model or scaler files not found")
            
        classifier = PlantDiseaseClassifier()
        classifier.load(MODEL_PATH, SCALER_PATH)
        return classifier
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

def predict_disease(data):
    """Make predictions for new data"""
    try:
        classifier = load_model()
        predictions = classifier.predict(data)
        return predictions
    except Exception as e:
        logger.error(f"Error making predictions: {str(e)}")
        raise

def main():
    try:
        # Example input data
        sample_data = pd.DataFrame({
            'temperature': [27.48, 24.30],
            'humidity': [33.21, 36.94],
            'rainfall': [0.57, 42.52],
            'soil_pH': [4.97, 8.16]
        })
        
        predictions = predict_disease(sample_data)
        
        for i, pred in enumerate(predictions):
            logger.info(f"Sample {i+1} - Disease Present: {'Yes' if pred == 1 else 'No'}")
            
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()