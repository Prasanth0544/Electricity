#!/bin/bash
# Andhra Pradesh Electricity Demand - Streamlit Dashboard
# Run this file to start the dashboard

echo "================================"
echo "Streamlit Dashboard Launcher"
echo "================================"
echo ""
echo "Starting Streamlit app..."
echo ""

cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

# Run Streamlit
streamlit run app.py
