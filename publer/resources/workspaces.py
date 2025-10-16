"""
Workspaces API endpoints.
"""

from typing import Any, Dict, List

from publer.models.workspaces import Workspace
from publer.resources.base import AsyncBaseResource, BaseResource


class WorkspacesResource(BaseResource):
    """Synchronous workspaces API endpoints."""

    def list(self) -> List[Workspace]:
        """
        List all workspaces accessible to the current user.

        Returns:
            List of workspace objects

        Raises:
            AuthenticationError: If API key is invalid
            PublerAPIError: If the request fails

        Example:
            >>> workspaces = client.workspaces.list()
            >>> for workspace in workspaces:
            ...     print(f"{workspace.name}: {workspace.id}")
        """
        response = self._get("/workspaces")
        # API might return {"workspaces": [...]} or just [...]
        workspaces_data = response.get("workspaces", response) if isinstance(response, dict) else response
        return [Workspace(**workspace) for workspace in workspaces_data]

    def get(self, workspace_id: str) -> Workspace:
        """
        Get details of a specific workspace.

        Args:
            workspace_id: Workspace ID

        Returns:
            Workspace object

        Raises:
            NotFoundError: If workspace doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> workspace = client.workspaces.get("workspace_123")
            >>> print(workspace.name)
        """
        response = self._get(f"/workspaces/{workspace_id}")
        return Workspace(**response)


class AsyncWorkspacesResource(AsyncBaseResource):
    """Asynchronous workspaces API endpoints."""

    async def list(self) -> List[Workspace]:
        """
        List all workspaces accessible to the current user.

        Returns:
            List of workspace objects

        Raises:
            AuthenticationError: If API key is invalid
            PublerAPIError: If the request fails

        Example:
            >>> workspaces = await client.workspaces.list()
            >>> for workspace in workspaces:
            ...     print(f"{workspace.name}: {workspace.id}")
        """
        response = await self._get("/workspaces")
        workspaces_data = response.get("workspaces", response) if isinstance(response, dict) else response
        return [Workspace(**workspace) for workspace in workspaces_data]

    async def get(self, workspace_id: str) -> Workspace:
        """
        Get details of a specific workspace.

        Args:
            workspace_id: Workspace ID

        Returns:
            Workspace object

        Raises:
            NotFoundError: If workspace doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> workspace = await client.workspaces.get("workspace_123")
            >>> print(workspace.name)
        """
        response = await self._get(f"/workspaces/{workspace_id}")
        return Workspace(**response)
