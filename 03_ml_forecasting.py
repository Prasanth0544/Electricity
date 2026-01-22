"""
Machine Learning Forecasting for AP Electricity Demand
Implements Prophet and XGBoost models for time-series forecasting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("[WARNING] Prophet not installed. Install with: pip install prophet")

try:
    from xgboost import XGBRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("[WARNING] XGBoost not installed. Install with: pip install xgboost scikit-learn")

def load_prepared_data(file_path="data/prepared_data.csv"):
    """Load the prepared dataset"""
    print(f"Loading prepared data from {file_path}...")
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    print(f"[OK] Loaded {len(df)} rows")
    return df

def prophet_forecast(df, periods=365):
    """
    Forecast using Facebook Prophet
    periods: number of days to forecast ahead
    """
    if not PROPHET_AVAILABLE:
        print("[WARNING] Prophet not available. Skipping Prophet forecast.")
        return None, None
    
    print("\n" + "="*60)
    print("PROPHET FORECASTING MODEL")
    print("="*60)
    
    # Prepare data for Prophet (requires 'ds' and 'y' columns)
    prophet_df = df.reset_index()[['Date', 'demand']].copy()
    prophet_df.columns = ['ds', 'y']
    
    print(f"Training Prophet model on {len(prophet_df)} data points...")
    
    # Initialize and fit model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,  # We have daily data, not hourly
        seasonality_mode='multiplicative',
        changepoint_prior_scale=0.05
    )
    
    # Add temperature as regressor if available
    if 'temp' in df.columns:
        temp_data = df.reset_index()[['Date', 'temp']].copy()
        temp_data.columns = ['ds', 'temp']
        prophet_df = prophet_df.merge(temp_data, on='ds', how='left')
        model.add_regressor('temp')
        print("[OK] Added temperature as external regressor")
    
    model.fit(prophet_df)
    print("[OK] Model trained successfully")
    
    # Create future dataframe
    future = model.make_future_dataframe(periods=periods)
    
    # Add temperature to future if available
    if 'temp' in df.columns:
        # Use last known temperature or average for future dates
        last_temp = df['temp'].iloc[-1]
        future = future.merge(temp_data, on='ds', how='left')
        future['temp'] = future['temp'].fillna(last_temp)
    
    # Make predictions
    print(f"Generating forecast for next {periods} days...")
    forecast = model.predict(future)
    
    print("[OK] Forecast complete")
    
    return model, forecast

def plot_prophet_forecast(model, forecast, output_path="dashboards/visualizations/08_prophet_forecast.png"):
    """Plot Prophet forecast results"""
    if model is None:
        return
    
    print("Creating Prophet forecast visualization...")
    
    fig = model.plot(forecast, figsize=(14, 8))
    ax = fig.gca()
    ax.set_title('Prophet Forecast: AP Electricity Demand', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Energy Required (MU)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {output_path}")

def plot_prophet_components(model, forecast, output_path="dashboards/visualizations/09_prophet_components.png"):
    """Plot Prophet forecast components"""
    if model is None:
        return
    
    print("Creating Prophet components visualization...")
    
    fig = model.plot_components(forecast, figsize=(14, 10))
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {output_path}")

def xgboost_forecast(df, forecast_days=30):
    """
    Forecast using XGBoost with lag features
    forecast_days: number of days to forecast ahead
    """
    if not XGBOOST_AVAILABLE:
        print("[WARNING] XGBoost not available. Skipping XGBoost forecast.")
        return None, None, None
    
    print("\n" + "="*60)
    print("XGBOOST FORECASTING MODEL")
    print("="*60)
    
    # Create a copy for feature engineering
    df_ml = df.copy()
    
    # Feature engineering - create lag features
    print("Creating lag features...")
    df_ml['lag_1'] = df_ml['demand'].shift(1)
    df_ml['lag_7'] = df_ml['demand'].shift(7)  # Weekly lag
    df_ml['lag_30'] = df_ml['demand'].shift(30)  # Monthly lag
    
    # Rolling statistics
    df_ml['rolling_mean_7'] = df_ml['demand'].rolling(window=7).mean()
    df_ml['rolling_mean_30'] = df_ml['demand'].rolling(window=30).mean()
    df_ml['rolling_std_7'] = df_ml['demand'].rolling(window=7).std()
    
    # Time-based features
    df_ml['year'] = df_ml.index.year
    df_ml['month'] = df_ml.index.month
    df_ml['day_of_year'] = df_ml.index.dayofyear
    df_ml['day_of_week'] = df_ml.index.dayofweek
    
    # Add temperature if available
    features = ['lag_1', 'lag_7', 'lag_30', 'rolling_mean_7', 
                'rolling_mean_30', 'rolling_std_7',
                'year', 'month', 'day_of_year', 'day_of_week']
    
    if 'temp' in df_ml.columns:
        features.append('temp')
    
    # Remove rows with NaN (from lag features)
    df_ml = df_ml.dropna()
    
    # Split into train and test
    train_size = len(df_ml) - forecast_days
    train = df_ml.iloc[:train_size]
    test = df_ml.iloc[train_size:]
    
    print(f"Training on {len(train)} samples, testing on {len(test)} samples")
    
    # Prepare features and target
    X_train = train[features]
    y_train = train['demand']
    X_test = test[features]
    y_test = test['demand']
    
    # Train XGBoost model
    print("Training XGBoost model...")
    model = XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)
    print("[OK] Model trained successfully")
    
    # Make predictions on test set
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)
    
    # Calculate metrics
    train_mae = mean_absolute_error(y_train, train_predictions)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_predictions))
    test_mae = mean_absolute_error(y_test, test_predictions)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_predictions))
    
    print(f"\nModel Performance:")
    print(f"  Train MAE: {train_mae:.2f} MU")
    print(f"  Train RMSE: {train_rmse:.2f} MU")
    print(f"  Test MAE: {test_mae:.2f} MU")
    print(f"  Test RMSE: {test_rmse:.2f} MU")
    print(f"  Test MAE %: {(test_mae / y_test.mean() * 100):.2f}%")
    
    # Generate future forecast
    print(f"\nGenerating forecast for next {forecast_days} days...")
    future_forecast = []
    last_data = df_ml.iloc[-1:].copy()
    
    for i in range(forecast_days):
        # Prepare features for next day
        next_date = df_ml.index[-1] + pd.Timedelta(days=i+1)
        next_row = last_data.copy()
        next_row.index = [next_date]
        
        # Update lag features (use previous predictions)
        if i == 0:
            next_row['lag_1'] = df_ml['demand'].iloc[-1]
        else:
            next_row['lag_1'] = future_forecast[-1]
        
        if i < 7:
            next_row['lag_7'] = df_ml['demand'].iloc[-(7-i)]
        else:
            next_row['lag_7'] = future_forecast[i-7]
        
        if i < 30:
            next_row['lag_30'] = df_ml['demand'].iloc[-(30-i)]
        else:
            next_row['lag_30'] = future_forecast[i-30]
        
        # Update rolling features (simplified - use recent average)
        next_row['rolling_mean_7'] = df_ml['demand'].tail(7).mean()
        next_row['rolling_mean_30'] = df_ml['demand'].tail(30).mean()
        next_row['rolling_std_7'] = df_ml['demand'].tail(7).std()
        
        # Update time features
        next_row['year'] = next_date.year
        next_row['month'] = next_date.month
        next_row['day_of_year'] = next_date.dayofyear
        next_row['day_of_week'] = next_date.dayofweek
        
        # Predict
        X_next = next_row[features]
        prediction = model.predict(X_next)[0]
        future_forecast.append(prediction)
        
        # Update for next iteration
        next_row['demand'] = prediction
        last_data = next_row
    
    # Create forecast dataframe
    future_dates = pd.date_range(start=df_ml.index[-1] + pd.Timedelta(days=1), 
                                 periods=forecast_days, freq='D')
    forecast_df = pd.DataFrame({
        'date': future_dates,
        'forecast': future_forecast
    })
    forecast_df.set_index('date', inplace=True)
    
    print("[OK] Forecast complete")
    
    return model, (test.index, y_test, test_predictions), forecast_df

def plot_xgboost_results(test_data, forecast_df, output_path="dashboards/visualizations/10_xgboost_forecast.png"):
    """Plot XGBoost forecast results"""
    if test_data is None:
        return
    
    print("Creating XGBoost forecast visualization...")
    
    test_dates, y_test, test_predictions = test_data
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot historical data (last 90 days)
    historical_start = test_dates[0] - pd.Timedelta(days=90)
    # This would need the full df, so we'll just plot test period
    ax.plot(test_dates, y_test, label='Actual', linewidth=2, color='#2E86AB', marker='o', markersize=3)
    ax.plot(test_dates, test_predictions, label='Predicted (Test)', 
            linewidth=2, color='#A23B72', linestyle='--', marker='s', markersize=3)
    
    # Plot future forecast
    if forecast_df is not None:
        ax.plot(forecast_df.index, forecast_df['forecast'], 
                label='Future Forecast', linewidth=2, color='#F18F01', linestyle=':', marker='^', markersize=3)
    
    ax.set_title('XGBoost Forecast: AP Electricity Demand', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Energy Required (MU)', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {output_path}")

def save_forecast_results(forecast_df, output_path="data/forecast_results.csv"):
    """Save forecast results to CSV"""
    if forecast_df is not None:
        forecast_df.to_csv(output_path)
        print(f"[OK] Saved forecast results to {output_path}")

if __name__ == "__main__":
    import os
    
    print("="*60)
    print("AP ELECTRICITY DEMAND - MACHINE LEARNING FORECASTING")
    print("="*60)
    
    # Create output directory
    os.makedirs("dashboards/visualizations", exist_ok=True)
    
    # Load data
    df = load_prepared_data()
    
    # Prophet Forecast
    if PROPHET_AVAILABLE:
        # Forecast until end of 2025
        # Current data ends May 2023.
        # Days to end of 2023 (~230) + 2024 (366) + 2025 (365) ~= 961 days
        # Let's forecast 1000 days to be safe
        periods = 1000
        model_prophet, forecast_prophet = prophet_forecast(df, periods=periods)
        if model_prophet is not None:
            plot_prophet_forecast(model_prophet, forecast_prophet)
            plot_prophet_components(model_prophet, forecast_prophet)
            
            # Save forecast
            forecast_prophet_df = forecast_prophet[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
            forecast_prophet_df.set_index('ds', inplace=True)
            forecast_prophet_df.to_csv("data/prophet_forecast.csv")
            print("[OK] Saved Prophet forecast to data/prophet_forecast.csv")
    else:
        print("\n[WARNING] Install Prophet to use: pip install prophet")
    
    # XGBoost Forecast
    if XGBOOST_AVAILABLE:
        model_xgb, test_data, forecast_xgb = xgboost_forecast(df, forecast_days=30)
        if model_xgb is not None:
            plot_xgboost_results(test_data, forecast_xgb)
            save_forecast_results(forecast_xgb, "data/xgboost_forecast.csv")
    else:
        print("\n[WARNING] Install XGBoost to use: pip install xgboost scikit-learn")
    
    print("\n" + "="*60)
    print("FORECASTING COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review forecast visualizations in dashboards/visualizations/")
    print("2. Use forecast data for your dashboard")
    print("3. Compare model performance and choose the best one")
