# Titanic Dashboard - Technical Overview

## Architecture

### Backend (Flask + SocketIO)
```
┌─────────────────────────────────────────┐
│           Flask Backend                 │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      REST API Endpoints         │   │
│  │  • /api/passengers              │   │
│  │  • /api/statistics              │   │
│  │  • /api/survival-by-class       │   │
│  │  • /api/survival-by-gender      │   │
│  │  • /api/age-distribution        │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      WebSocket Server           │   │
│  │  • Live metrics streaming       │   │
│  │  • Real-time updates (3s)       │   │
│  │  • Broadcast to all clients     │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      Data Layer (Pandas)        │   │
│  │  • Titanic dataset              │   │
│  │  • Statistical calculations     │   │
│  │  • Data aggregations            │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Frontend (Angular + TypeScript)
```
┌─────────────────────────────────────────┐
│         Angular Frontend                │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │    Dashboard Component          │   │
│  │  • Live metrics display         │   │
│  │  • Statistics cards             │   │
│  │  • Survival analysis charts     │   │
│  │  • Age distribution viz         │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │    Titanic Service              │   │
│  │  • HTTP Client (REST API)       │   │
│  │  • Socket.IO Client             │   │
│  │  • RxJS Observables             │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## Communication Flow

### REST API Communication
```
Frontend                    Backend
   │                          │
   │  HTTP GET /api/stats     │
   │─────────────────────────>│
   │                          │
   │  JSON Response           │
   │<─────────────────────────│
   │                          │
```

### WebSocket Communication
```
Frontend                    Backend
   │                          │
   │  Connect                 │
   │─────────────────────────>│
   │                          │
   │  connection_response     │
   │<─────────────────────────│
   │                          │
   │  request_live_metrics    │
   │─────────────────────────>│
   │                          │
   │  live_metrics (every 3s) │
   │<─────────────────────────│
   │<─────────────────────────│
   │<─────────────────────────│
   │         ...              │
```

## Data Flow

### Statistics Retrieval (REST)
1. Dashboard component calls `titanicService.getStatistics()`
2. Service makes HTTP GET to `/api/statistics`
3. Flask processes request with Pandas
4. Returns JSON with aggregated stats
5. Dashboard updates UI with data

### Live Metrics Streaming (WebSocket)
1. Dashboard subscribes to `liveMetrics$` observable
2. Service emits `request_live_metrics` event
3. Flask background thread generates metrics every 3 seconds
4. Metrics broadcast to all connected clients
5. Service receives and pushes to observable
6. Dashboard updates in real-time

## Key Features Implemented

### ✅ REST API Endpoints
- [x] Paginated passenger list
- [x] Individual passenger lookup
- [x] Overall statistics
- [x] Survival by passenger class
- [x] Survival by gender
- [x] Age distribution
- [x] Health check

### ✅ WebSocket Features
- [x] Real-time connection
- [x] Live metrics broadcasting
- [x] Automatic updates (3-second interval)
- [x] Multiple client support

### ✅ Frontend Features
- [x] Responsive dashboard
- [x] Real-time metrics display
- [x] Statistical visualizations
- [x] Progress bars and charts
- [x] TypeScript type safety
- [x] RxJS reactive programming

## Technology Justifications

### Why Flask?
- Lightweight and easy to set up
- Excellent for building REST APIs
- Flask-SocketIO provides seamless WebSocket support
- Great integration with Pandas for data analysis

### Why Angular?
- Full-featured framework with TypeScript
- Built-in HTTP client
- RxJS for reactive programming
- Component-based architecture
- Strong typing with TypeScript

### Why WebSockets?
- Real-time bidirectional communication
- Push updates from server to client
- Lower latency than polling
- Efficient for live dashboards

### Why Pandas?
- Powerful data manipulation
- Easy statistical calculations
- Built-in aggregation functions
- Efficient data filtering and grouping

## Performance Considerations

### Backend
- Uses background threading for WebSocket updates
- Pandas operations cached where possible
- Sample data generated at startup
- CORS enabled for development

### Frontend
- RxJS observables for efficient data handling
- Component-based updates (only affected parts re-render)
- Unsubscribe on component destroy to prevent memory leaks
- CSS animations for smooth transitions

## Security Notes

⚠️ **This is a development setup. For production:**
- Add authentication (JWT tokens)
- Implement rate limiting
- Use environment variables for configuration
- Enable HTTPS/WSS
- Add input validation
- Implement CSRF protection
- Add logging and monitoring

## Testing

### Backend Testing
```bash
# Test REST API
python backend/test_api.py

# Test WebSocket
python backend/test_websocket.py
```

### Frontend Testing
```bash
# Unit tests (when configured)
ng test

# E2E tests (when configured)
ng e2e
```

## Deployment Considerations

### Backend
- Use Gunicorn with eventlet worker
- Configure proper WSGI server
- Set up reverse proxy (Nginx)
- Use Redis for WebSocket scaling

### Frontend
- Build for production: `ng build --prod`
- Serve static files via CDN
- Enable gzip compression
- Configure proper caching headers

## Future Enhancements

### Backend
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication
- [ ] API rate limiting
- [ ] Request logging
- [ ] Error tracking
- [ ] API documentation (Swagger/OpenAPI)

### Frontend
- [ ] Chart.js/D3.js visualizations
- [ ] Passenger search/filter
- [ ] Data export (CSV/PDF)
- [ ] User preferences
- [ ] Multiple dashboard views
- [ ] Mobile app (Ionic/React Native)

### DevOps
- [ ] Docker containers
- [ ] CI/CD pipeline
- [ ] Automated testing
- [ ] Monitoring (Prometheus/Grafana)
- [ ] Load balancing
- [ ] Auto-scaling

## Common Issues & Solutions

### WebSocket Connection Failed
```
Error: WebSocket connection failed
Solution: Check Flask server is running and CORS is enabled
```

### CORS Error
```
Error: Access-Control-Allow-Origin
Solution: Verify Flask-CORS is installed and configured
```

### Port Already in Use
```
Error: Address already in use
Solution: Kill process or change port in configuration
```

### Module Not Found
```
Error: ModuleNotFoundError
Solution: Install requirements.txt or package.json
```

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Flask-SocketIO: https://flask-socketio.readthedocs.io/
- Angular Documentation: https://angular.io/docs
- Socket.IO: https://socket.io/docs/
- Pandas Documentation: https://pandas.pydata.org/docs/
- RxJS Documentation: https://rxjs.dev/

## License
MIT License - Free to use and modify
