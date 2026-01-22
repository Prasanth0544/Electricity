"""
Data Loading and Initial Exploration Script
Loads the AP Electricity Demand dataset and performs initial exploration
"""

import pandas as pd
import numpy as np
import os
import shutil
from pathlib import Path
import kagglehub

# Project data path
PROJECT_DATA_PATH = "data"

def copy_dataset_to_project():
    """Download and copy dataset files to project data folder for easier access"""
    os.makedirs(PROJECT_DATA_PATH, exist_ok=True)
    
    print("Downloading dataset from Kaggle...")
    try:
        # Download latest version
        path = kagglehub.dataset_download("ashtonronald/ap-dataset")
        print(f"Dataset downloaded to: {path}")
        
        # Copy main dataset file
        source_file = os.path.join(path, "finalAPData.csv")
        dest_file = os.path.join(PROJECT_DATA_PATH, "finalAPData.csv")
        
        if os.path.exists(source_file):
            shutil.copy2(source_file, dest_file)
            print(f"[OK] Copied finalAPData.csv to {PROJECT_DATA_PATH}/")
        else:
            print(f"[WARNING] {source_file} not found")
        
        # Also copy the detailed data.csv if needed
        source_file2 = os.path.join(path, "data.csv")
        dest_file2 = os.path.join(PROJECT_DATA_PATH, "data.csv")
        
        if os.path.exists(source_file2):
            shutil.copy2(source_file2, dest_file2)
            print(f"[OK] Copied data.csv to {PROJECT_DATA_PATH}/")
            
    except Exception as e:
        print(f"[ERROR] Failed to download dataset: {e}")

def load_data(file_path="data/finalAPData.csv"):
    """Load the dataset"""
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"[OK] Loaded {len(df)} rows and {len(df.columns)} columns")
    return df

def explore_data(df):
    """Perform initial data exploration"""
    print("\n" + "="*60)
    print("DATA EXPLORATION SUMMARY")
    print("="*60)
    
    # Basic info
    print("\n1. Dataset Shape:")
    print(f"   Rows: {df.shape[0]:,}")
    print(f"   Columns: {df.shape[1]}")
    
    # Column names
    print("\n2. Column Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    
    # Data types
    print("\n3. Data Types:")
    print(df.dtypes)
    
    # First few rows
    print("\n4. First 5 Rows:")
    print(df.head())
    
    # Missing values
    print("\n5. Missing Values:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("   [OK] No missing values found!")
    
    # Statistical summary
    print("\n6. Statistical Summary:")
    print(df.describe())
    
    # Date range
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        print("\n7. Date Range:")
        print(f"   Start: {df['Date'].min()}")
        print(f"   End: {df['Date'].max()}")
        print(f"   Total Days: {(df['Date'].max() - df['Date'].min()).days}")
    
    # Energy demand stats
    if 'Energy Required (MU)' in df.columns:
        print("\n8. Energy Demand Statistics:")
        energy_col = 'Energy Required (MU)'
        print(f"   Mean: {df[energy_col].mean():.2f} MU")
        print(f"   Median: {df[energy_col].median():.2f} MU")
        print(f"   Min: {df[energy_col].min():.2f} MU")
        print(f"   Max: {df[energy_col].max():.2f} MU")
        print(f"   Std Dev: {df[energy_col].std():.2f} MU")
    
    return df

def prepare_data(df):
    """Prepare data for analysis"""
    print("\n" + "="*60)
    print("DATA PREPARATION")
    print("="*60)
    
    # Convert date column
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        df.set_index('Date', inplace=True)
        print("[OK] Converted Date column and set as index")
    
    # Handle missing values
    if df.isnull().sum().sum() > 0:
        print("[OK] Filling missing values with forward fill...")
        df = df.ffill()
        df = df.bfill()  # Fill any remaining with backward fill
    
    # Rename energy column for easier access
    if 'Energy Required (MU)' in df.columns:
        df.rename(columns={'Energy Required (MU)': 'demand'}, inplace=True)
        print("[OK] Renamed 'Energy Required (MU)' to 'demand'")
    
    print("[OK] Data preparation complete!")
    return df

if __name__ == "__main__":
    print("="*60)
    print("AP ELECTRICITY DEMAND - DATA LOADING & EXPLORATION")
    print("="*60)
    
    # Step 1: Copy dataset to project folder
    print("\n[Step 1] Copying dataset to project folder...")
    copy_dataset_to_project()
    
    # Step 2: Load data
    print("\n[Step 2] Loading data...")
    df = load_data()
    
    # Step 3: Explore data
    print("\n[Step 3] Exploring data...")
    df = explore_data(df)
    
    # Step 4: Prepare data
    print("\n[Step 4] Preparing data...")
    df = prepare_data(df)
    
    # Step 5: Save prepared data
    output_path = "data/prepared_data.csv"
    df.to_csv(output_path)
    print(f"\n[OK] Saved prepared data to {output_path}")
    
    print("\n" + "="*60)
    print("DATA LOADING COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run '02_eda_visualization.py' for exploratory data analysis")
    print("2. Check the prepared_data.csv file in the data/ folder")
