"""
Andhra Pradesh Electricity Demand Analysis - Flask Application
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
from PIL import Image
import os
from prophet import Prophet
import warnings
import webbrowser
from threading import Timer

warnings.filterwarnings('ignore')

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_SORT_KEYS'] = False

# Configure matplotlib with professional classic styling
plt.style.use('default')
# Professional color palette
sns.set_palette(["#2563eb", "#1e40af", "#3b82f6", "#64748b", "#10b981", "#f59e0b"])
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['grid.color'] = '#e2e8f0'
plt.rcParams['grid.alpha'] = 0.5
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = 0.8
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.left'] = True
plt.rcParams['axes.spines.bottom'] = True
plt.rcParams['axes.edgecolor'] = '#e2e8f0'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial']
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['text.color'] = '#1e293b'

# ============================================================================
# CACHING FUNCTIONS
# ============================================================================

_cache = {}

def load_data():
    """Load prepared dataset with caching"""
    if 'data' not in _cache:
        try:
            df = pd.read_csv('data/prepared_data.csv', index_col=0, parse_dates=True)
            _cache['data'] = df
        except FileNotFoundError:
            return None
    return _cache['data']

def get_prophet_forecast():
    """Load Prophet forecast with caching"""
    if 'prophet_forecast' not in _cache:
        try:
            df = pd.read_csv('data/prophet_forecast.csv')
            if 'ds' in df.columns:
                df['ds'] = pd.to_datetime(df['ds'])
            _cache['prophet_forecast'] = df
        except FileNotFoundError:
            return None
    return _cache['prophet_forecast']

def get_xgboost_forecast():
    """Load XGBoost forecast with caching"""
    if 'xgboost_forecast' not in _cache:
        try:
            df = pd.read_csv('data/xgboost_forecast.csv', index_col=0, parse_dates=True)
            _cache['xgboost_forecast'] = df
        except FileNotFoundError:
            return None
    return _cache['xgboost_forecast']

def get_data_summary(df):
    """Pre-calculate data summaries"""
    if df is None:
        return {}
    return {
        'mean': float(df['demand'].mean()),
        'max': float(df['demand'].max()),
        'min': float(df['demand'].min()),
        'std': float(df['demand'].std()),
        'median': float(df['demand'].median()),
        'records': len(df)
    }

def load_visualization(filename):
    """Load visualization image"""
    path = f'dashboards/visualizations/{filename}'
    if os.path.exists(path):
        with open(path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode()
        return img_data
    return None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string"""
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=80)
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    return img_base64

def create_line_chart():
    """Create line chart from data with professional styling"""
    df = load_data()
    if df is None:
        return None
    
    fig = Figure(figsize=(12, 5), facecolor='white')
    ax = fig.subplots()
    
    # Professional blue color
    ax.plot(df.index, df['demand'], linewidth=2, color='#2563eb', alpha=0.9)
    
    ax.set_title('Electricity Demand Over Time (2015-2023)', 
                 fontsize=15, fontweight=600, color='#1e293b', pad=15)
    ax.set_ylabel('Demand (MU)', fontsize=12, fontweight=500, color='#334155')
    ax.set_xlabel('Year', fontsize=12, fontweight=500, color='#334155')
    ax.grid(True, alpha=0.5, linestyle='--', linewidth=0.8, color='#e2e8f0')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e2e8f0')
    ax.spines['bottom'].set_color('#e2e8f0')
    
    return fig_to_base64(fig)

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def home():
    """Home page"""
    df = load_data()
    summary = get_data_summary(df) if df is not None else {}
    
    return render_template('home.html', summary=summary)

@app.route('/data-overview')
def data_overview():
    """Data overview page"""
    df = load_data()
    if df is None:
        return render_template('error.html', message="Data not found")
    
    summary = get_data_summary(df)
    
    # Get data table (first 10 rows)
    data_table = df.head(10).to_html(classes='table table-striped')
    
    # Get statistics
    stats = df.describe().to_html(classes='table table-striped')
    
    return render_template('data_overview.html', 
                         summary=summary,
                         data_table=data_table,
                         stats=stats)

@app.route('/visualizations')
def visualizations():
    """Visualizations page"""
    visualizations_data = {}
    
    # Load all visualization images
    viz_files = [
        '01_demand_over_time.png',
        '02_monthly_seasonality.png',
        '03_yearly_comparison.png',
        '04_monthly_pattern.png',
        '05_temperature_correlation.png',
        '06_holiday_impact.png',
        '07_heatmap_monthly.png'
    ]
    
    for viz_file in viz_files:
        img_data = load_visualization(viz_file)
        if img_data:
            visualizations_data[viz_file] = f"data:image/png;base64,{img_data}"
    
    return render_template('visualizations.html', visualizations=visualizations_data)

@app.route('/forecasting')
def forecasting():
    """ML Forecasting page"""
    df = load_data()
    prophet_forecast = get_prophet_forecast()
    
    forecast_data = {
        'summary': get_data_summary(df) if df is not None else {},
        'prophet_available': prophet_forecast is not None,
        'xgboost_available': get_xgboost_forecast() is not None
    }
    
    if prophet_forecast is not None:
        forecast_data['prophet_stats'] = {
            'count': len(prophet_forecast),
            'avg_2024': float(prophet_forecast[prophet_forecast['ds'].dt.year == 2024]['yhat'].mean()) if len(prophet_forecast[prophet_forecast['ds'].dt.year == 2024]) > 0 else 0,
            'avg_2025': float(prophet_forecast[prophet_forecast['ds'].dt.year == 2025]['yhat'].mean()) if len(prophet_forecast[prophet_forecast['ds'].dt.year == 2025]) > 0 else 0
        }
    
    return render_template('forecasting.html', **forecast_data)

@app.route('/insights')
def insights():
    """Insights page"""
    df = load_data()
    if df is None:
        return render_template('error.html', message="Data not found")
    
    summary = get_data_summary(df)
    
    # Calculate growth
    growth = ((df['demand'].iloc[-1] - df['demand'].iloc[0]) / df['demand'].iloc[0] * 100)
    
    # Peak month
    df['month'] = df.index.month
    monthly_avg = df.groupby('month')['demand'].mean()
    peak_month_idx = monthly_avg.idxmax()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    peak_month = months[peak_month_idx - 1]
    
    insights_data = {
        'summary': summary,
        'growth': round(growth, 1),
        'peak_month': peak_month,
        'peak_value': round(monthly_avg.max(), 0),
        'volatility': round((summary['std'] / summary['mean']) * 100, 1),
        'avg_yearly_growth': round(growth / 8, 1)
    }
    
    return render_template('insights.html', **insights_data)

@app.route('/api/data-stats')
def api_data_stats():
    """API endpoint for data statistics"""
    df = load_data()
    summary = get_data_summary(df)
    return jsonify(summary)

@app.route('/api/forecast-data')
def api_forecast_data():
    """API endpoint for forecast data"""
    prophet_forecast = get_prophet_forecast()
    if prophet_forecast is None:
        return jsonify({'error': 'Forecast not available'}), 404
    
    # Return first 30 rows
    data = prophet_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head(30).to_dict('records')
    return jsonify(data)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', message="Server error"), 500

def open_browser():
    """Open browser automatically after server starts"""
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Open browser after 1 second (gives server time to start)
    timer = Timer(1.0, open_browser)
    timer.daemon = True
    timer.start()
    
    app.run(debug=True, port=5000)
