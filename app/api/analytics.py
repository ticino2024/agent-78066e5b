"""Analytics API routes."""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.analytics import AnalyticsSummary
from app.tools.analytics_tools import SocialMediaAnalytics
from app.core.security import get_current_user
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Initialize analytics
analytics = SocialMediaAnalytics()


@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> AnalyticsSummary:
    """Get overall analytics summary across all platforms."""
    try:
        # Calculate summary metrics
        total_posts = sum(analytics.mock_data[p]["posts"] for p in analytics.platforms)
        total_followers = sum(analytics.mock_data[p]["followers"] for p in analytics.platforms)
        
        # Calculate total engagement
        total_engagement = 0
        for platform in analytics.platforms:
            for post in analytics.mock_data[platform]["recent_posts"]:
                total_engagement += post["likes"] + post["shares"] + post["comments"]
        
        # Calculate average engagement rate
        avg_rates = [analytics.mock_data[p]["avg_engagement_rate"] for p in analytics.platforms]
        avg_engagement_rate = sum(avg_rates) / len(avg_rates)
        
        # Find top platform by followers
        top_platform = max(analytics.platforms, key=lambda p: analytics.mock_data[p]["followers"])
        
        # Sentiment overview
        sentiment_overview = {
            "positive": 65,
            "neutral": 25,
            "negative": 10,
        }
        
        # Engagement trends
        engagement_trends = [
            {
                "platform": platform,
                "trend": "increasing" if analytics.mock_data[platform]["avg_engagement_rate"] > 4 else "stable",
                "rate": analytics.mock_data[platform]["avg_engagement_rate"],
            }
            for platform in analytics.platforms
        ]
        
        return AnalyticsSummary(
            total_posts=total_posts,
            total_engagement=total_engagement,
            average_engagement_rate=round(avg_engagement_rate, 2),
            top_platform=top_platform,
            sentiment_overview=sentiment_overview,
            engagement_trends=engagement_trends,
        )

    except Exception as e:
        logger.error(f"Error getting analytics summary: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving analytics summary",
        )


@router.get("/platform/{platform}")
async def get_platform_analytics(
    platform: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get analytics for a specific platform."""
    if platform.lower() not in analytics.platforms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Platform '{platform}' not found",
        )
    
    platform_data = analytics.mock_data[platform.lower()]
    
    return {
        "platform": platform,
        "followers": platform_data["followers"],
        "total_posts": platform_data["posts"],
        "avg_engagement_rate": platform_data["avg_engagement_rate"],
        "recent_posts": platform_data["recent_posts"][:5],
    }
