"""
Accounts API endpoints.
"""

from typing import List, Optional

from publer.models.accounts import Account
from publer.resources.base import AsyncBaseResource, BaseResource


class AccountsResource(BaseResource):
    """Synchronous accounts API endpoints."""

    def list(self, workspace_id: Optional[str] = None) -> List[Account]:
        """
        List all connected social media accounts.

        Args:
            workspace_id: Optional workspace ID to filter accounts

        Returns:
            List of account objects

        Raises:
            AuthenticationError: If API key is invalid
            PublerAPIError: If the request fails

        Example:
            >>> accounts = client.accounts.list()
            >>> for account in accounts:
            ...     print(f"{account.name} ({account.type})")
        """
        params = {}
        if workspace_id:
            params["workspace_id"] = workspace_id

        response = self._get("/accounts", params=params)
        accounts_data = response.get("accounts", response) if isinstance(response, dict) else response
        return [Account(**account) for account in accounts_data]

    def get(self, account_id: str) -> Account:
        """
        Get details of a specific account.

        Args:
            account_id: Account ID

        Returns:
            Account object

        Raises:
            NotFoundError: If account doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> account = client.accounts.get("account_123")
            >>> print(f"{account.name}: {account.type}")
        """
        response = self._get(f"/accounts/{account_id}")
        return Account(**response)


class AsyncAccountsResource(AsyncBaseResource):
    """Asynchronous accounts API endpoints."""

    async def list(self, workspace_id: Optional[str] = None) -> List[Account]:
        """
        List all connected social media accounts.

        Args:
            workspace_id: Optional workspace ID to filter accounts

        Returns:
            List of account objects

        Raises:
            AuthenticationError: If API key is invalid
            PublerAPIError: If the request fails

        Example:
            >>> accounts = await client.accounts.list()
            >>> for account in accounts:
            ...     print(f"{account.name} ({account.type})")
        """
        params = {}
        if workspace_id:
            params["workspace_id"] = workspace_id

        response = await self._get("/accounts", params=params)
        accounts_data = response.get("accounts", response) if isinstance(response, dict) else response
        return [Account(**account) for account in accounts_data]

    async def get(self, account_id: str) -> Account:
        """
        Get details of a specific account.

        Args:
            account_id: Account ID

        Returns:
            Account object

        Raises:
            NotFoundError: If account doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> account = await client.accounts.get("account_123")
            >>> print(f"{account.name}: {account.type}")
        """
        response = await self._get(f"/accounts/{account_id}")
        return Account(**response)
