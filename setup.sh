#!/bin/bash

echo "=================================="
echo "Titanic Dashboard Setup Script"
echo "=================================="
echo ""

# Detect package manager
PACKAGE_MANAGER=""

if command -v poetry &> /dev/null; then
    echo "✅ Poetry detected"
    PACKAGE_MANAGER="poetry"
elif command -v uv &> /dev/null; then
    echo "✅ UV detected"
    PACKAGE_MANAGER="uv"
else
    echo "📦 Using pip (default)"
    PACKAGE_MANAGER="pip"
fi

# Backend Setup
echo "Setting up Backend with $PACKAGE_MANAGER..."
cd backend

if [ "$PACKAGE_MANAGER" = "poetry" ]; then
    echo "Installing dependencies with Poetry..."
    poetry install --no-root
    
    echo ""
    echo "Backend setup complete!"
    echo ""
    echo "To start the backend server:"
    echo "  cd backend"
    echo "  poetry run python app.py"
    echo ""
    
elif [ "$PACKAGE_MANAGER" = "uv" ]; then
    echo "Creating virtual environment with uv..."
    uv venv
    
    echo "Activating virtual environment..."
    source .venv/bin/activate
    
    echo "Installing Python dependencies with uv..."
    uv pip install -r requirements.txt
    
    echo ""
    echo "Backend setup complete!"
    echo ""
    echo "To start the backend server:"
    echo "  cd backend"
    echo "  source .venv/bin/activate"
    echo "  python app.py"
    echo ""
    
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    
    echo "Activating virtual environment..."
    source .venv/bin/activate
    
    echo "Installing Python dependencies with pip..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo ""
    echo "Backend setup complete!"
    echo ""
    echo "To start the backend server:"
    echo "  cd backend"
    echo "  source .venv/bin/activate"
    echo "  python app.py"
    echo ""
fi

# Frontend Setup
cd ../frontend

echo "Setting up Frontend..."
echo "Installing npm dependencies..."
npm install

echo ""
echo "Frontend setup complete!"
echo ""
echo "To start the frontend server:"
echo "  cd frontend"
echo "  npm start"
echo ""

echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""

if [ "$PACKAGE_MANAGER" = "poetry" ]; then
    echo "Quick Start:"
    echo "1. Terminal 1: cd backend && poetry run python app.py"
    echo "2. Terminal 2: cd frontend && npm start"
    echo "3. Open browser to http://localhost:4200"
else
    echo "Quick Start:"
    echo "1. Terminal 1: cd backend && source .venv/bin/activate && python app.py"
    echo "2. Terminal 2: cd frontend && npm start"
    echo "3. Open browser to http://localhost:4200"
fi
echo ""
