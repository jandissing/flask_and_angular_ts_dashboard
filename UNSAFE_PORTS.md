# Chrome Unsafe Ports - Why Port 8000?

## The Issue with Port 6000

Port 6000 is on Chrome's list of "unsafe ports" that are blocked by default for security reasons. When you try to access `http://localhost:6000` in a browser, you'll get:

```
ERR_UNSAFE_PORT
```

## Chrome's Unsafe Ports List

Chrome blocks these ports (partial list):
- 1, 7, 9, 11, 13, 15, 17, 19, 20, 21, 22, 23
- 25, 37, 42, 43, 53, 77, 79, 87, 95, 101
- 102, 103, 104, 109, 110, 111, 113, 115
- 117, 119, 123, 135, 139, 143, 179, 389
- 465, 512-515, 526, 530, 531, 532, 540
- 556, 563, 587, 601, 636, 993, 995
- 2049, 3659, 4045, 5060, 5061, **6000**, 6665-6669
- 6697, 10080

## Why Port 8000 is Safe

Port 8000 is:
- ✅ Not on the unsafe ports list
- ✅ Commonly used for development servers
- ✅ Works in all browsers (Chrome, Firefox, Safari, Edge)
- ✅ Industry standard alternative port

## Other Safe Port Options

If port 8000 is in use, you can use:
- **3000** - Common for Node.js/React apps
- **5001** - Common alternative to 5000
- **8080** - Very common for HTTP servers
- **8888** - Common for Jupyter notebooks
- **9000** - Common for various services

## Changing the Port

To use a different port, update these files:

1. **Backend**: `backend/app.py` (line ~197)
```python
socketio.run(app, debug=True, host='0.0.0.0', port=YOUR_PORT, ...)
```

2. **Frontend**: `frontend/src/app/services/titanic.service.ts` (lines ~51-52)
```typescript
private apiUrl = 'http://localhost:YOUR_PORT/api';
...
this.socket = io('http://localhost:YOUR_PORT', {
```

## References

- [Chromium Source - Restricted Ports](https://chromium.googlesource.com/chromium/src.git/+/refs/heads/master/net/base/port_util.cc)
- [Chrome ERR_UNSAFE_PORT Documentation](https://developer.chrome.com/blog/chromium-chronicle-23/)
