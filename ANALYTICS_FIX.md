# Analytics API Fix - Time-Series Chart Data

## Issue Summary

The `analytics.chart_data()` method was returning chart metadata (titles, tooltips, chart types) instead of actual time-series data points, making it impossible to recreate the analytics charts shown on the Publer website.

## Solution

Added a new method `get_chart_time_series()` that fetches actual time-series data points for analytics charts.

## Changes Made

### 1. New Models (`publer/models/analytics.py`)

Added two new Pydantic models for time-series data:

```python
class TimeSeriesDataPoint(BaseModel):
    """A single data point in a time series."""
    date: str  # Date in YYYY-MM-DD format
    value: Optional[float]  # Numeric value for this date
    count: Optional[int]  # Count value (if applicable)
    percentage: Optional[float]  # Percentage value (if applicable)
    label: Optional[str]  # Label for this data point

class TimeSeriesData(BaseModel):
    """Time series data response."""
    chart_id: str  # Chart identifier
    data: List[TimeSeriesDataPoint]  # Time series data points
    period: Optional[Dict[str, str]]  # Time period
    metadata: Optional[Dict[str, Any]]  # Chart metadata
```

### 2. New Method (`publer/resources/analytics.py`)

Added `get_chart_time_series()` method to both sync and async analytics resources:

```python
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
    """
```

### 3. Updated Documentation

Updated `chart_data()` documentation to clarify it returns metadata, not time-series data:

```python
def chart_data(...) -> ChartData:
    """
    Get metadata for a specific chart.
    
    **Note:** This method returns chart metadata (titles, tooltips, chart types),
    not the actual time-series data points. To get time-series data for creating
    visualizations, use `get_chart_time_series()` instead.
    """
```

## Usage

### Before (Returns Metadata Only)

```python
from publer import PublerClient

client = PublerClient(api_key)
client.set_workspace(workspace_id)

# This returns metadata, NOT data points
result = client.analytics.chart_data(
    chart_id="followers",
    account_id=account_id,
    from_date="2025-09-01",
    to_date="2025-10-01"
)

# Result contains chart configuration, not actual data:
# {
#   "chart_id": "followers",
#   "data": {
#     "values": [
#       {"id": "followers", "title": "Followers", "type": "vertical_bar_chart", ...}
#     ]
#   }
# }
```

### After (Returns Actual Data Points)

```python
from publer import PublerClient

client = PublerClient(api_key)
client.set_workspace(workspace_id)

# Get actual time-series data points
result = client.analytics.get_chart_time_series(
    chart_id="followers",
    account_id=account_id,
    from_date="2025-09-01",
    to_date="2025-10-01"
)

# Result contains actual data points:
# TimeSeriesData(
#   chart_id="followers",
#   data=[
#     TimeSeriesDataPoint(date="2025-09-01", value=120),
#     TimeSeriesDataPoint(date="2025-09-02", value=122),
#     TimeSeriesDataPoint(date="2025-09-03", value=125),
#     ...
#   ],
#   period={"from": "2025-09-01", "to": "2025-10-01", "account_id": "..."}
# )

# Use the data for visualization
for point in result.data:
    print(f"{point.date}: {point.value}")
```

## Implementation Details

### Endpoint Discovery

The `get_chart_time_series()` method tries multiple endpoint patterns to find the correct one:

1. `/analytics/{account_id}/charts/{chart_id}/data`
2. `/analytics/charts/{chart_id}/data`
3. `/analytics/{account_id}/{chart_id}`

This approach handles variations in the Publer API structure and provides resilience against API changes.

### Response Parsing

The method handles multiple response formats:

- Dictionary with `data`, `values`, `points`, or `series` keys
- Direct array of data points
- Nested structures with metadata

### Error Handling

- If all endpoints fail, the last error is raised
- If no data is available but no error occurs, returns empty `TimeSeriesData` with error metadata
- Gracefully handles missing or null values in data points

## Testing

Run the example script to test the implementation:

```bash
export PUBLER_API_KEY='your_api_key_here'
python examples/chart_time_series_example.py
```

The example demonstrates:
1. Difference between `chart_data()` and `get_chart_time_series()`
2. Testing multiple chart types
3. Simple ASCII visualization of time-series data

## Common Chart IDs

