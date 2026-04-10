# Backend System Integration Guide

Complete guide to using the AgentMesh backend system with database, authentication, file management, and analytics.

## Table of Contents

1. [Setup](#setup)
2. [Database Configuration](#database-configuration)
3. [Authentication & Security](#authentication--security)
4. [File Management](#file-management)
5. [Task Processing](#task-processing)
6. [Notifications](#notifications)
7. [Analytics](#analytics)
8. [Reports](#reports)
9. [Webhooks](#webhooks)
10. [Deployment](#deployment)

---

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 12+ (or MySQL 8.0+)
- Redis (for caching and queue)
- Node.js 14+ (optional, for frontend)

### Installation

```bash
# Clone the repository
git clone https://github.com/agentmesh/agentmesh.git
cd agentmesh

# Install dependencies
pip install -r backend/requirements_backend.txt
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Directory Structure

```
backend/
├── database.py              # Database management
├── db_models.py            # SQLAlchemy models
├── auth.py                 # Authentication & authorization
├── file_manager.py         # File management
├── report_generator.py     # Report generation
├── notifications.py        # Notification service
├── analytics.py            # Analytics engine
├── rest_api_v2.py         # REST API
└── api_client.py          # Python SDK
```

---

## Database Configuration

### Initialize Database

```python
from backend.database import db_manager

# Initialize database with models
db_manager.initialize()

# Create or migrate tables
db_manager.create_tables()

# Check connection
if db_manager.is_connected():
    print("Database connected successfully")
```

### Environment Variables

```bash
# PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/agentmesh

# Or MySQL
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/agentmesh

# Database connection pool
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40
DATABASE_POOL_RECYCLE=3600
```

### Database Schema

The system automatically creates tables for:

- **Users**: User accounts and profiles
- **APIKeys**: API key management
- **Analysis**: Code analysis records
- **Task**: Background task tracking
- **Notification**: User notifications
- **WebhookLog**: Webhook execution logs

---

## Authentication & Security

### User Registration and Login

```python
from backend.auth import UserManager, AuthenticationManager
from backend.database import db_manager

session = db_manager.get_session()

try:
    # Register new user
    user, api_key = UserManager.create_user(
        session=session,
        email="user@example.com",
        username="username",
        password="password"
    )
    print(f"User created: {user.id}")
    print(f"API Key: {api_key}")
    
    # Authenticate user
    authenticated_user = UserManager.authenticate_user(
        session=session,
        email="user@example.com",
        password="password"
    )
    
    if authenticated_user:
        # Generate JWT token
        token = AuthenticationManager.create_access_token(authenticated_user.id)
        print(f"JWT Token: {token}")
        
        # Validate token
        user_id = AuthenticationManager.verify_access_token(token)
        print(f"Token valid for user: {user_id}")

finally:
    session.close()
```

### API Key Management

```python
from backend.auth import APIKeyManager

session = db_manager.get_session()

try:
    # Create API key
    api_key = APIKeyManager.create_api_key(
        session=session,
        user_id=user_id,
        name="My API Key",
        rate_limit=1000
    )
    print(f"API Key created: {api_key}")
    
    # List API keys
    keys = APIKeyManager.list_user_api_keys(session, user_id)
    for key in keys:
        print(f"Key: {key.id}, Requests: {key.requests_made}")
    
    # Revoke API key
    APIKeyManager.revoke_api_key(session, user_id, key_id)
    print("API key revoked")

finally:
    session.close()
```

### Permission Control

```python
from backend.auth import PermissionManager

session = db_manager.get_session()

try:
    # Grant permission
    PermissionManager.grant_permission(
        session=session,
        user_id=user_id,
        resource_type="analysis",
        action="read"
    )
    
    # Check permission
    if PermissionManager.has_permission(
        session=session,
        user_id=user_id,
        resource_type="analysis",
        action="write"
    ):
        print("User can write analyses")

finally:
    session.close()
```

### Decorators for Flask Routes

```python
from flask import Flask
from backend.auth import require_auth, require_api_key

app = Flask(__name__)

# JWT Token authentication
@app.route('/user/profile')
@require_auth
def get_profile(user_id):
    return {'user_id': user_id}

# API Key authentication
@app.route('/api/analyses')
@require_api_key
def list_analyses(user_id):
    return {'user_id': user_id}
```

---

## File Management

### Upload and Store Files

```python
from backend.file_manager import FileManager, get_file_manager
import tempfile
from werkzeug.datastructures import FileStorage

file_manager = get_file_manager()

# From Flask request
file = request.files['file']
file_id, filename, size, hash = file_manager.save_uploaded_file(file, user_id)

# Or from local file
file_id, filename, size, hash = file_manager.save_file_from_path(
    file_path="/path/to/file.py",
    user_id=user_id,
    original_filename="main.py"
)

print(f"File stored: {file_id}")
print(f"File hash: {hash}")
```

### Retrieve Files

```python
# Read file content
content = file_manager.read_file_content(file_id)

# Get file metadata
metadata = file_manager.get_file_metadata(file_id)
print(f"Size: {metadata['size']}")
print(f"Hash: {metadata['hash']}")

# Verify file integrity
if file_manager.verify_file_integrity(file_id, expected_hash):
    print("File integrity verified")
```

### Code Diff Generation

```python
from backend.file_manager import CodeDiffGenerator

# Generate diff between two code versions
diff = CodeDiffGenerator.generate_diff(
    original_code=old_code,
    modified_code=new_code
)

# Generate unified diff
unified = CodeDiffGenerator.generate_unified_diff(old_code, new_code)

# Apply patch
patched_code = CodeDiffGenerator.apply_patch(original_code, patch_content)
```

---

## Task Processing

### Queue and Process Tasks

```python
from core.models import Task
from framework_init import initialize_framework

registry, loader, coordinator, logger = initialize_framework()

# Create task
task = Task(
    task_id="analysis_123",
    description="Analyze security vulnerabilities",
    priority="HIGH",
    task_type="code_review",
    payload={
        'code': code_content,
        'analysis_id': analysis_id,
        'agents': ['security', 'performance']
    }
)

# Process task with coordinator
logger.logger.info(f"Processing task: {task.task_id}")

# Get results
results = coordinator.coordinate(task)

# Store results
session = db_manager.get_session()
try:
    analysis = session.query(Analysis).get(analysis_id)
    analysis.result = results
    analysis.status = "COMPLETED"
    analysis.agents_consulted = list(results.keys())
    session.commit()
finally:
    session.close()
```

---

## Notifications

### Send Notifications

```python
from backend.notifications import NotificationService, EmailNotificationManager

session = db_manager.get_session()

try:
    # Send in-app notification
    NotificationService.create_notification(
        session=session,
        user_id=user_id,
        type="analysis_complete",
        message="Your analysis is complete",
        data={'analysis_id': analysis_id}
    )
    
    # Send email notification
    EmailNotificationManager.send_email(
        to_email=user_email,
        subject="Analysis Complete",
        template="analysis_complete",
        context={
            'analysis_id': analysis_id,
            'quality_score': 85.5
        }
    )

finally:
    session.close()
```

### Configure Webhooks

```python
from backend.notifications import WebhookManager

session = db_manager.get_session()

try:
    # Register webhook
    WebhookManager.register_webhook(
        session=session,
        user_id=user_id,
        event_type="analysis.completed",
        url="https://your-server.com/webhook",
        is_active=True
    )
    
    # Trigger webhook
    WebhookManager.trigger_webhook(
        session=session,
        event_type="analysis.completed",
        payload={
            'analysis_id': analysis_id,
            'status': 'COMPLETED',
            'quality_score': 85.5
        }
    )

finally:
    session.close()
```

---

## Analytics

### Collect Metrics

```python
from backend.analytics import AnalyticsManager

session = db_manager.get_session()

try:
    # Get user dashboard stats
    stats = AnalyticsManager.get_user_dashboard_stats(session, user_id)
    print(f"Total analyses: {stats['total_analyses']}")
    print(f"Average quality: {stats['avg_quality_score']}")
    
    # Get quality trend
    trend = AnalyticsManager.get_quality_trend(session, user_id, days=30)
    print(f"Quality trend: {trend['trend']}")
    
    # Get metrics summary
    summary = AnalyticsManager.get_metrics_summary(session, user_id)
    print(f"Metrics: {summary}")

finally:
    session.close()
```

### System Metrics

```python
from backend.analytics import SystemMetricsManager

# Get system statistics
stats = SystemMetricsManager.get_system_stats(session)
print(f"CPU: {stats['cpu_usage_percent']}%")
print(f"Memory: {stats['memory_usage_mb']}MB")
print(f"Active analyses: {stats['active_analyses']}")
```

---

## Reports

### Generate Reports

```python
from backend.report_generator import ReportGenerator

# Prepare analysis data
analysis_data = {
    'file_name': 'main.py',
    'quality_score': 85.5,
    'issues_found': 2,
    'result': {'security': {...}, 'performance': {...}}
}

# Generate JSON report
json_report = ReportGenerator.generate_report(
    analysis_data,
    format_type='json',
    template_type='default'
)

# Generate HTML report
html_report = ReportGenerator.generate_report(
    analysis_data,
    format_type='html',
    template_type='executive'
)

# Generate PDF report
pdf_report = ReportGenerator.generate_report(
    analysis_data,
    format_type='pdf',
    template_type='detailed'
)
```

---

## Webhooks

### Webhook Integration

```python
# Webhook handler in your application
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.json
    
    if payload['event_type'] == 'analysis.completed':
        analysis_id = payload['data']['analysis_id']
        quality_score = payload['data']['quality_score']
        
        # Process completion
        print(f"Analysis {analysis_id} completed with score {quality_score}")
        
        return {'status': 'received'}, 200
    
    return {'status': 'ignored'}, 200
```

Example webhook payload:
```json
{
  "event_type": "analysis.completed",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "analysis_id": "abc123",
    "user_id": "user123",
    "status": "COMPLETED",
    "quality_score": 85.5,
    "issues_found": 2
  }
}
```

---

## Deployment

### Production Configuration

```bash
# Create production environment
set DATABASE_URL=postgresql://prod_user:prod_pass@prod_db:5432/agentmesh
set FLASK_ENV=production
set JWT_SECRET_KEY=your_secret_key
set API_MAX_FILE_SIZE=104857600
set LOG_LEVEL=INFO
```

### Run API Server

```bash
# Development
python -m backend.rest_api_v2 --debug

# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.rest_api_v2:app

# With environment file
gunicorn --env-file .env -w 4 -b 0.0.0.0:5000 backend.rest_api_v2:app
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt backend/requirements_backend.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r backend/requirements_backend.txt

COPY . .

ENV FLASK_APP=backend.rest_api_v2
ENV FLASK_ENV=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.rest_api_v2:app"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: agentmesh
      POSTGRES_USERNAME: agentmesh
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://agentmesh:password@db:5432/agentmesh
      FLASK_ENV: production
      JWT_SECRET_KEY: your_secret_key
    depends_on:
      - db
    volumes:
      - uploads:/app/uploads

volumes:
  postgres_data:
  uploads:
```

---

## Best Practices

### 1. Connection Management

```python
# Always use try-finally for session management
session = db_manager.get_session()
try:
    # Perform database operations
    pass
finally:
    session.close()
```

### 2. Error Handling

```python
from backend.database import DatabaseError

try:
    # Database operation
    pass
except DatabaseError as e:
    logger.logger.error(f"Database error: {e}")
    # Handle gracefully
```

### 3. Transaction Management

```python
session = db_manager.get_session()
try:
    # Start transaction
    obj1 = Model1(...)
    obj2 = Model2(...)
    session.add(obj1)
    session.add(obj2)
    session.commit()  # Commit all changes
except Exception as e:
    session.rollback()  # Rollback on error
finally:
    session.close()
```

### 4. Caching

```python
from backend.cache import CacheManager

cache = CacheManager()

# Set cache
cache.set('analysis_' + analysis_id, analysis_data, ttl=3600)

# Get cache
data = cache.get('analysis_' + analysis_id)

# Delete cache
cache.delete('analysis_' + analysis_id)
```

### 5. Logging

```python
from utils.logger import logger

logger.logger.info("Operation completed successfully")
logger.logger.warning("This might be an issue")
logger.logger.error("An error occurred", exc_info=True)
```

---

## Troubleshooting

### Database Connection Issues

```python
# Check connection
if not db_manager.is_connected():
    print("Database not connected")
    # Try reconnecting
    db_manager.reconnect()
```

### API Key Rate Limiting

```python
# Check remaining requests
if rate_limit_remaining < 10:
    print("Approaching rate limit")
    # Wait before making more requests
```

### File Upload Issues

```python
# Check file size
if file.size > MAX_FILE_SIZE:
    raise ValueError("File too large")

# Verify file type
if not file.filename.endswith('.py'):
    raise ValueError("Invalid file type")
```

---

## Support and Resources

- [API Documentation](./REST_API_v2_DOCS.md)
- [Database Schema](./DATABASE.md)
- [Security Guidelines](./SECURITY.md)
- GitHub Issues: https://github.com/agentmesh/agentmesh/issues
