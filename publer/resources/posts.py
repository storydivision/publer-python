"""
Posts API endpoints.
"""

from typing import Any, Dict, List, Optional

from publer.models.posts import BulkPostCreate, Post, PostCreate, PostUpdate
from publer.resources.base import AsyncBaseResource, BaseResource


class PostsResource(BaseResource):
    """Synchronous posts API endpoints."""

    def create(
        self,
        text: Optional[str] = None,
        accounts: Optional[List[str]] = None,
        scheduled_at: Optional[str] = None,
        media_urls: Optional[List[str]] = None,
        media_ids: Optional[List[str]] = None,
        link: Optional[str] = None,
        state: str = "scheduled",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create a new post.

        Note: This endpoint returns a job_id for async processing.
        Use job_status() to check the status.

        Args:
            text: Post content text
            accounts: List of account IDs to post to
            scheduled_at: ISO 8601 timestamp for scheduling
            media_urls: List of media URLs to attach
            media_ids: List of media IDs from library
            link: Link to share
            state: Post state (scheduled/draft)
            **kwargs: Additional post parameters

        Returns:
            Dictionary with job_id for tracking

        Raises:
            ValidationError: If post data is invalid
            PublerAPIError: If the request fails

        Example:
            >>> result = client.posts.create(
            ...     text="Hello world!",
            ...     accounts=["account_123"],
            ...     scheduled_at="2025-10-15T10:00:00+00:00"
            ... )
            >>> job_id = result["job_id"]
        """
        post_data: Dict[str, Any] = {
            "state": state,
            **kwargs,
        }

        if text is not None:
            post_data["text"] = text
        if accounts is not None:
            post_data["accounts"] = accounts
        if scheduled_at is not None:
            post_data["scheduled_at"] = scheduled_at
        if media_urls is not None:
            post_data["media_urls"] = media_urls
        if media_ids is not None:
            post_data["media_ids"] = media_ids
        if link is not None:
            post_data["link"] = link

        return self._post("/posts", json=post_data)

    def create_bulk(self, posts: List[Dict[str, Any]], state: str = "scheduled") -> Dict[str, Any]:
        """
        Create multiple posts in bulk.

        Args:
            posts: List of post data dictionaries
            state: State for all posts (scheduled/draft)

        Returns:
            Dictionary with job_id for tracking

        Raises:
            ValidationError: If post data is invalid
            PublerAPIError: If the request fails

        Example:
            >>> result = client.posts.create_bulk([
            ...     {"text": "Post 1", "accounts": ["acc_1"]},
            ...     {"text": "Post 2", "accounts": ["acc_1"]},
            ... ])
            >>> job_id = result["job_id"]
        """
        bulk_data = {"bulk": {"state": state, "posts": posts}}
        return self._post("/posts", json=bulk_data)

    def list(
        self,
        state: Optional[str] = None,
        states: Optional[List[str]] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 0,
        account_ids: Optional[List[str]] = None,
        query: Optional[str] = None,
        post_type: Optional[str] = None,
        member_id: Optional[str] = None,
    ) -> List[Post]:
        """
        List posts with optional filters.

        Args:
            state: Filter by a single post state (all, scheduled, published, draft, failed, etc.)
            states: Filter by multiple post states (use state[] array)
            from_date: Filter posts from this date (ISO 8601 or YYYY-MM-DD)
            to_date: Filter posts until this date (ISO 8601 or YYYY-MM-DD)
            page: Page number for pagination (default: 0)
            account_ids: List of account IDs to filter by
            query: Full-text search keyword in post content
            post_type: Filter by post type (status, link, photo, video, reel, story, etc.)
            member_id: Filter posts created by a specific workspace member

        Returns:
            List of post objects

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> # Single state filter
            >>> posts = client.posts.list(state="scheduled", page=0)
            >>> 
            >>> # Multiple states
            >>> posts = client.posts.list(states=["scheduled", "published"])
            >>> 
            >>> # Filter by accounts and search
            >>> posts = client.posts.list(
            ...     account_ids=["acc_1", "acc_2"],
            ...     query="launch",
            ...     post_type="photo"
            ... )
        """
        params: Dict[str, Any] = {"page": page}

        if state:
            params["state"] = state
        if states:
            params["state[]"] = states
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if account_ids:
            params["account_ids[]"] = account_ids
        if query:
            params["query"] = query
        if post_type:
            params["postType"] = post_type
        if member_id:
            params["member_id"] = member_id

        response = self._get("/posts", params=params)
        posts_data = response.get("posts", response) if isinstance(response, dict) else response
        return [Post(**post) for post in posts_data]

    def get(self, post_id: str) -> Post:
        """
        Get details of a specific post.
        
        NOTE: The GET /api/v1/posts/{post_id} endpoint is not available in the Publer API.
        This method will raise a ForbiddenError (403).
        
        WORKAROUND: Use posts.list() with filters to retrieve post details instead.

        Args:
            post_id: Post ID

        Returns:
            Post object

        Raises:
            ForbiddenError: This endpoint is not available in the API
            NotFoundError: If post doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> # This will fail with 403 Forbidden
            >>> # post = client.posts.get("post_123")
            >>> 
            >>> # Use list() instead to get post details
            >>> posts = client.posts.list(state="all")
            >>> post = next((p for p in posts if p.id == "post_123"), None)
        """
        # This endpoint returns 403 Forbidden - not available in the API
        # Keeping the method for backwards compatibility but documenting the limitation
        response = self._get(f"/posts/{post_id}")
        return Post(**response)

    def update(self, post_id: str, **kwargs: Any) -> Post:
        """
        Update an existing post.

        Args:
            post_id: Post ID
            **kwargs: Fields to update (text, scheduled_at, accounts, etc.)

        Returns:
            Updated post object

        Raises:
            NotFoundError: If post doesn't exist
            ValidationError: If update data is invalid
            PublerAPIError: If the request fails

        Example:
            >>> post = client.posts.update(
            ...     "post_123",
            ...     text="Updated text",
            ...     scheduled_at="2025-10-16T10:00:00+00:00"
            ... )
        """
        response = self._put(f"/posts/{post_id}", json=kwargs)
        return Post(**response)

    def delete(self, post_id: str) -> Dict[str, Any]:
        """
        Delete a post.

        Args:
            post_id: Post ID

        Returns:
            Deletion confirmation

        Raises:
            NotFoundError: If post doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> result = client.posts.delete("post_123")
            >>> print(result)
        """
        return self._delete(f"/posts/{post_id}")


class AsyncPostsResource(AsyncBaseResource):
    """Asynchronous posts API endpoints."""

    async def create(
        self,
        text: Optional[str] = None,
        accounts: Optional[List[str]] = None,
        scheduled_at: Optional[str] = None,
        media_urls: Optional[List[str]] = None,
        media_ids: Optional[List[str]] = None,
        link: Optional[str] = None,
        state: str = "scheduled",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create a new post.

        Note: This endpoint returns a job_id for async processing.

        Args:
            text: Post content text
            accounts: List of account IDs to post to
            scheduled_at: ISO 8601 timestamp for scheduling
            media_urls: List of media URLs to attach
            media_ids: List of media IDs from library
            link: Link to share
            state: Post state (scheduled/draft)
            **kwargs: Additional post parameters

        Returns:
            Dictionary with job_id for tracking

        Example:
            >>> result = await client.posts.create(
            ...     text="Hello world!",
            ...     accounts=["account_123"]
            ... )
        """
        post_data: Dict[str, Any] = {
            "state": state,
            **kwargs,
        }

        if text is not None:
            post_data["text"] = text
        if accounts is not None:
            post_data["accounts"] = accounts
        if scheduled_at is not None:
            post_data["scheduled_at"] = scheduled_at
        if media_urls is not None:
            post_data["media_urls"] = media_urls
        if media_ids is not None:
            post_data["media_ids"] = media_ids
        if link is not None:
            post_data["link"] = link

        return await self._post("/posts", json=post_data)

    async def create_bulk(
        self, posts: List[Dict[str, Any]], state: str = "scheduled"
    ) -> Dict[str, Any]:
        """
        Create multiple posts in bulk.

        Args:
            posts: List of post data dictionaries
            state: State for all posts (scheduled/draft)

        Returns:
            Dictionary with job_id for tracking

        Example:
            >>> result = await client.posts.create_bulk([
            ...     {"text": "Post 1", "accounts": ["acc_1"]},
            ... ])
        """
        bulk_data = {"bulk": {"state": state, "posts": posts}}
        return await self._post("/posts", json=bulk_data)

    async def list(
        self,
        state: Optional[str] = None,
        states: Optional[List[str]] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 0,
        account_ids: Optional[List[str]] = None,
        query: Optional[str] = None,
        post_type: Optional[str] = None,
        member_id: Optional[str] = None,
    ) -> List[Post]:
        """List posts with optional filters."""
        params: Dict[str, Any] = {"page": page}

        if state:
            params["state"] = state
        if states:
            params["state[]"] = states
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if account_ids:
            params["account_ids[]"] = account_ids
        if query:
            params["query"] = query
        if post_type:
            params["postType"] = post_type
        if member_id:
            params["member_id"] = member_id

        response = await self._get("/posts", params=params)
        posts_data = response.get("posts", response) if isinstance(response, dict) else response
        return [Post(**post) for post in posts_data]

    async def get(self, post_id: str) -> Post:
        """
        Get details of a specific post.
        
        NOTE: The GET /api/v1/posts/{post_id} endpoint is not available in the Publer API.
        This method will raise a ForbiddenError (403).
        
        WORKAROUND: Use posts.list() with filters to retrieve post details instead.

        Args:
            post_id: Post ID

        Returns:
            Post object

        Raises:
            ForbiddenError: This endpoint is not available in the API

        Example:
            >>> # This will fail with 403 Forbidden
            >>> # post = await client.posts.get("post_123")
            >>> 
            >>> # Use list() instead
            >>> posts = await client.posts.list(state="all")
            >>> post = next((p for p in posts if p.id == "post_123"), None)
        """
        # This endpoint returns 403 Forbidden - not available in the API
        response = await self._get(f"/posts/{post_id}")
        return Post(**response)

    async def update(self, post_id: str, **kwargs: Any) -> Post:
        """
        Update an existing post.

        Args:
            post_id: Post ID
            **kwargs: Fields to update

        Returns:
            Updated post object

        Example:
            >>> post = await client.posts.update("post_123", text="New text")
        """
        response = await self._put(f"/posts/{post_id}", json=kwargs)
        return Post(**response)

    async def delete(self, post_id: str) -> Dict[str, Any]:
        """
        Delete a post.

        Args:
            post_id: Post ID

        Returns:
            Deletion confirmation

        Example:
            >>> result = await client.posts.delete("post_123")
        """
        return await self._delete(f"/posts/{post_id}")
