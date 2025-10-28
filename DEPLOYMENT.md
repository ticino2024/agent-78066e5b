# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- API keys for OpenAI or Anthropic
- PostgreSQL 15+ (if not using Docker)
- Redis 7+ (if not using Docker)

## Quick Start with Docker

### 1. Clone and Configure

```bash
git clone <repository-url>
cd workspace
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
OPENAI_API_KEY=sk-your-actual-key
# or
ANTHROPIC_API_KEY=sk-ant-your-actual-key
```

### 2. Build and Run

```bash
docker-compose up -d
```

### 3. Verify Deployment

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f app

# Health check
curl http://localhost:8000/health
```

### 4. Create Initial User

```bash
docker-compose exec app python scripts/create_test_user.py
```

## Production Deployment

### Environment Configuration

1. **Update `.env` for production**:
```bash
APP_ENV=production
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/db
```

2. **Generate Secret Key**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Using Docker Compose

```bash
# Build production image
docker-compose -f docker-compose.yml build

# Start services
docker-compose up -d

# Initialize database
docker-compose exec app python scripts/init_db.py

# Check logs
docker-compose logs -f
```

### Manual Deployment

#### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Configure Database

```bash
# Install PostgreSQL
sudo apt-get install postgresql-15

# Create database
sudo -u postgres psql
CREATE DATABASE social_analytics;
CREATE USER appuser WITH PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE social_analytics TO appuser;
```

#### 3. Install Redis

```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### 4. Initialize Application

```bash
# Initialize database
python scripts/init_db.py

# Create test user (optional)
python scripts/create_test_user.py
```

#### 5. Run with Gunicorn

```bash
pip install gunicorn
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Using Systemd Service

Create `/etc/systemd/system/social-analytics.service`:

```ini
[Unit]
Description=Social Media Analytics AI Agent
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/social-analytics
Environment="PATH=/opt/social-analytics/venv/bin"
ExecStart=/opt/social-analytics/venv/bin/gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start social-analytics
sudo systemctl enable social-analytics
sudo systemctl status social-analytics
```

## Cloud Deployment

### AWS Deployment

#### Using ECS (Elastic Container Service)

1. **Build and Push Docker Image**:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker build -t social-analytics .
docker tag social-analytics:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/social-analytics:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/social-analytics:latest
```

2. **Set Up RDS (PostgreSQL)**:
- Create RDS PostgreSQL instance
- Note connection details
- Update security groups

3. **Set Up ElastiCache (Redis)**:
- Create Redis cluster
- Note connection endpoint

4. **Create ECS Task Definition**:
- Use Fargate launch type
- Set environment variables
- Configure CloudWatch logging

5. **Deploy Service**:
- Create Application Load Balancer
- Configure target groups
- Create ECS service

#### Using EC2

1. **Launch EC2 Instance**:
```bash
# Use Ubuntu 22.04 LTS
# t3.medium or larger recommended
```

2. **Install Dependencies**:
```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv postgresql-client redis-tools
```

3. **Deploy Application**:
```bash
cd /opt
sudo git clone <repository-url> social-analytics
cd social-analytics
sudo python3.11 -m venv venv
sudo venv/bin/pip install -r requirements.txt
```

4. **Configure and Run** (follow manual deployment steps above)

### Google Cloud Platform

#### Using Cloud Run

1. **Build Container**:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/social-analytics
```

2. **Deploy**:
```bash
gcloud run deploy social-analytics \
  --image gcr.io/PROJECT_ID/social-analytics \
  --platform managed \
  --region us-central1 \
  --set-env-vars DATABASE_URL=...,OPENAI_API_KEY=... \
  --allow-unauthenticated
```

#### Using GKE (Google Kubernetes Engine)

1. **Create Cluster**:
```bash
gcloud container clusters create social-analytics-cluster \
  --num-nodes 3 \
  --machine-type n1-standard-2
```

2. **Deploy with Kubernetes** (see Kubernetes section)

### Azure Deployment

#### Using Azure Container Instances

1. **Push to Azure Container Registry**:
```bash
az acr build --registry myregistry --image social-analytics .
```

2. **Deploy**:
```bash
az container create \
  --resource-group myResourceGroup \
  --name social-analytics \
  --image myregistry.azurecr.io/social-analytics \
  --dns-name-label social-analytics \
  --ports 8000
```

## Kubernetes Deployment

### Create Deployment

`k8s/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: social-analytics
spec:
  replicas: 3
  selector:
    matchLabels:
      app: social-analytics
  template:
    metadata:
      labels:
        app: social-analytics
    spec:
      containers:
      - name: app
        image: social-analytics:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: openai-key
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Create Service

`k8s/service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: social-analytics
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: social-analytics
```

### Deploy

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Nginx Reverse Proxy

`/etc/nginx/sites-available/social-analytics`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts for long-running requests
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

Enable and test:
```bash
sudo ln -s /etc/nginx/sites-available/social-analytics /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## SSL/TLS Configuration

### Using Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Monitoring and Logging

### Application Logs

```bash
# Docker
docker-compose logs -f app

# Systemd
sudo journalctl -u social-analytics -f

# Direct logs
tail -f logs/app.log
```

### Health Monitoring

```bash
# Check health endpoint
curl http://localhost:8000/health

# Check metrics (if enabled)
curl http://localhost:8000/metrics
```

## Backup and Recovery

### Database Backup

```bash
# Backup
pg_dump -h localhost -U postgres social_analytics > backup.sql

# Restore
psql -h localhost -U postgres social_analytics < backup.sql
```

### Vector Store Backup

```bash
# Backup Chroma data
tar -czf chroma-backup.tar.gz data/chroma/

# Restore
tar -xzf chroma-backup.tar.gz
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer
- Multiple app instances
- Shared PostgreSQL and Redis
- Distributed vector store

### Vertical Scaling
- Increase CPU/memory
- Optimize database queries
- Tune connection pools

## Troubleshooting

### Common Issues

1. **Connection Refused**:
   - Check if services are running
   - Verify firewall rules
   - Check port bindings

2. **Database Connection Error**:
   - Verify DATABASE_URL
   - Check PostgreSQL is running
   - Verify credentials

3. **Agent Timeout**:
   - Increase AGENT_MAX_EXECUTION_TIME
   - Check API key validity
   - Monitor network connectivity

4. **High Memory Usage**:
   - Reduce CONVERSATION_MEMORY_SIZE
   - Implement agent session cleanup
   - Optimize vector store

## Performance Tuning

### Database
```python
# Connection pool settings
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40
```

### Workers
```bash
# Calculate workers: (2 * CPU cores) + 1
gunicorn --workers 9 --worker-class uvicorn.workers.UvicornWorker
```

### Caching
- Enable Redis caching
- Cache frequent queries
- Implement response caching

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use HTTPS in production
- [ ] Set strong database passwords
- [ ] Limit database access by IP
- [ ] Enable firewall rules
- [ ] Keep dependencies updated
- [ ] Implement rate limiting
- [ ] Enable CORS properly
- [ ] Use environment variables for secrets
- [ ] Regular security audits

## Maintenance

### Updates

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart social-analytics
```

### Database Migrations

```bash
# Using Alembic (when configured)
alembic upgrade head
```

## Support

For deployment issues:
- Check logs first
- Review this guide
- Consult ARCHITECTURE.md
- Open GitHub issue
