# Backend System Quick Start Guide

Get started with AgentMesh backend in 5 minutes.

## Prerequisites

- Python 3.9+
- PostgreSQL 12+ (or MySQL 8.0+)
- pip

## Installation

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/agentmesh/agentmesh.git
cd agentmesh

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements_backend.txt
```

### 2. Configure Database

Create `.env` file:

```bash
# PostgreSQL (recommended)
DATABASE_URL=postgresql://username:password@localhost:5432/agentmesh

# Or MySQL
# DATABASE_URL=mysql+pymysql://username:password@localhost:3306/agentmesh

JWT_SECRET_KEY=your_secret_key_here_change_in_production
API_MAX_FILE_SIZE=104857600
```

### 3. Initialize Database

```bash
python -c "
from backend.database import db_manager
db_manager.initialize()
db_manager.create_tables()
print('Database initialized successfully')
"
```

## Running the API

### Option 1: Development Mode

```bash
python -m backend.rest_api_v2 --debug
```

Open http://localhost:5000/health to verify

### Option 2: Production Mode

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.rest_api_v2:app
```

### Option 3: Docker

```bash
docker-compose up -d
```

## First API Call

### 1. Register User

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "myuser",
    "password": "password123"
  }'
```

Response:
```json
{
  "user_id": "abc123",
  "email": "user@example.com",
  "access_token": "eyJ0eXAi...",
  "api_key": "sk_live_..."
}
```

### 2. Submit Code for Analysis

```bash
curl -X POST http://localhost:5000/review \
  -H "X-API-Key: sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"Hello\")",
    "agents": ["security", "performance"],
    "priority": "HIGH"
  }'
```

Response:
```json
{
  "analysis_id": "analysis_123",
  "status": "submitted"
}
```

### 3. Get Results

```bash
curl http://localhost:5000/analyses/analysis_123 \
  -H "X-API-Key: sk_live_..."
```

## Python SDK Usage

```python
from backend.api_client import AgentMeshAPI

# Initialize client
client = AgentMeshAPI(api_key="sk_live_...", base_url="http://localhost:5000")

# Submit analysis
result = client.submit_analysis(
    code="def hello(): pass",
    agents=["security", "performance"]
)

print(f"Analysis ID: {result['analysis_id']}")

# Wait for completion
analysis = client.wait_for_analysis(result['analysis_id'])

print(f"Quality Score: {analysis['quality_score']}")
print(f"Final Decision: {analysis['final_decision']}")

# Generate report
report = client.generate_report(
    analysis['id'],
    format='pdf',
    save_path='report.pdf'
)

# Get analytics
analytics = client.get_dashboard_analytics()
print(f"Total Analyses: {analytics['total_analyses']}")
```

## Common Operations

### Upload File

```bash
curl -X POST http://localhost:5000/upload \
  -H "X-API-Key: sk_live_..." \
  -F "file=@mycode.py"
```

### Generate Report

```bash
curl -X POST http://localhost:5000/reports/analysis_123 \
  -H "X-API-Key: sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{"format": "pdf", "template": "executive"}' \
  -o report.pdf
```

### Get Analytics

```bash
curl http://localhost:5000/analytics/dashboard \
  -H "X-API-Key: sk_live_..."
```

### List API Keys

```bash
curl http://localhost:5000/api-keys \
  -H "Authorization: Bearer <access_token>"
```

## Testing

Run the test suite:

```bash
pip install pytest pytest-cov
pytest tests/test_backend_system.py -v

# With coverage
pytest tests/test_backend_system.py --cov=backend --cov-report=html
```

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
psql -U username -d agentmesh

# Or check MySQL
mysql -u username -p agentmesh
```

### API Won't Start

```bash
# Check port is available
lsof -i :5000  # On Linux/Mac
netstat -ano | findstr :5000  # On Windows
```

### All Tests Fail

```bash
# Reinitialize database
python -c "
from backend.database import db_manager
db_manager.drop_all_tables()
db_manager.create_tables()
print('Database reset')
"
```

## Next Steps

1. **Read Full Documentation**: [BACKEND_INTEGRATION_GUIDE.md](./BACKEND_INTEGRATION_GUIDE.md)
2. **API Reference**: [REST_API_v2_DOCS.md](./REST_API_v2_DOCS.md)
3. **Security**: Review authentication and API key management
4. **Deployment**: Set up production environment with proper configuration

## Key Features

✅ User authentication (JWT + API Keys)  
✅ Code analysis with multiple agents  
✅ File upload and management  
✅ Report generation (JSON, HTML, PDF)  
✅ Analytics and quality trends  
✅ Webhook notifications  
✅ Rate limiting  
✅ Database-backed persistence  

## Support

- GitHub Issues: https://github.com/agentmesh/agentmesh/issues
- Email: support@agentmesh.com
- Documentation: https://docs.agentmesh.com
