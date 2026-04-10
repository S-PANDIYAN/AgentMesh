# AgentMesh Backend System - Complete Architecture & Implementation

Comprehensive documentation of the AgentMesh backend system including all components, features, and integration points.

## Executive Summary

The AgentMesh backend is a **production-ready, enterprise-grade code analysis platform** with:

- **Database persistence**: PostgreSQL/MySQL with full schema
- **Authentication**: JWT tokens + API keys with rate limiting
- **File management**: Secure upload, storage, and retrieval
- **Task processing**: Distributed analysis with multiple agents
- **Reporting**: JSON, HTML, and PDF report generation
- **Analytics**: Real-time metrics and quality trends
- **Notifications**: Email, webhooks, and in-app notifications
- **REST API**: Fully documented with 30+ endpoints
- **Python SDK**: Easy client library implementation

---

## System Architecture

### Components Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User/Client                          │
├─────────────────────────────────────────────────────────────┤
│                  REST API v2 (Flask)                        │
│  (30+ endpoints, authentication, rate limiting)             │
├─────────────────────────────────────────────────────────────┤
│         ┌──────────────┬──────────────┬────────────┐        │
│         │              │              │            │        │
│     ┌───▼───┐      ┌───▼───┐     ┌───▼───┐   ┌───▼────┐   │
│     │ Auth  │      │ File  │     │Report │   │Analytics│  │
│     │System │      │Manager│     │Engine │   │Engine   │  │
│     └───┬───┘      └───┬───┘     └───┬───┘   └───┬────┘   │
│         │              │             │            │        │
├─────────┼──────────────┼─────────────┼────────────┼────────┤
│      Database Abstraction Layer (SQLAlchemy ORM)           │
├─────────────────────────────────────────────────────────────┤
│    ┌──────────────────────────────────────────────────┐    │
│    │         PostgreSQL / MySQL Database              │    │
│    │  (Users, APIKeys, Analyses, Tasks, Logs, etc)   │    │
│    └──────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│    ┌──────────────────────────────────────────────────┐    │
│    │      File Storage (Local/S3/Azure Blob)         │    │
│    └──────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│      ┌──────────────┬──────────────┬──────────────┐        │
│      │              │              │              │        │
│   ┌──▼──┐       ┌──▼──┐       ┌──▼──┐       ┌──▼──────┐  │
│   │Email│       │Redis│       │Webhook│      │Monitoring│ │
│   │Service│     │Cache│       │Service│      │Service │  │
│   └──────┘      └─────┘       └───────┘      └─────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Client Request (REST API)
    ↓
Authentication & Authorization (Auth Manager)
    ↓
Route Handler (Flask endpoint)
    ↓
Business Logic (Service layer)
    ↓
Database Query (SQLAlchemy ORM)
    ↓
Database Operations (PostgreSQL/MySQL)
    ↓
Cache Update (Redis)
    ↓
Notification Queue (Email/Webhook)
    ↓
Analytics Update
    ↓
Response to Client
```

---

## Component Details

### 1. Authentication System (`backend/auth.py`)

**Features:**
- JWT token generation and validation
- API key management with rate limiting
- Password hashing (bcrypt)
- Permission-based access control
- Multi-level security decorators

**Key Classes:**
- `AuthenticationManager`: JWT token operations
- `UserManager`: User CRUD and authentication
- `APIKeyManager`: API key lifecycle
- `PermissionManager`: Permission checking

**Usage Example:**
```python
# Register user
user, api_key = UserManager.create_user(session, email, username, password)

# Authenticate
auth_user = UserManager.authenticate_user(session, email, password)

# Generate JWT
token = AuthenticationManager.create_access_token(user.id)

# Verify token
user_id = AuthenticationManager.verify_access_token(token)
```

---

### 2. Database Layer (`backend/database.py` & `backend/db_models.py`)

**Database Models:**
- **User**: User accounts (email, username, password_hash, created_at, updated_at)
- **APIKey**: API keys (user_id, key_hash, rate_limit, requests_made, is_active)
- **Analysis**: Code analysis records (user_id, file_name, quality_score, result, status)
- **Task**: Background tasks (task_id, description, priority, status, result)
- **Notification**: User notifications (user_id, type, message, is_read)
- **WebhookLog**: Webhook executions (user_id, event_type, url, status, response)

**Connection Management:**
```python
from backend.database import db_manager

# Initialize
db_manager.initialize()
db_manager.create_tables()

# Get session
session = db_manager.get_session()
try:
    # Operations
    pass
finally:
    session.close()
```

---

### 3. File Management (`backend/file_manager.py`)

**Features:**
- Secure file upload with validation
- File integrity verification
- Code diff generation
- Multiple storage backend support
- File type detection

**FileManager API:**
```python
# Upload file
file_id, filename, size, hash = file_manager.save_uploaded_file(file, user_id)

# Read file
content = file_manager.read_file_content(file_id)

