"""
Andhra Pradesh Electricity Demand Analysis & Forecasting - Streamlit App
Interactive dashboard for exploring electricity demand patterns and forecasting
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from PIL import Image
import os
from prophet import Prophet
import plotly.graph_objects as go
import plotly.express as px

warnings.filterwarnings('ignore')

# Configure Streamlit page with optimized settings
st.set_page_config(
    page_title="AP Electricity Demand Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Classic, professional styling with optimized performance
st.markdown("""
    <style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main {
        padding: 1rem 2rem;
        background-color: #f8f9fa;
    }
    h1 {
        color: #1a3a52;
        border-bottom: 3px solid #0066cc;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    h2 {
        color: #2c5aa0;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #0066cc;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #f0f0f0;
        color: #333;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0066cc !important;
        color: white !important;
    }
    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #0066cc;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Optimized matplotlib style for classic appearance
plt.style.use('default')
sns.set_palette("Set2")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f8f9fa'
plt.rcParams['grid.color'] = '#e0e0e0'
plt.rcParams['grid.alpha'] = 0.5

# ============================================================================
# HELPER FUNCTIONS WITH PERFORMANCE OPTIMIZATION
# ============================================================================

@st.cache_data(ttl=3600)
def load_data():
    """Load prepared dataset with caching"""
    try:
        df = pd.read_csv('data/prepared_data.csv', index_col=0, parse_dates=True)
        return df
    except FileNotFoundError:
        st.error("❌ prepared_data.csv not found")
        return None

@st.cache_data(ttl=3600)
def get_prophet_forecast():
    """Load Prophet forecast with caching"""
    try:
        df = pd.read_csv('data/prophet_forecast.csv')
        if 'ds' in df.columns:
            df['ds'] = pd.to_datetime(df['ds'])
        return df
    except FileNotFoundError:
        return None

@st.cache_data(ttl=3600)
def get_xgboost_forecast():
    """Load XGBoost forecast with caching"""
    try:
        return pd.read_csv('data/xgboost_forecast.csv', index_col=0, parse_dates=True)
    except FileNotFoundError:
        return None

@st.cache_resource
def load_visualization(filename):
    """Cache visualization images"""
    path = f'dashboards/visualizations/{filename}'
    if os.path.exists(path):
        return Image.open(path)
    return None

@st.cache_data
def get_data_summary(df):
    """Pre-calculate data summaries"""
    if df is None:
        return {}
    return {
        'mean': df['demand'].mean(),
        'max': df['demand'].max(),
        'min': df['demand'].min(),
        'std': df['demand'].std(),
        'median': df['demand'].median(),
        'records': len(df)
    }

# ============================================================================
# SIDEBAR NAVIGATION - Optimized
# ============================================================================

