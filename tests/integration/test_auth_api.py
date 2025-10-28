"""Integration tests for authentication API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, test_user_data):
    """Test user registration."""
    response = await client.post("/api/v1/auth/register", json=test_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient, test_user_data):
    """Test registering with duplicate username."""
    # Register first user
    await client.post("/api/v1/auth/register", json=test_user_data)
    
    # Try to register again
    response = await client.post("/api/v1/auth/register", json=test_user_data)
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user_data):
    """Test successful login."""
    # Register user
    await client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": test_user_data["username"], "password": test_user_data["password"]},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, test_user_data):
    """Test login with invalid credentials."""
    # Register user
    await client.post("/api/v1/auth/register", json=test_user_data)
    
    # Try to login with wrong password
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": test_user_data["username"], "password": "WrongPassword"},
    )
    
    assert response.status_code == 401
