"""
Base resource class for API endpoints.
"""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from publer.session import AsyncPublerSession, PublerSession


class BaseResource:
    """Base class for synchronous API resources."""

    def __init__(self, session: "PublerSession") -> None:
        """
        Initialize a resource.

        Args:
            session: HTTP session for making requests
        """
        self._session = session

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json: JSON body
            data: Form data
            files: Files to upload

        Returns:
            Response data
        """
        return self._session.request(
            method=method,
            endpoint=endpoint,
            params=params,
            json=json,
            data=data,
            files=files,
        )

    def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response data
        """
        return self._request("GET", endpoint, params=params)

    def _post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a POST request.

        Args:
            endpoint: API endpoint
            json: JSON body
            data: Form data
            files: Files to upload

        Returns:
            Response data
        """
        return self._request("POST", endpoint, json=json, data=data, files=files)

    def _put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a PUT request.

        Args:
            endpoint: API endpoint
            json: JSON body

        Returns:
            Response data
        """
        return self._request("PUT", endpoint, json=json)

    def _patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a PATCH request.

        Args:
            endpoint: API endpoint
            json: JSON body

        Returns:
            Response data
        """
        return self._request("PATCH", endpoint, json=json)

    def _delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a DELETE request.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response data
        """
        return self._request("DELETE", endpoint, params=params)


class AsyncBaseResource:
    """Base class for asynchronous API resources."""

    def __init__(self, session: "AsyncPublerSession") -> None:
        """
        Initialize a resource.

        Args:
            session: Async HTTP session for making requests
        """
        self._session = session

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an async HTTP request.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json: JSON body
            data: Form data
            files: Files to upload

        Returns:
            Response data
        """
        return await self._session.request(
            method=method,
            endpoint=endpoint,
            params=params,
            json=json,
            data=data,
            files=files,
        )

    async def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an async GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response data
        """
        return await self._request("GET", endpoint, params=params)

    async def _post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an async POST request.

        Args:
            endpoint: API endpoint
            json: JSON body
            data: Form data
            files: Files to upload

        Returns:
            Response data
        """
        return await self._request("POST", endpoint, json=json, data=data, files=files)

    async def _put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an async PUT request.

        Args:
            endpoint: API endpoint
            json: JSON body

        Returns:
            Response data
        """
        return await self._request("PUT", endpoint, json=json)

    async def _patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an async PATCH request.

        Args:
            endpoint: API endpoint
            json: JSON body

        Returns:
            Response data
        """
        return await self._request("PATCH", endpoint, json=json)

    async def _delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an async DELETE request.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response data
        """
        return await self._request("DELETE", endpoint, params=params)
