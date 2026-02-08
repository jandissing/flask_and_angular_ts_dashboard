# Troubleshooting Guide - "Failed to load statistics"

## Quick Checklist

### 1. Is the Backend Running?
Check if you can access: http://localhost:8000/api/health

**If you see JSON response like `{"status": "healthy", ...}` - Backend is running ✅**

**If you get "Connection refused" or cannot connect:**
- Backend is not running
- Start it with: `cd backend && python app.py` (or `poetry run python app.py`)

### 2. Check Backend Logs
When you run `python app.py`, you should see:
```
Starting Flask server with WebSocket support...
Backend running on http://localhost:8000
 * Running on http://0.0.0.0:6000
```

### 3. Test API Directly
Run the test script:
```bash
cd backend
python test_api.py
```

This will test all endpoints and show you exactly what's working.

### 4. Check CORS
The frontend runs on `http://localhost:4200` and backend on `http://localhost:8000`.

Make sure CORS is enabled in `backend/app.py`:
```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

### 5. Check Browser Console
Open browser DevTools (F12) and check the Console tab for errors like:
- `net::ERR_CONNECTION_REFUSED` - Backend not running
- `CORS policy` error - CORS configuration issue
- `404 Not Found` - Wrong URL

### 6. Verify Port Configuration
**Backend should be on port 8000:**
Check `backend/app.py` last line:
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5000, ...)
```

**Frontend should point to port 8000:**
Check `frontend/src/app/services/titanic.service.ts`:
```typescript
private apiUrl = 'http://localhost:8000/api';
```

## Common Issues & Solutions

### Issue 1: "Failed to load statistics" - Backend Not Running
**Solution:**
```bash
# Terminal 1 - Start Backend
cd backend
poetry run python app.py  # or: python app.py

# Terminal 2 - Start Frontend (after backend is running)
cd frontend
npm start
```

### Issue 2: Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Find what's using port 8000
lsof -i :6000

# Kill the process
kill -9 <PID>

# Or use a different port in app.py:
socketio.run(app, port=5001)
# Then update frontend service to use port 5001
```

### Issue 3: CORS Error
**Error in browser console:** `Access to XMLHttpRequest at 'http://localhost:8000/api/statistics' from origin 'http://localhost:4200' has been blocked by CORS policy`

**Solution:**
Make sure `flask-cors` is installed:
```bash
pip install flask-cors
# or
poetry add flask-cors
```

### Issue 4: Module Not Found
**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
Install dependencies:
```bash
# With Poetry
poetry install --no-root

# With pip
pip install -r requirements.txt

# With uv
uv pip install -r requirements.txt
```

### Issue 5: Wrong Python Version
**Error:** `pandas requires Python >=3.9`

**Solution:**
```bash
# Check your Python version
python --version

# Must be 3.9 or higher
# If not, install Python 3.9+ or use pyenv
```

## Testing Steps

### Step 1: Test Backend Directly
```bash
# In backend directory
curl http://localhost:8000/api/health

# Should return:
# {"status":"healthy","timestamp":"..."}
```

### Step 2: Test Statistics Endpoint
```bash
curl http://localhost:8000/api/statistics

# Should return JSON with passenger data
```

### Step 3: Check Network Tab
1. Open browser to http://localhost:4200
2. Open DevTools (F12)
3. Go to Network tab
4. Refresh page
5. Look for requests to `localhost:8000`
6. Check if they're successful (200) or failing (red)

## Still Not Working?

### Get Detailed Logs

**Backend:**
```bash
cd backend
python app.py 2>&1 | tee backend.log
```

**Frontend - Check Console:**
1. Open http://localhost:4200
2. Press F12
3. Go to Console tab
4. Look for error messages
5. Copy and share the error

### Verify Everything is Installed

**Backend:**
```bash
cd backend
python -c "import flask, flask_cors, flask_socketio, pandas; print('All imports successful!')"
```

**Frontend:**
```bash
cd frontend
npm list socket.io-client
```

## Quick Fix Script

Run this to diagnose issues:

```bash
#!/bin/bash
echo "=== Titanic Dashboard Diagnostics ==="
echo ""
echo "1. Checking if backend port 8000 is in use..."
lsof -i :6000 || echo "Port 8000 is free"
echo ""
echo "2. Testing backend health endpoint..."
curl -s http://localhost:8000/api/health || echo "Backend not responding"
echo ""
echo "3. Testing statistics endpoint..."
curl -s http://localhost:8000/api/statistics | head -c 100 || echo "Statistics endpoint not responding"
echo ""
echo "4. Checking Python version..."
python --version
echo ""
echo "5. Checking Node version..."
node --version
echo ""
```

Save this as `diagnose.sh` and run: `bash diagnose.sh`
