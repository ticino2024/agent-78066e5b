"""Unit tests for security utilities."""

import pytest
from datetime import timedelta

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
)


def test_password_hashing():
    """Test password hashing."""
    password = "TestPassword123!"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword", hashed)


def test_create_and_decode_token():
    """Test JWT token creation and decoding."""
    data = {"sub": "123", "username": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(minutes=30))
    
    assert token is not None
    
    decoded = decode_access_token(token)
    assert decoded["sub"] == "123"
    assert decoded["username"] == "testuser"
    assert "exp" in decoded


def test_decode_invalid_token():
    """Test decoding invalid token."""
    from fastapi import HTTPException
    
    with pytest.raises(HTTPException):
        decode_access_token("invalid_token")
