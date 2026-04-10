# Complete Setup & Connection Guide

Quick guide to set up AgentMesh backend and frontend, and ensure they're connected.

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+
- Node.js 14+
- PostgreSQL 12+ or MySQL 8.0+

### 1. Backend Setup

```bash
# Navigate to project root
cd d:\project\AgentMesh

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Or (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements_backend.txt

# Create .env file
echo DATABASE_URL=postgresql://user:password@localhost/agentmesh > .env
echo JWT_SECRET_KEY=change_me_in_production >> .env

# Initialize database
python -c "from backend.database import db_manager; db_manager.initialize()"

# Start backend
python -m backend.rest_api_v2 --debug
```

✅ Backend running at: `http://localhost:5000`

### 2. Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd AgentMesh\UI\frontend

# Install dependencies
npm install

# Build CSS
npm run build

# Start frontend
npm run dev
```

✅ Frontend running at: `http://localhost:8080`

### 3. Test Connection

**Option 1: Integration Dashboard**
```
Open: http://localhost:8080/integration.html
- Should show "Backend Status: Connected"
- Click "Test API" to verify
```

**Option 2: Command Line**
```bash
# Test backend health
curl http://localhost:5000/health

# Test frontend is served
curl http://localhost:8080
```

**Option 3: Browser Console**
```javascript
// Open http://localhost:8080/integration.html
// Press F12, go to Console tab

// Check backend connection
await AgentMeshAPI.checkHealth()
// Should return: {status: "healthy", ...}

// Check auth
AuthManager.isAuthenticated()
// Should return: false (not logged in yet)
```

---

## 🔗 Verify Connected

### Frontend Should See Backend ✓

1. **Integration Dashboard Shows Connected**
   ```
   http://localhost:8080/integration.html
   → Backend Status: Connected ✓
   ```

2. **Can Register User**
   ```
   http://localhost:8080/integration.html
   → Register Tab
   → Enter email, username, password
   → Click Register
   → Should succeed
   ```

3. **Can Login**
   ```
   http://localhost:8080/integration.html
   → Login Tab
   → Enter credentials
   → Click Login
   → Should show "You are logged in"
   ```

4. **Can Make API Calls**
   ```
   http://localhost:8080/integration.html
   → Test API Tab
   → Select endpoint
   → Click Test
   → Should see JSON response
   ```

---

## 🐛 Connection Troubleshooting

### Problem 1: "Backend Disconnected" in Dashboard

**Diagnosis:**
```bash
# Terminal 1: Is backend running?
netstat -ano | findstr :5000  # Windows
# Or: lsof -i :5000           # Mac/Linux

# Terminal 2: Is database connected?
python
>>> from backend.database import db_manager
>>> db_manager.is_connected()  # Should be True
```

**Solution:**
```bash
# 1. Make sure backend is running
python -m backend.rest_api_v2 --debug

# 2. Check database connection
python -c "from backend.database import db_manager; db_manager.initialize()"

# 3. Check no firewall blocking port 5000
# Windows: Settings → Firewall → Allow through → Find Python
```

### Problem 2: CORS Error in Browser Console

**Error Message:**
```
Access to XMLHttpRequest from origin 'http://localhost:8080' has been blocked by CORS policy
```

**Solution:**
CORS is enabled by default. If still seeing error:

```python
# In backend/rest_api_v2.py (should be at top)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

Restart backend after fixing.

### Problem 3: "Unauthorized" When Making API Calls

**Error Message:**
```json
{"error": "Unauthorized: Missing authentication"}
```

**Solution:**
```javascript
// Must login first
const result = await AuthManager.login('user@example.com', 'password');

// Then API calls will work
const analyses = await AgentMeshAPI.listAnalyses();
```

### Problem 4: Database Connection Failed

**Error Message:**
```
ERROR: (psycopg2.OperationalError) could not connect to server: Connection refused
```

**Solution:**
```bash
# 1. Check database is running
# PostgreSQL:
psql -U postgres -d postgres  # Should connect

# MySQL:
mysql -u root -p              # Should connect

# 2. Create database if not exists
psql -U postgres
>>> CREATE DATABASE agentmesh;
>>> CREATE USER agentmesh_user WITH PASSWORD 'password';
>>> GRANT ALL PRIVILEGES ON DATABASE agentmesh TO agentmesh_user;

# 3. Update .env file
DATABASE_URL=postgresql://agentmesh_user:password@localhost:5432/agentmesh

