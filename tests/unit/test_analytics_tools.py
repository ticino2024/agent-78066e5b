"""Unit tests for analytics tools."""

import json
import pytest

from app.tools.analytics_tools import SocialMediaAnalytics


@pytest.fixture
def analytics():
    """Create analytics instance."""
    return SocialMediaAnalytics()


def test_get_engagement_metrics_single_platform(analytics):
    """Test getting engagement metrics for a single platform."""
    result = analytics.get_engagement_metrics(platform="twitter", days=7)
    data = json.loads(result)
    
    assert "platform" in data
    assert data["platform"] == "twitter"
    assert "followers" in data
    assert "total_posts" in data
    assert "avg_engagement_rate" in data
    assert "recent_activity" in data


def test_get_engagement_metrics_all_platforms(analytics):
    """Test getting engagement metrics for all platforms."""
    result = analytics.get_engagement_metrics()
    data = json.loads(result)
    
    assert "summary" in data
    assert "platforms" in data
    assert len(data["platforms"]) == 4


def test_get_top_performing_content(analytics):
    """Test getting top performing content."""
    result = analytics.get_top_performing_content(platform="instagram", limit=3)
    data = json.loads(result)
    
    assert isinstance(data, list)
    assert len(data) <= 3
    
    if len(data) > 1:
        # Check that results are sorted by engagement_rate
        for i in range(len(data) - 1):
            assert data[i]["engagement_rate"] >= data[i + 1]["engagement_rate"]


def test_analyze_engagement_trends(analytics):
    """Test analyzing engagement trends."""
    result = analytics.analyze_engagement_trends(platform="facebook", days=7)
    data = json.loads(result)
    
    assert "platform" in data
    assert "trends" in data
    assert "trend_direction" in data


def test_get_audience_insights(analytics):
    """Test getting audience insights."""
    result = analytics.get_audience_insights(platform="linkedin")
    data = json.loads(result)
    
    assert "platform" in data
    assert "followers" in data
    assert "demographics" in data
    assert "engagement_patterns" in data
