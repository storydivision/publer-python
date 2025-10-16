"""
Analytics API endpoints.
"""

from typing import Any, Dict, List, Optional

from publer.models.analytics import (
    BestTime,
    Chart,
    ChartData,
    Competitor,
    CompetitorAnalysis,
    HashtagPerformance,
    MemberPerformance,
    PostInsight,
)
from publer.resources.base import AsyncBaseResource, BaseResource


class AnalyticsResource(BaseResource):
    """Synchronous analytics API endpoints."""

    def available_charts(self) -> List[Chart]:
        """
        Get list of available analytics charts.

        Returns:
            List of available charts

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> charts = client.analytics.available_charts()
            >>> for chart in charts:
            ...     print(f"{chart.name}: {chart.description}")
        """
        response = self._get("/analytics/charts")
        charts_data = response.get("charts", response) if isinstance(response, dict) else response
        return [Chart(**chart) for chart in charts_data]

    def chart_data(
        self,
        chart_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> ChartData:
        """
        Get data for a specific chart.

        Args:
            chart_id: Chart identifier
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
            account_id: Optional account ID to filter by

        Returns:
            Chart data

        Raises:
            NotFoundError: If chart doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> data = client.analytics.chart_data(
            ...     "engagement_over_time",
            ...     from_date="2025-01-01",
            ...     to_date="2025-01-31"
            ... )
        """
        params: Dict[str, Any] = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if account_id:
            params["account_id"] = account_id

        response = self._get(f"/analytics/charts/{chart_id}", params=params)
        # Handle both dict and list responses
        if isinstance(response, list):
            return ChartData(chart_id=chart_id, data={"values": response}, period=params)
        return ChartData(chart_id=chart_id, data=response, period=params)

    def post_insights(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
        sort_by: str = "scheduled_at",
        sort_type: str = "DESC",
        page: int = 0,
    ) -> List[PostInsight]:
        """
        Get post performance insights with filtering and sorting.

        Args:
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            account_id: Filter by account (optional, if omitted returns all accounts)
            sort_by: Sort field (scheduled_at, engagement, reach, engagement_rate, etc.)
            sort_type: Sort direction (ASC or DESC)
            page: Page number (0-based, 10 posts per page)

        Returns:
            List of post insights

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> insights = client.analytics.post_insights(
            ...     account_id="account_123",
            ...     from_date="2025-01-01",
            ...     sort_by="engagement",
            ...     sort_type="DESC",
            ...     page=0
            ... )
        """
        params: Dict[str, Any] = {
            "sort_by": sort_by,
            "sort_type": sort_type,
            "page": page,
        }
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        # Build endpoint URL with account_id in path if provided
        if account_id:
            endpoint = f"/analytics/{account_id}/post_insights"
        else:
            endpoint = "/analytics/post_insights"

        response = self._get(endpoint, params=params)
        
        # Handle different response formats
        if isinstance(response, str):
            # API returned an error message as string
            return []
        elif isinstance(response, dict):
            insights_data = response.get("insights", response.get("data", []))
        elif isinstance(response, list):
            insights_data = response
        else:
            insights_data = []
            
        return [PostInsight(**insight) for insight in insights_data if isinstance(insight, dict)]

    def hashtag_analysis(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
        sort_by: str = "posts",
        sort_type: str = "DESC",
        page: int = 0,
        query: Optional[str] = None,
        member_id: Optional[str] = None,
    ) -> List[HashtagPerformance]:
        """
        Get hashtag performance analysis.

        Args:
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            account_id: Filter by account (optional, if omitted returns all accounts)
            sort_by: Sort field (posts, reach, likes, comments, shares, video_views)
            sort_type: Sort direction (ASC or DESC)
            page: Page number (0-based, 10 hashtags per page)
            query: Search filter by hashtag text
            member_id: Filter by member ID

        Returns:
            List of hashtag performance data

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> hashtags = client.analytics.hashtag_analysis(
            ...     account_id="account_123",
            ...     from_date="2025-01-01",
            ...     sort_by="engagement",
            ...     page=0
            ... )
            >>> for tag in hashtags:
            ...     print(f"#{tag.hashtag}: {tag.posts_count} posts")
        """
        params: Dict[str, Any] = {
            "sort_by": sort_by,
            "sort_type": sort_type,
            "page": page,
        }
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if query:
            params["query"] = query
        if member_id:
            params["member_id"] = member_id

        # Build endpoint URL with account_id in path if provided
        if account_id:
            endpoint = f"/analytics/{account_id}/hashtag_insights"
        else:
            endpoint = "/analytics/hashtag_insights"

        response = self._get(endpoint, params=params)
        
        # Handle different response formats
        if isinstance(response, dict):
            hashtags_data = response.get("records", response.get("hashtags", []))
        elif isinstance(response, list):
            hashtags_data = response
        else:
            hashtags_data = []
            
        return [HashtagPerformance(**tag) for tag in hashtags_data if isinstance(tag, dict)]

    def best_times_to_post(
        self,
        from_date: str,
        to_date: str,
        account_id: Optional[str] = None,
        competitors: bool = False,
        competitor_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get best times to post based on historical performance.

        Args:
            from_date: Start date (YYYY-MM-DD) - REQUIRED
            to_date: End date (YYYY-MM-DD) - REQUIRED
            account_id: Filter by account (optional, if omitted returns all accounts)
            competitors: Include competitor data (default False)
            competitor_id: Specific competitor ID to analyze

        Returns:
            Dict keyed by day of week (Monday-Sunday), each with 24 hourly scores

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> times = client.analytics.best_times_to_post(
            ...     account_id="account_123",
            ...     from_date="2025-01-01",
            ...     to_date="2025-01-31"
            ... )
            >>> for day, hours in times.items():
            ...     print(f"{day}: best hour is {hours.index(max(hours))}:00")
        """
        params: Dict[str, Any] = {
            "from": from_date,
            "to": to_date,
        }
        if competitors:
            params["competitors"] = "true"
        if competitor_id:
            params["competitor_id"] = competitor_id

        # Build endpoint URL with account_id in path if provided
        if account_id:
            endpoint = f"/analytics/{account_id}/best_times"
        else:
            endpoint = "/analytics/best_times"

        response = self._get(endpoint, params=params)
        # Response is a dict keyed by day of week
        return response if isinstance(response, dict) else {}

    def member_performance(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[MemberPerformance]:
        """
        Get team member performance metrics.

        Args:
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)

        Returns:
            List of member performance data

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> members = client.analytics.member_performance(
            ...     from_date="2025-01-01"
            ... )
            >>> for member in members:
            ...     print(f"{member.name}: {member.posts_count} posts")
        """
        params: Dict[str, Any] = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = self._get("/analytics/members", params=params)
        members_data = response.get("members", response) if isinstance(response, dict) else response
        return [MemberPerformance(**member) for member in members_data]

    def list_competitors(self) -> List[Competitor]:
        """
        List competitor accounts.

        Returns:
            List of competitors

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> competitors = client.analytics.list_competitors()
            >>> for comp in competitors:
            ...     print(f"{comp.name} on {comp.platform}")
        """
        response = self._get("/analytics/competitors")
        competitors_data = (
            response.get("competitors", response) if isinstance(response, dict) else response
        )
        return [Competitor(**comp) for comp in competitors_data]

    def competitor_analysis(
        self,
        competitor_ids: Optional[List[str]] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[CompetitorAnalysis]:
        """
        Get competitor performance analysis.

        Args:
            competitor_ids: List of competitor IDs (None for all)
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)

        Returns:
            List of competitor analysis data

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> analysis = client.analytics.competitor_analysis(
            ...     from_date="2025-01-01"
            ... )
            >>> for comp in analysis:
            ...     print(f"{comp.name}: {comp.followers} followers")
        """
        params: Dict[str, Any] = {}
        if competitor_ids:
            params["competitor_ids"] = ",".join(competitor_ids)
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = self._get("/analytics/competitors/analysis", params=params)
        analysis_data = response.get("analysis", response) if isinstance(response, dict) else response
        return [CompetitorAnalysis(**comp) for comp in analysis_data]


class AsyncAnalyticsResource(AsyncBaseResource):
    """Asynchronous analytics API endpoints."""

    async def available_charts(self) -> List[Chart]:
        """Get list of available analytics charts."""
        response = await self._get("/analytics/charts")
        charts_data = response.get("charts", response) if isinstance(response, dict) else response
        return [Chart(**chart) for chart in charts_data]

    async def chart_data(
        self,
        chart_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> ChartData:
        """Get data for a specific chart."""
        params: Dict[str, Any] = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if account_id:
            params["account_id"] = account_id

        response = await self._get(f"/analytics/charts/{chart_id}", params=params)
        # Handle both dict and list responses
        if isinstance(response, list):
            return ChartData(chart_id=chart_id, data={"values": response}, period=params)
        return ChartData(chart_id=chart_id, data=response, period=params)

    async def post_insights(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
        sort_by: str = "scheduled_at",
        sort_type: str = "DESC",
        page: int = 0,
    ) -> List[PostInsight]:
        """Get post performance insights."""
        params: Dict[str, Any] = {
            "sort_by": sort_by,
            "sort_type": sort_type,
            "page": page,
        }
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        # Build endpoint URL with account_id in path if provided
        if account_id:
            endpoint = f"/analytics/{account_id}/post_insights"
        else:
            endpoint = "/analytics/post_insights"

        response = await self._get(endpoint, params=params)
        
        # Handle different response formats
        if isinstance(response, str):
            # API returned an error message as string
            return []
        elif isinstance(response, dict):
            insights_data = response.get("insights", response.get("data", []))
        elif isinstance(response, list):
            insights_data = response
        else:
            insights_data = []
            
        return [PostInsight(**insight) for insight in insights_data if isinstance(insight, dict)]

    async def hashtag_analysis(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
        sort_by: str = "posts",
        sort_type: str = "DESC",
        page: int = 0,
        query: Optional[str] = None,
        member_id: Optional[str] = None,
    ) -> List[HashtagPerformance]:
        """Get hashtag performance analysis."""
        params: Dict[str, Any] = {
            "sort_by": sort_by,
            "sort_type": sort_type,
            "page": page,
        }
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if query:
            params["query"] = query
        if member_id:
            params["member_id"] = member_id

        # Build endpoint URL with account_id in path if provided
        if account_id:
            endpoint = f"/analytics/{account_id}/hashtag_insights"
        else:
            endpoint = "/analytics/hashtag_insights"

        response = await self._get(endpoint, params=params)
        
        # Handle different response formats
        if isinstance(response, dict):
            hashtags_data = response.get("records", response.get("hashtags", []))
        elif isinstance(response, list):
            hashtags_data = response
        else:
            hashtags_data = []
            
        return [HashtagPerformance(**tag) for tag in hashtags_data if isinstance(tag, dict)]

    async def best_times_to_post(
        self,
        from_date: str,
        to_date: str,
        account_id: Optional[str] = None,
        competitors: bool = False,
        competitor_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get best times to post."""
        params: Dict[str, Any] = {
            "from": from_date,
            "to": to_date,
        }
        if competitors:
            params["competitors"] = "true"
        if competitor_id:
            params["competitor_id"] = competitor_id

        # Build endpoint URL with account_id in path if provided
        if account_id:
            endpoint = f"/analytics/{account_id}/best_times"
        else:
            endpoint = "/analytics/best_times"

        response = await self._get(endpoint, params=params)
        # Response is a dict keyed by day of week
        return response if isinstance(response, dict) else {}

    async def member_performance(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[MemberPerformance]:
        """Get team member performance metrics."""
        params: Dict[str, Any] = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = await self._get("/analytics/members", params=params)
        members_data = response.get("members", response) if isinstance(response, dict) else response
        return [MemberPerformance(**member) for member in members_data]

    async def list_competitors(self) -> List[Competitor]:
        """List competitor accounts."""
        response = await self._get("/analytics/competitors")
        competitors_data = (
            response.get("competitors", response) if isinstance(response, dict) else response
        )
        return [Competitor(**comp) for comp in competitors_data]

    async def competitor_analysis(
        self,
        competitor_ids: Optional[List[str]] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[CompetitorAnalysis]:
        """Get competitor performance analysis."""
        params: Dict[str, Any] = {}
        if competitor_ids:
            params["competitor_ids"] = ",".join(competitor_ids)
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = await self._get("/analytics/competitors/analysis", params=params)
        analysis_data = response.get("analysis", response) if isinstance(response, dict) else response
        return [CompetitorAnalysis(**comp) for comp in analysis_data]
