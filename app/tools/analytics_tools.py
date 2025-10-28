"""Social media analytics tools for LangChain agent."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random
import json
from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field

from app.core.logging import get_logger

logger = get_logger(__name__)


class AnalyticsToolInput(BaseModel):
    """Input schema for analytics tools."""

    platform: Optional[str] = Field(None, description="Social media platform (twitter, instagram, facebook, linkedin)")
    days: Optional[int] = Field(7, description="Number of days to look back")
    metric_type: Optional[str] = Field(None, description="Type of metric to retrieve")


class SocialMediaAnalytics:
    """Social media analytics tool implementation."""

    def __init__(self) -> None:
        """Initialize analytics tools."""
        self.platforms = ["twitter", "instagram", "facebook", "linkedin"]
        self.mock_data = self._generate_mock_data()

    def _generate_mock_data(self) -> Dict[str, Any]:
        """Generate mock social media data."""
        data = {
            "twitter": {
                "followers": 15234,
                "posts": 342,
                "avg_engagement_rate": 4.5,
                "recent_posts": [],
            },
            "instagram": {
                "followers": 23456,
                "posts": 198,
                "avg_engagement_rate": 6.2,
                "recent_posts": [],
            },
            "facebook": {
                "followers": 45678,
                "posts": 276,
                "avg_engagement_rate": 3.8,
                "recent_posts": [],
            },
            "linkedin": {
                "followers": 8901,
                "posts": 145,
                "avg_engagement_rate": 5.1,
                "recent_posts": [],
            },
        }

        # Generate recent posts for each platform
        for platform in self.platforms:
            for i in range(10):
                post = {
                    "id": f"{platform}_post_{i}",
                    "content": f"Sample post {i} on {platform}",
                    "likes": random.randint(50, 500),
                    "shares": random.randint(10, 100),
                    "comments": random.randint(5, 50),
                    "views": random.randint(500, 5000),
                    "timestamp": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat(),
                }
                post["engagement_rate"] = round(
                    ((post["likes"] + post["shares"] + post["comments"]) / post["views"]) * 100, 2
                )
                data[platform]["recent_posts"].append(post)

        return data

    def get_engagement_metrics(self, platform: Optional[str] = None, days: int = 7) -> str:
        """Get engagement metrics for specified platform."""
        try:
            if platform and platform.lower() in self.platforms:
                platform = platform.lower()
                data = self.mock_data[platform]
                result = {
                    "platform": platform,
                    "days": days,
                    "followers": data["followers"],
                    "total_posts": data["posts"],
                    "avg_engagement_rate": data["avg_engagement_rate"],
                    "recent_activity": {
                        "total_likes": sum(p["likes"] for p in data["recent_posts"][:days]),
                        "total_shares": sum(p["shares"] for p in data["recent_posts"][:days]),
                        "total_comments": sum(p["comments"] for p in data["recent_posts"][:days]),
                    },
                }
            else:
                # Return summary for all platforms
                result = {
                    "summary": "All Platforms",
                    "days": days,
                    "platforms": {},
                }
                for plat in self.platforms:
                    data = self.mock_data[plat]
                    result["platforms"][plat] = {
                        "followers": data["followers"],
                        "avg_engagement_rate": data["avg_engagement_rate"],
                        "total_posts": data["posts"],
                    }

            logger.info(f"Retrieved engagement metrics for platform: {platform or 'all'}")
            return json.dumps(result, indent=2)

        except Exception as e:
            logger.error(f"Error getting engagement metrics: {str(e)}")
            return json.dumps({"error": str(e)})

    def get_top_performing_content(self, platform: Optional[str] = None, limit: int = 5) -> str:
        """Get top performing content by engagement."""
        try:
            results = []

            if platform and platform.lower() in self.platforms:
                platform = platform.lower()
                posts = sorted(
                    self.mock_data[platform]["recent_posts"],
                    key=lambda x: x["engagement_rate"],
                    reverse=True,
                )[:limit]
                results = posts
            else:
                # Get top posts from all platforms
                all_posts = []
                for plat in self.platforms:
                    for post in self.mock_data[plat]["recent_posts"]:
                        post["platform"] = plat
                        all_posts.append(post)
                results = sorted(all_posts, key=lambda x: x["engagement_rate"], reverse=True)[:limit]

            logger.info(f"Retrieved top {limit} performing content for platform: {platform or 'all'}")
            return json.dumps(results, indent=2)

        except Exception as e:
            logger.error(f"Error getting top performing content: {str(e)}")
            return json.dumps({"error": str(e)})

    def analyze_engagement_trends(self, platform: Optional[str] = None, days: int = 7) -> str:
        """Analyze engagement trends over time."""
        try:
            if platform and platform.lower() in self.platforms:
                platform = platform.lower()
                posts = self.mock_data[platform]["recent_posts"][:days]
                
                # Calculate daily trends
                daily_trends = []
                for i in range(days):
                    day_posts = [p for p in posts if (datetime.now() - datetime.fromisoformat(p["timestamp"])).days == i]
                    if day_posts:
                        avg_engagement = sum(p["engagement_rate"] for p in day_posts) / len(day_posts)
                        daily_trends.append({
                            "day": i,
                            "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                            "avg_engagement_rate": round(avg_engagement, 2),
                            "posts_count": len(day_posts),
                        })

                result = {
                    "platform": platform,
                    "days": days,
                    "trends": daily_trends,
                    "trend_direction": "increasing" if daily_trends and daily_trends[0]["avg_engagement_rate"] > daily_trends[-1]["avg_engagement_rate"] else "decreasing",
                }
            else:
                # Aggregate trends across all platforms
                result = {
                    "summary": "All Platforms",
                    "days": days,
                    "platform_trends": {},
                }
                for plat in self.platforms:
                    avg_engagement = self.mock_data[plat]["avg_engagement_rate"]
                    result["platform_trends"][plat] = {
                        "avg_engagement_rate": avg_engagement,
                        "status": "strong" if avg_engagement > 5 else "moderate" if avg_engagement > 3 else "needs_improvement",
                    }

            logger.info(f"Analyzed engagement trends for platform: {platform or 'all'}")
            return json.dumps(result, indent=2)

        except Exception as e:
            logger.error(f"Error analyzing engagement trends: {str(e)}")
            return json.dumps({"error": str(e)})

    def get_audience_insights(self, platform: Optional[str] = None) -> str:
        """Get audience insights and demographics."""
        try:
            if platform and platform.lower() in self.platforms:
                platform = platform.lower()
                result = {
                    "platform": platform,
                    "followers": self.mock_data[platform]["followers"],
                    "demographics": {
                        "age_groups": {
                            "18-24": random.randint(15, 30),
                            "25-34": random.randint(25, 40),
                            "35-44": random.randint(20, 35),
                            "45+": random.randint(10, 25),
                        },
                        "top_locations": [
                            {"country": "United States", "percentage": random.randint(30, 50)},
                            {"country": "United Kingdom", "percentage": random.randint(10, 20)},
                            {"country": "Canada", "percentage": random.randint(8, 15)},
                        ],
                    },
                    "engagement_patterns": {
                        "best_posting_times": ["9AM-11AM", "2PM-4PM", "7PM-9PM"],
                        "best_days": ["Tuesday", "Wednesday", "Thursday"],
                    },
                }
            else:
                result = {
                    "summary": "All Platforms",
                    "total_followers": sum(self.mock_data[p]["followers"] for p in self.platforms),
                    "platform_breakdown": {
                        plat: self.mock_data[plat]["followers"] for plat in self.platforms
                    },
                }

            logger.info(f"Retrieved audience insights for platform: {platform or 'all'}")
            return json.dumps(result, indent=2)

        except Exception as e:
            logger.error(f"Error getting audience insights: {str(e)}")
            return json.dumps({"error": str(e)})


def create_analytics_tools() -> List[Tool]:
    """Create and return all analytics tools."""
    analytics = SocialMediaAnalytics()

    tools = [
        Tool(
            name="get_engagement_metrics",
            func=lambda x: analytics.get_engagement_metrics(
                platform=x.get("platform") if isinstance(x, dict) else None,
                days=x.get("days", 7) if isinstance(x, dict) else 7,
            ),
            description="Get engagement metrics (likes, shares, comments) for social media platforms. "
            "Input should be a dictionary with optional 'platform' (twitter/instagram/facebook/linkedin) "
            "and 'days' (number of days to look back, default 7).",
        ),
        Tool(
            name="get_top_performing_content",
            func=lambda x: analytics.get_top_performing_content(
                platform=x.get("platform") if isinstance(x, dict) else None,
                limit=x.get("limit", 5) if isinstance(x, dict) else 5,
            ),
            description="Get top performing content ranked by engagement rate. "
            "Input should be a dictionary with optional 'platform' and 'limit' (default 5).",
        ),
        Tool(
            name="analyze_engagement_trends",
            func=lambda x: analytics.analyze_engagement_trends(
                platform=x.get("platform") if isinstance(x, dict) else None,
                days=x.get("days", 7) if isinstance(x, dict) else 7,
            ),
            description="Analyze engagement trends over time to identify patterns. "
            "Input should be a dictionary with optional 'platform' and 'days'.",
        ),
        Tool(
            name="get_audience_insights",
            func=lambda x: analytics.get_audience_insights(
                platform=x.get("platform") if isinstance(x, dict) else None,
            ),
            description="Get audience demographics and insights including age groups, locations, and best posting times. "
            "Input should be a dictionary with optional 'platform'.",
        ),
    ]

    return tools
