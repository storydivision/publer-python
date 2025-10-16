"""
HTTP session management for the Publer API.
"""

from typing import Any, Dict, Optional, Union

import httpx

from publer.exceptions import get_exception_for_status


class PublerSession:
    """Synchronous HTTP session for Publer API requests."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://app.publer.com/api/v1",
        workspace_id: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        """
        Initialize a Publer API session.

        Args:
            api_key: Publer API key
            base_url: Base URL for API requests
            workspace_id: Optional workspace ID for requests
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.workspace_id = workspace_id
        self.timeout = timeout

        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers=self._build_headers(),
        )

    def _build_headers(self) -> Dict[str, str]:
        """
        Build request headers.

        Returns:
            Dictionary of headers
        """
        headers = {
            "Authorization": f"Bearer-API {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "publer-python/0.1.0",
        }

        if self.workspace_id:
            headers["Publer-Workspace-Id"] = self.workspace_id

        return headers

    def set_workspace(self, workspace_id: str) -> None:
        """
        Set the workspace ID for subsequent requests.

        Args:
            workspace_id: Workspace ID to use
        """
        self.workspace_id = workspace_id
        self.client.headers["Publer-Workspace-Id"] = workspace_id

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the Publer API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path (e.g., "/posts")
            params: Query parameters
            json: JSON request body
            data: Form data
            files: Files to upload

        Returns:
            Response data as dictionary

        Raises:
            PublerAPIError: If the request fails
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        try:
            response = self.client.request(
                method=method,
                url=endpoint,
                params=params,
                json=json,
                data=data,
                files=files,
            )

            # Handle error responses
            if response.status_code >= 400:
                self._handle_error_response(response)

            # Return JSON response
            return response.json()

        except httpx.HTTPError as e:
            raise get_exception_for_status(
                status_code=0,
                message=f"HTTP error occurred: {str(e)}",
            ) from e

    def _handle_error_response(self, response: httpx.Response) -> None:
        """
        Handle error responses from the API.

        Args:
            response: HTTP response object

        Raises:
            PublerAPIError: Appropriate exception for the error
        """
        try:
            error_data = response.json()
            errors = error_data.get("errors", [])
            message = "; ".join(errors) if errors else response.text
        except Exception:
            message = response.text or f"HTTP {response.status_code}"
            error_data = None
            errors = None

        # Extract retry-after header for rate limit errors
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    error_data = error_data or {}
                    error_data["retry_after"] = int(retry_after)
                except ValueError:
                    pass

        raise get_exception_for_status(
            status_code=response.status_code,
            message=message,
            response=error_data,
            errors=errors,
        )

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self) -> "PublerSession":
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()


class AsyncPublerSession:
    """Asynchronous HTTP session for Publer API requests."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://app.publer.com/api/v1",
        workspace_id: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        """
        Initialize an async Publer API session.

        Args:
            api_key: Publer API key
            base_url: Base URL for API requests
            workspace_id: Optional workspace ID for requests
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.workspace_id = workspace_id
        self.timeout = timeout

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers=self._build_headers(),
        )

    def _build_headers(self) -> Dict[str, str]:
        """
        Build request headers.

        Returns:
            Dictionary of headers
        """
        headers = {
            "Authorization": f"Bearer-API {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "publer-python/0.1.0",
        }

        if self.workspace_id:
            headers["Publer-Workspace-Id"] = self.workspace_id

        return headers

    def set_workspace(self, workspace_id: str) -> None:
        """
        Set the workspace ID for subsequent requests.

        Args:
            workspace_id: Workspace ID to use
        """
        self.workspace_id = workspace_id
        self.client.headers["Publer-Workspace-Id"] = workspace_id

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an async HTTP request to the Publer API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path (e.g., "/posts")
            params: Query parameters
            json: JSON request body
            data: Form data
            files: Files to upload

        Returns:
            Response data as dictionary

        Raises:
            PublerAPIError: If the request fails
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        try:
            response = await self.client.request(
                method=method,
                url=endpoint,
                params=params,
                json=json,
                data=data,
                files=files,
            )

            # Handle error responses
            if response.status_code >= 400:
                self._handle_error_response(response)

            # Return JSON response
            return response.json()

        except httpx.HTTPError as e:
            raise get_exception_for_status(
                status_code=0,
                message=f"HTTP error occurred: {str(e)}",
            ) from e

    def _handle_error_response(self, response: httpx.Response) -> None:
        """
        Handle error responses from the API.

        Args:
            response: HTTP response object

        Raises:
            PublerAPIError: Appropriate exception for the error
        """
        try:
            error_data = response.json()
            errors = error_data.get("errors", [])
            message = "; ".join(errors) if errors else response.text
        except Exception:
            message = response.text or f"HTTP {response.status_code}"
            error_data = None
            errors = None

        # Extract retry-after header for rate limit errors
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    error_data = error_data or {}
                    error_data["retry_after"] = int(retry_after)
                except ValueError:
                    pass

        raise get_exception_for_status(
            status_code=response.status_code,
            message=message,
            response=error_data,
            errors=errors,
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self) -> "AsyncPublerSession":
        """Async context manager entry."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()
