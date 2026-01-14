#!/bin/bash
# Script untuk menjalankan HR Chatbot

echo "🏢 HR Internal Chatbot"
echo "======================"
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting Streamlit application..."
echo "Open your browser at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py --server.headless true
