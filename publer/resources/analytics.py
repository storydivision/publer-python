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
        return ChartData(chart_id=chart_id, **response)

    def post_insights(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
        sort_by: str = "published_at",
        order: str = "desc",
        limit: int = 50,
        offset: int = 0,
    ) -> List[PostInsight]:
        """
        Get post performance insights with filtering and sorting.

        Args:
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
            account_id: Filter by account
            sort_by: Sort field (published_at, engagement, reach, impressions)
            order: Sort order (asc, desc)
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of post insights

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> insights = client.analytics.post_insights(
            ...     from_date="2025-01-01",
            ...     sort_by="engagement",
            ...     order="desc",
            ...     limit=10
            ... )
        """
        params: Dict[str, Any] = {
            "sort_by": sort_by,
            "order": order,
            "limit": limit,
            "offset": offset,
        }
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if account_id:
            params["account_id"] = account_id

        response = self._get("/analytics/post-insights", params=params)
        insights_data = response.get("insights", response) if isinstance(response, dict) else response
        return [PostInsight(**insight) for insight in insights_data]

    def hashtag_analysis(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        limit: int = 50,
    ) -> List[HashtagPerformance]:
        """
        Get hashtag performance analysis.

        Args:
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
            limit: Maximum results

        Returns:
            List of hashtag performance data

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> hashtags = client.analytics.hashtag_analysis(
            ...     from_date="2025-01-01",
            ...     limit=20
            ... )
            >>> for tag in hashtags:
            ...     print(f"#{tag.hashtag}: {tag.posts_count} posts")
        """
        params: Dict[str, Any] = {"limit": limit}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = self._get("/analytics/hashtags", params=params)
        hashtags_data = response.get("hashtags", response) if isinstance(response, dict) else response
        return [HashtagPerformance(**tag) for tag in hashtags_data]

    def best_times_to_post(
        self,
        account_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[BestTime]:
        """
        Get best times to post based on historical performance.

        Args:
            account_id: Optional account ID
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)

        Returns:
            List of best posting times

        Raises:
            PublerAPIError: If the request fails

        Example:
            >>> times = client.analytics.best_times_to_post()
            >>> for time in times[:5]:
            ...     print(f"{time.day} at {time.hour}:00 - Score: {time.score}")
        """
        params: Dict[str, Any] = {}
        if account_id:
            params["account_id"] = account_id
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = self._get("/analytics/best-times", params=params)
        times_data = response.get("times", response) if isinstance(response, dict) else response
        return [BestTime(**time) for time in times_data]

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
        return ChartData(chart_id=chart_id, **response)

    async def post_insights(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
        sort_by: str = "published_at",
        order: str = "desc",
        limit: int = 50,
        offset: int = 0,
    ) -> List[PostInsight]:
        """Get post performance insights."""
        params: Dict[str, Any] = {
            "sort_by": sort_by,
            "order": order,
            "limit": limit,
            "offset": offset,
        }
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if account_id:
            params["account_id"] = account_id

        response = await self._get("/analytics/post-insights", params=params)
        insights_data = response.get("insights", response) if isinstance(response, dict) else response
        return [PostInsight(**insight) for insight in insights_data]

    async def hashtag_analysis(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        limit: int = 50,
    ) -> List[HashtagPerformance]:
        """Get hashtag performance analysis."""
        params: Dict[str, Any] = {"limit": limit}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = await self._get("/analytics/hashtags", params=params)
        hashtags_data = response.get("hashtags", response) if isinstance(response, dict) else response
        return [HashtagPerformance(**tag) for tag in hashtags_data]

    async def best_times_to_post(
        self,
        account_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[BestTime]:
        """Get best times to post."""
        params: Dict[str, Any] = {}
        if account_id:
            params["account_id"] = account_id
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = await self._get("/analytics/best-times", params=params)
        times_data = response.get("times", response) if isinstance(response, dict) else response
        return [BestTime(**time) for time in times_data]

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
