"""Analytics schemas for API."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class SocialMediaPostBase(BaseModel):
    """Base social media post schema."""

    platform: str
    post_id: str
    content: str
    author: str
    likes: int = 0
    shares: int = 0
    comments: int = 0
    views: int = 0
    engagement_rate: float = 0.0
    sentiment_score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    posted_at: datetime


class SocialMediaPostCreate(SocialMediaPostBase):
    """Social media post creation schema."""

    pass


class SocialMediaPostResponse(SocialMediaPostBase):
    """Social media post response schema."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EngagementMetricBase(BaseModel):
    """Base engagement metric schema."""

    platform: str
    metric_type: str
    metric_value: float
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class EngagementMetricCreate(EngagementMetricBase):
    """Engagement metric creation schema."""

    pass


class EngagementMetricResponse(EngagementMetricBase):
    """Engagement metric response schema."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AnalyticsSummary(BaseModel):
    """Analytics summary schema."""

    total_posts: int
    total_engagement: int
    average_engagement_rate: float
    top_platform: str
    sentiment_overview: Dict[str, Any]
    engagement_trends: List[Dict[str, Any]]
