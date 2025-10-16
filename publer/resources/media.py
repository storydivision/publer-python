"""
Media API endpoints.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from publer.models.media import Media
from publer.resources.base import AsyncBaseResource, BaseResource


class MediaResource(BaseResource):
    """Synchronous media API endpoints."""

    def list(self, limit: int = 50, offset: int = 0) -> List[Media]:
        """
        List media files in the library.

        Args:
            limit: Maximum number of items to return
            offset: Pagination offset

        Returns:
            List of media objects

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> media_list = client.media.list(limit=20)
            >>> for media in media_list:
            ...     print(f"{media.title}: {media.url}")
        """
        params = {"limit": limit, "offset": offset}
        response = self._get("/media", params=params)
        media_data = response.get("media", response) if isinstance(response, dict) else response
        return [Media(**item) for item in media_data]

    def get(self, media_id: str) -> Media:
        """
        Get details of a specific media file.

        Args:
            media_id: Media ID

        Returns:
            Media object

        Raises:
            NotFoundError: If media doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> media = client.media.get("media_123")
            >>> print(media.url)
        """
        response = self._get(f"/media/{media_id}")
        return Media(**response)

    def upload(self, file_path: str, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a media file from local filesystem.

        Args:
            file_path: Path to the file to upload
            title: Optional title for the media

        Returns:
            Upload result with media details or job_id

        Raises:
            FileNotFoundError: If file doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> result = client.media.upload("/path/to/image.jpg", title="My Image")
            >>> print(result)
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, "rb") as f:
            files = {"file": (path.name, f, self._guess_mime_type(path))}
            data = {}
            if title:
                data["title"] = title

            return self._post("/media", files=files, data=data)

    def upload_from_url(self, url: str, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload media from a URL.

        Args:
            url: URL of the media to upload
            title: Optional title for the media

        Returns:
            Upload result with media details or job_id

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> result = client.media.upload_from_url(
            ...     "https://example.com/image.jpg",
            ...     title="Remote Image"
            ... )
        """
        data: Dict[str, Any] = {"url": url}
        if title:
            data["title"] = title

        return self._post("/media", json=data)

    def delete(self, media_id: str) -> Dict[str, Any]:
        """
        Delete a media file.

        Args:
            media_id: Media ID

        Returns:
            Deletion confirmation

        Raises:
            NotFoundError: If media doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> result = client.media.delete("media_123")
        """
        return self._delete(f"/media/{media_id}")

    @staticmethod
    def _guess_mime_type(path: Path) -> str:
        """Guess MIME type from file extension."""
        import mimetypes

        mime_type, _ = mimetypes.guess_type(str(path))
        return mime_type or "application/octet-stream"


class AsyncMediaResource(AsyncBaseResource):
    """Asynchronous media API endpoints."""

    async def list(self, limit: int = 50, offset: int = 0) -> List[Media]:
        """
        List media files in the library.

        Args:
            limit: Maximum number of items to return
            offset: Pagination offset

        Returns:
            List of media objects

        Example:
            >>> media_list = await client.media.list(limit=20)
        """
        params = {"limit": limit, "offset": offset}
        response = await self._get("/media", params=params)
        media_data = response.get("media", response) if isinstance(response, dict) else response
        return [Media(**item) for item in media_data]

    async def get(self, media_id: str) -> Media:
        """
        Get details of a specific media file.

        Args:
            media_id: Media ID

        Returns:
            Media object

        Example:
            >>> media = await client.media.get("media_123")
        """
        response = await self._get(f"/media/{media_id}")
        return Media(**response)

    async def upload(self, file_path: str, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a media file from local filesystem.

        Args:
            file_path: Path to the file to upload
            title: Optional title for the media

        Returns:
            Upload result with media details or job_id

        Example:
            >>> result = await client.media.upload("/path/to/image.jpg")
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, "rb") as f:
            files = {"file": (path.name, f, MediaResource._guess_mime_type(path))}
            data = {}
            if title:
                data["title"] = title

            return await self._post("/media", files=files, data=data)

    async def upload_from_url(self, url: str, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload media from a URL.

        Args:
            url: URL of the media to upload
            title: Optional title for the media

        Returns:
            Upload result with media details or job_id

        Example:
            >>> result = await client.media.upload_from_url("https://example.com/image.jpg")
        """
        data: Dict[str, Any] = {"url": url}
        if title:
            data["title"] = title

        return await self._post("/media", json=data)

    async def delete(self, media_id: str) -> Dict[str, Any]:
        """
        Delete a media file.

        Args:
            media_id: Media ID

        Returns:
            Deletion confirmation

        Example:
            >>> result = await client.media.delete("media_123")
        """
        return await self._delete(f"/media/{media_id}")
