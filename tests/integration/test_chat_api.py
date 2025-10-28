"""Integration tests for chat API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_send_message_new_conversation(authenticated_client):
    """Test sending a message in a new conversation."""
    client, _ = authenticated_client
    
    response = await client.post(
        "/api/v1/chat/message",
        json={"message": "What are my top performing posts?"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "message" in data
    assert len(data["message"]) > 0


@pytest.mark.asyncio
async def test_send_message_existing_conversation(authenticated_client):
    """Test sending messages in an existing conversation."""
    client, _ = authenticated_client
    
    # Send first message
    response1 = await client.post(
        "/api/v1/chat/message",
        json={"message": "Show me engagement metrics"},
    )
    session_id = response1.json()["session_id"]
    
    # Send second message in same conversation
    response2 = await client.post(
        "/api/v1/chat/message",
        json={"message": "What about Instagram?", "session_id": session_id},
    )
    
    assert response2.status_code == 200
    assert response2.json()["session_id"] == session_id


@pytest.mark.asyncio
async def test_get_conversations(authenticated_client):
    """Test getting user conversations."""
    client, _ = authenticated_client
    
    # Create a conversation
    await client.post(
        "/api/v1/chat/message",
        json={"message": "Hello"},
    )
    
    # Get conversations
    response = await client.get("/api/v1/chat/conversations")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_specific_conversation(authenticated_client):
    """Test getting a specific conversation."""
    client, _ = authenticated_client
    
    # Create a conversation
    create_response = await client.post(
        "/api/v1/chat/message",
        json={"message": "Test message"},
    )
    session_id = create_response.json()["session_id"]
    
    # Get the conversation
    response = await client.get(f"/api/v1/chat/conversations/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert "messages" in data


@pytest.mark.asyncio
async def test_delete_conversation(authenticated_client):
    """Test deleting a conversation."""
    client, _ = authenticated_client
    
    # Create a conversation
    create_response = await client.post(
        "/api/v1/chat/message",
        json={"message": "Test message"},
    )
    session_id = create_response.json()["session_id"]
    
    # Delete the conversation
    response = await client.delete(f"/api/v1/chat/conversations/{session_id}")
    
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = await client.get(f"/api/v1/chat/conversations/{session_id}")
    assert get_response.status_code == 404
