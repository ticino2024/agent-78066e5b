# Social Media Analytics AI Agent

A production-ready LangChain-based AI agent application for social media analytics with real-time data visualization, user engagement metrics, and content performance tracking.

## 🚀 Features

- **Conversational AI Agent**: LangChain-powered agent with OpenAI GPT-4 or Anthropic Claude
- **Social Media Analytics**: Track engagement metrics across Twitter, Instagram, Facebook, and LinkedIn
- **Vector Database Integration**: Chroma vector store for RAG (Retrieval Augmented Generation)
- **Memory Management**: Conversation history and context management
- **Authentication**: JWT-based authentication and authorization
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Real-time Analysis**: Engagement trends, top-performing content, and audience insights
- **Docker Support**: Full containerization with Docker Compose
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Production Ready**: Proper error handling, logging, and configuration management

## 📋 Requirements

- Python 3.9+
- PostgreSQL 15+
- Redis 7+
- OpenAI API Key or Anthropic API Key

## 🛠️ Installation

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd workspace
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
python scripts/init_db.py
```

6. **Create test user (optional)**
```bash
python scripts/create_test_user.py
```

7. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Using Docker

1. **Configure environment variables**
```bash
cp .env.example .env
# Add your API keys to .env
```

2. **Build and start containers**
```bash
docker-compose up -d
```

3. **View logs**
```bash
docker-compose logs -f app
```

4. **Stop containers**
```bash
docker-compose down
```

## 🎯 Usage

### API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example API Calls

#### 1. Register a User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

#### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=SecurePass123!"
```

#### 3. Chat with AI Agent
```bash
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "message": "Show me the engagement metrics for Instagram"
  }'
```

#### 4. Get Analytics Summary
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/summary" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Example Conversations with AI Agent

**Example 1: Engagement Metrics**
```
User: What are my engagement metrics for Twitter in the last 7 days?
Agent: Based on the data, your Twitter account has shown strong engagement...
```

**Example 2: Top Performing Content**
```
User: Show me my top 5 performing posts across all platforms
Agent: Here are your top 5 performing posts by engagement rate...
```

**Example 3: Audience Insights**
```
User: What are the demographics of my Instagram audience?
Agent: Your Instagram audience demographics show...
```

## 🏗️ Architecture

### Project Structure
```
workspace/
├── app/
│   ├── agents/              # LangChain AI agents
│   │   ├── social_media_agent.py
│   │   └── vector_store.py
│   ├── api/                 # API routes
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── analytics.py
│   ├── core/                # Core utilities
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── db/                  # Database configuration
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── tools/               # LangChain tools
│   └── main.py              # FastAPI application
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── scripts/                 # Utility scripts
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

### Technology Stack

- **Framework**: FastAPI
- **AI/ML**: LangChain, OpenAI GPT-4, Anthropic Claude
- **Vector Store**: Chroma with HuggingFace embeddings
- **Database**: PostgreSQL with AsyncPG
- **Cache**: Redis
- **Authentication**: JWT with python-jose
- **Testing**: pytest with pytest-asyncio
- **Containerization**: Docker & Docker Compose

## 🧪 Testing

### Run All Tests
```bash
make test
# or
pytest tests/ --cov=app --cov-report=html -v
```

### Run Specific Tests
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Specific test file
pytest tests/integration/test_chat_api.py -v
```

### View Coverage Report
```bash
# Open in browser
open htmlcov/index.html
```

## 🔧 Development

### Code Formatting
```bash
make format
# or
black app tests
isort app tests
```

### Linting
```bash
make lint
# or
flake8 app tests
mypy app
```

### Running Development Server
```bash
make dev
# or
uvicorn app.main:app --reload
```

## 📊 AI Agent Capabilities

The social media analytics agent can:

1. **Analyze Engagement Metrics**
   - Track likes, shares, comments, and views
   - Calculate engagement rates
   - Compare performance across platforms

2. **Identify Top Content**
   - Rank posts by engagement
   - Highlight best-performing content
   - Provide content insights

3. **Track Trends**
   - Analyze engagement over time
   - Identify patterns and anomalies
   - Predict trend directions

4. **Audience Insights**
   - Demographics and locations
   - Optimal posting times
   - Engagement patterns

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- Environment-based configuration
- CORS middleware
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy

## 📝 Configuration

### Environment Variables

Key environment variables to configure:

```bash
# LLM Configuration
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db

# Security
SECRET_KEY=your-secret-key
```

See `.env.example` for full configuration options.

## 🚢 Production Deployment

### Prerequisites
1. Set up PostgreSQL database
2. Set up Redis instance
3. Obtain API keys (OpenAI or Anthropic)
4. Configure domain and SSL certificates

### Deployment Steps
1. Update `.env` with production values
2. Set `APP_ENV=production`
3. Use strong `SECRET_KEY`
4. Configure proper CORS origins
5. Set up reverse proxy (nginx)
6. Enable HTTPS
7. Set up monitoring and logging

### Docker Production
```bash
docker-compose -f docker-compose.yml up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

MIT License

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation at `/docs`
- Review API documentation at `/api/v1/docs`

## 🎓 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [Chroma Documentation](https://docs.trychroma.com/)

## 📈 Roadmap

- [ ] WebSocket support for streaming responses
- [ ] More social media platforms
- [ ] Advanced analytics visualizations
- [ ] Custom report generation
- [ ] Sentiment analysis integration
- [ ] Scheduled analytics reports
- [ ] Multi-language support
- [ ] Export functionality (PDF, CSV)

---

Built with ❤️ using LangChain, FastAPI, and modern AI technologies.
