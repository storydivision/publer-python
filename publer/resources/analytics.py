"""
Analytics API endpoints.
"""

from typing import Any, Optional

from publer.models.analytics import (
    Chart,
    ChartData,
    Competitor,
    CompetitorAnalysis,
    HashtagPerformance,
    MemberPerformance,
    PostInsight,
    TimeSeriesData,
    TimeSeriesDataPoint,
)
from publer.resources.base import AsyncBaseResource, BaseResource


class AnalyticsResource(BaseResource):
    """Synchronous analytics API endpoints."""

    def available_charts(self) -> list[Chart]:
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
        Get metadata for a specific chart.

        **Note:** This method returns chart metadata (titles, tooltips, chart types),
        not the actual time-series data points. To get time-series data for creating
        visualizations, use `get_chart_time_series()` instead.

        Args:
            chart_id: Chart identifier
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            account_id: Optional account ID to filter by

        Returns:
            Chart metadata

        Raises:
            NotFoundError: If chart doesn't exist
            PublerAPIError: If the request fails

        Example:
            >>> # Get chart metadata
            >>> metadata = client.analytics.chart_data(
            ...     "followers",
            ...     from_date="2025-01-01",
            ...     to_date="2025-01-31",
            ...     account_id="account_123"
            ... )
            >>> print(metadata.data)  # Chart configuration, not data points
        """
        params: dict[str, Any] = {}
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

    def get_chart_time_series(
        self,
        chart_id: str,
        account_id: str,
        from_date: str,
        to_date: str,
    ) -> TimeSeriesData:
        """
        Get time-series data points for a specific analytics chart.

        This method fetches the actual data points needed to recreate the charts
        shown on the Publer website, unlike `chart_data()` which returns metadata.

        Args:
            chart_id: Chart identifier (e.g., "followers", "engagement", "reach")
            account_id: Social media account ID (required)
            from_date: Start date in YYYY-MM-DD format (required)
            to_date: End date in YYYY-MM-DD format (required)

        Returns:
            Time series data with date/value pairs

        Raises:
            NotFoundError: If chart doesn't exist or account not found
            ValidationError: If date format is invalid
            PublerAPIError: If the request fails

        Example:
            >>> # Get follower count over time
            >>> data = client.analytics.get_chart_time_series(
            ...     chart_id="followers",
            ...     account_id="account_123",
            ...     from_date="2025-09-01",
            ...     to_date="2025-10-01"
            ... )
            >>> for point in data.data:
            ...     print(f"{point.date}: {point.value}")
            2025-09-01: 120
            2025-09-02: 122
            ...

        Note:
            The Publer API may use different endpoint patterns for different chart types.
            This method tries multiple endpoint variations to find the correct one:
            1. /analytics/{account_id}/charts/{chart_id}/data
            2. /analytics/charts/{chart_id}/data
            3. /analytics/{account_id}/{chart_id}
        """
        params: dict[str, Any] = {
            "from": from_date,
            "to": to_date,
        }

        # Try different endpoint patterns based on Publer API structure
        endpoints_to_try = [
            f"/analytics/{account_id}/charts/{chart_id}/data",
            f"/analytics/charts/{chart_id}/data",
            f"/analytics/{account_id}/{chart_id}",
        ]

        last_error = None
        for endpoint in endpoints_to_try:
            try:
                response = self._get(endpoint, params=params)

                # Parse response into time-series format
                data_points = []
                metadata = {}

                if isinstance(response, dict):
                    # Extract data points from various possible structures
                    if "data" in response and isinstance(response["data"], list):
                        raw_data = response["data"]
                    elif "values" in response and isinstance(response["values"], list):
                        raw_data = response["values"]
                    elif "points" in response and isinstance(response["points"], list):
                        raw_data = response["points"]
                    elif "series" in response and isinstance(response["series"], list):
                        raw_data = response["series"]
                    else:
                        # Response might be the data array directly
                        raw_data = response if isinstance(response, list) else []

                    # Extract metadata if present
                    metadata = {
                        k: v
                        for k, v in response.items()
                        if k not in ["data", "values", "points", "series"]
                    }
                elif isinstance(response, list):
                    raw_data = response
                else:
                    raw_data = []

                # Convert to TimeSeriesDataPoint objects
                for item in raw_data:
                    if isinstance(item, dict):
                        data_points.append(TimeSeriesDataPoint(**item))

                # If we got data, return it
                if data_points:
                    return TimeSeriesData(
                        chart_id=chart_id,
                        data=data_points,
                        period={"from": from_date, "to": to_date, "account_id": account_id},
                        metadata=metadata if metadata else None,
                    )

            except Exception as e:
                last_error = e
                continue

        # If all endpoints failed, raise the last error or a generic one
        if last_error:
            raise last_error
        else:
            # Return empty data if no endpoint worked but no error was raised
            return TimeSeriesData(
                chart_id=chart_id,
                data=[],
                period={"from": from_date, "to": to_date, "account_id": account_id},
                metadata={"error": "No data available for this chart"},
            )

    def post_insights(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
        sort_by: str = "scheduled_at",
        sort_type: str = "DESC",
        page: int = 0,
    ) -> list[PostInsight]:
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
        params: dict[str, Any] = {
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
    ) -> list[HashtagPerformance]:
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
        params: dict[str, Any] = {
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
    ) -> dict[str, Any]:
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
        params: dict[str, Any] = {
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
    ) -> list[MemberPerformance]:
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
        params: dict[str, Any] = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = self._get("/analytics/members", params=params)
        members_data = response.get("members", response) if isinstance(response, dict) else response
        return [MemberPerformance(**member) for member in members_data]

    def list_competitors(self) -> list[Competitor]:
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
        competitor_ids: Optional[list[str]] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> list[CompetitorAnalysis]:
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
        params: dict[str, Any] = {}
        if competitor_ids:
            params["competitor_ids"] = ",".join(competitor_ids)
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = self._get("/analytics/competitors/analysis", params=params)
        analysis_data = (
            response.get("analysis", response)
            if isinstance(response, dict)
            else response
        )
        return [CompetitorAnalysis(**comp) for comp in analysis_data]


class AsyncAnalyticsResource(AsyncBaseResource):
    """Asynchronous analytics API endpoints."""

    async def available_charts(self) -> list[Chart]:
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
        """
        Get metadata for a specific chart.

        **Note:** This method returns chart metadata (titles, tooltips, chart types),
        not the actual time-series data points. To get time-series data for creating
        visualizations, use `get_chart_time_series()` instead.
        """
        params: dict[str, Any] = {}
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

    async def get_chart_time_series(
        self,
        chart_id: str,
        account_id: str,
        from_date: str,
        to_date: str,
    ) -> TimeSeriesData:
        """
        Get time-series data points for a specific analytics chart.

        This method fetches the actual data points needed to recreate the charts
        shown on the Publer website, unlike `chart_data()` which returns metadata.

        See the synchronous version for full documentation.
        """
        params: dict[str, Any] = {
            "from": from_date,
            "to": to_date,
        }

        # Try different endpoint patterns based on Publer API structure
        endpoints_to_try = [
            f"/analytics/{account_id}/charts/{chart_id}/data",
            f"/analytics/charts/{chart_id}/data",
            f"/analytics/{account_id}/{chart_id}",
        ]

        last_error = None
        for endpoint in endpoints_to_try:
            try:
                response = await self._get(endpoint, params=params)

                # Parse response into time-series format
                data_points = []
                metadata = {}

                if isinstance(response, dict):
                    # Extract data points from various possible structures
                    if "data" in response and isinstance(response["data"], list):
                        raw_data = response["data"]
                    elif "values" in response and isinstance(response["values"], list):
                        raw_data = response["values"]
                    elif "points" in response and isinstance(response["points"], list):
                        raw_data = response["points"]
                    elif "series" in response and isinstance(response["series"], list):
                        raw_data = response["series"]
                    else:
                        # Response might be the data array directly
                        raw_data = response if isinstance(response, list) else []

                    # Extract metadata if present
                    metadata = {
                        k: v
                        for k, v in response.items()
                        if k not in ["data", "values", "points", "series"]
                    }
                elif isinstance(response, list):
                    raw_data = response
                else:
                    raw_data = []

                # Convert to TimeSeriesDataPoint objects
                for item in raw_data:
                    if isinstance(item, dict):
                        data_points.append(TimeSeriesDataPoint(**item))

                # If we got data, return it
                if data_points:
                    return TimeSeriesData(
                        chart_id=chart_id,
                        data=data_points,
                        period={"from": from_date, "to": to_date, "account_id": account_id},
                        metadata=metadata if metadata else None,
                    )

            except Exception as e:
                last_error = e
                continue

        # If all endpoints failed, raise the last error or a generic one
        if last_error:
            raise last_error
        else:
            # Return empty data if no endpoint worked but no error was raised
            return TimeSeriesData(
                chart_id=chart_id,
                data=[],
                period={"from": from_date, "to": to_date, "account_id": account_id},
                metadata={"error": "No data available for this chart"},
            )

    async def post_insights(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        account_id: Optional[str] = None,
        sort_by: str = "scheduled_at",
        sort_type: str = "DESC",
        page: int = 0,
    ) -> list[PostInsight]:
        """Get post performance insights."""
        params: dict[str, Any] = {
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
    ) -> list[HashtagPerformance]:
        """Get hashtag performance analysis."""
        params: dict[str, Any] = {
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
    ) -> dict[str, Any]:
        """Get best times to post."""
        params: dict[str, Any] = {
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
    ) -> list[MemberPerformance]:
        """Get team member performance metrics."""
        params: dict[str, Any] = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = await self._get("/analytics/members", params=params)
        members_data = response.get("members", response) if isinstance(response, dict) else response
        return [MemberPerformance(**member) for member in members_data]

    async def list_competitors(self) -> list[Competitor]:
        """List competitor accounts."""
        response = await self._get("/analytics/competitors")
        competitors_data = (
            response.get("competitors", response) if isinstance(response, dict) else response
        )
        return [Competitor(**comp) for comp in competitors_data]

    async def competitor_analysis(
        self,
        competitor_ids: Optional[list[str]] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> list[CompetitorAnalysis]:
        """Get competitor performance analysis."""
        params: dict[str, Any] = {}
        if competitor_ids:
            params["competitor_ids"] = ",".join(competitor_ids)
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = await self._get("/analytics/competitors/analysis", params=params)
        analysis_data = (
            response.get("analysis", response)
            if isinstance(response, dict)
            else response
        )
        return [CompetitorAnalysis(**comp) for comp in analysis_data]
