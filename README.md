# 🔌 Andhra Pradesh Electricity Demand Analysis & Forecasting

A comprehensive visualization and machine learning project for analyzing and forecasting electricity demand patterns in Andhra Pradesh.

## 📋 Project Overview

This project analyzes electricity demand data for Andhra Pradesh from 2015-2023, creating visualizations and implementing machine learning models for forecasting future demand.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Dataset

The dataset is downloaded and prepared when you run the data loading script:

```bash
python 01_data_loading.py
```

This will:
- Copy dataset to project folder
- Load and explore the data
- Prepare data for analysis
- Save prepared data to `data/prepared_data.csv`

#### Step 2: Create Visualizations
```bash
python 02_eda_visualization.py
```

This will generate:
- Demand over time plot
- Monthly seasonality patterns
- Yearly comparisons
- Temperature correlations
- Holiday impact analysis
- Heatmaps

All visualizations are saved to `dashboards/visualizations/`

#### Step 3: Machine Learning Forecasting
```bash
python 03_ml_forecasting.py
```

This will:
- Train Prophet model for time-series forecasting
- Train XGBoost model with lag features
- Generate forecasts for future periods
- Create forecast visualizations
- Save forecast results to CSV

## 📁 Project Structure

```
visulization/
├── app.py                      # Streamlit Dashboard App
├── 01_data_loading.py          # Data loading and exploration
├── 02_eda_visualization.py     # EDA and visualizations
├── 03_ml_forecasting.py        # ML forecasting models
├── requirements.txt            # Python dependencies
├── plan.md                     # Project plan and roadmap
├── README.md                   # This file
├── data/                       # Dataset files
│   ├── finalAPData.csv
│   ├── prepared_data.csv
│   └── forecast_results.csv
├── notebooks/                  # (Optional) Jupyter notebooks
└── dashboards/                 # Visualizations and dashboards
    └── visualizations/         # Generated plots and charts
```

## 📊 Dataset Information

- **Source**: [Kaggle - AP Dataset](https://www.kaggle.com/datasets/ashtonronald/ap-dataset)
- **Time Period**: 2015-2023
- **Features**:
  - Date
  - Energy Required (MU)
  - Temperature
  - Rainfall
  - Inflation
  - Day of week
  - Holiday indicators

## 🎯 Key Insights

- **Demand Trends**: Analyze electricity demand patterns over time
- **Seasonality**: Identify monthly and yearly patterns
- **Temperature Correlation**: Understand relationship between temperature and demand
- **Holiday Impact**: Compare demand on holidays vs work days
- **Forecasting**: Predict future demand using ML models

## 🛠️ Technologies Used

- **Python**: Data processing and analysis
- **Pandas**: Data manipulation
- **Matplotlib/Seaborn**: Visualization
- **Prophet**: Time-series forecasting
- **XGBoost**: Machine learning forecasting

## 📈 Next Steps

1. ✅ Download dataset
2. ✅ Run data loading script
3. ✅ Generate visualizations
4. ✅ Implement forecasting models
5. 🔄 Build Power BI/Tableau dashboard (optional)
6. 🔄 Deploy interactive dashboard (optional)

## 📝 Notes

- Make sure you have Kaggle credentials set up for dataset download
- Install all dependencies from `requirements.txt`
- Visualizations are saved as high-resolution PNG files
- Forecast results are saved as CSV files for further analysis

## 🤝 Contributing

This is a portfolio project. Feel free to fork and modify for your own use!

---

**Project Title**: AP Electricity Demand Visualization & ML Forecasting (Prophet/XGBoost)
