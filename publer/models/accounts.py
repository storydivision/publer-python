"""
Account models.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class Account(BaseModel):
    """A connected social media account."""

    id: str = Field(..., description="Unique account identifier")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v: Any) -> str:
        """Convert ID to string if it's an integer."""
        return str(v) if v is not None else v
    name: str = Field(..., description="Account name/username")
    type: str = Field(
        ...,
        description="Account type (facebook, instagram, twitter, linkedin, etc.)",
    )
    avatar: Optional[str] = Field(None, description="Account avatar URL")
    connected_at: Optional[datetime] = Field(None, description="Connection timestamp")
    is_active: Optional[bool] = Field(None, description="Whether account is active")
    workspace_id: Optional[str] = Field(None, description="Associated workspace ID")
    platform_id: Optional[str] = Field(None, description="Platform-specific account ID")
    capabilities: Optional[List[str]] = Field(
        None, description="Supported capabilities (post, story, reel, etc.)"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True
