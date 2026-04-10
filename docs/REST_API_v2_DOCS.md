# AgentMesh REST API v2 Documentation

## Overview
Complete REST API with database integration, authentication, and analytics support.

Base URL: `http://localhost:5000`

## Authentication

### JWT Token Authentication
Use JWT tokens for most endpoints:
```bash
Authorization: Bearer <access_token>
```

### API Key Authentication
Use API keys for programmatic access:
```bash
X-API-Key: <api_key>
```

---

## Endpoints

### Authentication

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password"
}

Returns:
{
  "user_id": "uuid",
  "email": "user@example.com",
  "username": "username",
  "access_token": "jwt_token",
  "api_key": "api_key"
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}

Returns:
{
  "user_id": "uuid",
  "email": "user@example.com",
  "username": "username",
  "access_token": "jwt_token"
}
```

#### Validate Token
```
GET /auth/validate-token
Authorization: Bearer <token>

Returns:
{
  "user_id": "uuid",
  "email": "user@example.com",
  "username": "username"
}
```

---

### API Keys

#### Generate API Key
```
POST /api-keys/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My API Key",
  "rate_limit": 100
}

Returns:
{
  "api_key": "sk_live_...",
  "name": "My API Key"
}
```

#### List API Keys
```
GET /api-keys
Authorization: Bearer <token>

Returns:
{
  "api_keys": [
    {
      "id": "key_id",
      "name": "My API Key",
      "created_at": "2024-01-01T00:00:00Z",
      "last_used_at": "2024-01-02T00:00:00Z",
      "requests_made": 150,
      "is_active": true
    }
  ]
}
```

#### Revoke API Key
```
DELETE /api-keys/<key_id>
Authorization: Bearer <token>

Returns:
{
  "message": "API key revoked"
}
```

---

### Code Analysis

#### Submit Code for Analysis
```
POST /review
X-API-Key: <api_key>
Content-Type: application/json

{
  "code": "def hello(): pass",
  "file_name": "hello.py",
  "description": "Analyze this function",
  "agents": ["security", "performance", "code_quality"],
  "priority": "HIGH"
}

Returns:
{
  "analysis_id": "uuid",
  "status": "submitted",
  "message": "Analysis queued for processing"
}
```

#### Get Analysis Results
```
GET /analyses/<analysis_id>
X-API-Key: <api_key>

Returns:
{
  "id": "analysis_id",
  "file_name": "hello.py",
  "status": "COMPLETED",
  "quality_score": 85.5,
  "confidence_score": 92.0,
  "final_decision": "APPROVED",
  "issues_found": 2,
  "critical_issues": 0,
  "processing_time_ms": 1250,
  "agents_consulted": ["security", "performance"],
  "result": {
    "security": {...},
    "performance": {...}
  },
  "created_at": "2024-01-01T00:00:00Z",
  "completed_at": "2024-01-01T00:00:05Z"
}
```

#### List All Analyses
```
GET /analyses?limit=50&status=COMPLETED
X-API-Key: <api_key>

Query Parameters:
- limit: Number of results (default: 50)
- status: Filter by status (SUBMITTED, PROCESSING, COMPLETED, FAILED)

