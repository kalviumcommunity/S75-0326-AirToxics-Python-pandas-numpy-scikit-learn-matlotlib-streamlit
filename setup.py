# setup.py
"""
Setup script to initialize the project
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import AirQualityDataLoader
from ml_models import AQIPredictor
from visualizations import AQIVisualizer

def setup_project():
    """Initialize the project"""
    print("🚀 Setting up Air Quality Intelligence Dashboard...")
    print("\n1️⃣  Loading and preprocessing data...")
    
    loader = AirQualityDataLoader()
    df = loader.load_data()
    df = loader.preprocess_data(df)
    df = loader.categorize_aqi(df)
    loader.save_processed_data(df)
    
    print(f"✅ Data loaded: {len(df)} records from {len(df['city'].unique())} cities")
    
    print("\n2️⃣  Training machine learning models...")
    predictor = AQIPredictor()
    predictor.train_city_models(df)
    predictor.save_model()
    
    print("✅ Models trained and saved successfully!")
    
    print("\n3️⃣  Creating sample visualizations...")
    visualizer = AQIVisualizer()
    print("✅ Visualization utilities ready!")
    
    print("\n✨ Setup complete! Run the following command to start the dashboard:")
    print("   streamlit run app.py")

if __name__ == "__main__":
    setup_project()