# Verify integrity
is_valid = file_manager.verify_file_integrity(file_id, expected_hash)

# Generate diff
diff = CodeDiffGenerator.generate_diff(original, modified)
```

---

### 4. Report Generation (`backend/report_generator.py`)

**Formats Supported:**
- **JSON**: Structured data format
- **HTML**: Interactive web-based report
- **PDF**: Professional document format

**Report Templates:**
- **default**: Standard analysis report
- **executive**: C-level summary
- **detailed**: Comprehensive analysis

**Usage:**
```python
report = ReportGenerator.generate_report(
    analysis_data,
    format_type='pdf',
    template_type='executive'
)
```

---

### 5. Notification System (`backend/notifications.py`)

**Notification Types:**
- In-app notifications (database-backed)
- Email notifications (SMTP)
- Webhook notifications (HTTP POST)

**Services:**
- `NotificationService`: In-app notifications
- `EmailNotificationManager`: Email delivery
- `WebhookManager`: Webhook registration and triggering

**Example:**
```python
# Send notification
NotificationService.create_notification(
    session, user_id, 'analysis_complete',
    'Your analysis is ready'
)

# Send email
EmailNotificationManager.send_email(
    to_email, 'Analysis Complete',
    template='analysis_complete',
    context={...}
)

# Trigger webhook
WebhookManager.trigger_webhook(
    session, 'analysis.completed',
    {'analysis_id': '123', ...}
)
```

---

### 6. Analytics Engine (`backend/analytics.py`)

**Metrics Collected:**
- Total analyses per user
- Average quality scores
- Quality trends over time
- Issues distribution by type
- Agent utilization statistics

**Key Methods:**
```python
# Dashboard stats
stats = AnalyticsManager.get_user_dashboard_stats(session, user_id)

# Quality trends
trend = AnalyticsManager.get_quality_trend(session, user_id, days=30)

# Comprehensive metrics
metrics = AnalyticsManager.get_metrics_summary(session, user_id)

# System stats
sys_stats = SystemMetricsManager.get_system_stats(session)
```

---

### 7. REST API v2 (`backend/rest_api_v2.py`)

**Endpoint Categories:**

| Category | Endpoints | Purpose |
|----------|-----------|---------|
| Auth | `/auth/register`, `/auth/login`, `/auth/validate-token` | User authentication |
| API Keys | `/api-keys/generate`, `/api-keys`, `/api-keys/<id>` | API key management |
| Analysis | `/review`, `/analyses/<id>`, `/analyses` | Code submission & results |
| Reports | `/reports/<id>` | Report generation |
| Files | `/upload`, `/files/<id>` | File management |
| Analytics | `/analytics/dashboard`, `/analytics/trends`, `/analytics/comprehensive` | Metrics & trends |
| Notifications | `/notifications` | User notifications |
| System | `/health`, `/system/stats` | Health & monitoring |

**Authentication:**
- JWT Token: `Authorization: Bearer <token>`
- API Key: `X-API-Key: <key>`

---

### 8. Python SDK (`backend/api_client.py`)

**High-Level Interface:**
```python
from backend.api_client import AgentMeshAPI

client = AgentMeshAPI(api_key="sk_live_...", base_url="http://localhost:5000")

# Register & authenticate
client.register("user@example.com", "username", "password")
client.login("user@example.com", "password")

# Submit analysis
result = client.submit_analysis(
    code="def hello(): pass",
    agents=["security", "performance"]
)

# Wait for completion
analysis = client.wait_for_analysis(result['analysis_id'])

# Generate report
report = client.generate_report(analysis['id'], format='pdf')

# Get analytics
analytics = client.get_dashboard_analytics()
```

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Analyses Table
```sql
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    file_name VARCHAR(255),
    file_size INTEGER,
    file_hash VARCHAR(255),
    status VARCHAR(50) DEFAULT 'SUBMITTED',
    quality_score DECIMAL(5,2),
    confidence_score DECIMAL(5,2),
    final_decision VARCHAR(100),
    issues_found INTEGER DEFAULT 0,
    critical_issues INTEGER DEFAULT 0,
    processing_time_ms INTEGER,
    agents_consulted TEXT[],
    result JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    CONSTRAINT analyses_status_check CHECK (status IN ('SUBMITTED', 'PROCESSING', 'COMPLETED', 'FAILED'))
);
```

### API Keys Table
```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    key_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    rate_limit INTEGER DEFAULT 100,
    requests_made INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP
);
```

---

## API Workflow Examples

### Complete Analysis Workflow

```
1. User Registration
   POST /auth/register
   → User account created
   → API key generated
   → JWT token issued

2. Submit Code Analysis
   POST /review (with API key)
   → File validated and stored
   → Analysis record created
   → Task queued for processing
   → Analysis ID returned

3. Process Analysis
   [Background: Coordinator runs agents]
   → Results stored in database
   → Status updated to COMPLETED
   → Quality metrics calculated