Returns:
{
  "analyses": [
    {
      "id": "analysis_id",
      "file_name": "hello.py",
      "status": "COMPLETED",
      "quality_score": 85.5,
      "issues_found": 2,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

---

### Reports

#### Generate Report
```
POST /reports/<analysis_id>
X-API-Key: <api_key>
Content-Type: application/json

{
  "format": "pdf",
  "template": "executive"
}

Format Options:
- json: JSON format
- html: HTML report
- pdf: PDF document

Template Options:
- default: Standard report
- executive: Executive summary
- detailed: Comprehensive analysis

Returns:
- PDF file or HTML/JSON content
```

---

### File Management

#### Upload File
```
POST /upload
X-API-Key: <api_key>
Content-Type: multipart/form-data

Parameters:
- file: Python file to analyze

Returns:
{
  "file_id": "file_id",
  "filename": "hello.py",
  "file_size": 1024,
  "file_hash": "sha256_hash"
}
```

#### Get File Content
```
GET /files/<file_id>
X-API-Key: <api_key>

Returns:
{
  "content": "def hello(): pass"
}
```

---

### Analytics

#### Dashboard Analytics
```
GET /analytics/dashboard
X-API-Key: <api_key>

Returns:
{
  "total_analyses": 100,
  "avg_quality_score": 82.5,
  "analyses_by_status": {
    "COMPLETED": 95,
    "PROCESSING": 3,
    "FAILED": 2
  },
  "top_issues": [
    {
      "type": "security",
      "count": 12,
      "severity": "HIGH"
    }
  ]
}
```

#### Quality Trends
```
GET /analytics/trends?days=30
X-API-Key: <api_key>

Query Parameters:
- days: Number of days to analyze (default: 30)

Returns:
{
  "dates": ["2024-01-01", "2024-01-02", ...],
  "quality_scores": [80.0, 82.5, ...],
  "issue_counts": [5, 4, ...],
  "trend": "improving"
}
```

#### Comprehensive Metrics
```
GET /analytics/comprehensive
X-API-Key: <api_key>

Returns:
{
  "summary": {...},
  "by_agent": {
    "security": {...},
    "performance": {...},
    "code_quality": {...}
  },
  "time_series": {...}
}
```

---

### Notifications

#### Get Notifications
```
GET /notifications?unread=true&limit=50
Authorization: Bearer <token>

Query Parameters:
- unread: Only unread notifications (default: false)
- limit: Number of notifications (default: 50)

Returns:
{
  "notifications": [
    {
      "id": "notification_id",
      "type": "analysis_complete",
      "message": "Analysis #123 is complete",
      "is_read": false,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

### System

#### Health Check
```
GET /health

Returns:
{
  "status": "healthy",
  "database": "connected",
  "users_total": 150,
  "analyses_total": 5000,
  "agents_loaded": 6
}
```

#### System Statistics
```
GET /system/stats

Returns:
{
  "cpu_usage_percent": 25.5,
  "memory_usage_mb": 512,
  "database_connections": 10,
  "api_requests_per_minute": 150,
  "active_analyses": 5,
  "queue_depth": 10
}
```

---

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created
- `202 Accepted`: Request accepted for processing
- `400 Bad Request`: Invalid request
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `413 Payload Too Large`: File too large
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

---

## Rate Limiting

API keys have rate limits (default: 100 requests per minute).

Headers:
- `X-RateLimit-Limit`: Maximum requests per minute
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Time when limit resets

---

## Error Responses

All errors return JSON:
```json
{
  "error": "Error message describing what went wrong"
}
```

---

## Examples

### Example 1: Complete Analysis Workflow
```bash
# 1. Register user
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "user",
    "password": "password"
  }'

# 2. Generate API key
curl -X POST http://localhost:5000/api-keys/generate \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My API Key"}'

# 3. Submit code for analysis
curl -X POST http://localhost:5000/review \
  -H "X-API-Key: <api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello(): print(\"hello\")",
    "agents": ["security", "performance"]
  }'

# 4. Get analysis results
curl -X GET http://localhost:5000/analyses/<analysis_id> \
  -H "X-API-Key: <api_key>"

# 5. Generate PDF report
curl -X POST http://localhost:5000/reports/<analysis_id> \
  -H "X-API-Key: <api_key>" \
  -H "Content-Type: application/json" \
  -d '{"format": "pdf"}' \
  -o report.pdf
```

### Example 2: File Upload and Analysis
```bash
# Upload file
curl -X POST http://localhost:5000/upload \
  -H "X-API-Key: <api_key>" \
  -F "file=@src/main.py"

# Get file content
curl -X GET http://localhost:5000/files/<file_id> \
  -H "X-API-Key: <api_key>"
```

---

## Configuration

### Environment Variables
```bash
DATABASE_URL=postgresql://user:password@localhost/agentmesh
JWT_SECRET_KEY=your_secret_key_here
API_MAX_FILE_SIZE=104857600  # 100MB in bytes
```

### Running the API
```bash
python -m backend.rest_api_v2 --host 0.0.0.0 --port 5000
```

To enable debug mode:
```bash
python -m backend.rest_api_v2 --debug
```

---

## SDK Examples

### Python SDK
```python
from backend.api_client import AgentMeshAPI

client = AgentMeshAPI(api_key="sk_live_...", base_url="http://localhost:5000")

# Submit analysis
result = client.submit_analysis(
    code="def hello(): pass",
    agents=["security", "performance"]
)

# Get results
analysis = client.get_analysis(result['analysis_id'])
print(f"Quality Score: {analysis['quality_score']}")

# Generate report
client.generate_report(
    analysis_id=result['analysis_id'],
    format='pdf'
)
```

### JavaScript/Node.js SDK
```javascript
const AgentMesh = require('agentmesh-sdk');

const client = new AgentMesh.Client({
  apiKey: 'sk_live_...',
  baseUrl: 'http://localhost:5000'
});

// Submit analysis
const result = await client.submitAnalysis({
  code: 'def hello(): pass',
  agents: ['security', 'performance']
});

// Get results
const analysis = await client.getAnalysis(result.analysisId);
console.log(`Quality Score: ${analysis.qualityScore}`);
```

---

## Webhook Integrations

Configure webhooks to receive notifications when analyses complete:

```
POST /webhooks/configure
X-API-Key: <api_key>
Content-Type: application/json

{
  "url": "https://your-server.com/webhook",
  "events": ["analysis.completed", "analysis.failed"]
}
```

---

## Support

For issues or questions, open an issue on GitHub or contact support@agentmesh.com
