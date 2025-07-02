#!/bin/bash

# AI Catalog Assistant - Run Script
# This script helps you start the application easily

echo "🛍️ AI Catalog Assistant"
echo "========================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating one from template..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it and add your OpenAI API key."
    echo "   Edit: nano .env"
    echo ""
fi

# Check if virtual environment should be created
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created."
fi

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo "🚀 Starting AI Catalog Assistant..."
echo "   Open your browser to: http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo ""

# Start the Streamlit app
streamlit run app.py