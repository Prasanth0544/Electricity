# 🔌 Andhra Pradesh Electricity Demand Analysis & Forecasting

> A comprehensive visualization and machine learning project for analyzing and forecasting electricity demand patterns in Andhra Pradesh.

---

## 📊 Dataset

| Dataset | Description | Link |
|---------|-------------|------|
| **AP Electricity Demand** | Andhra Pradesh electricity demand forecast dataset (2015–2023) | [Kaggle - AP Dataset](https://www.kaggle.com/datasets/ashtonronald/ap-dataset) |

---

## ✅ Project Status

| Phase | Status | Notes |
|-------|--------|-------|
| Data Preparation | ✅ Complete | `01_data_loading.py` |
| EDA Visualizations | ✅ Complete | `02_eda_visualization.py` |
| ML Forecasting | ✅ Complete | `03_ml_forecasting.py` |
| Flask Dashboard | ✅ Complete | `app_flask.py` |
| Styling & CSS | ✅ Complete | Teal theme applied |
| Documentation | ✅ Complete | README, QUICK_START, GUIDE |

---

## 🛠️ Project Phases

### Phase 1: Data Preparation ✅

- Load and explore dataset (3,015 records)
- Data cleaning and preprocessing  
- Feature engineering (day types, months)
- Save prepared data to CSV

### Phase 2: Visualization Dashboard ✅

| Visual | Description |
|--------|-------------|
| 📈 Line Chart | Demand over time (2015-2023) |
| 📊 Bar Chart | Yearly/monthly comparisons |
| 🌡️ Heatmap | Month vs Year patterns |
| ⚡ Scatter Plot | Temperature correlation |
| 🎉 Holiday Impact | Work days vs holidays |

### Phase 3: Machine Learning ✅

| Model | Purpose | Accuracy |
|-------|---------|----------|
| **Prophet** | Long-term forecasting (6-12 months) | Good |
| **XGBoost** | Short-term forecasting (1-30 days) | ~96% |

### Phase 4: Web Dashboard ✅

- Flask-based web application
- Interactive tabs and navigation
- Responsive design (mobile-friendly)
- Professional teal color theme

---

## 📁 Project Structure

```
visulization/
├── app_flask.py            # Flask Dashboard
├── 01_data_loading.py      # Data preparation
├── 02_eda_visualization.py # Visualizations
├── 03_ml_forecasting.py    # ML models
├── run_flask.bat/.sh       # Quick launchers
├── requirements.txt        # Dependencies
├── static/style.css        # Styling
├── templates/              # HTML pages
├── data/                   # Datasets
└── dashboards/             # Chart images
```

---

## 🎯 Key Insights

- 📈 **Demand peaks in summer** (temperature correlation r ≈ 0.5)
- 📊 **Steady growth**: ~3-5% annual increase
- ⚡ **Seasonal patterns**: Higher in March-June
- 🎉 **Holiday effect**: Slight decrease on holidays

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
python app_flask.py

# Open browser: http://127.0.0.1:5000
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview |
| [QUICK_START.md](QUICK_START.md) | Quick start guide |
| [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) | Dashboard development guide |

---

> **Project Title**: AP Electricity Demand Visualization & ML Forecasting (Prophet/XGBoost)