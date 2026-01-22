# 🔌 Andhra Pradesh Electricity Demand Analysis & Forecasting

> A comprehensive visualization and machine learning project for analyzing and forecasting electricity demand patterns in Andhra Pradesh.

---

## 📊 Recommended Dataset Links

### Primary Recommendation (Best for this project)
| Dataset | Description | Link |
|---------|-------------|------|
| **AP Electricity Demand** | Andhra Pradesh electricity demand forecast dataset (2019–2023) with daily/hourly features including demand, temperature, holidays — perfect for ML forecasting | [Kaggle - AP Dataset](https://www.kaggle.com/datasets/ashtonronald/ap-dataset) |

### Alternative/Complementary Sources
| Dataset | Description | Link |
|---------|-------------|------|
| Energy Demanded vs. Met | Energy demand data (2012–2023, monthly/daily) — great for trend analysis | [Kaggle - CSV Data](https://www.kaggle.com/datasets/ashishkumarak/csv-for-same-period) |
| Official CEA Dashboard | Central Electricity Authority — monthly reports & state-wise data | [CEA Dashboard](https://cea.nic.in/dashboard?lang=en) |
| All India Statistics (PDF) | General Review 2025 — comprehensive state-level electricity data | [CEA PDF Report](https://cea.nic.in/wp-content/uploads/general/2025/Updated_GR_2025_merged_new.pdf) |
| Ember Energy Data | Monthly CSV downloads (generation/consumption by state) — filter for AP | [Ember Energy](https://ember-energy.org/data/india-electricity-data) |

> [!TIP]
> Download the **first Kaggle dataset** — it's clean and ready for both visualization + ML!

---

## 🛠️ Project Phases

### Phase 1: Data Preparation (Python)

**Tools**: Jupyter Notebook / Google Colab (free if no local setup)

#### Step 1: Load & Explore Data
```python
import pandas as pd

# Load the dataset
df = pd.read_csv('your_downloaded_file.csv')  # e.g., ap-dataset.csv
df.head()  # Check columns (date, demand, temp, etc.)
```

#### Step 2: Data Preprocessing
```python
# Convert date column
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
df = df.sort_index()

# Basic cleaning
df.isnull().sum()
df.fillna(method='ffill', inplace=True)
```

#### Step 3: Exploratory Data Analysis (EDA)
```python
# Plot demand trends
df['demand'].plot(figsize=(12, 6), title='Electricity Demand Over Time')

# Monthly seasonality
df.resample('M').mean().plot(title='Monthly Average Demand')
```

---

### Phase 2: Visualization Dashboard

**Tools**: Power BI Desktop (free) or Tableau Public (free)

#### Key Visualizations
| Visual Type | Purpose |
|-------------|---------|
| 📈 **Line Chart** | Demand over time (yearly/monthly trends) |
| 📊 **Area Chart** | Peak vs. off-peak demand patterns |
| 🌡️ **Heatmap** | Hourly demand patterns |
| 🔢 **KPI Cards** | Average demand, growth rate |
| ⚡ **Scatter Plot** | Temperature vs. demand correlation |

#### Dashboard Features
- ✅ Date slicer for time-range filtering
- ✅ Interactive filters
- ✅ Drill-down capabilities

#### Publishing Options
| Platform | Action |
|----------|--------|
| Power BI | Publish → Generate shareable link |
| Tableau | Upload to Tableau Public gallery |

> [!NOTE]
> **Reference Dashboards**: Search for electricity demand dashboards on LinkedIn, YouTube, and professional portfolio sites for design inspiration.

---

### Phase 3: Machine Learning (Time-Series Forecasting)

> This adds AIML strength — forecast future demand (e.g., next 30 days to 1 year)

#### Option A: Facebook Prophet (Recommended for Beginners)

```python
from prophet import Prophet
# pip install prophet

# Prepare data for Prophet
m_df = df.reset_index()[['date', 'demand']]
m_df.columns = ['ds', 'y']

# Build model
model = Prophet(
    yearly_seasonality=True, 
    weekly_seasonality=True, 
    daily_seasonality=True
)
model.fit(m_df)

# Forecast 1 year ahead
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

# Visualize forecast
model.plot(forecast)
```

#### Option B: XGBoost (Advanced)

```python
from sklearn.metrics import mean_absolute_error
import numpy as np
from xgboost import XGBRegressor

# Feature engineering - Add lag features
df['lag1'] = df['demand'].shift(1)
df['lag7'] = df['demand'].shift(7)  # Weekly lag

# Train-test split
train = df[:-30]
test = df[-30:]

# Fit model
model = XGBRegressor()
model.fit(train[['lag1', 'lag7']], train['demand'])
predictions = model.predict(test[['lag1', 'lag7']])
```

#### Model Evaluation

| Metric | Target |
|--------|--------|
| MAE (Mean Absolute Error) | < 10% of average demand |
| RMSE (Root Mean Square Error) | < 10% of average demand |

---

## 🎯 Expected Insights

- 📈 **Demand peaks in summer** (correlation with temperature r ≈ 0.8)
- 📊 **Forecasted growth**: ~15% increase in 2026
- ⚡ **Seasonal patterns**: Higher consumption during festival periods
- 🌡️ **Temperature correlation**: Strong positive relationship

---

## 📁 Portfolio Presentation

### GitHub Repository Structure
```
visulization/
├── 📓 notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_eda_visualization.ipynb
│   └── 03_ml_forecasting.ipynb
├── 📊 dashboards/
│   └── screenshots/
├── 📂 data/
│   └── ap-dataset.csv
├── 📄 README.md
└── 📄 plan.md
```

### Project Title Suggestion
> **"AP Electricity Demand Visualization & ML Forecasting (Prophet/XGBoost)"**

### What Makes This Project Stand Out
- ✅ Regional focus (Andhra Pradesh) — unique and relevant
- ✅ End-to-end pipeline (Data → Visualization → ML)
- ✅ Interactive dashboards with real insights
- ✅ Time-series forecasting with multiple models
- ✅ Clean, well-documented code

---

## 🚀 Next Steps

- [ ] Download dataset from Kaggle
- [ ] Set up Jupyter Notebook environment
- [ ] Complete data preparation & EDA
- [ ] Build Power BI / Tableau dashboard
- [ ] Implement Prophet forecasting model
- [ ] (Optional) Implement XGBoost model
- [ ] Create GitHub repository with documentation
- [ ] Publish dashboard & share links

---

> [!IMPORTANT]
> This combo of **visualization + ML forecasting** will stand out uniquely — few students do local AP energy with forecasting. A great addition to your portfolio! 🎓