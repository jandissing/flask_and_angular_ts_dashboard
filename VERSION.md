# Titanic Dashboard - Version History

## v1.5 - Fixed Chrome ERR_UNSAFE_PORT + Angular Tutorials
**Release Date:** 2025-02-08

### Critical Fix
- ✅ **Changed backend port from 6000 to 8000**
- ✅ Fixed Chrome ERR_UNSAFE_PORT error  
- ✅ All browsers now work correctly

### New Learning Materials
- ✅ **ANGULAR_TUTORIAL.md** - Comprehensive 10,000+ word Angular + TypeScript guide
- ✅ **ANGULAR_EXERCISES.md** - 15+ hands-on practice exercises (Easy → Hard → Advanced)
- ✅ **UNSAFE_PORTS.md** - Explanation of browser port restrictions

### Tutorial Includes
- TypeScript basics, interfaces, and type system
- Angular architecture (Components, Services, Modules)
- Dependency Injection explained with examples
- Observables & RxJS with real code
- HTTP requests with HttpClient
- WebSocket integration step-by-step
- Template syntax (*ngIf, *ngFor, property/event binding)
- Component lifecycle (ngOnInit, ngOnDestroy)
- Complete code walkthroughs from this project
- Common patterns and best practices

### Practice Exercises
- 🟢 Easy: Display data, change text, console logging
- 🟡 Medium: Create methods, add buttons, style components, make API calls
- 🔴 Hard: Build new components, implement filtering, handle errors
- 🚀 Advanced: Search, pagination, charts, sorting, localStorage

### The Problem with Port 6000
Port 6000 is on Chrome's "unsafe ports" list and blocked by browsers. API worked with curl/scripts but not in browsers, showing ERR_UNSAFE_PORT.

### The Solution
Port 8000 is safe, commonly used for development, and works in all browsers.

---

## v1.4 - Backend Debugging Tools
**Release Date:** 2025-02-08

### Changes
- ✅ Added test_minimal.py - Minimal Flask test server
- ✅ Added debug_backend.sh - Comprehensive diagnostics
- ✅ Added BACKEND_DEBUG.md - Troubleshooting guide

---

## v1.3 - Port Change to 6000
**Release Date:** 2025-02-08
- Changed port from 5000 to 6000 (later found to be unsafe in v1.5)

---

## v1.2 - Enhanced Debugging
**Release Date:** 2025-02-08
- Added TROUBLESHOOTING.md and diagnose.sh
- Enhanced WebSocket error handling

---

## v1.1 - Poetry Support
**Release Date:** 2025-02-08
- Added Poetry support
- Fixed Python version (^3.9)
- Auto-detect package manager

---

## v1.0 - Initial Release
**Release Date:** 2025-02-08
- Flask backend with REST API
- Angular frontend with TypeScript
- WebSocket real-time metrics
- Complete documentation

---

## Future Versions

### v2.0 (Planned)
- Database integration
- Authentication system
- Advanced visualizations
- More interactive features
