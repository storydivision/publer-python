"""
Analytics models.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class Chart(BaseModel):
    """An available analytics chart."""

    id: str = Field(..., description="Chart identifier")
    name: str = Field(..., description="Chart name")
    description: Optional[str] = Field(None, description="Chart description")
    type: Optional[str] = Field(None, description="Chart type")
    available_for: Optional[List[str]] = Field(None, description="Available for which accounts")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class ChartData(BaseModel):
    """Chart data response."""

    chart_id: str = Field(..., description="Chart identifier")
    data: Dict[str, Any] = Field(..., description="Chart data")
    period: Optional[Dict[str, str]] = Field(None, description="Time period")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class PostInsight(BaseModel):
    """Post performance insights."""

    post_id: str = Field(..., description="Post identifier")

    @field_validator("post_id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v: Any) -> str:
        """Convert ID to string if it's an integer."""
        return str(v) if v is not None else v

    text: Optional[str] = Field(None, description="Post text")
    published_at: Optional[datetime] = Field(None, description="Publish timestamp")
    account_type: Optional[str] = Field(None, description="Account type")
    account_name: Optional[str] = Field(None, description="Account name")
    
    # Metrics
    impressions: Optional[int] = Field(None, description="Number of impressions")
    reach: Optional[int] = Field(None, description="Number of unique users reached")
    engagement: Optional[int] = Field(None, description="Total engagements")
    likes: Optional[int] = Field(None, description="Number of likes")
    comments: Optional[int] = Field(None, description="Number of comments")
    shares: Optional[int] = Field(None, description="Number of shares")
    clicks: Optional[int] = Field(None, description="Number of clicks")
    saves: Optional[int] = Field(None, description="Number of saves")
    
    # Calculated metrics
    engagement_rate: Optional[float] = Field(None, description="Engagement rate percentage")
    ctr: Optional[float] = Field(None, description="Click-through rate")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class HashtagPerformance(BaseModel):
    """Hashtag performance data."""

    hashtag: str = Field(..., description="Hashtag text")
    posts_count: int = Field(..., description="Number of posts using this hashtag")
    total_impressions: Optional[int] = Field(None, description="Total impressions")
    total_reach: Optional[int] = Field(None, description="Total reach")
    total_engagement: Optional[int] = Field(None, description="Total engagement")
    avg_engagement_rate: Optional[float] = Field(None, description="Average engagement rate")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class BestTime(BaseModel):
    """Best time to post data."""

    day: str = Field(..., description="Day of week")
    hour: int = Field(..., description="Hour of day (0-23)")
    score: float = Field(..., description="Performance score")
    posts_count: Optional[int] = Field(None, description="Number of posts at this time")
    avg_engagement: Optional[float] = Field(None, description="Average engagement")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class MemberPerformance(BaseModel):
    """Team member performance data."""

    member_id: str = Field(..., description="Member identifier")
    name: str = Field(..., description="Member name")
    email: Optional[str] = Field(None, description="Member email")
    posts_count: int = Field(..., description="Number of posts created")
    total_impressions: Optional[int] = Field(None, description="Total impressions")
    total_reach: Optional[int] = Field(None, description="Total reach")
    total_engagement: Optional[int] = Field(None, description="Total engagement")
    avg_engagement_rate: Optional[float] = Field(None, description="Average engagement rate")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class Competitor(BaseModel):
    """Competitor account."""

    id: str = Field(..., description="Competitor identifier")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v: Any) -> str:
        """Convert ID to string if it's an integer."""
        return str(v) if v is not None else v

    name: str = Field(..., description="Competitor name")
    platform: str = Field(..., description="Social media platform")
    handle: Optional[str] = Field(None, description="Account handle/username")
    added_at: Optional[datetime] = Field(None, description="When competitor was added")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class CompetitorAnalysis(BaseModel):
    """Competitor performance analysis."""

    competitor_id: str = Field(..., description="Competitor identifier")
    name: str = Field(..., description="Competitor name")
    platform: str = Field(..., description="Platform")
    
    # Metrics
    followers: Optional[int] = Field(None, description="Follower count")
    followers_growth: Optional[int] = Field(None, description="Follower growth in period")
    posts_count: Optional[int] = Field(None, description="Number of posts")
    avg_engagement: Optional[float] = Field(None, description="Average engagement")
    engagement_rate: Optional[float] = Field(None, description="Engagement rate")
    total_reach: Optional[int] = Field(None, description="Total reach")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True
