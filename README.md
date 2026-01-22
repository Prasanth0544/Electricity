# 🔌 Andhra Pradesh Electricity Demand Analysis & Forecasting

A comprehensive visualization and machine learning project for analyzing and forecasting electricity demand patterns in Andhra Pradesh.

## 📋 Project Overview

This project analyzes electricity demand data for Andhra Pradesh from 2015-2023, creating visualizations and implementing machine learning models for forecasting future demand. It includes an interactive Flask web dashboard.

## 🚀 Quick Start

### Option 1: Run the Dashboard (Recommended)

**Windows:**
```bash
run_flask.bat
```

**Or manually:**
```bash
pip install -r requirements.txt
python app_flask.py
```

Then open: **http://127.0.0.1:5000**

### Option 2: Run Analysis Scripts

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Load Data
```bash
python 01_data_loading.py
```

#### Step 3: Create Visualizations
```bash
python 02_eda_visualization.py
```

#### Step 4: Run ML Forecasting
```bash
python 03_ml_forecasting.py
```

## 📁 Project Structure

```
visulization/
├── app_flask.py            # Flask Dashboard App
├── 01_data_loading.py      # Data loading and exploration
├── 02_eda_visualization.py # EDA and visualizations
├── 03_ml_forecasting.py    # ML forecasting models
├── requirements.txt        # Python dependencies
├── run_flask.bat/.sh       # Quick launchers
├── README.md               # This file
├── QUICK_START.md          # Quick start guide
├── DASHBOARD_GUIDE.md      # Dashboard development guide
├── plan.md                 # Project plan
├── static/
│   └── style.css           # Dashboard styling
├── templates/              # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── data_overview.html
│   ├── visualizations.html
│   ├── forecasting.html
│   └── insights.html
├── data/                   # Dataset files
│   ├── finalAPData.csv
│   ├── prepared_data.csv
│   ├── prophet_forecast.csv
│   └── xgboost_forecast.csv
├── notebooks/              # Jupyter notebooks
└── dashboards/
    └── visualizations/     # Generated plots
```

## 📊 Dataset Information

- **Source**: [Kaggle - AP Dataset](https://www.kaggle.com/datasets/ashtonronald/ap-dataset)
- **Time Period**: 2015-2023
- **Records**: 3,015 daily observations
- **Features**:
  - Date
  - Energy Required (MU)
  - Temperature
  - Rainfall
  - Inflation
  - Day of week
  - Holiday indicators

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **Interactive Dashboard** | Flask-based web interface |
| **Data Exploration** | View dataset statistics and preview |
| **Visualizations** | 10+ analytical charts |
| **ML Forecasting** | Prophet & XGBoost models |
| **Responsive Design** | Works on all screen sizes |

## 🛠️ Technologies Used

- **Python 3.10+** - Core language
- **Flask** - Web framework
- **Pandas** - Data manipulation
- **Matplotlib/Seaborn** - Visualization
- **Prophet** - Time-series forecasting
- **XGBoost** - Machine learning forecasting
- **Bootstrap 5** - UI framework

## � Dashboard Pages

1. **Home** - Overview and key metrics
2. **Data Overview** - Dataset statistics and preview
3. **Visualizations** - EDA charts (trends, seasonality, correlations)
4. **Forecasting** - ML model predictions
5. **Insights** - Key findings and recommendations

## 🤝 Contributing

This is a portfolio project. Feel free to fork and modify for your own use!

---

**Author**: Prasanth  
**Project**: AP Electricity Demand Visualization & ML Forecasting
