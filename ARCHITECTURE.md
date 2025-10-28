# Architecture Documentation

## System Overview

The Social Media Analytics AI Agent is a production-ready application built with LangChain and FastAPI, designed to provide conversational access to social media analytics data.

## Core Components

### 1. AI Agent Layer

**Location**: `app/agents/`

#### Social Media Agent (`social_media_agent.py`)
- **Purpose**: Main conversational AI agent
- **Technology**: LangChain with OpenAI/Anthropic LLMs
- **Features**:
  - Tool integration for analytics queries
  - Conversation memory management
  - Error handling and recovery
  - Session-based agent instances

#### Vector Store (`vector_store.py`)
- **Purpose**: Knowledge base for RAG
- **Technology**: Chroma with HuggingFace embeddings
- **Features**:
  - Semantic search for analytics insights
  - Pre-loaded knowledge base
  - Document chunking and indexing

### 2. API Layer

**Location**: `app/api/`

#### Authentication (`auth.py`)
- User registration
- JWT token-based login
- Password hashing

#### Chat Interface (`chat.py`)
- Message processing
- Conversation management
- Session handling

#### Analytics (`analytics.py`)
- Direct analytics data access
- Platform-specific queries
- Summary statistics

### 3. Tools Layer

**Location**: `app/tools/`

#### Analytics Tools (`analytics_tools.py`)
- **get_engagement_metrics**: Retrieve engagement data
- **get_top_performing_content**: Identify best posts
- **analyze_engagement_trends**: Track changes over time
- **get_audience_insights**: Demographics and patterns

### 4. Data Layer

#### Database Models (`app/models/`)
- **User**: Authentication and user management
- **Conversation**: Chat session tracking
- **Message**: Individual message storage
- **SocialMediaPost**: Post data and metrics
- **EngagementMetric**: Aggregated metrics

#### Database
- **PostgreSQL**: Primary data store
- **Redis**: Caching and session management
- **Chroma**: Vector database for embeddings

### 5. Service Layer

**Location**: `app/services/`

#### Auth Service (`auth_service.py`)
- User CRUD operations
- Authentication logic
- Password verification

#### Conversation Service (`conversation_service.py`)
- Conversation CRUD
- Message management
- History retrieval

## Data Flow

### Chat Request Flow

```
User Request
    ↓
API Endpoint (chat.py)
    ↓
Authentication Check
    ↓
Get/Create Conversation (DB)
    ↓
Social Media Agent
    ↓
LLM Processing with Tools
    ↓
Tool Execution (Analytics)
    ↓
Response Generation
    ↓
Save to Database
    ↓
Return to User
```

### Tool Execution Flow

```
Agent Decision
    ↓
Tool Selection
    ↓
Input Validation
    ↓
Analytics Processing
    ↓
Data Retrieval (Mock/Real)
    ↓
Format Results
    ↓
Return to Agent
```

## Memory Management

### Conversation Memory
- **Type**: ConversationBufferWindowMemory
- **Size**: Configurable (default: 10 messages)
- **Persistence**: Database-backed
- **Scope**: Per-session

### Agent Sessions
- **Management**: AgentManager singleton
- **Lifecycle**: Created on first message, cached
- **Cleanup**: Manual removal or timeout

## Security Architecture

### Authentication Flow
1. User registers with credentials
2. Password hashed with bcrypt
3. Login returns JWT token
4. Token includes user ID and expiration
5. All protected endpoints validate token

### Authorization
- Bearer token in Authorization header
- Token verification middleware
- User context injection

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Shared PostgreSQL database
- Redis for distributed caching
- Session affinity not required

### Performance Optimization
- Database connection pooling
- Async I/O throughout
- Vector store indexing
- Response streaming (future)

## Configuration Management

### Environment-Based Config
- Development: `.env` file
- Production: Environment variables
- Docker: `docker-compose.yml`

### Key Configuration Areas
- LLM provider and model
- Database connections
- API keys and secrets
- Agent behavior parameters

## Error Handling

### Levels
1. **Tool Level**: Catch tool execution errors
2. **Agent Level**: Handle agent failures gracefully
3. **API Level**: HTTP exception handling
4. **Global Level**: Catch-all exception handler

### Logging
- Structured JSON logging (production)
- Human-readable logs (development)
- Multiple log levels
- Request/response tracking

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock external dependencies
- Fast execution

### Integration Tests
- API endpoint testing
- Database interactions
- End-to-end flows

### Coverage Goals
- Minimum 80% code coverage
- Critical paths 100% covered
- All API endpoints tested

## Deployment Architecture

### Development
```
Developer Machine
├── Python Virtual Environment
├── Local PostgreSQL
├── Local Redis
└── Chroma (filesystem)
```

### Docker
```
Docker Network
├── App Container (FastAPI)
├── PostgreSQL Container
├── Redis Container
└── Shared Volumes
```

### Production (Recommended)
```
Load Balancer
├── App Instance 1
├── App Instance 2
└── App Instance N
    ↓
Managed PostgreSQL (RDS/Cloud SQL)
    ↓
Managed Redis (ElastiCache/Memory Store)
    ↓
Object Storage (S3/GCS) for Chroma
```

## Monitoring and Observability

### Metrics to Track
- Request latency
- Agent response time
- Tool execution time
- Error rates
- Active sessions

### Logging Best Practices
- Structured logging
- Correlation IDs
- User context
- Performance metrics

## Future Enhancements

### Planned Features
1. WebSocket support for streaming
2. Advanced analytics visualizations
3. Multi-tenancy support
4. Scheduled reports
5. Real social media API integration

### Scalability Improvements
1. Caching layer optimization
2. Database query optimization
3. Agent response streaming
4. Background job processing with Celery

## Dependencies

### Core
- FastAPI: Web framework
- LangChain: AI orchestration
- SQLAlchemy: ORM
- Pydantic: Data validation

### AI/ML
- OpenAI/Anthropic: LLM providers
- Chroma: Vector database
- HuggingFace: Embeddings

### Infrastructure
- PostgreSQL: Primary database
- Redis: Caching
- Docker: Containerization

## API Design Principles

1. **RESTful**: Standard HTTP methods and status codes
2. **Versioned**: `/api/v1` prefix for API versioning
3. **Consistent**: Uniform response format
4. **Documented**: OpenAPI/Swagger documentation
5. **Secure**: Authentication on all protected endpoints

## Code Organization Principles

1. **Separation of Concerns**: Clear layer boundaries
2. **Dependency Injection**: FastAPI's Depends
3. **Type Safety**: Pydantic models throughout
4. **Async First**: Async/await for I/O operations
5. **Configuration**: Environment-based settings
