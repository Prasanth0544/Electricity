"""
Exploratory Data Analysis and Visualization
Creates comprehensive visualizations of the AP Electricity Demand data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_prepared_data(file_path="data/prepared_data.csv"):
    """Load the prepared dataset"""
    print(f"Loading prepared data from {file_path}...")
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    print(f"[OK] Loaded {len(df)} rows")
    return df

def create_output_dir():
    """Create output directory for visualizations"""
    os.makedirs("dashboards/visualizations", exist_ok=True)
    return "dashboards/visualizations"

def plot_demand_over_time(df, output_dir):
    """Plot 1: Electricity demand over time"""
    print("Creating: Demand over time plot...")
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df.index, df['demand'], linewidth=1.5, alpha=0.8, color='#2E86AB')
    ax.set_title('Andhra Pradesh Electricity Demand Over Time (2015-2023)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Energy Required (MU)', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/01_demand_over_time.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: 01_demand_over_time.png")

def plot_monthly_seasonality(df, output_dir):
    """Plot 2: Monthly average demand"""
    print("Creating: Monthly seasonality plot...")
    
    # Select only numeric columns for resampling
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    monthly_avg = df[numeric_cols].resample('M').mean()
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(monthly_avg.index, monthly_avg['demand'], 
            marker='o', linewidth=2, markersize=4, color='#A23B72')
    ax.set_title('Monthly Average Electricity Demand', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Average Energy Required (MU)', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/02_monthly_seasonality.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: 02_monthly_seasonality.png")

def plot_yearly_comparison(df, output_dir):
    """Plot 3: Yearly comparison"""
    print("Creating: Yearly comparison plot...")
    
    df['year'] = df.index.year
    df['month'] = df.index.month
    
    yearly_avg = df.groupby('year')['demand'].mean()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(yearly_avg.index, yearly_avg.values, color='#F18F01', alpha=0.8)
    ax.set_title('Average Electricity Demand by Year', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average Energy Required (MU)', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/03_yearly_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: 03_yearly_comparison.png")

def plot_monthly_pattern(df, output_dir):
    """Plot 4: Average demand by month"""
    print("Creating: Monthly pattern plot...")
    
    df['month'] = df.index.month
    monthly_pattern = df.groupby('month')['demand'].mean()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(range(1, 13), monthly_pattern.values, color='#C73E1D', alpha=0.8)
    ax.set_title('Average Electricity Demand by Month', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Average Energy Required (MU)', fontsize=12)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/04_monthly_pattern.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: 04_monthly_pattern.png")

def plot_temperature_correlation(df, output_dir):
    """Plot 5: Temperature vs Demand correlation"""
    print("Creating: Temperature correlation plot...")
    
    if 'temp' in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(df['temp'], df['demand'], 
                           alpha=0.5, s=20, c=df['demand'], 
                           cmap='viridis', edgecolors='black', linewidth=0.5)
        
        # Calculate correlation
        correlation = df['temp'].corr(df['demand'])
        
        ax.set_title(f'Temperature vs Electricity Demand (Correlation: {correlation:.3f})', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Temperature (°C)', fontsize=12)
        ax.set_ylabel('Energy Required (MU)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.colorbar(scatter, ax=ax, label='Demand (MU)')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/05_temperature_correlation.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: 05_temperature_correlation.png")
    else:
        print("[WARNING] Temperature column not found, skipping...")

def plot_holiday_impact(df, output_dir):
    """Plot 6: Holiday vs Work day comparison"""
    print("Creating: Holiday impact plot...")
    
    if 'Holiday' in df.columns:
        holiday_stats = df.groupby('Holiday')['demand'].agg(['mean', 'std', 'count'])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        categories = holiday_stats.index
        means = holiday_stats['mean'].values
        
        bars = ax.bar(categories, means, color=['#06A77D', '#F77F00'], alpha=0.8)
        ax.set_title('Average Electricity Demand: Holiday vs Work Days', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Day Type', fontsize=12)
        ax.set_ylabel('Average Energy Required (MU)', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/06_holiday_impact.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Saved: 06_holiday_impact.png")
    else:
        print("[WARNING] Holiday column not found, skipping...")

def plot_heatmap_monthly(df, output_dir):
    """Plot 7: Heatmap of demand by month and year"""
    print("Creating: Monthly heatmap...")
    
    df['year'] = df.index.year
    df['month'] = df.index.month
    
    pivot_data = df.pivot_table(values='demand', index='year', columns='month', aggfunc='mean')
    
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='YlOrRd', 
                cbar_kws={'label': 'Energy Required (MU)'}, ax=ax)
    ax.set_title('Electricity Demand Heatmap: Year vs Month', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Year', fontsize=12)
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_xticklabels(month_names)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/07_heatmap_monthly.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: 07_heatmap_monthly.png")

def generate_summary_statistics(df, output_dir):
    """Generate summary statistics report"""
    print("Generating summary statistics...")
    
    stats = {
        'Total Records': len(df),
        'Date Range': f"{df.index.min().date()} to {df.index.max().date()}",
        'Total Days': (df.index.max() - df.index.min()).days,
        'Mean Demand (MU)': f"{df['demand'].mean():.2f}",
        'Median Demand (MU)': f"{df['demand'].median():.2f}",
        'Min Demand (MU)': f"{df['demand'].min():.2f}",
        'Max Demand (MU)': f"{df['demand'].max():.2f}",
        'Std Deviation (MU)': f"{df['demand'].std():.2f}",
    }
    
    if 'temp' in df.columns:
        stats['Mean Temperature (°C)'] = f"{df['temp'].mean():.2f}"
        stats['Temp-Demand Correlation'] = f"{df['temp'].corr(df['demand']):.3f}"
    
    if 'Holiday' in df.columns:
        holiday_avg = df[df['Holiday'] == 'Holiday']['demand'].mean()
        work_avg = df[df['Holiday'] == 'Work']['demand'].mean()
        stats['Holiday Avg Demand (MU)'] = f"{holiday_avg:.2f}"
        stats['Work Day Avg Demand (MU)'] = f"{work_avg:.2f}"
    
    # Save to file
    with open(f"{output_dir}/summary_statistics.txt", 'w') as f:
        f.write("="*60 + "\n")
        f.write("AP ELECTRICITY DEMAND - SUMMARY STATISTICS\n")
        f.write("="*60 + "\n\n")
        for key, value in stats.items():
            f.write(f"{key:.<40} {value}\n")
    
    print("[OK] Saved: summary_statistics.txt")
    return stats

if __name__ == "__main__":
    import os
    
    print("="*60)
    print("AP ELECTRICITY DEMAND - EXPLORATORY DATA ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_prepared_data()
    
    # Create output directory
    output_dir = create_output_dir()
    
    # Generate all visualizations
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60 + "\n")
    
    plot_demand_over_time(df, output_dir)
    plot_monthly_seasonality(df, output_dir)
    plot_yearly_comparison(df, output_dir)
    plot_monthly_pattern(df, output_dir)
    plot_temperature_correlation(df, output_dir)
    plot_holiday_impact(df, output_dir)
    plot_heatmap_monthly(df, output_dir)
    
    # Generate summary statistics
    print("\n" + "="*60)
    print("GENERATING SUMMARY STATISTICS")
    print("="*60 + "\n")
    stats = generate_summary_statistics(df, output_dir)
    
    print("\n" + "="*60)
    print("EDA COMPLETE!")
    print("="*60)
    print(f"\n[OK] All visualizations saved to: {output_dir}/")
    print("\nNext steps:")
    print("1. Review the visualizations in dashboards/visualizations/")
    print("2. Run '03_ml_forecasting.py' for time-series forecasting")
    print("3. Use these insights to build your Power BI/Tableau dashboard")
