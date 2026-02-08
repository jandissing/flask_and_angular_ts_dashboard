# Backend Not Responding - Troubleshooting Guide

## Your Issue: API/Health endpoint not reachable

Let's debug this step by step:

## Step 1: Run the Debug Script

```bash
cd backend
bash debug_backend.sh
```

This will check:
- Python version
- All dependencies
- Port availability
- Basic Flask functionality

## Step 2: Check What You See When Starting Backend

When you run `python app.py`, what do you see?

### Expected Output:
```
Starting Flask server with WebSocket support...
Backend running on http://localhost:8000
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:6000
 * Running on http://192.168.x.x:6000
Press CTRL+C to quit
 * Restarting with stat
Starting Flask server with WebSocket support...
Backend running on http://localhost:8000
 * Debugger is active!
```

### Common Error Messages:

**1. "Address already in use"**
```bash
# Kill the process using port 8000
lsof -i :6000
kill -9 <PID>
```

**2. "ModuleNotFoundError: No module named 'flask'"**
```bash
# You're not in the virtual environment or dependencies not installed
source .venv/bin/activate
poetry install --no-root
# OR
pip install -r requirements.txt
```

**3. "ImportError: cannot import name 'x' from 'y'"**
```bash
# Dependency version conflict
pip uninstall flask flask-cors flask-socketio -y
pip install -r requirements.txt
```

**4. No output at all**
```bash
# Python not found or wrong Python version
which python3
python3 --version  # Should be 3.9+
```

## Step 3: Test with Minimal Server

If the main app won't start, try the minimal test:

```bash
cd backend
python test_minimal.py
```

Then in another terminal:
```bash
curl http://localhost:8000/test
```

**If this works:** The problem is in app.py (likely socketio or pandas issue)
**If this doesn't work:** The problem is with Flask/Python setup

## Step 4: Common Fixes

### Fix 1: Reinstall Dependencies
```bash
cd backend
rm -rf .venv
poetry install --no-root
poetry run python app.py
```

### Fix 2: Try Without Poetry
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

### Fix 3: Check Firewall
```bash
# On macOS, allow Python through firewall
# System Preferences > Security & Privacy > Firewall > Firewall Options
# Allow incoming connections for Python
```

### Fix 4: Try Different Port
Edit `backend/app.py` line 197:
```python
socketio.run(app, debug=True, host='0.0.0.0', port=7000, allow_unsafe_werkzeug=True)
```

Then update frontend service to use port 7000.

## Step 5: Detailed Diagnostics

### Check if Python can bind to port 8000:
```python
python3 << EOF
import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 6000))
    s.listen(1)
    print("✅ Can bind to port 8000")
    s.close()
except Exception as e:
    print(f"❌ Cannot bind to port 8000: {e}")
EOF
```

### Check Flask installation:
```bash
python3 -c "import flask; print('Flask version:', flask.__version__)"
```

### Check if backend is actually running:
```bash
# While app.py is running in another terminal
ps aux | grep python | grep app.py
netstat -an | grep 6000
# OR on macOS
lsof -i :6000
```

## Step 6: What to Share for Help

If still not working, please provide:

1. **Exact error message** when running `python app.py`
2. **Python version**: `python3 --version`
3. **OS**: macOS, Linux, Windows?
4. **Output of**: `bash debug_backend.sh`
5. **Port check**: `lsof -i :6000` (while backend is supposed to be running)

## Quick Checklist

- [ ] Python 3.9+ installed
- [ ] In backend directory
- [ ] Virtual environment activated
- [ ] Dependencies installed (poetry install or pip install -r requirements.txt)
- [ ] Port 8000 not in use by another process
- [ ] No firewall blocking localhost:8000
- [ ] Can run `python test_minimal.py` successfully

## Alternative: Use Different Host/Port

If localhost:8000 absolutely won't work, edit these files:

**backend/app.py** (line 197):
```python
socketio.run(app, debug=True, host='127.0.0.1', port=8080, allow_unsafe_werkzeug=True)
```

**frontend/src/app/services/titanic.service.ts** (lines 51-52):
```typescript
private apiUrl = 'http://127.0.0.1:8080/api';
...
this.socket = io('http://127.0.0.1:8080', {
```

Then try again.
