# Titanic Dashboard - Frontend

Angular application for the Titanic Dashboard.

## Prerequisites

- Node.js 18+ or 20+ (LTS versions recommended)
- npm or yarn

**Note:** If you're using Node.js v25 (odd-numbered version), consider downgrading to v20 (LTS) for production use.

## Installation

```bash
npm install
```

## Development Server

```bash
npm start
```

Navigate to `http://localhost:4200/`. The application will automatically reload if you change any source files.

## Build

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Project Structure

```
src/
├── app/
│   ├── services/
│   │   └── titanic.service.ts      # API & WebSocket service
│   ├── dashboard/
│   │   ├── dashboard.component.ts   # Main dashboard component
│   │   ├── dashboard.component.html # Dashboard template
│   │   └── dashboard.component.css  # Dashboard styles
│   ├── app.component.ts             # Root component
│   └── app.module.ts                # App module
├── assets/                          # Static assets
├── index.html                       # Main HTML file
├── main.ts                          # Application entry point
└── styles.css                       # Global styles
```

## Configuration

The backend API URL is configured in `src/app/services/titanic.service.ts`:

```typescript
private apiUrl = 'http://localhost:8000/api';
private socket: Socket = io('http://localhost:8000');
```

If you change the backend port, update these URLs accordingly.

## Features

- Real-time WebSocket connection for live metrics
- REST API integration for statistics
- Responsive dashboard design
- TypeScript type safety
- RxJS for reactive programming

## Troubleshooting

### Port 4200 already in use
```bash
ng serve --port 4201
```

### Cannot find module errors
```bash
rm -rf node_modules package-lock.json
npm install
```

### WebSocket connection issues
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify CORS is enabled on backend
