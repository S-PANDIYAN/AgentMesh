# Backend System: Deployment & Scaling Guide

Complete guide for deploying AgentMesh backend in production environments.

## Table of Contents

1. [Deployment Architectures](#deployment-architectures)
2. [Database Setup](#database-setup)
3. [API Server Configuration](#api-server-configuration)
4. [Containerization](#containerization)
5. [Scaling](#scaling)
6. [Monitoring](#monitoring)
7. [Security](#security)
8. [Disaster Recovery](#disaster-recovery)

---

## Deployment Architectures

### Single Server (Development/Small Scale)

```
┌─────────────────────────────────────┐
│        Single Server                │
├─────────────────────────────────────┤
│  Flask API (Port 5000)              │
│  PostgreSQL Database                │
│  File Storage                       │
└─────────────────────────────────────┘
```

### Load Balanced (Production)

```
┌──────────────────────────────────────────────────┐
│              Load Balancer (Nginx)               │
└────────┬─────────────────────────────┬───────────┘
         │                             │
    ┌────▼────────┐          ┌────────▼────┐
    │ API Server 1│          │ API Server 2 │
    ├─────────────┤          ├──────────────┤
    │  Flask App  │          │   Flask App  │
    └──────┬──────┘          └─────┬────────┘
           │                       │
           └───────────┬───────────┘
                       │
           ┌───────────▼──────────┐
           │   PostgreSQL DB      │
           │  (Connection Pool)   │
           └──────────────────────┘
           
           ┌──────────────────────┐
           │   File Storage (S3)  │
           └──────────────────────┘
```

### Distributed (Enterprise Scale)

```
┌────────────────────────────────────────────────────────┐
│     CDN (CloudFlare / AWS CloudFront)                  │
└─────────────┬──────────────────────────────┬───────────┘
              │                              │
    ┌─────────▼────────┐          ┌─────────▼────────┐
    │ API Cluster 1    │          │ API Cluster 2    │
    │ (3+ Servers)     │          │ (3+ Servers)     │
    └────────┬─────────┘          └────────┬─────────┘
             │                             │
    ┌────────▼───────────────────────────▼────────┐
    │       Database Cluster (Primary + Replicas) │
    └─────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────┐
    │  Redis Cache (Session + Rate Limiting)      │
    └─────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────┐
    │      Object Storage (S3 / MinIO)            │
    └─────────────────────────────────────────────┘
```

---

## Database Setup

### PostgreSQL Production Configuration

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE agentmesh;
CREATE USER agentmesh_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE agentmesh TO agentmesh_user;
\q
```

### PostgreSQL Optimization

```sql
-- postgresql.conf
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

-- Enable WAL archiving for backups
wal_level = replica
archive_mode = on
archive_command = 'test ! -f /backup/wal_archive/%f && cp %p /backup/wal_archive/%f'

-- Enable streaming replication
max_wal_senders = 3
wal_keep_size = 1GB
hot_standby = on
```

### Connection Pooling (PgBouncer)

```ini
# pgbouncer.ini
[databases]
agentmesh = host=localhost port=5432 dbname=agentmesh

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 10
reserve_pool_size = 5
reserve_pool_timeout = 3
max_idle = 600
```

### Database Backup

```bash
#!/bin/bash
# backup_db.sh

BACKUP_DIR="/backup/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)

# Full backup
pg_dump -U agentmesh_user -d agentmesh | gzip > $BACKUP_DIR/agentmesh_$DATE.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/agentmesh_$DATE.sql.gz s3://agentmesh-backups/

# Keep only last 30 days
find $BACKUP_DIR -name "agentmesh_*.sql.gz" -mtime +30 -delete
```

#### Schedule Backup

```bash
# Add to crontab
0 2 * * * /backup/backup_db.sh  # Daily at 2 AM
```

---

## API Server Configuration

### Gunicorn Configuration

```python
# gunicorn_config.py
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "agentmesh-api"

# SSL/TLS
keyfile = "/etc/ssl/private/key.pem"
certfile = "/etc/ssl/certs/cert.pem"
```

### Systemd Service File

```ini
# /etc/systemd/system/agentmesh-api.service
[Unit]
Description=AgentMesh API Service
After=network.target postgresql.service

[Service]
Type=notify
User=agentmesh
WorkingDirectory=/app/agentmesh
Environment="PATH=/app/agentmesh/venv/bin"
Environment="DATABASE_URL=postgresql://agentmesh_user:password@localhost/agentmesh"
Environment="FLASK_ENV=production"
Environment="JWT_SECRET_KEY=your_secret_key"

ExecStart=/app/agentmesh/venv/bin/gunicorn \
    --config gunicorn_config.py \
    backend.rest_api_v2:app

ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
KillSignal=SIGTERM

Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/agentmesh
upstream agentmesh_backend {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    listen 80;
    server_name api.agentmesh.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.agentmesh.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
    limit_req zone=api_limit burst=200 nodelay;
    
    # Request size limits
    client_max_body_size 100M;
    
    # Gzip compression
    gzip on;
    gzip_types text/plain application/json;
    
    # Proxy settings
    location / {
        proxy_pass http://agentmesh_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffering
        proxy_buffering on;
        proxy_buffer_size 8k;
        proxy_buffers 24 8k;
    }
    
    # Health check endpoint (no logging)
    location /health {
        proxy_pass http://agentmesh_backend;
        access_log off;
    }
}
```

---

## Containerization

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt backend/requirements_backend.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r backend/requirements_backend.txt && \
    pip install gunicorn

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run application
CMD ["gunicorn", \
     "--config", "gunicorn_config.py", \
     "--workers", "4", \
     "--bind", "0.0.0.0:5000", \
     "backend.rest_api_v2:app"]
```

### Docker Compose (Production)

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: agentmesh
      POSTGRES_USER: agentmesh_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backup:/backup
    restart: unless-stopped
    networks:
      - agentmesh

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://agentmesh_user:${DB_PASSWORD}@db:5432/agentmesh
      FLASK_ENV: production
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    depends_on:
      - db
    restart: unless-stopped
    networks:
      - agentmesh
    volumes:
      - uploads:/app/uploads
    ports:
      - "5000:5000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/ssl
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - agentmesh

volumes:
  postgres_data:
  uploads:

networks:
  agentmesh:
    driver: bridge
```

---

## Scaling

### Horizontal Scaling

```bash
# Start multiple API instances
for i in {1..4}; do
  PORT=$((5000 + i))
  gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    -e DATABASE_URL='postgresql://...' \
    backend.rest_api_v2:app &
done
```

### Load Balancing

```bash
# Install HAProxy
sudo apt-get install haproxy

# Configure load balancer
sudo systemctl enable haproxy
sudo systemctl start haproxy
```

### Database Replication

```bash
# Setup read replica
sudo -u postgres pg_basebackup \
  -h primary_host \
  -D /var/lib/postgresql/replica \
  -U replication_user
```

---

## Monitoring

### Prometheus Metrics

```python
# Add to rest_api_v2.py
from prometheus_client import Counter, Histogram, generate_latest

http_requests_total = Counter(
    'http_requests_total', 'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration = Histogram(
    'http_request_duration_seconds', 'HTTP request duration'
)

@app.route('/metrics')
def metrics():
    return generate_latest()
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "AgentMesh Backend Monitoring",
    "panels": [
      {
        "title": "API Requests Per Second",
        "targets": [{"expr": "rate(http_requests_total[5m])"}]
      },
      {
        "title": "Database Connections",
        "targets": [{"expr": "pg_stat_activity_count"}]
      },
      {
        "title": "Request Latency",
        "targets": [{"expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket)"}]
      }
    ]
  }
}
```

### Logging

```python
# Setup ELK Stack logging
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.FileHandler('app.log')
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```

---

## Security

### SSL/TLS Certificates

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365

# Or use Let's Encrypt
certbot certonly --standalone -d api.agentmesh.com
```

### Environment Variable Management

```bash
# Use .env file (never commit)
# Load with python-dotenv or os.getenv

# Or use secrets management
aws secretsmanager get-secret-value --secret-id agentmesh/production
```

### Database Security

```sql
-- Create restricted user
CREATE USER api_user WITH PASSWORD 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO api_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO api_user;

-- Enable SSL for remote connections
hostssl agentmesh api_user 0.0.0.0/0 md5
```

---

## Disaster Recovery

### Backup Strategy

```bash
# Daily full backup
0 2 * * * /backup/backup_db.sh

# Hourly incremental backup
0 * * * * pg_dump --incremental ...

# Replicate to secondary site
*/5 * * * * rsync -avz /backup/ user@backup-server:/backup/
```

### Recovery Procedure

```bash
# 1. Stop API servers
systemctl stop agentmesh-api

# 2. Restore database
psql -U agentmesh_user -d agentmesh < backup/latest.sql

# 3. Verify
psql -U agentmesh_user -d agentmesh -c "SELECT COUNT(*) FROM analyses;"

# 4. Restart API
systemctl start agentmesh-api
```

### High Availability Setup

```yaml
# Patroni configuration for PostgreSQL HA
scope: agentmesh
namespace: /agentmesh/
name: postgres-1

etcd:
  host: etcd-server:2379

postgresql:
  data_dir: /var/lib/postgresql/data
  parameters:
    wal_level: replica
    max_wal_senders: 10
    wal_keep_size: 1GB

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
```

---

## Performance Tuning

### Connection Pooling

```ini
# pgBouncer optimization
default_pool_size = 25
min_pool_size = 10
reserve_pool_size = 5
idle_in_transaction_session_timeout = 600000
```

### Query Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_analyses_user_status 
  ON analyses(user_id, status) 
  WHERE status = 'COMPLETED';

CREATE INDEX idx_analyses_created_at 
  ON analyses(created_at DESC);

-- Analyze tables regularly
ANALYZE analyses;
```

### Caching Strategy

```python
# Redis caching
from redis import Redis

cache = Redis(host='localhost', port=6379)

# Cache user analyses for 1 hour
cache.setex(f'user:{user_id}:analyses', 3600, json.dumps(analyses))
```

---

## Deployment Checklist

- [ ] Database configured and optimized
- [ ] SSL certificates installed
- [ ] Load balancer configured
- [ ] Database backups scheduled
- [ ] Monitoring and alerting set up
- [ ] Firewall rules configured
- [ ] Database replication verified
- [ ] Disaster recovery plan tested
- [ ] Performance baseline established
- [ ] Security audit completed

---

## Support

For deployment assistance, contact support@agentmesh.com or open an issue on GitHub.
