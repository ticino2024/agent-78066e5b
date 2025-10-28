# Testing Guide

## Overview

The project includes comprehensive test coverage with unit tests and integration tests using pytest.

## Test Structure

```
tests/
├── conftest.py                 # Shared fixtures and configuration
├── unit/                       # Unit tests (isolated components)
│   ├── test_security.py       # Security utilities tests
│   └── test_analytics_tools.py # Analytics tools tests
└── integration/               # Integration tests (API endpoints)
    ├── test_auth_api.py       # Authentication API tests
    ├── test_chat_api.py       # Chat API tests
    └── test_analytics_api.py  # Analytics API tests
```

## Running Tests

### All Tests
```bash
# Using Make
make test

# Using pytest directly
pytest tests/ -v

# With coverage report
pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
```

### Unit Tests Only
```bash
pytest tests/unit/ -v
```

### Integration Tests Only
```bash
pytest tests/integration/ -v
```

### Specific Test File
```bash
pytest tests/unit/test_security.py -v
```

### Specific Test Function
```bash
pytest tests/unit/test_security.py::test_password_hashing -v
```

### With Output
```bash
pytest tests/ -v -s  # -s shows print statements
```

## Test Coverage

### View Coverage Report
```bash
# Generate HTML report
pytest tests/ --cov=app --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage Goals
- Minimum: 80% overall coverage
- Critical paths: 100% coverage
- All API endpoints: Tested

## Test Fixtures

### Database Fixtures

#### `db_engine`
Creates an in-memory SQLite database for testing.

```python
@pytest.fixture
async def db_engine():
    """Create a test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
```

#### `db_session`
Provides a database session for tests.

```python
async def test_create_user(db_session):
    user = User(username="test", email="test@example.com")
    db_session.add(user)
    await db_session.commit()
```

### HTTP Client Fixtures

#### `client`
Provides an async HTTP client for API testing.

```python
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
```

#### `authenticated_client`
Provides an authenticated HTTP client with JWT token.

```python
async def test_protected_endpoint(authenticated_client):
    client, user_data = authenticated_client
    response = await client.get("/api/v1/chat/conversations")
    assert response.status_code == 200
```

### Data Fixtures

#### `test_user_data`
Provides sample user data for testing.

```python
@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123!",
    }
```

## Writing Tests

### Unit Test Example

```python
def test_password_hashing():
    """Test password hashing and verification."""
    password = "SecurePassword123!"
    hashed = get_password_hash(password)
    
    # Assertions
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword", hashed)
```

### Async Unit Test Example

```python
@pytest.mark.asyncio
async def test_create_user(db_session):
    """Test user creation."""
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="Test123!"
    )
    
    user = await AuthService.create_user(db_session, user_data)
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password != "Test123!"
```

### Integration Test Example

```python
@pytest.mark.asyncio
async def test_register_user(client, test_user_data):
    """Test user registration endpoint."""
    response = await client.post(
        "/api/v1/auth/register",
        json=test_user_data
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert "hashed_password" not in data
```

### Testing with Authentication

```python
@pytest.mark.asyncio
async def test_chat_message(authenticated_client):
    """Test sending a chat message."""
    client, _ = authenticated_client
    
    response = await client.post(
        "/api/v1/chat/message",
        json={"message": "What are my engagement metrics?"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "message" in data
```

## Test Best Practices

### 1. Test Naming
- Use descriptive names: `test_user_registration_with_invalid_email`
- Follow pattern: `test_<what>_<condition>_<expected_result>`

### 2. Arrange-Act-Assert Pattern
```python
def test_something():
    # Arrange: Set up test data
    user = User(username="test")
    
    # Act: Perform action
    result = user.get_full_name()
    
    # Assert: Verify result
    assert result == "test"
```

### 3. Test Independence
- Each test should be independent
- Don't rely on test execution order
- Clean up after each test

### 4. Use Fixtures
- Reuse common setup code
- Keep tests DRY (Don't Repeat Yourself)
- Use scopes appropriately

### 5. Mock External Dependencies
```python
from unittest.mock import Mock, patch

@patch('app.agents.social_media_agent.ChatOpenAI')
def test_agent_creation(mock_llm):
    """Test agent creation with mocked LLM."""
    mock_llm.return_value = Mock()
    agent = SocialMediaAgent("session-123")
    assert agent.session_id == "session-123"
```

## Testing Async Code

### Mark Tests as Async
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### Testing Async Context Managers
```python
@pytest.mark.asyncio
async def test_database_session():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        assert result is not None
```

## Mocking

### Mock LLM Responses
```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_agent_response():
    mock_agent = AsyncMock()
    mock_agent.process_message.return_value = {
        "session_id": "test-123",
        "message": "Test response"
    }
    
    result = await mock_agent.process_message("test")
    assert result["message"] == "Test response"
```

### Mock External APIs
```python
@patch('httpx.AsyncClient.get')
async def test_api_call(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: {"data": "test"}
    )
    
    # Test code that uses httpx
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Test Data Management

### Using Factories
```python
def create_test_user(**kwargs):
    """Factory for creating test users."""
    defaults = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test123!",
    }
    defaults.update(kwargs)
    return UserCreate(**defaults)

def test_something():
    user1 = create_test_user()
    user2 = create_test_user(username="another")
```

### Using Fixtures for Data
```python
@pytest.fixture
def sample_posts():
    """Provide sample social media posts."""
    return [
        {
            "platform": "twitter",
            "content": "Test post 1",
            "likes": 100,
        },
        {
            "platform": "instagram",
            "content": "Test post 2",
            "likes": 200,
        },
    ]
```

## Performance Testing

### Measure Test Duration
```bash
pytest tests/ --durations=10
```

### Benchmark Tests
```python
def test_performance(benchmark):
    """Benchmark a function."""
    result = benchmark(some_function, arg1, arg2)
    assert result is not None
```

## Debugging Tests

### Run with Print Statements
```bash
pytest tests/ -v -s
```

### Run with PDB
```bash
pytest tests/ --pdb
```

### Add Breakpoint in Test
```python
def test_something():
    result = some_function()
    import pdb; pdb.set_trace()  # Debugger stops here
    assert result is not None
```

## Common Test Scenarios

### 1. Testing Authentication
```python
async def test_login_success(client, test_user_data):
    # Register user
    await client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### 2. Testing Protected Endpoints
```python
async def test_protected_endpoint(authenticated_client):
    client, _ = authenticated_client
    response = await client.get("/api/v1/protected-route")
    assert response.status_code == 200
```

### 3. Testing Error Handling
```python
async def test_invalid_input(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "test"}  # Missing required fields
    )
    assert response.status_code == 422
```

### 4. Testing Database Operations
```python
async def test_create_and_retrieve(db_session):
    # Create
    user = User(username="test", email="test@example.com")
    db_session.add(user)
    await db_session.commit()
    
    # Retrieve
    result = await db_session.execute(
        select(User).where(User.username == "test")
    )
    retrieved_user = result.scalar_one_or_none()
    
    assert retrieved_user is not None
    assert retrieved_user.username == "test"
```

## Test Coverage by Module

### Target Coverage

- **app/core/**: 90%+ (critical utilities)
- **app/api/**: 85%+ (all endpoints)
- **app/agents/**: 80%+ (agent logic)
- **app/models/**: 75%+ (data models)
- **app/services/**: 85%+ (business logic)
- **app/tools/**: 80%+ (tool implementations)

## Troubleshooting

### Tests Hang
- Check for missing `await` in async tests
- Verify database cleanup in fixtures
- Look for infinite loops

### Import Errors
- Ensure virtual environment is activated
- Check if dependencies are installed
- Verify PYTHONPATH

### Database Errors
- Ensure test database is properly set up
- Check fixture scopes
- Verify async session handling

### Fixture Errors
- Check fixture names match parameters
- Verify fixture scopes
- Ensure fixtures are in conftest.py or test file

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)

---

For questions or issues with tests, check the test output carefully and refer to this guide.