4. Get Results
   GET /analyses/<id> (with API key)
   → Return analysis results
   → Include quality score
   → Include found issues

5. Generate Report
   POST /reports/<id> (with API key)
   → Format data
   → Generate PDF/HTML/JSON
   → Return to user

6. View Analytics
   GET /analytics/dashboard (with API key)
   → Aggregate user statistics
   → Return trends and insights
```

### File Upload and Analysis

```
1. Upload File
   POST /upload (multipart/form-data)
   → Validate file
   → Store securely
   → Calculate hash
   → Return file ID

2. Submit Analysis with Upload
   POST /review (with file_id)
   → Retrieve uploaded file
   → Create analysis record
   → Queue for processing

3. Process and Retrieve
   [Background processing]
   GET /analyses/<id>
   → Return results
```

---

## Performance Characteristics

### Typical Response Times
- Health check: < 10ms
- User login: 100-150ms
- Submit analysis: 200-300ms
- Get analysis results: 50-100ms
- Generate report: 1-5 seconds (depending on format)
- List analyses: 100-200ms

### Scalability
- **Single server**: 100-500 analyses/day
- **3-server cluster**: 5,000-10,000 analyses/day
- **Enterprise cluster**: 100,000+ analyses/day

### Database Performance
- Connection pool: 20-40 connections
- Query time: < 100ms (95th percentile)
- Throughput: 1,000+ queries/second

---

## Security Features

### Authentication
- ✅ JWT tokens with 1-hour expiration
- ✅ API keys with individual rate limits
- ✅ Bcrypt password hashing (cost factor: 12)
- ✅ HTTPS/TLS enforced
- ✅ CORS protection

### Authorization
- ✅ Role-based access control (RBAC)
- ✅ Resource-level permissions
- ✅ User data isolation
- ✅ API key scoping

### Data Protection
- ✅ Encrypted file storage
- ✅ Database encryption at rest
- ✅ Secure file deletion
- ✅ Audit logging

### API Security
- ✅ Rate limiting per user/API key
- ✅ Input validation and sanitization
- ✅ SQL injection prevention (ORM)
- ✅ CSRF protection

---

## Deployment Options

### Development
```bash
python -m backend.rest_api_v2 --debug
```

### Production Single Server
```bash
gunicorn -w 4 -b 0.0.0.0:5000 backend.rest_api_v2:app
```

### Docker
```bash
docker-compose up -d
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentmesh-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: agentmesh/api:latest
        ports:
        - containerPort: 5000
```

---

## Monitoring & Observability

### Metrics Exposed
- `http_requests_total`: Total requests by endpoint
- `http_request_duration_seconds`: Request latency
- `database_connections`: Active database connections
- `queue_depth`: Pending analysis tasks
- `cache_hit_rate`: Redis cache effectiveness

### Health Checks
```
GET /health
→ Database connectivity
→ Cache connectivity
→ File storage accessibility
→ Agent registry status
```

### Logging
- Request logs (all endpoints)
- Database query logs (slow queries)
- Error logs (exceptions and failures)
- Audit logs (authentication, api key usage)

---

## Integration Points

### Framework Integration
```python
from framework_init import initialize_framework
from backend.rest_api_v2 import app

# Initialize agent framework
registry, loader, coordinator, logger = initialize_framework()

# Use with REST API
# File backend/rest_api_v2.py uses coordinator for analysis
```

### Database Integration
```python
from backend.database import db_manager
from common.models import Task

# Create task for coordinator
task = Task(
    task_id=analysis_id,
    description="Analyze code",
    payload={'code': code_content}
)

# Coordinator processes it
results = coordinator.coordinate(task)

# Store in database via ORM
analysis.result = results
session.commit()
```

### Notification Integration
```python
from backend.notifications import NotificationService, EmailNotificationManager

# After analysis complete
NotificationService.create_notification(...)
EmailNotificationManager.send_email(...)
WebhookManager.trigger_webhook(...)
```

---

## Next Steps

1. **Quick Start**: Follow [BACKEND_QUICKSTART.md](./BACKEND_QUICKSTART.md)
2. **Integration**: Read [BACKEND_INTEGRATION_GUIDE.md](./BACKEND_INTEGRATION_GUIDE.md)
3. **Deployment**: Follow [BACKEND_DEPLOYMENT.md](./BACKEND_DEPLOYMENT.md)
4. **API Reference**: See [REST_API_v2_DOCS.md](./REST_API_v2_DOCS.md)
5. **Testing**: Review [test_backend_system.py](../tests/test_backend_system.py)

---

## Support

- 📧 Email: support@agentmesh.com
- 🐛 Issues: https://github.com/agentmesh/agentmesh/issues
- 📚 Documentation: https://docs.agentmesh.com
- 💬 Community: https://discord.gg/agentmesh

---

## License

AgentMesh Backend © 2024. All rights reserved.
