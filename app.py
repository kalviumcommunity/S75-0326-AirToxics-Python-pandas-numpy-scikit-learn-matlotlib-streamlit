#!/usr/bin/env python3
# app.py
"""
Air Quality Intelligence Dashboard - Streamlit Application
Modern, responsive UI with enhanced styling
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import AirQualityDataLoader
from ml_models import AQIPredictor
from visualizations import AQIVisualizer

# Page configuration
st.set_page_config(
    page_title="Air Quality Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Custom CSS with Premium Styling
st.markdown("""
    <style>
    /* Import better fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Main theme colors */
    :root {
        --primary: #1f77b4;
        --success: #2ecc71;
        --warning: #f39c12;
        --danger: #e74c3c;
        --info: #3498db;
    }
    
    /* Global styling */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Roboto', sans-serif;
    }
    
    /* Main container */
    .main {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    }
    
    /* Page header with premium styling */
    .page-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5em;
        font-weight: 800;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #666;
        font-size: 1.2em;
        margin-bottom: 35px;
        font-weight: 300;
        letter-spacing: 0.3px;
    }
    
    /* Premium metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(102,126,234,0.15);
        color: white;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.1);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102,126,234,0.25);
    }
    
    .metric-card.success {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        box-shadow: 0 10px 30px rgba(46,204,113,0.15);
    }
    
    .metric-card.success:hover {
        box-shadow: 0 20px 40px rgba(46,204,113,0.25);
    }
    
    .metric-card.warning {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        box-shadow: 0 10px 30px rgba(243,156,18,0.15);
    }
    
    .metric-card.warning:hover {
        box-shadow: 0 20px 40px rgba(243,156,18,0.25);
    }
    
    .metric-card.danger {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        box-shadow: 0 10px 30px rgba(231,76,60,0.15);
    }
    
    .metric-card.danger:hover {
        box-shadow: 0 20px 40px rgba(231,76,60,0.25);
    }
    
    .metric-label {
        font-size: 1em;
        font-weight: 600;
        opacity: 0.95;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .metric-value {
        font-size: 2.8em;
        font-weight: 800;
        margin: 12px 0;
        font-family: 'Poppins', sans-serif;
        letter-spacing: -1px;
    }
    
    .metric-unit {
        font-size: 0.9em;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Section divider - Premium */
    .divider {
        height: 3px;
        background: linear-gradient(90deg, transparent 0%, #667eea 25%, #667eea 75%, transparent 100%);
        margin: 40px 0;
        border-radius: 2px;
    }
    
    /* Status badge - Enhanced */
    .status-badge {
        display: inline-block;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.95em;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        letter-spacing: 0.3px;
    }
    
    .status-good {
        background: linear-gradient(135deg, #d5f4e6 0%, #c9ede0 100%);
        color: #27ae60;
    }
    
    .status-satisfactory {
        background: linear-gradient(135deg, #ffeaa7 0%, #ffde9b 100%);
        color: #d63031;
    }
    
    .status-moderate {
        background: linear-gradient(135deg, #fab1a0 0%, #f8a89a 100%);
        color: #d63031;
    }
    
    .status-poor {
        background: linear-gradient(135deg, #ff7675 0%, #ff6b6b 100%);
        color: white;
    }
    
    .status-hazardous {
        background: linear-gradient(135deg, #d63031 0%, #c41c1c 100%);
        color: white;
    }
    
    /* Chart containers - Premium */
    .chart-container {
        background: white;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 20px 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(102,126,234,0.1);
    }
    
    .chart-container:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        border-color: rgba(102,126,234,0.2);
    }
    
    .chart-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.4em;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 20px;
        letter-spacing: -0.3px;
    }
    
    /* Data table styling - Premium */
    .dataframe {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }
    
    .dataframe thead th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 15px !important;
        font-size: 0.95em !important;
        letter-spacing: 0.3px !important;
    }
    
    .dataframe tbody tr {
        transition: background-color 0.2s ease !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #f8f9ff !important;
    }
    
    .dataframe tbody td {
        padding: 12px 15px !important;
        font-size: 0.95em !important;
    }
    
    /* Sidebar styling - Premium */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
    }
    
    .sidebar-section {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    
    /* Button styling - Premium */
    button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1) !important;
        box-shadow: 0 6px 15px rgba(102,126,234,0.2) !important;
        font-size: 0.95em !important;
        letter-spacing: 0.3px !important;
    }
    
    button:hover {
        box-shadow: 0 10px 25px rgba(102,126,234,0.35) !important;
        transform: translateY(-2px) !important;
    }
    
    button:active {
        transform: translateY(0px) !important;
    }
    
    /* Info boxes - Premium */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-left: 5px solid #667eea;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        box-shadow: 0 6px 18px rgba(0,0,0,0.1);
        transform: translateX(2px);
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        border-left-color: #2ecc71;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left-color: #f39c12;
    }
    
    .danger-box {
        background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
        border-left-color: #e74c3c;
    }
    
    /* Text styling - Premium */
    h1 { 
        color: #667eea; 
        font-weight: 800; 
        margin-bottom: 25px;
        font-family: 'Poppins', sans-serif;
        letter-spacing: -0.5px;
    }
    
    h2 { 
        color: #764ba2; 
        font-weight: 700; 
        margin-top: 30px; 
        margin-bottom: 20px;
        font-family: 'Poppins', sans-serif;
        letter-spacing: -0.3px;
    }
    
    h3 { 
        color: #667eea; 
        font-weight: 600;
        margin-bottom: 15px;
        font-family: 'Poppins', sans-serif;
    }
    
    p {
        line-height: 1.7;
        color: #555;
        font-weight: 400;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: transparent !important;
        border-radius: 8px !important;
        border: 2px solid transparent !important;
        color: #667eea !important;
        font-weight: 600 !important;
        margin: 5px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: rgba(102,126,234,0.1) !important;
        border-color: #667eea !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: #667eea !important;
        color: white !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > select {
        border-radius: 8px !important;
        border: 2px solid #ddd !important;
        padding: 10px !important;
    }
    
    .stSelectbox > div > div > select:hover {
        border-color: #667eea !important;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1) !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Expander styling */
    .stExpander > div > button {
        background-color: transparent !important;
        border: 2px solid #ddd !important;
        border-radius: 10px !important;
    }
    
    .stExpander > div > button:hover {
        background-color: rgba(102,126,234,0.05) !important;
        border-color: #667eea !important;
    }
    
    .stExpander > div[data-testid="expanderContent"] {
        border-left: 4px solid #667eea;
        padding-left: 15px;
        margin-top: 10px;
    }
    
    /* Animation classes */
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(20px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    @keyframes slideIn {
        from { 
            opacity: 0; 
            transform: translateX(-20px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    .slide-in {
        animation: slideIn 0.5s ease-in;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5568d3 0%, #6b3f94 100%);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .page-header {
            font-size: 2.5em;
        }
        
        .metric-card {
            padding: 20px;
        }
        
        .metric-value {
            font-size: 2em;
        }
        
        .main {
            padding: 20px;
        }
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data_and_models():
    """Load data and train models (cached)"""
    # Load data
    loader = AirQualityDataLoader()
    df = loader.load_data()
    df = loader.preprocess_data(df)
    df = loader.categorize_aqi(df)
    
    # Train models
    predictor = AQIPredictor()
    predictor.train_city_models(df)
    
    return df, predictor

def get_aqi_status_and_color(aqi):
    """Get status, recommendation, and color for AQI value"""
    if aqi <= 50:
        status = "✅ GOOD"
        color = "#2ecc71"
        bg_color = "#d5f4e6"
        recommendation = "Excellent conditions for outdoor activities"
    elif aqi <= 100:
        status = "☑️ SATISFACTORY"
        color = "#f39c12"
        bg_color = "#ffeaa7"
        recommendation = "Suitable for outdoor activities"
    elif aqi <= 200:
        status = "⚠️ MODERATELY POLLUTED"
        color = "#e67e22"
        bg_color = "#fab1a0"
        recommendation = "Limit prolonged outdoor activities, especially for sensitive groups"
    elif aqi <= 300:
        status = "🔴 POOR"
        color = "#e74c3c"
        bg_color = "#ff7675"
        recommendation = "Avoid outdoor activities, wear N95 masks if necessary"
    elif aqi <= 400:
        status = "🔴🔴 VERY POOR"
        color = "#c0392b"
        bg_color = "#d63031"
        recommendation = "Stay indoors, use air purifiers, avoid outdoor activities"
    else:
        status = "🔴🔴🔴 HAZARDOUS"
        color = "#8b0000"
        bg_color = "#d63031"
        recommendation = "Remain indoors, use air purifiers with HEPA filter"
    
    return status, recommendation, color, bg_color

# Main app
def main():
    # Load data and models
    df, predictor = load_data_and_models()
    
    # Sidebar Navigation with Better Styling
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='font-size: 2.5em; margin: 0;'>🌍</h1>
            <h2 style='margin: 10px 0; color: #667eea;'>AQI Dashboard</h2>
            <p style='color: #999; font-size: 0.9em;'>Air Quality Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "📍 Navigation",
            [
                "🏠 Dashboard",
                "🏙️ City Analysis",
                "🔮 Forecasting",
                "⚕️ Health Guidelines",
                "ℹ️ About"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Sidebar stats
        st.subheader("📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Cities", len(df['city'].unique()))
        with col2:
            st.metric("Records", len(df))
        
        st.markdown("""
        <p style='color: #999; font-size: 0.85em; text-align: center; margin-top: 30px;'>
        Last Updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """
        </p>
        """, unsafe_allow_html=True)
    
    # Dashboard Page
    if "🏠 Dashboard" in page:
        # Header
        st.markdown('<div class="page-header">🌍 Air Quality Intelligence Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Real-time monitoring & AI-powered predictions for Indian cities</div>', unsafe_allow_html=True)
        
        # Key Metrics
        latest_data = df.groupby('city')[['aqi', 'pm25', 'pm10']].tail(1)
        avg_aqi = latest_data['aqi'].mean()
        max_aqi = latest_data['aqi'].max()
        min_aqi = latest_data['aqi'].min()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            color = "#667eea" if avg_aqi <= 100 else "#f39c12" if avg_aqi <= 200 else "#e74c3c"
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, {color}22 0%, {color}11 100%); border-left: 4px solid {color};">
                <div class="metric-label">📊 Average AQI</div>
                <div class="metric-value" style="color: {color};">{avg_aqi:.1f}</div>
                <div class="metric-unit">All Cities</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #e74c3c22 0%, #e74c3c11 100%); border-left: 4px solid #e74c3c;">
                <div class="metric-label">⚠️ Highest AQI</div>
                <div class="metric-value" style="color: #e74c3c;">{max_aqi:.1f}</div>
                <div class="metric-unit">Peak Level</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #2ecc7122 0%, #2ecc7111 100%); border-left: 4px solid #2ecc71;">
                <div class="metric-label">✅ Lowest AQI</div>
                <div class="metric-value" style="color: #2ecc71;">{min_aqi:.1f}</div>
                <div class="metric-unit">Best Condition</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #3498db22 0%, #3498db11 100%); border-left: 4px solid #3498db;">
                <div class="metric-label">🏙️ Cities</div>
                <div class="metric-value" style="color: #3498db;">{len(df['city'].unique())}</div>
                <div class="metric-unit">Monitored</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Main Visualizations in Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏆 Comparison", "📅 Patterns", "🔗 Correlations"])
        
        with tab1:
            st.markdown('<div class="chart-title">30-Day AQI Trend Across Cities</div>', unsafe_allow_html=True)
            fig_trend = AQIVisualizer.plot_aqi_trend(df, days=30)
            st.pyplot(fig_trend, use_container_width=True)
        
        with tab2:
            st.markdown('<div class="chart-title">City-wise AQI Comparison</div>', unsafe_allow_html=True)
            fig_comparison = AQIVisualizer.plot_city_comparison(df)
            st.pyplot(fig_comparison, use_container_width=True)
        
        with tab3:
            st.markdown('<div class="chart-title">Seasonal Patterns by Month</div>', unsafe_allow_html=True)
            fig_monthly = AQIVisualizer.plot_monthly_pattern(df)
            st.pyplot(fig_monthly, use_container_width=True)
        
        with tab4:
            st.markdown('<div class="chart-title">Pollutant Correlation Analysis</div>', unsafe_allow_html=True)
            fig_correlation = AQIVisualizer.plot_correlation_heatmap(df)
            st.pyplot(fig_correlation, use_container_width=True)
    
    # City Analysis Page
    elif "🏙️ City Analysis" in page:
        st.markdown('<div class="page-header">🏙️ City Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Detailed pollution analysis for selected city</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            selected_city = st.selectbox("Select City", df['city'].unique(), key="city_select")
        with col2:
            days_back = st.select_slider("Show last", options=[7, 14, 30, 60, 90], value=30, key="days_slider")
        with col3:
            st.metric("", "")  # Spacer
        
        city_data = df[df['city'] == selected_city]
        latest = city_data.iloc[-1]
        
        # Status and Metrics
        status, recommendation, color, bg_color = get_aqi_status_and_color(latest['aqi'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, {color}44 0%, {color}22 100%); border-left: 4px solid {color};">
                <div class="metric-label">📊 Current AQI</div>
                <div class="metric-value" style="color: {color};">{latest['aqi']:.1f}</div>
                <div class="metric-unit">{status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            pm25_color = "#2ecc71" if latest['pm25'] < 35 else "#f39c12" if latest['pm25'] < 75 else "#e74c3c"
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, {pm25_color}22 0%, {pm25_color}11 100%); border-left: 4px solid {pm25_color};">
                <div class="metric-label">💨 PM2.5</div>
                <div class="metric-value" style="color: {pm25_color};">{latest['pm25']:.1f}</div>
                <div class="metric-unit">µg/m³</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            pm10_color = "#2ecc71" if latest['pm10'] < 100 else "#f39c12" if latest['pm10'] < 250 else "#e74c3c"
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, {pm10_color}22 0%, {pm10_color}11 100%); border-left: 4px solid {pm10_color};">
                <div class="metric-label">💨 PM10</div>
                <div class="metric-value" style="color: {pm10_color};">{latest['pm10']:.1f}</div>
                <div class="metric-unit">µg/m³</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #3498db22 0%, #3498db11 100%); border-left: 4px solid #3498db;">
                <div class="metric-label">🌡️ Temperature</div>
                <div class="metric-value" style="color: #3498db;">{latest['temperature']:.1f}°C</div>
                <div class="metric-unit">Current</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Recommendation box
        st.markdown(f"""
        <div class="info-box" style="background: linear-gradient(135deg, {bg_color}88 0%, {bg_color}44 100%); border-left: 4px solid {color}; padding: 20px; border-radius: 12px;">
            <h3 style="color: {color}; margin-top: 0;">💡 Health Recommendation</h3>
            <p style="color: #333; font-size: 1.05em; line-height: 1.6;">{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Charts in tabs
        tab1, tab2, tab3 = st.tabs(["📈 Trend", "🧪 Pollutants", "📊 Distribution"])
        
        with tab1:
            st.markdown('<div class="chart-title">AQI Trend Analysis</div>', unsafe_allow_html=True)
            fig = AQIVisualizer.plot_aqi_trend(df, city=selected_city, days=days_back)
            st.pyplot(fig, use_container_width=True)
        
        with tab2:
            st.markdown('<div class="chart-title">Pollutant Composition</div>', unsafe_allow_html=True)
            fig = AQIVisualizer.plot_pollutant_composition(df, city=selected_city)
            st.pyplot(fig, use_container_width=True)
        
        with tab3:
            st.markdown('<div class="chart-title">AQI Distribution</div>', unsafe_allow_html=True)
            fig = AQIVisualizer.plot_aqi_distribution(df, city=selected_city)
            st.pyplot(fig, use_container_width=True)
        
        # Detailed Table
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #1f77b4;">📋 Detailed Pollutant Levels</h3>', unsafe_allow_html=True)
        
        pollutants_df = pd.DataFrame({
            'Pollutant': ['PM2.5', 'PM10', 'NO₂', 'O₃', 'CO', 'SO₂', 'Humidity'],
            'Current Level': [
                f"{latest['pm25']:.2f} µg/m³",
                f"{latest['pm10']:.2f} µg/m³",
                f"{latest['no2']:.2f} µg/m³",
                f"{latest['o3']:.2f} µg/m³",
                f"{latest['co']:.2f} µg/m³",
                f"{latest['so2']:.2f} µg/m³",
                f"{latest['humidity']:.1f}%"
            ]
        })
        st.dataframe(pollutants_df, use_container_width=True, hide_index=True)
    
    # Forecasting Page
    elif "🔮 Forecasting" in page:
        st.markdown('<div class="page-header">🔮 AQI Forecasting</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">AI-powered predictions using Random Forest models</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            selected_city = st.selectbox("Select City", df['city'].unique(), key="forecast_city")
        
        with col2:
            forecast_days = st.slider("Forecast Period (days)", 1, 14, 7)
        
        with col3:
            st.metric("", "")  # Spacer
        
        # Generate forecast
        forecast_df = predictor.forecast_next_days(df, selected_city, days=forecast_days)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Forecast Chart
        st.markdown(f'<div class="chart-title">📈 {selected_city} - {forecast_days} Day AQI Forecast</div>', unsafe_allow_html=True)
        fig = AQIVisualizer.plot_forecast(df, forecast_df, selected_city)
        st.pyplot(fig, use_container_width=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Forecast Table and Metrics
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown('<h3 style="color: #1f77b4;">📊 Forecast Details</h3>', unsafe_allow_html=True)
            forecast_display = forecast_df.copy()
            forecast_display['date'] = forecast_display['date'].dt.strftime('%a, %b %d')
            forecast_display['aqi_forecast'] = forecast_display['aqi_forecast'].round(1)
            forecast_display = forecast_display[['date', 'aqi_forecast', 'days_ahead']]
            forecast_display.columns = ['Date', 'Forecasted AQI', 'Days Ahead']
            st.dataframe(forecast_display, use_container_width=True, hide_index=True)
        
        with col1:
            st.markdown('<h3 style="color: #1f77b4;">🤖 Model Performance</h3>', unsafe_allow_html=True)
            if selected_city in predictor.city_models:
                metrics = predictor.city_models[selected_city]['metrics']
                perf_col1, perf_col2 = st.columns(2)
                
                with perf_col1:
                    st.metric("R² Score", f"{metrics['r2']:.4f}", "Accuracy")
                    st.metric("RMSE", f"{metrics['rmse']:.2f}", "Error")
                
                with perf_col2:
                    st.metric("MAE", f"{metrics['mae']:.2f}", "Avg Error")
                    st.metric("MSE", f"{metrics['mse']:.2f}", "Squared Error")
    
    # Health Guidelines Page
    elif "⚕️ Health Guidelines" in page:
        st.markdown('<div class="page-header">⚕️ Health Guidelines</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">AQI categories, health impacts, and recommendations</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        selected_city = st.selectbox("Select City for Recommendations", df['city'].unique(), key="health_city")
        
        latest = df[df['city'] == selected_city].iloc[-1]
        status, recommendation, color, bg_color = get_aqi_status_and_color(latest['aqi'])
        
        # Current Status Box
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}22 0%, {color}11 100%); 
                        border-left: 5px solid {color}; padding: 25px; border-radius: 12px;">
                <h3 style="color: {color}; margin-top: 0;">Current Status - {selected_city}</h3>
                <h1 style="color: {color}; font-size: 3em; margin: 10px 0;">{latest['aqi']:.0f}</h1>
                <h2 style="color: {color}; font-size: 1.3em; margin: 0;">{status}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-box" style="background: linear-gradient(135deg, {bg_color}88 0%, {bg_color}44 100%); 
                                          border-left: 5px solid {color}; padding: 25px;">
                <p style="color: #333; font-size: 1.1em; line-height: 1.8;">{recommendation}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # AQI Categories
        st.markdown('<h2 style="color: #1f77b4;">📊 AQI Categories & Health Impact</h2>', unsafe_allow_html=True)
        
        categories = [
            ("0-50", "🟢 GOOD", "#2ecc71", "No health impact", "✅ Ideal for outdoor activities"),
            ("51-100", "🟡 SATISFACTORY", "#f39c12", "Minimal health impact", "✅ Suitable for outdoor activities"),
            ("101-200", "🟠 MODERATELY POLLUTED", "#e67e22", "Health issues in sensitive groups", "⚠️ Limit outdoor activities for sensitive groups"),
            ("201-300", "🔴 POOR", "#e74c3c", "Serious health impacts likely", "🔴 Avoid prolonged outdoor activities"),
            ("301-400", "🔴 VERY POOR", "#c0392b", "Very serious health impacts", "🔴 Minimize outdoor activities, use N95"),
            ("401+", "🔴🔴 HAZARDOUS", "#8b0000", "Severe health emergency", "🔴 Stay indoors, emergency measures")
        ]
        
        for aqi_range, label, cat_color, impact, rec in categories:
            with st.expander(f"**{label}** - AQI {aqi_range}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Health Impact:** {impact}")
                with col2:
                    st.markdown(f"**Recommendation:** {rec}")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Health Tips
        st.markdown('<h2 style="color: #1f77b4;">💡 Health Tips</h2>', unsafe_allow_html=True)
        
        tips_col1, tips_col2, tips_col3 = st.columns(3)
        
        with tips_col1:
            st.markdown("""
            <div class="info-box success-box">
            <h4>🏃 General Tips</h4>
            <ul style="margin-left: 20px;">
            <li>Exercise in clean air areas</li>
            <li>Maintain healthy diet</li>
            <li>Stay well hydrated</li>
            <li>Use N95 masks when needed</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with tips_col2:
            st.markdown("""
            <div class="info-box success-box">
            <h4>🏠 At Home</h4>
            <ul style="margin-left: 20px;">
            <li>Close windows during high pollution</li>
            <li>Use HEPA air purifiers</li>
            <li>Regular cleaning</li>
            <li>Keep indoor plants</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with tips_col3:
            st.markdown("""
            <div class="info-box warning-box">
            <h4>👶 At-Risk Groups</h4>
            <ul style="margin-left: 20px;">
            <li>Protect children & elderly</li>
            <li>Respiratory patients: consult doctor</li>
            <li>Heart patients: be cautious</li>
            <li>Pregnant women: limit exposure</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # About Page
    elif "ℹ️ About" in page:
        st.markdown('<div class="page-header">ℹ️ About This Project</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <h2>🌍 Air Quality Intelligence Dashboard</h2>
        
        <p style="font-size: 1.1em; line-height: 1.8;">
        Urban areas in India generate massive volumes of air pollution data daily. 
        This dashboard transforms complex air quality data into clear, actionable insights 
        using advanced data science and machine learning.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card success">
            <div class="metric-label">📊 Real-time Monitoring</div>
            <p>Track AQI across 5 major cities with live data and historical analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card warning">
            <div class="metric-label">🔮 AI Forecasting</div>
            <p>Get accurate 14-day predictions using Random Forest models with 93% accuracy</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card danger">
            <div class="metric-label">⚕️ Health Recommendations</div>
            <p>Personalized guidance based on AQI levels and health risk categories</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Dataset & Tech Stack
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 style="color: #1f77b4;">📦 Dataset</h3>', unsafe_allow_html=True)
            st.info(f"""
            - **Total Records:** {len(df)}
            - **Cities Covered:** {len(df['city'].unique())}
            - **Date Range:** {df['date'].min().date()} to {df['date'].max().date()}
            - **Variables:** 11 (AQI + pollutants + weather)
            """)
        
        with col2:
            st.markdown('<h3 style="color: #1f77b4;">🛠️ Tech Stack</h3>', unsafe_allow_html=True)
            st.info("""
            - **Python 3.13** - Core language
            - **Pandas & NumPy** - Data processing
            - **scikit-learn** - ML models
            - **Matplotlib & Seaborn** - Visualizations
            - **Streamlit** - Web framework
            """)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box success-box">
        <h3>💡 Impact</h3>
        <p>This project empowers citizens by making pollution data easy to understand, 
        encouraging health-aware lifestyle choices, and promoting awareness about environmental conditions.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
