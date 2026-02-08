# Titanic Dashboard - Full Stack Application

A full-stack dashboard application for analyzing Titanic dataset with real-time metrics via WebSockets.

## Technology Stack

### Backend
- **Flask** - Python web framework
- **Flask-SocketIO** - WebSocket support for real-time data
- **Flask-CORS** - Cross-origin resource sharing
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical operations

### Frontend
- **Angular 17** - Frontend framework
- **TypeScript** - Type-safe JavaScript
- **Socket.IO Client** - WebSocket client for real-time updates
- **RxJS** - Reactive programming

## Features

### REST API Endpoints
1. `GET /api/passengers` - Get paginated list of passengers
2. `GET /api/passengers/:id` - Get specific passenger details
3. `GET /api/statistics` - Get overall statistics
4. `GET /api/survival-by-class` - Get survival rates by passenger class
5. `GET /api/survival-by-gender` - Get survival rates by gender
6. `GET /api/age-distribution` - Get age distribution data
7. `GET /api/health` - Health check endpoint

### WebSocket Features
- **Live Metrics Streaming** - Real-time dashboard metrics updated every 3 seconds
- Metrics include:
  - Active queries
  - Current survival rate
  - Passengers analyzed
  - Average response time
  - Memory usage
  - Recent survivor information

### Dashboard Features
- Overview statistics (total passengers, survivors, survival rate)
- Real-time metrics via WebSocket
- Gender-based survival analysis
- Class-based survival analysis
- Age distribution visualization
- Responsive design

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Choose your preferred package manager:

   **Option 1: Poetry (recommended for dependency management)**
   ```bash
   poetry install --no-root
   poetry run python app.py
   ```

   **Option 2: UV (fast Python package installer)**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   python app.py
   ```
   
   **Option 3: pip (traditional)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

   The backend will start on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Angular development server:
   ```bash
   npm start
   ```

   The frontend will start on `http://localhost:4200`

## API Documentation

### REST Endpoints

#### Get Passengers (Paginated)
```
GET /api/passengers?page=1&per_page=10

Response:
{
  "data": [...],
  "total": 891,
  "page": 1,
  "per_page": 10,
  "total_pages": 90
}
```

#### Get Statistics
```
GET /api/statistics

Response:
{
  "total_passengers": 891,
  "survived": 342,
  "perished": 549,
  "survival_rate": 0.383838,
  "avg_age": 29.699,
  "avg_fare": 32.204,
  "male_passengers": 577,
  "female_passengers": 314,
  "class_distribution": {
    "first": 216,
    "second": 184,
    "third": 491
  }
}
```

### WebSocket Events

#### Client to Server
- `connect` - Establish connection
- `request_live_metrics` - Request live metrics streaming
- `disconnect` - Close connection

#### Server to Client
- `connection_response` - Connection confirmation
- `live_metrics_started` - Metrics streaming started
- `live_metrics` - Live metrics data (emitted every 3 seconds)

#### Live Metrics Data Structure
```typescript
{
  timestamp: string;
  active_queries: number;
  current_survival_rate: number;
  passengers_analyzed: number;
  avg_response_time: number;
  memory_usage: number;
  recent_survivor: {
    name: string;
    age: number;
    class: number;
  };
}
```

## Project Structure

```
titanic-dashboard/
├── backend/
│   ├── app.py                 # Flask application with REST & WebSocket
│   └── requirements.txt       # Python dependencies
│
└── frontend/
    ├── src/
    │   └── app/
    │       ├── services/
    │       │   └── titanic.service.ts    # API & WebSocket service
    │       ├── dashboard/
    │       │   ├── dashboard.component.ts
    │       │   ├── dashboard.component.html
    │       │   └── dashboard.component.css
    │       ├── app.component.ts
    │       └── app.module.ts
    └── package.json          # npm dependencies
```

## Development Notes

### Backend
- The backend uses Flask-SocketIO for WebSocket support
- Live metrics are broadcast to all connected clients every 3 seconds
- Sample Titanic data is generated if the actual dataset is not available
- CORS is enabled for frontend development

### Frontend
- Angular service handles both HTTP requests and WebSocket connections
- RxJS observables are used for reactive data handling
- Dashboard updates in real-time when WebSocket data arrives
- Responsive design works on mobile and desktop

## Customization

### Adding Your Own Titanic Dataset
Replace the sample data generation in `app.py` with:
```python
df = pd.read_csv('titanic.csv')
```

### Adjusting WebSocket Update Interval
Modify the sleep time in the `send_live_metrics()` function:
```python
time.sleep(3)  # Change to desired interval in seconds
```

### Styling
Modify `dashboard.component.css` to customize the appearance

## Testing the Application

1. Start the backend server (port 8000)
2. Start the frontend development server (port 4200)
3. Open browser to `http://localhost:4200`
4. You should see:
   - Live metrics updating every 3 seconds (WebSocket)
   - Static statistics from REST API
   - Various survival analysis charts

## Troubleshooting

### CORS Issues
- Ensure Flask-CORS is installed
- Check that backend is running on port 8000
- Verify frontend is making requests to correct URL

### WebSocket Connection Issues
- Check browser console for connection errors
- Verify Flask-SocketIO is installed
- Ensure firewall allows WebSocket connections

### Port Already in Use
- Change backend port in `app.py`: `socketio.run(app, port=5001)`
- Update frontend service URL in `titanic.service.ts`

## Future Enhancements

- Add authentication
- Implement data filtering
- Add more visualizations (charts with Chart.js or D3.js)
- Add passenger search functionality
- Implement data export features
- Add unit tests for both frontend and backend

## License
MIT License
