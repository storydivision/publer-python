"""
Post models.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class Post(BaseModel):
    """A Publer post."""

    id: str = Field(..., description="Unique post identifier")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v: Any) -> str:
        """Convert ID to string if it's an integer."""
        return str(v) if v is not None else v
    text: Optional[str] = Field(None, description="Post content text")
    state: str = Field(
        ...,
        description="Post state: scheduled, published, draft, failed, etc.",
    )
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled publish time")
    published_at: Optional[datetime] = Field(None, description="Actual publish time")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    accounts: Optional[List[str]] = Field(None, description="Account IDs to post to")
    media: Optional[List[Dict[str, Any]]] = Field(None, description="Attached media")
    link: Optional[str] = Field(None, description="Link to share")
    workspace_id: Optional[str] = Field(None, description="Associated workspace ID")
    created_by: Optional[str] = Field(None, description="Creator user ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class PostCreate(BaseModel):
    """Data for creating a new post."""

    text: Optional[str] = Field(None, description="Post content text")
    accounts: List[str] = Field(..., description="Account IDs to post to")
    scheduled_at: Optional[datetime] = Field(
        None, description="When to publish (None for immediate)"
    )
    media_urls: Optional[List[str]] = Field(None, description="Media URLs to attach")
    media_ids: Optional[List[str]] = Field(None, description="Media IDs from library")
    link: Optional[str] = Field(None, description="Link to share")
    state: Optional[str] = Field("scheduled", description="Post state (scheduled/draft)")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class PostUpdate(BaseModel):
    """Data for updating an existing post."""

    text: Optional[str] = Field(None, description="Updated post content")
    scheduled_at: Optional[datetime] = Field(None, description="Updated schedule time")
    accounts: Optional[List[str]] = Field(None, description="Updated account IDs")
    media_urls: Optional[List[str]] = Field(None, description="Updated media URLs")
    media_ids: Optional[List[str]] = Field(None, description="Updated media IDs")
    link: Optional[str] = Field(None, description="Updated link")
    state: Optional[str] = Field(None, description="Updated state")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class BulkPostCreate(BaseModel):
    """Data for creating multiple posts in bulk."""

    state: str = Field("scheduled", description="State for all posts")
    posts: List[PostCreate] = Field(..., description="List of posts to create")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class JobStatus(BaseModel):
    """Status of an async job."""

    job_id: str = Field(..., description="Job identifier")
    status: str = Field(..., description="Job status: pending, processing, completed, failed")
    payload: Optional[Dict[str, Any]] = Field(None, description="Job result data")
    failures: Optional[Dict[str, Any]] = Field(None, description="Failure information")
    created_at: Optional[datetime] = Field(None, description="Job creation time")
    completed_at: Optional[datetime] = Field(None, description="Job completion time")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True
