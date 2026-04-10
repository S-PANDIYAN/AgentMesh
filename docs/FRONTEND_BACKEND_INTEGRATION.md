# Frontend-Backend Integration Guide

Complete guide to connecting AgentMesh frontend with the REST API v2 backend.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
5. [Configuration](#configuration)
6. [Testing Connection](#testing-connection)
7. [API Integration](#api-integration)
8. [Authentication Flow](#authentication-flow)
9. [Error Handling](#error-handling)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The AgentMesh frontend is a JavaScript-based web UI that communicates with the REST API v2 backend through HTTP/HTTPS. The integration supports:

- **User Authentication**: JWT tokens and API keys
- **Code Analysis**: Submit code and retrieve results
- **File Upload**: Upload Python files for analysis
- **Reports**: Generate PDF, HTML, and JSON reports
- **Analytics**: View quality metrics and trends
- **Notifications**: In-app and email notifications

---

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Web Browser                            │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │         Frontend UI (HTML/CSS/JS)               │    │
│  │  public/                                         │    │
│  │  ├── index.html                                 │    │
│  │  ├── integration.html (setup & testing)         │    │
│  │  └── js/                                        │    │
│  │      ├── app.js (main application)              │    │
│  │      ├── pages/ (dashboard, results, etc)       │    │
│  │      └── router.js (routing)                    │    │
│  └──────────────────┬──────────────────────────────┘    │
│                     │                                     │
│  ┌──────────────────▼──────────────────────────────┐    │
│  │     Frontend API Clients                         │    │
│  │  src/js/                                         │    │
│  │  ├── config.js (configuration)                  │    │
│  │  ├── auth.js (authentication manager)           │    │
│  │  ├── api.js (legacy API client)                 │    │
│  │  └── api-v2.js (new v2 API client)              │    │
│  └──────────────────┬──────────────────────────────┘    │
│                     │ HTTP/HTTPS                         │
└─────────────────────┼─────────────────────────────────────┘
                      │
                      │ 30+ endpoints
                      │ JWT/API Key auth
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Backend REST API v2                         │
│          backend/rest_api_v2.py (Flask)                │
├─────────────────────────────────────────────────────────┤
│  ├── Authentication (/auth/*)                          │
│  ├── API Keys (/api-keys/*)                            │
│  ├── Analysis (/review, /analyses/*)                   │
│  ├── Reports (/reports/*)                              │
│  ├── Files (/upload, /files/*)                         │
│  ├── Analytics (/analytics/*)                          │
│  ├── Notifications (/notifications)                    │
│  └── System (/health, /system/*)                       │
└─────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### Frontend
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Node.js 14+ (for development with live-server)
- npm (comes with Node.js)

### Backend
- Python 3.9+
- PostgreSQL 12+ or MySQL 8.0+
- Gunicorn (production)

### Network
- Frontend and backend on same network or accessible via network
- Port 5000 accessible from frontend machine (backend API)
- Port 8080 accessible from your machine (frontend dev server)

---

## Setup Instructions

### Step 1: Install and Start Backend

```bash
# Navigate to backend directory
cd d:\project\AgentMesh

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements_backend.txt

# Configure environment
echo "DATABASE_URL=postgresql://user:password@localhost/agentmesh" > .env
echo "JWT_SECRET_KEY=your_secret_key_change_in_production" >> .env
echo "FLASK_ENV=production" >> .env

# Initialize database
python -c "from backend.database import db_manager; db_manager.initialize()"

# Start backend API
python -m backend.rest_api_v2 --debug
# Or: gunicorn -w 4 -b 0.0.0.0:5000 backend.rest_api_v2:app
```

Verify backend is running:
```bash
curl http://localhost:5000/health
# Should return: {"status":"healthy","database":"connected",...}
```

### Step 2: Install and Start Frontend

```bash
# Navigate to frontend directory
cd d:\project\AgentMesh\AgentMesh\UI\frontend

# Install dependencies
npm install

# Build Tailwind CSS
npm run build

# Start development server
npm run dev
# Frontend will be available at http://localhost:8080
```

### Step 3: Test Integration

Open browser and navigate to integration dashboard:
```
http://localhost:8080/integration.html
```

You should see:
- ✓ Backend Status: Connected
- ✓ Authentication: Not authenticated (yet)
- Configuration showing http://localhost:5000

---

## Configuration

### Frontend Configuration

Edit `src/js/config.js` to customize:

```javascript
const CONFIG = {
  // Backend API URL (change for production)
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  
  // Authentication timeout (1 hour)
  AUTH_TIMEOUT: 3600000,
  
  // File upload limit (100MB)
  MAX_FILE_SIZE: 100 * 1024 * 1024,
  
  // Feature flags
  ENABLE_WEBHOOKS: true,
  ENABLE_NOTIFICATIONS: true,
  ENABLE_ANALYTICS: true,
  
  // Debug mode
  DEBUG_MODE: false,
  LOG_LEVEL: 'info',
};
```

### Environment Variables

For production deployment, use environment variables:

```bash
# .env or system environment
REACT_APP_API_URL=https://api.agentmesh.com
REACT_APP_DEBUG_MODE=false
```

### Frontend HTML Integration

Script inclusions needed in HTML files:

```html
<!-- Required scripts (in order) -->
<script src="../js/config.js"></script>      <!-- Configuration -->
<script src="../js/auth.js"></script>        <!-- Authentication -->
<script src="../js/api-v2.js"></script>      <!-- API Client -->
<script src="../js/app.js"></script>         <!-- Your application -->
```

---

## Testing Connection

### Method 1: Integration Dashboard

```
1. Open http://localhost:8080/integration.html
2. Check "Backend Status" - should show "Connected"
3. Navigate to "Test API" tab
4. Click "Test" button
5. Should see successful response
```

### Method 2: Console Test

```javascript
// Open browser console (F12)

// 1. Check backend health
await AgentMeshAPI.checkHealth()

// 2. Test API connectivity
await fetch('http://localhost:5000/health').then(r => r.json())

// 3. Check auth status
AuthManager.isAuthenticated()
```

### Method 3: Command Line

```bash
# Test backend health
curl http://localhost:5000/health

# Test frontend is served
curl http://localhost:8080

# Test with authentication (after login)
curl -H "Authorization: Bearer <token>" http://localhost:5000/analyses
```

---

## API Integration

### Authentication Required

Most API endpoints require authentication. Use either:

**Option 1: JWT Token (Recommended for UI)**
```javascript
// Automatically handled by AuthManager
const result = await AuthManager.login('user@example.com', 'password');

// Then make API calls
const analyses = await AgentMeshAPI.listAnalyses();
```

**Option 2: API Key (Recommended for scripts)**
```python
# Python backend client
from backend.api_client import AgentMeshAPI

client = AgentMeshAPI(api_key="sk_live_...")
result = client.submit_analysis(code="def hello(): pass")
```

### Core API Usage Examples

#### 1. Register and Login
```javascript
// Register
const registerResult = await AuthManager.register(
  'user@example.com',
  'username',
  'password'
);

// Login
const loginResult = await AuthManager.login(
  'user@example.com',
  'password'
);

// Check auth status
if (AuthManager.isAuthenticated()) {
  console.log('User:', AuthManager.getUserInfo());
}
```

#### 2. Submit Code Analysis
```javascript
// Simple analysis
const result = await AgentMeshAPI.submitAnalysis(
  "def hello():\n    print('Hello')",
  'hello.py',
  'Analyze this function',
  ['security', 'performance'],
  'HIGH'
);

console.log('Analysis ID:', result.analysis_id);

// Wait for results
const analysis = await AgentMeshAPI.pollAnalysisStatus(result.analysis_id);
console.log('Quality Score:', analysis.quality_score);
```

#### 3. Upload and Analyze File
```javascript
// Upload file
const file = document.getElementById('fileInput').files[0];
const uploadResult = await AgentMeshAPI.uploadFile(file);

// Submit for analysis using uploaded file
const analysis = await AgentMeshAPI.submitAnalysis(
  null,
  uploadResult.filename,
  'Analyze uploaded file'
);
```

#### 4. Generate Reports
```javascript
// JSON report
const jsonReport = await AgentMeshAPI.generateReport(
  'analysis_id',
  'json'
);

// HTML report
const htmlReport = await AgentMeshAPI.generateReport(
  'analysis_id',
  'html',
  'executive'  // template
);

// Download PDF report
const pdfBlob = await AgentMeshAPI.generateReport(
  'analysis_id',
  'pdf'
);

// Download PDF with link
const url = URL.createObjectURL(pdfBlob);
const link = document.createElement('a');
link.href = url;
link.download = 'report.pdf';
link.click();
```

#### 5. Analytics and Metrics
```javascript
// Get dashboard
const dashboard = await AgentMeshAPI.getDashboardAnalytics();
console.log('Total analyses:', dashboard.total_analyses);
console.log('Average quality:', dashboard.avg_quality_score);

// Get trends
const trends = await AgentMeshAPI.getQualityTrends(30);
console.log('Quality trend:', trends.trend);

// Comprehensive metrics
const metrics = await AgentMeshAPI.getComprehensiveAnalytics();
```

---

## Authentication Flow

### JWT Token Flow

```
User Request
    ↓
[Login Form]
    ↓
POST /auth/login
    ↓
Backend validates credentials
    ↓
[Backend returns JWT token + API key]
    ↓
AuthManager stores in localStorage
    ↓
AuthManager.setupInterceptors() adds token to all requests
    ↓
API calls automatically include: Authorization: Bearer <token>
    ↓
API requests proceed
```

### Session Management

```javascript
// Check if still authenticated
if (!AuthManager.isAuthenticated()) {
  // Token expired or invalid
  // Show login page
  redirectToLogin();
}

// Validate token with backend
const isValid = await AuthManager.validateToken();
if (!isValid) {
  // Refresh or re-login
  AuthManager.logout();
  redirectToLogin();
}
```

---

## Error Handling

### API Error Responses

All API errors return JSON with error message:

```javascript
// Error response example
{
  "error": "Unauthorized: Invalid API key"
}
```

### Frontend Error Handling

```javascript
try {
  const result = await AgentMeshAPI.submitAnalysis(...);
  
  if (result.error) {
    console.error('API Error:', result.error);
    // Show error to user
    showErrorMessage(result.error);
  } else {
    // Success
    processResult(result);
  }
} catch (error) {
  console.error('Network Error:', error);
  showErrorMessage('Network error: ' + error.message);
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Cannot reach backend` | Backend not running | Start backend: `python -m backend.rest_api_v2 --debug` |
| `CORS error` | Browser security | Enable CORS in backend (already enabled in v2 API) |
| `Unauthorized: Invalid API key` | Invalid or missing API key | Re-authenticate: `AuthManager.login(...)` |
| `Analysis not found` | Invalid analysis ID | Check analysis ID is correct |
| `File too large` | File exceeds 100MB limit | Upload smaller file or increase limit |

---

## Troubleshooting

### Backend Connection Issues

**Problem**: Frontend shows "Backend Disconnected"

**Solutions**:
```bash
# 1. Check backend is running
netstat -ano | findstr :5000  # Windows
lsof -i :5000                  # Mac/Linux

# 2. Check database is connected
python -c "from backend.database import db_manager; print(db_manager.is_connected())"

# 3. Check firewall allows port 5000
# Windows Firewall: Allow Python through firewall

# 4. Check API URL is correct
# console: console.log(CONFIG.API_BASE_URL)

# 5. Restart backend
python -m backend.rest_api_v2 --debug
```

### Authentication Issues

**Problem**: Login fails but credentials are correct

**Solutions**:
```bash
# 1. Check user exists in database
psql -U agentmesh_user -d agentmesh
# SELECT * FROM users WHERE email = 'user@example.com';

# 2. Check localStorage in browser
# console: localStorage.getItem('agentmesh_access_token')

# 3. Clear authentication and re-login
# console: AuthManager.logout(); AuthManager.login(...)

# 4. Verify JWT_SECRET_KEY in backend
# grep JWT_SECRET_KEY .env
```

### CORS Issues

**Problem**: "Access to XMLHttpRequest blocked by CORS policy"

**Solution**:
CORS is already enabled in `backend/rest_api_v2.py` with:
```python
CORS(app)
```

If still issues, ensure:
```python
# In rest_api_v2.py
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8080", "http://localhost:3000"],
        "methods": ["GET", "POST", "DELETE", "PUT", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-API-Key"]
    }
})
```

### File Upload Issues

**Problem**: File upload fails

**Solutions**:
```bash
# 1. Check file size
du -h filename.py  # Mac/Linux
# Windows: Properties → General

# 2. Check uploads directory exists
ls -la backend/uploads/  # or create it

# 3. Check file permissions
chmod 755 backend/uploads/

# 4. Check max file size setting
# In frontend: CONFIG.MAX_FILE_SIZE
# In backend: app.config['MAX_CONTENT_LENGTH']
```

### Performance Issues

**Problem**: Slow API responses or timeouts

**Solutions**:
```bash
# 1. Check database performance
psql -U agentmesh_user -d agentmesh
# SELECT COUNT(*) FROM analyses;

# 2. Check connection pool size
# In config: DATABASE_POOL_SIZE, DATABASE_MAX_OVERFLOW

# 3. Check API server load
# Windows: Task Manager → Performance
# Mac/Linux: top, htop

# 4. Monitor with Prometheus
# See BACKEND_DEPLOYMENT.md for metrics configuration
```

---

## Production Deployment

### Frontend Production Build

```bash
# Build for production
npm run build

# Serve with web server (Nginx, Apache, etc)
# See Frontend README for deployment options
```

### Backend Production Deployment

```bash
# Set environment
set FLASK_ENV=production
set JWT_SECRET_KEY=your_secret_key_here

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.rest_api_v2:app

# Or use systemd service file
sudo systemctl start agentmesh-api
```

### HTTPS Configuration

```nginx
# In reverse proxy (Nginx)
server {
    listen 443 ssl http2;
    server_name api.agentmesh.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    location / {
        proxy_pass http://backend:5000;
    }
}
```

Update frontend configuration:
```javascript
CONFIG.API_BASE_URL = 'https://api.agentmesh.com'
```

---

## Support

- 📧 Email: support@agentmesh.com
- 🐛 Issues: https://github.com/agentmesh/agentmesh/issues
- 📚 Docs: https://docs.agentmesh.com
- 💬 Discord: https://discord.gg/agentmesh

---

## Next Steps

1. ✅ Start backend and frontend
2. ✅ Test integration dashboard
3. ✅ Register a user account
4. ✅ Submit code for analysis
5. ✅ View results and reports
6. ✅ Deploy to production

Happy analyzing! 🚀
