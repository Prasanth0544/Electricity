# 🚀 Streamlit Deployment Guide

## Quick Start

### Run Locally

```bash
# Navigate to project directory
cd C:\Users\prasa\Desktop\visulization

# Run the Streamlit app
streamlit run app.py
```

The app will open at: `http://localhost:8501`

---

## 📱 Features

### Home Page
- Project overview and statistics
- Quick navigation to all sections
- Key metrics dashboard

### Data Overview
- Dataset summary (3,015 records)
- Statistical analysis
- Data quality checks
- Preview of raw data

### Visualizations
- 10+ high-quality charts organized by category:
  - **Trends**: Time series and yearly comparison
  - **Seasonality**: Monthly patterns
  - **Correlations**: Temperature impact, holiday effects
  - **Heatmaps**: Year-month demand patterns

### ML Forecasting
- **Prophet Model**: Long-term forecasts (365 days)
  - Trend analysis
  - Seasonal components
  - Confidence intervals
  
- **XGBoost Model**: Short-term forecasts (30 days)
  - High accuracy (3.58% error)
  - Feature importance analysis
  
- **Model Comparison**: Side-by-side comparison

### Insights
- Key findings and statistics
- Business implications
- Future predictions
- Growth trends

---

## 🌐 Deploy Online

### Option 1: Streamlit Cloud (Free)

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git push -u origin main
```

2. **Deploy to Streamlit Cloud**:
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repo
   - Choose `app.py` as entry point

### Option 2: Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Create requirements.txt (already exists)

# Deploy
heroku login
heroku create your-app-name
git push heroku main
```

### Option 3: AWS/Azure

Use Docker with the provided Dockerfile structure:

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 📊 File Structure

```
visulization/
├── app.py                           ← Main Streamlit app
├── requirements.txt                 ← Python dependencies
├── data/
│   ├── prepared_data.csv           ← Raw data for app
│   ├── prophet_forecast.csv        ← Prophet predictions
│   └── xgboost_forecast.csv        ← XGBoost predictions
└── dashboards/
    └── visualizations/             ← All PNG charts
        ├── 01_demand_over_time.png
        ├── 02_monthly_seasonality.png
        ├── ... (10 total)
```

---

## 🎯 Customization

### Change Port
```bash
streamlit run app.py --server.port=9000
```

### Change Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### Add New Pages

Create `pages/` folder with new `.py` files:
```bash
pages/
├── 1_Custom_Analysis.py
├── 2_Advanced_Models.py
└── 3_Settings.py
```

---

## 🐛 Troubleshooting

### Port already in use
```bash
streamlit run app.py --server.port=8502
```

### Cache issues
```bash
streamlit cache clear
streamlit run app.py
```

### Missing data files
- Ensure `data/` folder has all CSV files
- Run `01_data_loading.py` and `03_ml_forecasting.py` first

---

## 📈 Performance Tips

- Use `@st.cache_data` for expensive operations ✓
- Load images once, not on every rerun ✓
- Optimize visualizations with PNG format ✓

---

## 🔗 Access Your App

- **Local**: http://localhost:8501
- **Streamlit Cloud**: https://your-app-name.streamlit.app
- **Heroku**: https://your-app-name.herokuapp.com

---

**Ready to deploy!** 🚀
