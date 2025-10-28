"""Analytics database models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from app.db.base import Base


class SocialMediaPost(Base):
    """Social media post model."""

    __tablename__ = "social_media_posts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # twitter, instagram, facebook, linkedin
    post_id = Column(String, unique=True, index=True, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    views = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    sentiment_score = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=True)
    posted_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class EngagementMetric(Base):
    """Engagement metrics model."""

    __tablename__ = "engagement_metrics"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)
    metric_type = Column(String, nullable=False)  # daily_engagement, follower_growth, etc.
    metric_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
