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

warnings.filterwarnings('ignore')

# Configure Streamlit page
st.set_page_config(
    page_title="AP Electricity Demand Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main { padding: 0rem 1rem; }
    .metric-card { 
        background-color: #f0f2f6; 
        padding: 20px; 
        border-radius: 10px; 
        text-align: center;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Set style for plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data
def load_data():
    """Load prepared dataset"""
    try:
        df = pd.read_csv('data/prepared_data.csv', index_col=0, parse_dates=True)
        return df
    except FileNotFoundError:
        st.error("❌ prepared_data.csv not found. Please run 01_data_loading.py first.")
        return None

@st.cache_data
def load_prophet_forecast():
    """Load Prophet forecast"""
    try:
        return pd.read_csv('data/prophet_forecast.csv')
    except FileNotFoundError:
        return None

@st.cache_data
def load_xgboost_forecast():
    """Load XGBoost forecast"""
    try:
        return pd.read_csv('data/xgboost_forecast.csv')
    except FileNotFoundError:
        return None

def load_visualization(filename):
    """Load visualization image"""
    path = f'dashboards/visualizations/{filename}'
    if os.path.exists(path):
        return Image.open(path)
    return None

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.title("🔌 Navigation")
page = st.sidebar.radio(
    "Select a section:",
    ["🏠 Home", "📊 Data Overview", "📈 Visualizations", "🤖 ML Forecasting", "💡 Insights"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**AP Electricity Demand Analysis**\n\n"
    "Comprehensive analysis and forecasting of electricity demand patterns "
    "in Andhra Pradesh using machine learning models.\n\n"
    "📊 Data: 2015-2023 (3,015 days)\n"
    "🤖 Models: Prophet & XGBoost"
)

# ============================================================================
# PAGE 1: HOME
# ============================================================================

if page == "🏠 Home":
    st.title("⚡ Andhra Pradesh Electricity Demand Analysis")
    st.markdown("### Comprehensive Analysis & ML Forecasting")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📅 Data Period", "2015-2023", "3,015 Days")
    with col2:
        st.metric("📊 Data Points", "3,015", "Complete Dataset")
    with col3:
        st.metric("🎯 Models", "2", "Prophet + XGBoost")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📌 Project Overview")
        st.write("""
        This project analyzes electricity demand patterns in Andhra Pradesh 
        and provides forecasting using advanced machine learning models:
        
        ✅ **Data Exploration** - Understand demand trends and patterns
        ✅ **Visualizations** - 10+ charts for insights
        ✅ **Forecasting** - Prophet & XGBoost models
        ✅ **Predictions** - 365-day future forecast
        """)
    
    with col2:
        st.subheader("🎯 Key Metrics")
        df = load_data()
        if df is not None:
            st.write(f"""
            - **Average Demand:** {df['demand'].mean():.2f} MU
            - **Peak Demand:** {df['demand'].max():.2f} MU
            - **Min Demand:** {df['demand'].min():.2f} MU
            - **Std Dev:** {df['demand'].std():.2f} MU
            """)
    
    st.markdown("---")
    st.subheader("🚀 Quick Navigation")
    
    st.info("👈 Use the navigation menu on the left to explore different sections!")

# ============================================================================
# PAGE 2: DATA OVERVIEW
# ============================================================================

elif page == "📊 Data Overview":
    st.title("📊 Data Overview & Exploration")
    
    df = load_data()
    if df is not None:
        st.success("✓ Data loaded successfully!")
        
        # Summary Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        with col2:
            st.metric("Date Range", f"{df.index.min().strftime('%Y-%m-%d')}")
        with col3:
            st.metric("Average Demand", f"{df['demand'].mean():.2f} MU")
        with col4:
            st.metric("Max Demand", f"{df['demand'].max():.2f} MU")
        
        st.markdown("---")
        
        # Data Table
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10))
        
        # Statistical Summary
        st.subheader("Statistical Summary")
        st.write(df.describe())
        
        # Missing Values
        st.subheader("Data Quality")
        missing = df.isnull().sum()
        if missing.sum() == 0:
            st.success("✓ No missing values found!")
        else:
            st.warning("⚠️ Missing values detected:")
            st.write(missing[missing > 0])

# ============================================================================
# PAGE 3: VISUALIZATIONS
# ============================================================================

elif page == "📈 Visualizations":
    st.title("📈 Exploratory Data Analysis Visualizations")
    
    st.info("View all generated visualizations from the EDA phase")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Trends", "Seasonality", "Correlations", "Heatmaps"])
    
    with tab1:
        st.subheader("Demand Trends")
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_visualization("01_demand_over_time.png")
            if img:
                st.image(img, caption="Electricity Demand Over Time (2015-2023)")
        
        with col2:
            img = load_visualization("03_yearly_comparison.png")
            if img:
                st.image(img, caption="Average Demand by Year")
    
    with tab2:
        st.subheader("Seasonal Patterns")
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_visualization("02_monthly_seasonality.png")
            if img:
                st.image(img, caption="Monthly Average Demand")
        
        with col2:
            img = load_visualization("04_monthly_pattern.png")
            if img:
                st.image(img, caption="Average Demand by Month")
    
    with tab3:
        st.subheader("Correlations & External Factors")
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_visualization("05_temperature_correlation.png")
            if img:
                st.image(img, caption="Temperature vs Demand Correlation")
        
        with col2:
            img = load_visualization("06_holiday_impact.png")
            if img:
                st.image(img, caption="Holiday vs Work Day Impact")
    
    with tab4:
        st.subheader("Heatmaps")
        img = load_visualization("07_heatmap_monthly.png")
        if img:
            st.image(img, caption="Demand Heatmap: Year vs Month")

# ============================================================================
# PAGE 4: ML FORECASTING
# ============================================================================

elif page == "🤖 ML Forecasting":
    st.title("🤖 Machine Learning Forecasting Models")
    
    # Model Selection
    model_choice = st.radio(
        "Select Forecasting Model:",
        ["Prophet Model", "XGBoost Model", "Model Comparison"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if model_choice == "Prophet Model":
        st.subheader("📊 Facebook Prophet Forecast")
        st.write("""
        **Prophet** is ideal for:
        - Long-term trend forecasting (6-12 months)
        - Handling seasonal patterns
        - Managing special events and holidays
        - Providing confidence intervals
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            img = load_visualization("08_prophet_forecast.png")
            if img:
                st.image(img, caption="Prophet Forecast with Confidence Intervals")
        
        with col2:
            img = load_visualization("09_prophet_components.png")
            if img:
                st.image(img, caption="Prophet Components (Trend & Seasonality)")
        
        # Display forecast data
        prophet_forecast = load_prophet_forecast()
        if prophet_forecast is not None:
            st.subheader("Forecast Data (Next 365 Days)")
            st.write(f"Total predictions: {len(prophet_forecast)}")
            st.dataframe(
                prophet_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head(10)
            )
    
    elif model_choice == "XGBoost Model":
        st.subheader("🚀 XGBoost Forecast")
        st.write("""
        **XGBoost** is ideal for:
        - Short-term forecasting (1-30 days)
        - Capturing non-linear patterns
        - Operational/tactical decisions
        - Feature importance analysis
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            img = load_visualization("10_xgboost_forecast.png")
            if img:
                st.image(img, caption="XGBoost 30-Day Forecast")
        
        with col2:
            st.metric("Test MAE", "7.83 MU", "3.58% Error")
            st.metric("Test RMSE", "9.72 MU", "High Accuracy")
        
        # Display forecast data
        xgb_forecast = load_xgboost_forecast()
        if xgb_forecast is not None:
            st.subheader("Forecast Data (Next 30 Days)")
            st.dataframe(xgb_forecast.head(10))
    
    else:  # Model Comparison
        st.subheader("📊 Prophet vs XGBoost Comparison")
        
        comparison_data = {
            "Aspect": [
                "Time Horizon",
                "Seasonality Handling",
                "Speed",
                "Interpretability",
                "Best For",
                "Confidence Intervals"
            ],
            "Prophet": [
                "6-12 months",
                "Excellent",
                "Fast",
                "High",
                "Strategic Planning",
                "Yes"
            ],
            "XGBoost": [
                "1-30 days",
                "Good",
                "Medium",
                "Medium",
                "Operational Planning",
                "No"
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, hide_index=True)
        
        st.info("**Recommendation:** Use both models for complementary insights!")

# ============================================================================
# PAGE 5: INSIGHTS
# ============================================================================

elif page == "💡 Insights":
    st.title("💡 Key Insights & Findings")
    
    df = load_data()
    if df is not None:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success("📈 **Growth Trend**")
            growth = ((df['demand'].iloc[-1] - df['demand'].iloc[0]) / df['demand'].iloc[0] * 100)
            st.metric("YoY Growth", f"{growth:.1f}%", "Consistent Increase")
        
        with col2:
            st.info("🌞 **Seasonal Peak**")
            df['month'] = df.index.month
            monthly_avg = df.groupby('month')['demand'].mean()
            peak_month = monthly_avg.idxmax()
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            st.metric("Peak Month", months[peak_month-1], f"{monthly_avg.max():.1f} MU")
        
        with col3:
            st.warning("🌡️ **Temperature Effect**")
            if 'temp' in df.columns:
                correlation = df['temp'].corr(df['demand'])
                st.metric("Correlation", f"{correlation:.3f}", "Strong Positive")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Demand Statistics")
            stats = {
                "Mean": f"{df['demand'].mean():.2f} MU",
                "Median": f"{df['demand'].median():.2f} MU",
                "Std Dev": f"{df['demand'].std():.2f} MU",
                "Min": f"{df['demand'].min():.2f} MU",
                "Max": f"{df['demand'].max():.2f} MU",
                "Range": f"{df['demand'].max() - df['demand'].min():.2f} MU"
            }
            for key, value in stats.items():
                st.write(f"**{key}:** {value}")
        
        with col2:
            st.subheader("🎯 Business Implications")
            st.markdown("""
            1. **Summer Peak Planning** - Prepare for 30% higher demand in May-June
            2. **Temperature Sensitivity** - Monitor weather forecasts
            3. **Seasonal Staffing** - Adjust workforce for peak/off-peak seasons
            4. **Growth Capacity** - ~12% annual growth requires infrastructure expansion
            5. **Holiday Planning** - Lower demand during holidays, opportunity for maintenance
            """)
        
        st.markdown("---")
        st.subheader("🔮 Future Predictions")
        
        prophet_forecast = load_prophet_forecast()
        if prophet_forecast is not None:
            last_actual = df['demand'].iloc[-1]
            future_pred = prophet_forecast[prophet_forecast['ds'] > df.index[-1]]['yhat'].values
            if len(future_pred) > 0:
                pred_365 = future_pred[-1]
                expected_change = ((pred_365 - last_actual) / last_actual * 100)
                
                st.write(f"""
                **Next 365 Days Forecast (Prophet Model):**
                - Current demand: **{last_actual:.2f} MU**
                - Predicted (1 year): **{pred_365:.2f} MU**
                - Expected change: **{expected_change:+.1f}%**
                """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; margin-top: 50px;">
    <p>🔌 Andhra Pradesh Electricity Demand Analysis & Forecasting Dashboard</p>
    <p>Built with Streamlit | Data: 2015-2023 | Models: Prophet & XGBoost</p>
</div>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
# If you have XGBoost code, import it too

st.title("Andhra Pradesh Electricity Demand Analysis & Forecasting")

# Load data
df = load_data()
if df is not None:
    st.header("Key Insights")
st.write("- Strong summer peaks (Apr–Jun)")
st.write("- Positive correlation with temperature")
st.write("- Higher demand on weekdays/non-holidays")

st.header("Demand Over Time")
fig, ax = plt.subplots(figsize=(12,6))
df['demand'].plot(ax=ax)
st.pyplot(fig)

st.header("Temperature vs Demand Correlation")
fig, ax = plt.subplots()
sns.scatterplot(x='temp', y='demand', data=df, ax=ax)
st.pyplot(fig)

# Add more: Upload your existing PNGs or recreate plots here
st.header("Monthly Seasonality Heatmap")
# Recreate your heatmap code
fig, ax = plt.subplots()
# Your heatmap code...
st.pyplot(fig)

# Prophet Forecast (interactive)
st.header("Prophet Forecast")
# Load your trained model or retrain quickly
try:
    df_prophet = df[['Date', 'demand']].copy()
    df_prophet.columns = ['ds', 'y']
    m = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='multiplicative',
        changepoint_prior_scale=0.05
    )
    m.fit(df_prophet)
    # Forecast and plot
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    fig = m.plot(forecast)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"Prophet forecast error: {e}")

st.header("XGBoost 30-Day Forecast")
try:
    if os.path.exists('dashboards/visualizations/10_xgboost_forecast.png'):
        st.image('dashboards/visualizations/10_xgboost_forecast.png')
    else:
        st.info("XGBoost forecast visualization not available")
except Exception as e:
    st.warning(f"XGBoost forecast error: {e}")

st.header("All Visualizations")
viz_files = [
    '01_demand_over_time.png',
    '02_monthly_seasonality.png',
    '03_yearly_comparison.png',
    '04_monthly_pattern.png',
    '05_temperature_correlation.png',
    '06_holiday_impact.png',
    '07_heatmap_monthly.png',
    '08_prophet_forecast.png',
    '09_prophet_components.png',
    '10_xgboost_forecast.png'
]
for viz_file in viz_files:
    path = f'dashboards/visualizations/{viz_file}'
    if os.path.exists(path):
        st.image(path, caption=viz_file)
    else:
        st.warning(f"Missing: {viz_file}")