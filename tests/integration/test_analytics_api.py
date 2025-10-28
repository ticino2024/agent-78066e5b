"""Integration tests for analytics API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_analytics_summary(authenticated_client):
    """Test getting analytics summary."""
    client, _ = authenticated_client
    
    response = await client.get("/api/v1/analytics/summary")
    
    assert response.status_code == 200
    data = response.json()
    assert "total_posts" in data
    assert "total_engagement" in data
    assert "average_engagement_rate" in data
    assert "top_platform" in data
    assert "sentiment_overview" in data
    assert "engagement_trends" in data


@pytest.mark.asyncio
async def test_get_platform_analytics(authenticated_client):
    """Test getting platform-specific analytics."""
    client, _ = authenticated_client
    
    platforms = ["twitter", "instagram", "facebook", "linkedin"]
    
    for platform in platforms:
        response = await client.get(f"/api/v1/analytics/platform/{platform}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["platform"] == platform
        assert "followers" in data
        assert "total_posts" in data
        assert "avg_engagement_rate" in data
        assert "recent_posts" in data


@pytest.mark.asyncio
async def test_get_invalid_platform_analytics(authenticated_client):
    """Test getting analytics for invalid platform."""
    client, _ = authenticated_client
    
    response = await client.get("/api/v1/analytics/platform/invalid_platform")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_analytics_requires_authentication(client: AsyncClient):
    """Test that analytics endpoints require authentication."""
    response = await client.get("/api/v1/analytics/summary")
    
    assert response.status_code == 403
