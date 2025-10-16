"""
Workspace models.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class Workspace(BaseModel):
    """A Publer workspace."""

    id: str = Field(..., description="Unique workspace identifier")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id_to_str(cls, v: Any) -> str:
        """Convert ID to string if it's an integer."""
        return str(v) if v is not None else v
    name: str = Field(..., description="Workspace name")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    members_count: Optional[int] = Field(None, description="Number of members")
    accounts_count: Optional[int] = Field(None, description="Number of connected accounts")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True
