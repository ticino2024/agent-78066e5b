# API Usage Guide

## Getting Started

Base URL: `http://localhost:8000`
API Version: `v1`
API Prefix: `/api/v1`

## Authentication

All endpoints except registration and login require authentication using JWT Bearer tokens.

### Register a New User

**Endpoint**: `POST /api/v1/auth/register`

**Request Body**:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### Login

**Endpoint**: `POST /api/v1/auth/login`

**Request Body** (form-data):
```
username=johndoe
password=SecurePass123!
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Using the Token**:
```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Chat Endpoints

### Send a Message to AI Agent

**Endpoint**: `POST /api/v1/chat/message`

**Headers**:
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "What are my engagement metrics for Instagram?",
  "session_id": "optional-existing-session-id"
}
```

**Response** (200 OK):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Based on your Instagram data, your account has 23,456 followers with an average engagement rate of 6.2%...",
  "metadata": {
    "timestamp": "2024-01-15T10:35:00",
    "intermediate_steps": 2,
    "tools_used": ["get_engagement_metrics"]
  }
}
```

### Get All Conversations

**Endpoint**: `GET /api/v1/chat/conversations`

**Query Parameters**:
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": 1,
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Analytics Discussion",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:35:00",
    "messages": []
  }
]
```

### Get Specific Conversation

**Endpoint**: `GET /api/v1/chat/conversations/{session_id}`

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Analytics Discussion",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:35:00",
  "messages": [
    {
      "id": 1,
      "conversation_id": 1,
      "role": "user",
      "content": "What are my engagement metrics?",
      "metadata": null,
      "created_at": "2024-01-15T10:30:00"
    },
    {
      "id": 2,
      "conversation_id": 1,
      "role": "assistant",
      "content": "Here are your engagement metrics...",
      "metadata": {
        "tools_used": ["get_engagement_metrics"]
      },
      "created_at": "2024-01-15T10:30:05"
    }
  ]
}
```

### Delete a Conversation

**Endpoint**: `DELETE /api/v1/chat/conversations/{session_id}`

**Response** (204 No Content)

## Analytics Endpoints

### Get Analytics Summary

**Endpoint**: `GET /api/v1/analytics/summary`

**Response** (200 OK):
```json
{
  "total_posts": 961,
  "total_engagement": 15432,
  "average_engagement_rate": 4.9,
  "top_platform": "instagram",
  "sentiment_overview": {
    "positive": 65,
    "neutral": 25,
    "negative": 10
  },
  "engagement_trends": [
    {
      "platform": "twitter",
      "trend": "stable",
      "rate": 4.5
    },
    {
      "platform": "instagram",
      "trend": "increasing",
      "rate": 6.2
    }
  ]
}
```

### Get Platform-Specific Analytics

**Endpoint**: `GET /api/v1/analytics/platform/{platform}`

**Path Parameters**:
- `platform`: twitter, instagram, facebook, or linkedin

**Response** (200 OK):
```json
{
  "platform": "instagram",
  "followers": 23456,
  "total_posts": 198,
  "avg_engagement_rate": 6.2,
  "recent_posts": [
    {
      "id": "instagram_post_0",
      "content": "Sample post 0 on instagram",
      "likes": 342,
      "shares": 45,
      "comments": 23,
      "views": 3421,
      "engagement_rate": 11.98,
      "timestamp": "2024-01-14T15:30:00"
    }
  ]
}
```

## Example Use Cases

### Use Case 1: Check Overall Performance

```bash
# 1. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=demo&password=Demo123!"

# 2. Get analytics summary
curl -X GET "http://localhost:8000/api/v1/analytics/summary" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Use Case 2: AI-Powered Analytics Query

```bash
# Ask the AI agent
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Which platform has the best engagement rate and what type of content performs best there?"
  }'
```

### Use Case 3: Multi-Turn Conversation

```bash
# First message
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me Instagram engagement metrics"}'

# Get session_id from response, then continue conversation
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What about the last 30 days?",
    "session_id": "YOUR_SESSION_ID"
  }'
```

## AI Agent Capabilities

The AI agent can understand and respond to various queries:

### Engagement Metrics
- "What are my engagement metrics for [platform]?"
- "Show me engagement data for the last 7 days"
- "Compare engagement across all platforms"

### Top Content
- "What are my top performing posts?"
- "Show me the best content on Instagram"
- "Which posts got the most engagement?"

### Trends Analysis
- "Analyze my engagement trends"
- "Is my Twitter engagement increasing?"
- "Show me performance trends over time"

### Audience Insights
- "What are my audience demographics?"
- "When is the best time to post?"
- "Tell me about my Instagram audience"

### General Questions
- "Which platform should I focus on?"
- "How can I improve my engagement rate?"
- "What type of content works best?"

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Currently, there are no rate limits in place. For production use, consider implementing rate limiting based on your requirements.

## Best Practices

1. **Store Tokens Securely**: Never expose JWT tokens in client-side code or logs
2. **Reuse Sessions**: Use the same `session_id` for related questions to maintain context
3. **Handle Errors**: Always check response status codes and handle errors gracefully
4. **Timeout Handling**: Agent responses may take 5-30 seconds depending on complexity
5. **Pagination**: Use `skip` and `limit` parameters for large result sets

## Testing with cURL

Complete example workflow:

```bash
# 1. Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"Test123!"}'

# 2. Login
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=testuser&password=Test123!" | jq -r '.access_token')

# 3. Chat with agent
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Show me my top 5 posts"}'

# 4. Get analytics
curl -X GET "http://localhost:8000/api/v1/analytics/summary" \
  -H "Authorization: Bearer $TOKEN"
```

## Testing with Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Register
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test123!"
    }
)

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    data={
        "username": "testuser",
        "password": "Test123!"
    }
)
token = response.json()["access_token"]

# Set up headers
headers = {"Authorization": f"Bearer {token}"}

# Chat with agent
response = requests.post(
    f"{BASE_URL}/chat/message",
    headers=headers,
    json={"message": "What are my top performing posts?"}
)
print(response.json())

# Get analytics
response = requests.get(
    f"{BASE_URL}/analytics/summary",
    headers=headers
)
print(response.json())
```

## WebSocket Support (Coming Soon)

Future versions will support WebSocket connections for real-time streaming responses:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat?token=YOUR_TOKEN');

ws.onmessage = (event) => {
  console.log('Received:', event.data);
};

ws.send(JSON.stringify({
  message: "Show me engagement metrics"
}));
```

## Support

For issues or questions:
- Check the main documentation: `/docs`
- Interactive API docs: `/api/v1/docs`
- Health check: `/health`
