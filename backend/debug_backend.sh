#!/bin/bash

echo "╔════════════════════════════════════════════════╗"
echo "║  Backend Debugging Script                     ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Check if we're in the backend directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this from the backend directory."
    echo "   cd backend && bash debug_backend.sh"
    exit 1
fi

# Check Python version
echo "1️⃣  Checking Python version..."
python3 --version || python --version
echo ""

# Check if virtual environment is activated
echo "2️⃣  Checking virtual environment..."
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual environment is active: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected"
    echo "   Activate with: source .venv/bin/activate"
    echo "   Or use Poetry: poetry shell"
fi
echo ""

# Test imports
echo "3️⃣  Testing Python imports..."
python3 << 'EOF'
import sys
try:
    import flask
    print("✅ flask imported successfully - version:", flask.__version__)
except ImportError as e:
    print("❌ flask import failed:", e)
    sys.exit(1)

try:
    import flask_cors
    print("✅ flask_cors imported successfully")
except ImportError as e:
    print("❌ flask_cors import failed:", e)
    sys.exit(1)

try:
    import flask_socketio
    print("✅ flask_socketio imported successfully")
except ImportError as e:
    print("❌ flask_socketio import failed:", e)
    sys.exit(1)

try:
    import pandas
    print("✅ pandas imported successfully - version:", pandas.__version__)
except ImportError as e:
    print("❌ pandas import failed:", e)
    sys.exit(1)

try:
    import numpy
    print("✅ numpy imported successfully - version:", numpy.__version__)
except ImportError as e:
    print("❌ numpy import failed:", e)
    sys.exit(1)

try:
    import eventlet
    print("✅ eventlet imported successfully")
except ImportError as e:
    print("❌ eventlet import failed:", e)
    sys.exit(1)

print("\n✅ All required packages are installed!")
EOF

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Some dependencies are missing!"
    echo "   Install with: poetry install --no-root"
    echo "   Or: pip install -r requirements.txt"
    exit 1
fi
echo ""

# Check if port 6000 is already in use
echo "4️⃣  Checking if port 6000 is available..."
if lsof -i :8000 > /dev/null 2>&1; then
    echo "⚠️  Port 6000 is already in use!"
    echo "   Process using port 6000:"
    lsof -i :8000
    echo ""
    echo "   To kill this process: kill -9 <PID>"
else
    echo "✅ Port 6000 is available"
fi
echo ""

# Test basic Flask app
echo "5️⃣  Testing minimal Flask app..."
echo "   Starting test server for 5 seconds..."
python3 test_minimal.py &
TEST_PID=$!
sleep 3

echo "   Testing /test endpoint..."
if curl -s http://localhost:8000/test > /dev/null 2>&1; then
    echo "✅ Minimal Flask server is working!"
    curl -s http://localhost:8000/test | python3 -m json.tool 2>/dev/null
else
    echo "❌ Minimal Flask server is not responding"
fi
echo ""

echo "   Testing /api/health endpoint..."
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Health endpoint is working!"
    curl -s http://localhost:8000/api/health | python3 -m json.tool 2>/dev/null
else
    echo "❌ Health endpoint is not responding"
fi

# Stop test server
kill $TEST_PID 2>/dev/null
wait $TEST_PID 2>/dev/null
echo ""

# Test main app syntax
echo "6️⃣  Checking app.py syntax..."
python3 -m py_compile app.py
if [ $? -eq 0 ]; then
    echo "✅ app.py has no syntax errors"
else
    echo "❌ app.py has syntax errors!"
    exit 1
fi
echo ""

echo "╔════════════════════════════════════════════════╗"
echo "║  Debugging Complete                           ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "📋 Summary:"
echo "   - If all checks passed, try running: python app.py"
echo "   - If port 6000 is in use, kill the process or change the port"
echo "   - If imports failed, install dependencies"
echo ""
echo "🚀 Next steps:"
echo "   1. Make sure you're in a virtual environment"
echo "   2. Run: python app.py"
echo "   3. Test: curl http://localhost:8000/api/health"
echo ""
