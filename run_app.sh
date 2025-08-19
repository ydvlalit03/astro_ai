#!/bin/bash

echo "🌟 Astro AI - Startup Script"
echo "============================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    
    # Activate and install dependencies
    echo "📥 Installing Python dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "🚀 Ready to start Astro AI Application!"
echo ""
echo "💻 To start the backend (in one terminal):"
echo "   source venv/bin/activate"
echo "   python start_backend.py"
echo ""
echo "💻 To start the frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "🌐 Then open: http://localhost:5173"
echo ""
echo "📚 API docs will be at: http://localhost:8000/docs"

# Ask if user wants to start the backend now
read -p "🤔 Start the backend server now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "🚀 Starting backend server..."
    source venv/bin/activate
    python start_backend.py
fi