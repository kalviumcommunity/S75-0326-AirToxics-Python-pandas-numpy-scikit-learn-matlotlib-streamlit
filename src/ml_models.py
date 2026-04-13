# ml_models.py
"""
Machine Learning Models for AQI Prediction and Forecasting
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
import os

class AQIPredictor:
    """ML models for predicting AQI levels"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        self.scaler = StandardScaler()
        self.model = None
        self.feature_names = None
        self.city_models = {}
    
    def prepare_features(self, df, city=None):
        """Prepare features for modeling"""
        if city:
            df = df[df['city'] == city].copy()
        
        # Create lag features
        for lag in [1, 7, 30]:
            df[f'aqi_lag_{lag}'] = df['aqi'].shift(lag)
        
        # Create rolling averages
        for window in [7, 30]:
            df[f'aqi_ma_{window}'] = df['aqi'].shift(1).rolling(window=window).mean()
        
        # Drop rows with NaN values from lag features
        df = df.dropna()
        
        # Feature selection
        feature_cols = [
            'pm25', 'pm10', 'no2', 'o3', 'co', 'so2',
            'temperature', 'humidity', 'month', 'is_weekend',
            'aqi_lag_1', 'aqi_lag_7', 'aqi_lag_30',
            'aqi_ma_7', 'aqi_ma_30'
        ]
        
        # Keep only available features
        feature_cols = [col for col in feature_cols if col in df.columns]
        self.feature_names = feature_cols
        
        X = df[feature_cols]
        y = df['aqi']
        
        return X, y, df
    
    def train_model(self, df, city=None, model_type='random_forest'):
        """Train AQI prediction model"""
        X, y, processed_df = self.prepare_features(df, city)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        if model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        else:
            self.model = LinearRegression()
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred)
        }
        
        return self.model, metrics, (X_train_scaled, X_test_scaled, y_train, y_test)
    
    def train_city_models(self, df):
        """Train separate models for each city"""
        cities = df['city'].unique()
        
        for city in cities:
            print(f"Training model for {city}...")
            model, metrics, _ = self.train_model(df, city=city)
            self.city_models[city] = {
                'model': model,
                'scaler': self.scaler,
                'metrics': metrics
            }
            print(f"  R² Score: {metrics['r2']:.4f}, RMSE: {metrics['rmse']:.2f}")
        
        return self.city_models
    
    def predict(self, X, city=None):
        """Make predictions"""
        if city and city in self.city_models:
            model = self.city_models[city]['model']
            scaler = self.city_models[city]['scaler']
            X_scaled = scaler.transform(X)
            return model.predict(X_scaled)
        else:
            X_scaled = self.scaler.transform(X)
            return self.model.predict(X_scaled)
    
    def forecast_next_days(self, df, city, days=7):
        """Forecast AQI for next N days"""
        city_data = df[df['city'] == city].copy()
        last_date = city_data['date'].max()
        
        forecasts = []
        
        # Use last row as base for prediction
        last_row = city_data.iloc[-1].copy()
        
        for day in range(1, days + 1):
            forecast_date = last_date + pd.Timedelta(days=day)
            
            # Create feature vector from last available data
            features = {col: [last_row[col]] 
                       for col in self.feature_names if col in last_row.index}
            
            # Fill missing features
            for feature in self.feature_names:
                if feature not in features:
                    if 'lag' in feature or 'ma' in feature:
                        features[feature] = [last_row['aqi']]
                    else:
                        features[feature] = [last_row.get(feature, 0)]
            
            X_pred = pd.DataFrame(features)
            prediction = self.predict(X_pred, city=city)[0]
            
            forecasts.append({
                'date': forecast_date,
                'city': city,
                'aqi_forecast': max(0, prediction),
                'days_ahead': day
            })
        
        return pd.DataFrame(forecasts)
    
    def save_model(self, filepath=None):
        """Save model to disk"""
        if filepath is None:
            filepath = os.path.join(self.model_dir, 'aqi_model.pkl')
        
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'city_models': self.city_models
            }, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath=None):
        """Load model from disk"""
        if filepath is None:
            filepath = os.path.join(self.model_dir, 'aqi_model.pkl')
        
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
                self.feature_names = data['feature_names']
                self.city_models = data['city_models']
            print(f"Model loaded from {filepath}")
            return True
        return False


if __name__ == "__main__":
    from data_loader import AirQualityDataLoader
    
    # Load data
    loader = AirQualityDataLoader()
    df = loader.load_data()
    df = loader.preprocess_data(df)
    
    # Train models
    predictor = AQIPredictor()
    predictor.train_city_models(df)
    predictor.save_model()
    
    # Show forecast example
    forecast = predictor.forecast_next_days(df, 'Delhi', days=7)
    print("\nForecast for Delhi (next 7 days):")
    print(forecast[['date', 'aqi_forecast']])
