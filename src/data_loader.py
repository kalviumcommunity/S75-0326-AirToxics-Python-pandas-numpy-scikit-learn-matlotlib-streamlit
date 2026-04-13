# data_loader.py
"""
Air Quality Data Loader and Preprocessing Module
Handles data loading, cleaning, and preparation for analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class AirQualityDataLoader:
    """Load and preprocess air quality data"""
    
    def __init__(self, data_dir='data/raw'):
        self.data_dir = data_dir
        self.processed_dir = 'data/processed'
        
        # Create directories if they don't exist
        os.makedirs(self.processed_dir, exist_ok=True)
    
    @staticmethod
    def generate_sample_data(num_days=365, cities=None):
        """Generate sample air quality data for demonstration"""
        if cities is None:
            cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata"]
        
        dates = pd.date_range(end=datetime.now(), periods=num_days, freq='D')
        data = []
        
        for city in cities:
            # Define base pollution levels for each city (for realism)
            city_base = {
                "Delhi": 180,
                "Mumbai": 140,
                "Chennai": 110,
                "Bangalore": 95,
                "Kolkata": 160
            }
            
            base_aqi = city_base.get(city, 120)
            
            for date in dates:
                # Add seasonal variation
                month = date.month
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * month / 12)
                
                # Add weekly variation (higher on weekdays)
                weekday_factor = 1.1 if date.weekday() < 5 else 1.0
                
                # Add random noise
                noise = np.random.normal(0, 15)
                
                aqi = base_aqi * seasonal_factor * weekday_factor + noise
                aqi = max(0, min(500, aqi))  # Keep within realistic range
                
                # Calculate pollutant constituents (PM2.5, PM10, NO2, O3, CO, SO2)
                pm25 = aqi * 0.3 + np.random.normal(0, 5)
                pm10 = aqi * 0.4 + np.random.normal(0, 8)
                no2 = aqi * 0.15 + np.random.normal(0, 3)
                o3 = aqi * 0.1 + np.random.normal(0, 2)
                co = aqi * 0.05 + np.random.normal(0, 1)
                so2 = aqi * 0.05 + np.random.normal(0, 1)
                
                data.append({
                    'date': date,
                    'city': city,
                    'aqi': max(0, aqi),
                    'pm25': max(0, pm25),
                    'pm10': max(0, pm10),
                    'no2': max(0, no2),
                    'o3': max(0, o3),
                    'co': max(0, co),
                    'so2': max(0, so2),
                    'temperature': 15 + 15 * np.sin(2 * np.pi * month / 12) + np.random.normal(0, 3),
                    'humidity': 60 + np.random.normal(0, 10)
                })
        
        return pd.DataFrame(data)
    
    def load_data(self):
        """Load data from raw files or generate sample data"""
        csv_file = os.path.join(self.data_dir, 'air_quality_data.csv')
        
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df['date'] = pd.to_datetime(df['date'])
            return df
        else:
            # Generate sample data if no file exists
            print(f"No data file found at {csv_file}. Generating sample data...")
            df = self.generate_sample_data()
            os.makedirs(self.data_dir, exist_ok=True)
            df.to_csv(csv_file, index=False)
            return df
    
    def preprocess_data(self, df):
        """Clean and prepare data for analysis"""
        # Handle missing values
        df = df.ffill().bfill()
        
        # Ensure date is datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date and city
        df = df.sort_values(['city', 'date']).reset_index(drop=True)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['date', 'city'])
        
        # Add derived features
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        return df
    
    def categorize_aqi(self, df):
        """Add AQI category based on ranges"""
        def get_category(aqi):
            if aqi <= 50:
                return 'Good'
            elif aqi <= 100:
                return 'Satisfactory'
            elif aqi <= 200:
                return 'Moderately Polluted'
            elif aqi <= 300:
                return 'Poor'
            elif aqi <= 400:
                return 'Very Poor'
            else:
                return 'Hazardous'
        
        df['aqi_category'] = df['aqi'].apply(get_category)
        return df
    
    def save_processed_data(self, df, filename='processed_data.csv'):
        """Save processed data"""
        filepath = os.path.join(self.processed_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
        return filepath


if __name__ == "__main__":
    loader = AirQualityDataLoader()
    df = loader.load_data()
    df = loader.preprocess_data(df)
    df = loader.categorize_aqi(df)
    loader.save_processed_data(df)
    print(df.head(10))
    print(f"\nDataset shape: {df.shape}")
    print(f"\nAQI Categories:\n{df['aqi_category'].value_counts()}")
