# Quick Start Guide

Get up and running with the Social Media Analytics AI Agent in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- OpenAI or Anthropic API key
- Basic terminal/command line knowledge

## Option 1: Quick Start with Docker (Recommended)

### Step 1: Clone and Configure

```bash
git clone <repository-url>
cd workspace
cp .env.example .env
```

### Step 2: Add Your API Key

Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

Or use Anthropic Claude:
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
LLM_PROVIDER=anthropic
```

### Step 3: Start Everything

```bash
docker-compose up -d
```

### Step 4: Verify It's Running

```bash
curl http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "app": "Social Media Analytics AI Agent",
  "version": "1.0.0",
  "environment": "production"
}
```

### Step 5: Access the API

Open your browser and go to:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

🎉 **You're all set!** Jump to [Using the API](#using-the-api) below.

## Option 2: Local Development Setup

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Set Up PostgreSQL

```bash
# Using Docker
docker run -d \
  --name social_analytics_db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=social_analytics \
  -p 5432:5432 \
  postgres:15-alpine
```

Or install PostgreSQL locally and create the database:
```sql
CREATE DATABASE social_analytics;
```

### Step 3: Set Up Redis

```bash
# Using Docker
docker run -d --name social_analytics_redis -p 6379:6379 redis:7-alpine
```

### Step 4: Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### Step 5: Initialize Database

```bash
python scripts/init_db.py
```

### Step 6: Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

🎉 **You're running!** Visit http://localhost:8000/docs

## Using the API

### 1. Register a User

Using the interactive docs at http://localhost:8000/docs:

1. Go to **POST /api/v1/auth/register**
2. Click "Try it out"
3. Enter:
```json
{
  "username": "demo",
  "email": "demo@example.com",
  "password": "Demo123!"
}
```
4. Click "Execute"

Or use curl:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"Demo123!"}'
```

### 2. Login

Using curl:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=demo&password=Demo123!"
```

Save the `access_token` from the response!

### 3. Chat with the AI Agent

```bash
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"message":"What are my top performing posts?"}'
```

### 4. Get Analytics Summary

```bash
curl -X GET "http://localhost:8000/api/v1/analytics/summary" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Example Conversations

Try these questions with the AI agent:

1. **"Show me engagement metrics for Instagram"**
   - Get detailed engagement data for Instagram

2. **"What are my top 5 performing posts?"**
   - See your best content ranked by engagement

3. **"Analyze my Twitter engagement trends"**
   - Track performance over time

4. **"Which platform has the best engagement rate?"**
   - Compare performance across platforms

5. **"What's the best time to post on Instagram?"**
   - Get audience insights and recommendations

## Quick Test Script

Save this as `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"

# Register
echo "Registering user..."
curl -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"quicktest","email":"test@example.com","password":"Test123!"}'

# Login and get token
echo -e "\n\nLogging in..."
TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -d "username=quicktest&password=Test123!" | jq -r '.access_token')

echo "Token: $TOKEN"

# Chat
echo -e "\n\nChatting with AI..."
curl -X POST "$BASE_URL/chat/message" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Show me my top performing posts"}' | jq

# Analytics
echo -e "\n\nGetting analytics..."
curl -X GET "$BASE_URL/analytics/summary" \
  -H "Authorization: Bearer $TOKEN" | jq
```

Run it:
```bash
chmod +x test_api.sh
./test_api.sh
```

## Troubleshooting

### "Connection refused" error
```bash
# Check if the app is running
docker-compose ps

# Or check the port
curl http://localhost:8000/health
```

### "Could not validate credentials"
- Make sure you're using the correct token
- Check if token has expired (default: 30 minutes)
- Try logging in again

### "Database connection error"
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check DATABASE_URL in .env
```

### "Missing API key" error
- Verify OPENAI_API_KEY or ANTHROPIC_API_KEY is set in .env
- Make sure there are no quotes around the key
- Restart the application after changing .env

## Stopping the Application

### Docker
```bash
docker-compose down
```

### Local
Press `Ctrl+C` in the terminal where the app is running

## Next Steps

1. **Read the Full Documentation**: Check out [README.md](README.md)
2. **Explore API Guide**: See [API_GUIDE.md](API_GUIDE.md) for detailed endpoints
3. **Deploy to Production**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Understand Architecture**: Read [ARCHITECTURE.md](ARCHITECTURE.md)

## Getting Help

- **Check the docs**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health
- **View logs**: 
  ```bash
  # Docker
  docker-compose logs -f app
  
  # Local
  # Check terminal output
  ```

## Tips

1. **Use the interactive docs** at `/docs` - it's the easiest way to test
2. **Save your token** - you'll need it for authenticated requests
3. **Ask natural questions** - the AI understands conversational language
4. **Start a conversation** - use the same `session_id` for follow-up questions
5. **Check examples** - see [API_GUIDE.md](API_GUIDE.md) for more examples

---

**Need more help?** Open an issue or check the comprehensive [README.md](README.md)
