"""
Media models.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class Media(BaseModel):
    """A media file in the Publer library."""

    id: str = Field(..., description="Unique media identifier")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v: Any) -> str:
        """Convert ID to string if it's an integer."""
        return str(v) if v is not None else v

    title: Optional[str] = Field(None, description="Media title")
    type: str = Field(..., description="Media type (image, video, gif, document)")
    url: str = Field(..., description="Media URL")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail URL")
    size: Optional[int] = Field(None, description="File size in bytes")
    width: Optional[int] = Field(None, description="Width in pixels (for images/videos)")
    height: Optional[int] = Field(None, description="Height in pixels (for images/videos)")
    duration: Optional[float] = Field(None, description="Duration in seconds (for videos)")
    created_at: Optional[datetime] = Field(None, description="Upload timestamp")
    workspace_id: Optional[str] = Field(None, description="Associated workspace ID")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class MediaUpload(BaseModel):
    """Data for uploading media."""

    title: Optional[str] = Field(None, description="Media title")
    url: Optional[str] = Field(None, description="URL to download media from")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True