Based on the Publer API, common chart IDs include:

- `followers` - Follower count over time
- `engagement` - Engagement metrics
- `reach` - Reach metrics
- `impressions` - Impression counts
- `profile_views` - Profile view counts
- `post_reach` - Post reach metrics
- `post_engagement` - Post engagement metrics

**Note:** Available chart IDs may vary by account type (Instagram, Facebook, Twitter, etc.)

## Async Support

Both sync and async versions are available:

```python
# Synchronous
client = PublerClient(api_key)
data = client.analytics.get_chart_time_series(...)

# Asynchronous
async_client = AsyncPublerClient(api_key)
data = await async_client.analytics.get_chart_time_series(...)
```

## Backward Compatibility

The existing `chart_data()` method remains unchanged and continues to work as before. Users can:

1. Continue using `chart_data()` for metadata
2. Use the new `get_chart_time_series()` for actual data points
3. Migrate gradually without breaking existing code

## Known Limitations

1. **API Endpoint Uncertainty**: The exact Publer API endpoint for time-series data is not documented. The implementation tries multiple patterns, but some chart types may not work.

2. **Account-Specific Charts**: Some chart IDs may only be available for specific account types (e.g., Instagram-only metrics).

3. **Data Availability**: Not all accounts have historical data for all chart types.

## Troubleshooting

### "No data available for this chart"

**Possible causes:**
- The chart ID is not valid for your account type
- The account doesn't have historical data for the requested period
- The API endpoint structure is different than expected

**Solutions:**
- Use `available_charts()` to see which charts are available
- Try a different date range
- Check if the account has published posts in the date range

### 404 Not Found Error

**Possible causes:**
- Invalid chart ID
- Invalid account ID
- Chart type not supported by the API

**Solutions:**
- Verify the chart ID using `available_charts()`
- Verify the account ID using `accounts.list()`
- Try a different chart type

### Empty Data Array

**Possible causes:**
- No data available for the specified period
- Account is too new
- No posts published in the date range

**Solutions:**
- Extend the date range
- Check if posts exist using `post_insights()`
- Try aggregate endpoints like `hashtag_analysis()` or `member_performance()`

## Alternative Approaches

If `get_chart_time_series()` doesn't work for your use case, consider:

### 1. Aggregate Post Metrics

Use `post_insights()` to get post-level data and aggregate manually:

```python
insights = client.analytics.post_insights(
    account_id=account_id,
    from_date="2025-09-01",
    to_date="2025-10-01",
    sort_by="scheduled_at"
)

# Aggregate by date
from collections import defaultdict
daily_metrics = defaultdict(lambda: {"reach": 0, "engagement": 0})

for post in insights:
    date = post.published_at.strftime("%Y-%m-%d")
    daily_metrics[date]["reach"] += post.reach or 0
    daily_metrics[date]["engagement"] += post.engagement or 0
```

### 2. Use Hashtag Analysis

For hashtag-based metrics:

```python
hashtags = client.analytics.hashtag_analysis(
    account_id=account_id,
    from_date="2025-09-01",
    to_date="2025-10-01"
)
```

### 3. Use Best Times Data

For time-based patterns:

```python
best_times = client.analytics.best_times_to_post(
    account_id=account_id,
    from_date="2025-09-01",
    to_date="2025-10-01"
)
```

## Future Improvements

1. **API Documentation**: Work with Publer to document the correct endpoints for time-series data
2. **Chart Type Detection**: Automatically detect which endpoint pattern to use based on chart type
3. **Caching**: Add optional caching for frequently requested time-series data
4. **Data Interpolation**: Fill gaps in time-series data with interpolated values
5. **Export Utilities**: Add helper methods to export data to CSV, JSON, or pandas DataFrames

## Contributing

If you discover the correct API endpoints for specific chart types, please contribute:

1. Test the endpoint with your Publer account
2. Document the request/response format
3. Submit a pull request with the updated endpoint patterns
4. Add tests to verify the endpoint works

## References

- Publer API Documentation: https://app.publer.io/settings/api
- Issue Report: See `ANALYTICS_FIX.md` (this file)
- Example Usage: `examples/chart_time_series_example.py`
- Related Code: `publer/resources/analytics.py`, `publer/models/analytics.py`