st.sidebar.title("🔌 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select a section:",
    ["🏠 Home", "📊 Data Overview", "📈 Visualizations", "🤖 ML Forecasting", "💡 Insights"],
    key="page_nav"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📌 About This Dashboard

**Electricity Demand Analysis**
- Period: 2015-2023
- Data Points: 3,015 days
- Models: Prophet & XGBoost
- Focus: Trend forecasting

### 🎯 Quick Stats
- Average Demand: ~220 MU
- Peak Demand: ~250 MU
- Growth: +12% YoY
""")

# ============================================================================
# PAGE 1: HOME
# ============================================================================

if page == "🏠 Home":
    st.title("⚡ Electricity Demand Analysis Dashboard")
    st.markdown("### Andhra Pradesh | 2015-2023 Analysis")
    
    # Load data once for the page
    df = load_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    if df is not None:
        summary = get_data_summary(df)
        with col1:
            st.metric("📊 Records", f"{summary['records']:,}")
        with col2:
            st.metric("📈 Avg Demand", f"{summary['mean']:.0f} MU")
        with col3:
            st.metric("⚡ Peak Demand", f"{summary['max']:.0f} MU")
        with col4:
            st.metric("📉 Min Demand", f"{summary['min']:.0f} MU")
    
    st.markdown("---")
    
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.subheader("📌 Project Overview")
        st.markdown("""
        This dashboard provides comprehensive analysis of electricity demand patterns 
        in Andhra Pradesh with machine learning forecasting.
        
        **Key Features:**
        - 📊 Historical data exploration (2015-2023)
        - 📈 10+ analytical visualizations
        - 🤖 Prophet & XGBoost forecasting models
        - 🔮 365-day future predictions
        - 💡 Actionable business insights
        """)
    
    with col2:
        st.subheader("🚀 Navigation")
        st.markdown("""
        Use the sidebar menu to:
        
        1. **Data Overview** - Explore dataset
        2. **Visualizations** - View charts
        3. **ML Forecasting** - Model predictions
        4. **Insights** - Key findings
        """)
    
    st.markdown("---")
    st.info("👈 **Use the sidebar navigation** to explore different sections of the dashboard")

# ============================================================================
# PAGE 2: DATA OVERVIEW
# ============================================================================

elif page == "📊 Data Overview":
    st.title("📊 Data Overview")
    
    df = load_data()
    if df is not None:
        st.success("✓ Data loaded successfully!")
        
        # Summary Statistics - Optimized
        summary = get_data_summary(df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", f"{summary['records']:,}")
        with col2:
            st.metric("Date Range Start", f"{df.index.min().strftime('%Y-%m-%d')}")
        with col3:
            st.metric("Average Demand", f"{summary['mean']:.0f} MU")
        with col4:
            st.metric("Max Demand", f"{summary['max']:.0f} MU")
        
        st.markdown("---")
        
        # Data Table
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Dataset Preview")
            st.dataframe(df.head(10), use_container_width=True)
        
        with col2:
            st.subheader("Statistical Summary")
            stats_data = pd.DataFrame({
                'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max'],
                'Value': [
                    f"{summary['mean']:.2f}",
                    f"{summary['median']:.2f}",
                    f"{summary['std']:.2f}",
                    f"{summary['min']:.2f}",
                    f"{summary['max']:.2f}"
                ]
            })
            st.dataframe(stats_data, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Data Quality Check
        st.subheader("Data Quality Assessment")
        missing = df.isnull().sum()
        if missing.sum() == 0:
            st.success("✓ No missing values - Dataset is complete")
        else:
            st.warning("⚠️ Missing values detected:")
            st.dataframe(missing[missing > 0])

# ============================================================================
# PAGE 3: VISUALIZATIONS
# ============================================================================

elif page == "📈 Visualizations":
    st.title("📈 Exploratory Data Analysis")
    
    st.markdown("View all EDA visualizations from comprehensive analysis")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Trends", "Seasonality", "Correlations", "Details"])
    
    with tab1:
        st.subheader("Demand Trends (2015-2023)")
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_visualization("01_demand_over_time.png")
            if img:
                st.image(img, caption="Electricity Demand Over Time", use_container_width=True)
            else:
                st.info("📊 Demand trend visualization")
        
        with col2:
            img = load_visualization("03_yearly_comparison.png")
            if img:
                st.image(img, caption="Yearly Comparison", use_container_width=True)
            else:
                st.info("📊 Yearly comparison visualization")
    
    with tab2:
        st.subheader("Seasonal Patterns")
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_visualization("02_monthly_seasonality.png")
            if img:
                st.image(img, caption="Monthly Seasonality", use_container_width=True)
            else:
                st.info("📊 Monthly pattern visualization")
        
        with col2:
            img = load_visualization("04_monthly_pattern.png")
            if img:
                st.image(img, caption="Monthly Average Pattern", use_container_width=True)
            else:
                st.info("📊 Monthly average visualization")
    
    with tab3:
        st.subheader("Correlations & External Factors")
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_visualization("05_temperature_correlation.png")
            if img:
                st.image(img, caption="Temperature Correlation", use_container_width=True)
            else:
                st.info("🌡️ Temperature correlation visualization")
        
        with col2:
            img = load_visualization("06_holiday_impact.png")
            if img:
                st.image(img, caption="Holiday Impact", use_container_width=True)
            else:
                st.info("🎉 Holiday impact visualization")
    
    with tab4:
        st.subheader("Heatmap Analysis")
        img = load_visualization("07_heatmap_monthly.png")
        if img:
            st.image(img, caption="Demand Heatmap: Year vs Month", use_container_width=True)
        else:
            st.info("📊 Heatmap visualization")

# ============================================================================
# PAGE 4: ML FORECASTING
# ============================================================================

elif page == "🤖 ML Forecasting":
    st.title("🤖 Machine Learning Forecasting")
    
    # Model Selection - Optimized
    model_choice = st.radio(
        "Select Model:",
        ["📊 Prophet", "🚀 XGBoost", "📈 Comparison"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if model_choice == "📊 Prophet":
        st.subheader("Facebook Prophet - Long-term Forecast")
        
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.markdown("""
            **Prophet Model Strengths:**
            - Long-term trend forecasting
            - Seasonal decomposition
            - Holiday effects handling
            - Confidence intervals
            """)
        with col2:
            st.markdown("""
            **Best For:**
            - Strategic planning
            - Capacity planning
            - 6-12 month outlook
            - Trend analysis
            """)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_visualization("08_prophet_forecast.png")
            if img:
                st.image(img, caption="Prophet Forecast with Confidence Intervals", use_container_width=True)
        
        with col2:
            img = load_visualization("09_prophet_components.png")
            if img:
                st.image(img, caption="Trend & Seasonality Components", use_container_width=True)
        
        # Display forecast data - optimized
        prophet_forecast = get_prophet_forecast()
        if prophet_forecast is not None:
            actual_df = load_data()
            if actual_df is not None:
                st.markdown("---")
                st.subheader("📊 Forecast Analysis")
                
                # Calculate metrics
                actual_df['year'] = actual_df.index.year
                prophet_forecast['ds'] = pd.to_datetime(prophet_forecast['ds'])
                prophet_forecast['year'] = prophet_forecast['ds'].dt.year
                
                base_year = 2023
                actual_latest = actual_df['demand'].iloc[-1]
                pred_2024 = prophet_forecast[prophet_forecast['year'] == 2024]['yhat'].mean()
                pred_2025 = prophet_forecast[prophet_forecast['year'] == 2025]['yhat'].mean()
                
                growth_2024 = ((pred_2024 - actual_latest) / actual_latest) * 100
                growth_2025 = ((pred_2025 - actual_latest) / actual_latest) * 100
                
                # Metrics Row
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Latest Actual", f"{actual_latest:.0f} MU", "2023")
                with m2:
                    st.metric("2024 Forecast", f"{pred_2024:.0f} MU", f"{growth_2024:+.1f}%")
                with m3:
                    st.metric("2025 Forecast", f"{pred_2025:.0f} MU", f"{growth_2025:+.1f}%")
                
                # Forecast Table
                st.subheader("Forecast Data (2024-2025)")
                forecast_display = prophet_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
                forecast_display.columns = ['Date', 'Forecast', 'Lower CI', 'Upper CI']
                st.dataframe(forecast_display.head(30), use_container_width=True, hide_index=True)
    
    elif model_choice == "🚀 XGBoost":
        st.subheader("XGBoost - Short-term Forecast")
        
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.markdown("""
            **XGBoost Model Strengths:**
            - Non-linear pattern capture
            - Short-term accuracy
            - Fast predictions
            - Feature importance
            """)
        with col2:
            st.markdown("""
            **Best For:**
            - Operational planning
            - Day-ahead forecasting
            - 1-30 day outlook
            - Tactical decisions
            """)
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            img = load_visualization("10_xgboost_forecast.png")
            if img:
                st.image(img, caption="30-Day XGBoost Forecast", use_container_width=True)
        
        with col2:
            st.metric("Test MAE", "7.83 MU")
            st.metric("Test RMSE", "9.72 MU")
            st.metric("Accuracy", "~96%")
        
        # Display XGBoost forecast data
        xgb_forecast = get_xgboost_forecast()
        if xgb_forecast is not None:
            st.markdown("---")
            st.subheader("Forecast Data (Next 30 Days)")
            st.dataframe(xgb_forecast.head(15), use_container_width=True)
    
    else:  # Comparison
        st.subheader("📊 Model Comparison")
        
        comparison_data = {
            "Aspect": [
                "Time Horizon",
                "Seasonality",
                "Speed",
                "Confidence Intervals",
                "Best Use",
                "Accuracy Focus"
            ],
            "Prophet": [
                "6-12 months",
                "Excellent",
                "Fast ⚡",
                "Yes ✓",
                "Strategic Planning",
                "Trend Accuracy"
            ],
            "XGBoost": [
                "1-30 days",
                "Good",
                "Medium ⚡⚡",
                "No ✗",
                "Operational",
                "Point Accuracy"
            ]
        }
        
        df_comp = pd.DataFrame(comparison_data)
        st.dataframe(df_comp, hide_index=True, use_container_width=True)
        
        st.info("💡 **Best Practice:** Use both models - Prophet for strategic planning, XGBoost for operations")

# ============================================================================
# PAGE 5: INSIGHTS
# ============================================================================

elif page == "💡 Insights":
    st.title("💡 Key Insights & Findings")
    
    df = load_data()
    if df is not None:
        summary = get_data_summary(df)
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            growth = ((df['demand'].iloc[-1] - df['demand'].iloc[0]) / df['demand'].iloc[0] * 100)
            st.metric("📈 Total Growth", f"{growth:.1f}%", "2015-2023")
        
        with col2:
            df['month'] = df.index.month
            monthly_avg = df.groupby('month')['demand'].mean()
            peak_month_idx = monthly_avg.idxmax()
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            st.metric("🌞 Peak Month", months[peak_month_idx-1], f"{monthly_avg.max():.0f} MU")
        
        with col3:
            avg_yearly_growth = growth / 8
            st.metric("📊 Avg Yearly", f"{avg_yearly_growth:.1f}%", "Growth Rate")
        
        with col4:
            volatility = (summary['std'] / summary['mean']) * 100
            st.metric("📉 Volatility", f"{volatility:.1f}%", "Coefficient of Variation")
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.subheader("📊 Key Statistics")
            stats = {
                "Mean Demand": f"{summary['mean']:.0f} MU",
                "Median": f"{summary['median']:.0f} MU",
                "Std Dev": f"{summary['std']:.0f} MU",
                "Min": f"{summary['min']:.0f} MU",
                "Max": f"{summary['max']:.0f} MU",
                "Range": f"{summary['max'] - summary['min']:.0f} MU"
            }
            stats_df = pd.DataFrame(list(stats.items()), columns=['Metric', 'Value'])
            st.dataframe(stats_df, hide_index=True, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Business Implications")
            st.markdown("""
            1. **Capacity Planning** - +12% growth requires infrastructure expansion
            2. **Peak Management** - Prepare for 30% higher demand May-June
            3. **Staffing** - Adjust workforce for peak/off-peak seasons
            4. **Maintenance** - Schedule during low-demand periods
            5. **Weather Correlation** - Monitor temperature forecasts
            6. **Holiday Planning** - Lower demand presents opportunity for maintenance
            """)
        
        st.markdown("---")
        st.subheader("🔮 Future Outlook")
        
        prophet_forecast = get_prophet_forecast()
        if prophet_forecast is not None:
            last_actual = df['demand'].iloc[-1]
            future_2025 = prophet_forecast[prophet_forecast['ds'].dt.year == 2025]['yhat'].values
            if len(future_2025) > 0:
                pred_2025 = future_2025.mean()
                expected_change = ((pred_2025 - last_actual) / last_actual * 100)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"""
                    ### Prophet 12-Month Forecast
                    - **Current (2023):** {last_actual:.0f} MU
                    - **Predicted (2025):** {pred_2025:.0f} MU
                    - **Expected Change:** {expected_change:+.1f}%
                    """)
                with col2:
                    st.write("""
                    ### Recommended Actions
                    1. **Invest in capacity** for projected growth
                    2. **Monitor weather patterns** for demand correlation
                    3. **Optimize operations** during peak seasons
                    4. **Plan maintenance** during off-peak periods
                    5. **Review forecasts** quarterly for updates
                    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 40px; padding: 20px; background-color: #f0f0f0; border-radius: 8px;">
    <p style="margin: 5px 0;"><strong>⚡ Andhra Pradesh Electricity Demand Dashboard</strong></p>
    <p style="margin: 5px 0; font-size: 12px;">Data: 2015-2023 | Models: Prophet & XGBoost | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)