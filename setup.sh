#!/bin/bash

echo "🔧 Stock Size Selector - Quick Start"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "   1. Activate the virtual environment:"
echo "      - On macOS/Linux: source venv/bin/activate"
echo "      - On Windows: venv\\Scripts\\activate"
echo "   2. Run: python app.py"
echo "   3. Open your browser to: http://localhost:5000"
echo ""
echo "📚 See README.md for more information"
