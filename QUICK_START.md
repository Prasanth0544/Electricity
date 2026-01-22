# 🚀 Quick Start Guide

Get the AP Electricity Dashboard running in minutes!

---

## ⚡ Fastest Way to Start

### Windows
```bash
# Double-click or run:
run_flask.bat
```

### Manual Start
```bash
pip install -r requirements.txt
python app_flask.py
```

Then open: **http://127.0.0.1:5000**

---

## 📊 Run Analysis Scripts (Optional)

If you want to regenerate visualizations or forecasts:

### 1. Load Data
```bash
python 01_data_loading.py
```
- Prepares the dataset
- Saves to `data/prepared_data.csv`

### 2. Generate Visualizations
```bash
python 02_eda_visualization.py
```
- Creates 7+ charts
- Saves to `dashboards/visualizations/`

### 3. Run ML Forecasting
```bash
python 03_ml_forecasting.py
```
- Trains Prophet & XGBoost models
- Generates forecasts

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app_flask.py` | Main dashboard app |
| `run_flask.bat` | Quick launcher (Windows) |
| `requirements.txt` | Dependencies |
| `static/style.css` | Dashboard styling |
| `templates/` | HTML pages |

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | Run `pip install -r requirements.txt` |
| Port in use | Change port in `app_flask.py` |
| Charts missing | Run `python 02_eda_visualization.py` |

---

**Ready?** Run `run_flask.bat` or `python app_flask.py` 🚀
