# Quick Start Guide - Titanic Dashboard

## 🚀 Get Started in 3 Steps

### Step 1: Start the Backend
```bash
cd titanic-dashboard/backend

# Option 1: Using Poetry (recommended for dependency management)
poetry install --no-root
poetry run python app.py

# Option 2: Using uv (fast installer)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
python app.py

# Option 3: Using pip (traditional)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
✅ Backend running on http://localhost:8000

### Step 2: Start the Frontend
```bash
cd titanic-dashboard/frontend
npm install
npm start
```
✅ Frontend running on http://localhost:4200

### Step 3: Open Browser
Navigate to: http://localhost:4200

---

## 📊 What You'll See

### Live Metrics (WebSocket) - Updates Every 3 Seconds
- Active Queries
- Current Survival Rate
- Passengers Analyzed
- Response Time
- Memory Usage
- Recent Survivor Info

### Statistics (REST API)
- Total Passengers
- Survivors & Perished
- Survival Rate
- Average Age & Fare
- Gender Distribution
- Class Distribution

---

## 🧪 Testing

### Test REST API
```bash
cd backend
python test_api.py
```

### Test WebSocket
```bash
cd backend
python test_websocket.py
```

---

## 📁 Project Structure

```
titanic-dashboard/
├── backend/
│   ├── app.py                    # Flask server with REST + WebSocket
│   ├── requirements.txt          # Python dependencies
│   ├── test_api.py              # REST API test script
│   └── test_websocket.py        # WebSocket test script
│
├── frontend/
│   ├── src/app/
│   │   ├── services/
│   │   │   └── titanic.service.ts    # API & WebSocket service
│   │   ├── dashboard/
│   │   │   ├── dashboard.component.ts
│   │   │   ├── dashboard.component.html
│   │   │   └── dashboard.component.css
│   │   ├── app.component.ts
│   │   └── app.module.ts
│   └── package.json             # npm dependencies
│
├── README.md                     # Full documentation
├── TECHNICAL_OVERVIEW.md         # Architecture details
└── setup.sh                      # Automated setup script

```

---

## ⚡ Quick Commands

**Backend:**
- Install with Poetry: `poetry install --no-root`
- Install with uv: `uv pip install -r requirements.txt`
- Install with pip: `pip install -r requirements.txt`
- Run with Poetry: `poetry run python app.py`
- Run (other): `python app.py`
- Test API: `python test_api.py`
- Test WebSocket: `python test_websocket.py`

**Frontend:**
- Install: `npm install`
- Run: `npm start`
- Build: `npm run build`

---

## 🔧 Configuration

### Backend (app.py)
- **Port:** 5000 (change in `socketio.run(app, port=5000)`)
- **Update Interval:** 3 seconds (change in `time.sleep(3)`)
- **CORS:** Enabled for all origins (restrict in production)

### Frontend (titanic.service.ts)
- **API URL:** http://localhost:8000/api
- **WebSocket URL:** http://localhost:8000

---

## 🎯 Features

✅ REST API with 7 endpoints
✅ Real-time WebSocket updates
✅ Interactive dashboard
✅ Responsive design
✅ TypeScript type safety
✅ Pandas data analysis
✅ CORS enabled
✅ Sample Titanic dataset

---

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python 3.7+ installed
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 not in use

**Frontend won't start:**
- Check Node.js 16+ installed
- Install dependencies: `npm install`
- Check port 4200 not in use

**WebSocket not connecting:**
- Ensure backend is running first
- Check browser console for errors
- Verify CORS settings

**CORS errors:**
- Install Flask-CORS: `pip install flask-cors`
- Check backend URL in frontend service

---

## 📚 Documentation

- **README.md** - Complete documentation
- **TECHNICAL_OVERVIEW.md** - Architecture and design details

---

## 📝 Notes

This is a development setup. For production:
- Add authentication
- Use environment variables
- Enable HTTPS/WSS
- Add rate limiting
- Configure proper WSGI server
- Use database instead of in-memory data

---

Happy coding! 🎉
