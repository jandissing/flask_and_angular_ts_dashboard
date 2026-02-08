#!/bin/bash

echo "╔════════════════════════════════════════════════╗"
echo "║  Titanic Dashboard Diagnostics                ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "📊 Python Version:"
python3 --version || python --version
echo ""

# Check Node version
echo "📦 Node.js Version:"
node --version
echo ""

# Check if backend port is in use
echo "🔍 Checking Backend Port (6000):"
if lsof -i :8000 > /dev/null 2>&1; then
    echo "✅ Port 6000 is IN USE (backend might be running)"
    lsof -i :8000
else
    echo "❌ Port 6000 is FREE (backend is NOT running)"
fi
echo ""

# Test backend health endpoint
echo "🏥 Testing Backend Health Endpoint:"
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend is responding!"
    curl -s http://localhost:8000/api/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8000/api/health
else
    echo "❌ Backend is NOT responding"
    echo "   Start backend with: cd backend && python app.py"
fi
echo ""

# Test statistics endpoint
echo "📈 Testing Statistics Endpoint:"
if curl -s http://localhost:8000/api/statistics > /dev/null 2>&1; then
    echo "✅ Statistics endpoint is working!"
    echo "First 200 characters of response:"
    curl -s http://localhost:8000/api/statistics | head -c 200
    echo "..."
else
    echo "❌ Statistics endpoint is NOT responding"
fi
echo ""

# Check if frontend port is in use
echo "🔍 Checking Frontend Port (4200):"
if lsof -i :4200 > /dev/null 2>&1; then
    echo "✅ Port 4200 is IN USE (frontend might be running)"
else
    echo "❌ Port 4200 is FREE (frontend is NOT running)"
    echo "   Start frontend with: cd frontend && npm start"
fi
echo ""

# Check backend dependencies
echo "📚 Checking Backend Dependencies:"
cd backend 2>/dev/null || cd ../backend 2>/dev/null
if python3 -c "import flask, flask_cors, flask_socketio, pandas, numpy" 2>/dev/null; then
    echo "✅ All backend dependencies installed"
else
    echo "❌ Missing backend dependencies"
    echo "   Install with: poetry install --no-root"
    echo "   Or: pip install -r requirements.txt"
fi
cd ..
echo ""

# Check frontend dependencies
echo "📚 Checking Frontend Dependencies:"
cd frontend 2>/dev/null || cd ../frontend 2>/dev/null
if [ -d "node_modules" ]; then
    echo "✅ node_modules directory exists"
else
    echo "❌ node_modules directory NOT found"
    echo "   Install with: npm install"
fi
cd ..
echo ""

echo "╔════════════════════════════════════════════════╗"
echo "║  Diagnostic Complete                          ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "Quick Start Commands:"
echo "  Terminal 1: cd backend && poetry run python app.py"
echo "  Terminal 2: cd frontend && npm start"
echo "  Browser:    http://localhost:4200"
echo ""