# 4. Test connection
python -c "from backend.database import db_manager; print(db_manager.is_connected())"
```

### Problem 5: "npm: command not found"

**Error Message:**
```
npm: command not found
```

**Solution:**
```bash
# Install Node.js from https://nodejs.org
# Then verify installation
node --version    # Should show v14+
npm --version     # Should show 6+

# Try again
npm install
npm run dev
```

---

## 📊 Test Full Workflow

Complete end-to-end test:

```javascript
// In browser console at http://localhost:8080/integration.html

// 1. Register
const reg = await AuthManager.register('test@example.com', 'testuser', 'test123');
console.log('Registered:', reg);

// 2. Login
const login = await AuthManager.login('test@example.com', 'test123');
console.log('Logged in:', login);

// 3. Submit analysis
const analysis = await AgentMeshAPI.submitAnalysis(
  "def hello():\n    print('hello')",
  'hello.py',
  'Test analysis',
  ['security', 'performance'],
  'HIGH'
);
console.log('Analysis submitted:', analysis);

// 4. Poll for results
const result = await AgentMeshAPI.pollAnalysisStatus(analysis.analysis_id, 5, 2000);
console.log('Results:', result);

// 5. Generate report
const report = await AgentMeshAPI.generateReport(analysis.analysis_id, 'json');
console.log('Report:', report);

// 6. Get analytics
const analytics = await AgentMeshAPI.getDashboardAnalytics();
console.log('Analytics:', analytics);
```

Expected output shows all operations successful! ✓

---

## 🔧 Configuration Reference

### Backend Configuration (.env)

```properties
# Database connection string
DATABASE_URL=postgresql://user:password@localhost:5432/agentmesh

# JWT secret key (change in production!)
JWT_SECRET_KEY=your_secret_key_here

# Max file upload size (bytes, default 100MB)
API_MAX_FILE_SIZE=104857600

# Environment
FLASK_ENV=development  # or 'production'

# Logging
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=*
```

### Frontend Configuration (AgentMesh/UI/frontend/.env)

```properties
# Backend API URL
REACT_APP_API_URL=http://localhost:5000

# Debug mode
REACT_APP_DEBUG_MODE=false

# Logging level
REACT_APP_LOG_LEVEL=info

# Features
REACT_APP_ENABLE_WEBHOOKS=true
REACT_APP_ENABLE_NOTIFICATIONS=true
REACT_APP_ENABLE_ANALYTICS=true
```

---

## 📚 Documentation Links

| Document | Purpose |
|----------|---------|
| [REST_API_v2_DOCS.md](../docs/REST_API_v2_DOCS.md) | Full API reference |
| [BACKEND_INTEGRATION_GUIDE.md](../docs/BACKEND_INTEGRATION_GUIDE.md) | Backend integration |
| [FRONTEND_BACKEND_INTEGRATION.md](../docs/FRONTEND_BACKEND_INTEGRATION.md) | Frontend-backend connection |
| [BACKEND_QUICKSTART.md](../docs/BACKEND_QUICKSTART.md) | Backend setup |
| [BACKEND_DEPLOYMENT.md](../docs/BACKEND_DEPLOYMENT.md) | Production deployment |
| [BACKEND_ARCHITECTURE.md](../docs/BACKEND_ARCHITECTURE.md) | System architecture |

---

## 🎯 Integration Checklist

- [ ] Backend installed and running on http://localhost:5000
- [ ] Frontend installed and running on http://localhost:8080
- [ ] Integration dashboard shows "Connected"
- [ ] Can successfully register a new user
- [ ] Can successfully login with registered account
- [ ] Can submit code for analysis
- [ ] Can retrieve analysis results
- [ ] Can generate reports
- [ ] Can view analytics
- [ ] Configuration verified

---

## 🚀 Ready for Production?

See [BACKEND_DEPLOYMENT.md](../docs/BACKEND_DEPLOYMENT.md) for:
- SSL/TLS configuration
- Load balancing
- Database replication
- Monitoring and alerting
- Docker deployment
- Kubernetes setup

---

## 💬 Need Help?

- **Integration Dashboard**: `/integration.html` - Interactive testing and debugging
- **Browser Console**: `F12` - Run JavaScript commands directly
- **GitHub Issues**: Report bugs or ask questions
- **Email**: support@agentmesh.com

---

**Congratulations!** Your backend and frontend are now connected and ready to use! 🎉
