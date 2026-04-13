# visualizations.py
"""
Visualization utilities for Air Quality Dashboard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

class AQIVisualizer:
    """Create visualizations for air quality data"""
    
    @staticmethod
    def get_aqi_color(aqi_value):
        """Get color based on AQI value"""
        if aqi_value <= 50:
            return '#2ecc71'  # Green - Good
        elif aqi_value <= 100:
            return '#f1c40f'  # Yellow - Satisfactory
        elif aqi_value <= 200:
            return '#e67e22'  # Orange - Moderately Polluted
        elif aqi_value <= 300:
            return '#e74c3c'  # Red - Poor
        elif aqi_value <= 400:
            return '#c0392b'  # Dark Red - Very Poor
        else:
            return '#8b0000'  # Dark Red - Hazardous
    
    @staticmethod
    def plot_aqi_trend(df, city=None, days=30):
        """Plot AQI trend over time"""
        if city:
            data = df[df['city'] == city].copy()
            title = f"AQI Trend - {city} (Last {days} days)"
        else:
            data = df.copy()
            title = f"AQI Trend (Last {days} days)"
        
        # Get last N days
        data = data.tail(days * (len(df['city'].unique()) if not city else 1))
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        if city:
            ax.plot(data['date'], data['aqi'], linewidth=2, color='#3498db', marker='o', markersize=4)
            ax.fill_between(data['date'], data['aqi'], alpha=0.3, color='#3498db')
        else:
            for c in data['city'].unique():
                c_data = data[data['city'] == c]
                ax.plot(c_data['date'], c_data['aqi'], linewidth=2, marker='o', label=c, markersize=4)
        
        # Add AQI zones
        ax.axhspan(0, 50, alpha=0.1, color='green', label='Good (0-50)')
        ax.axhspan(50, 100, alpha=0.1, color='yellow', label='Satisfactory (51-100)')
        ax.axhspan(100, 200, alpha=0.1, color='orange', label='Moderately Polluted (101-200)')
        ax.axhspan(200, 300, alpha=0.1, color='red', label='Poor (201-300)')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('AQI Value', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_city_comparison(df):
        """Compare AQI across cities"""
        # Get latest values for each city
        latest = df.groupby('city')['aqi'].tail(1)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = [AQIVisualizer.get_aqi_color(val) for val in latest.values]
        bars = ax.bar(latest.index, latest.values, color=colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax.axhline(y=100, color='red', linestyle='--', linewidth=2, label='Moderate Threshold (100)')
        ax.axhline(y=200, color='darkred', linestyle='--', linewidth=2, label='Poor Threshold (200)')
        
        ax.set_ylabel('AQI Value', fontsize=12)
        ax.set_title('Current AQI Levels - City Comparison', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_pollutant_composition(df, city=None):
        """Plot composition of different pollutants"""
        if city:
            data = df[df['city'] == city].iloc[-1]
            title = f"Pollutant Composition - {city}"
        else:
            data = df.iloc[-1]
            title = "Pollutant Composition (Latest)"
        
        pollutants = ['pm25', 'pm10', 'no2', 'o3', 'co', 'so2']
        values = [data.get(p, 0) for p in pollutants]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = ['#e74c3c', '#e67e22', '#f1c40f', '#3498db', '#9b59b6', '#1abc9c']
        wedges, texts, autotexts = ax.pie(values, labels=[p.upper() for p in pollutants],
                                           autopct='%1.1f%%', colors=colors,
                                           startangle=90, textprops={'fontsize': 11})
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_monthly_pattern(df, city=None):
        """Plot monthly AQI pattern"""
        if city:
            data = df[df['city'] == city]
            title = f"Monthly AQI Pattern - {city}"
        else:
            data = df
            title = "Monthly AQI Pattern"
        
        monthly = data.groupby('month')['aqi'].agg(['mean', 'max', 'min'])
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(monthly.index, monthly['mean'], linewidth=2.5, marker='o', 
               label='Average', color='#3498db', markersize=8)
        ax.fill_between(monthly.index, monthly['min'], monthly['max'], 
                       alpha=0.2, color='#3498db', label='Min-Max Range')
        
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('AQI Value', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_aqi_distribution(df, city=None):
        """Plot AQI distribution"""
        if city:
            data = df[df['city'] == city]['aqi']
            title = f"AQI Distribution - {city}"
        else:
            data = df['aqi']
            title = "AQI Distribution (All Cities)"
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.hist(data, bins=30, color='#3498db', edgecolor='black', alpha=0.7)
        ax.axvline(data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {data.mean():.1f}')
        ax.axvline(data.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {data.median():.1f}')
        
        ax.set_xlabel('AQI Value', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_correlation_heatmap(df):
        """Plot correlation between pollutants"""
        pollutants = ['aqi', 'pm25', 'pm10', 'no2', 'o3', 'co', 'so2', 'temperature', 'humidity']
        corr_data = df[pollutants].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   square=True, ax=ax, cbar_kws={'label': 'Correlation'})
        
        ax.set_title('Correlation Matrix - Air Quality Variables', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_forecast(df, forecast_df, city):
        """Plot forecast with historical data"""
        historical = df[df['city'] == city].tail(30)
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Historical data
        ax.plot(historical['date'], historical['aqi'], linewidth=2, 
               color='#3498db', marker='o', label='Historical', markersize=5)
        ax.fill_between(historical['date'], historical['aqi'], alpha=0.2, color='#3498db')
        
        # Forecast
        ax.plot(forecast_df['date'], forecast_df['aqi_forecast'], linewidth=2.5,
               color='#e74c3c', marker='s', label='Forecast', markersize=6, linestyle='--')
        ax.fill_between(forecast_df['date'], forecast_df['aqi_forecast'], alpha=0.2, color='#e74c3c')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('AQI Value', fontsize=12)
        ax.set_title(f"AQI Forecast - {city}", fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig


if __name__ == "__main__":
    from data_loader import AirQualityDataLoader
    
    loader = AirQualityDataLoader()
    df = loader.load_data()
    df = loader.preprocess_data(df)
    
    visualizer = AQIVisualizer()
    
    # Create visualizations
    fig1 = visualizer.plot_aqi_trend(df, city='Delhi')
    fig2 = visualizer.plot_city_comparison(df)
    fig3 = visualizer.plot_pollutant_composition(df, city='Delhi')
    
    plt.show()
