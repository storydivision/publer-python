"""
Example: Fetching Time-Series Chart Data

This example demonstrates how to use the new `get_chart_time_series()` method
to fetch actual time-series data points for analytics charts, which can be used
to recreate the visualizations shown on the Publer website.

This addresses the issue where `chart_data()` was returning metadata instead of
actual data points.
"""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from publer import PublerClient

# Load environment variables from .env file
load_dotenv()


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demonstrate_chart_metadata_vs_data(client, chart_id: str, account_id: str):
    """
    Demonstrate the difference between chart_data() and get_chart_time_series().
    """
    print_section("Comparing chart_data() vs get_chart_time_series()")

    # Calculate date range (last 30 days)
    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)
    from_str = from_date.strftime("%Y-%m-%d")
    to_str = to_date.strftime("%Y-%m-%d")

    print(f"\n📅 Date Range: {from_str} to {to_str}")
    print(f"📊 Chart ID: {chart_id}")
    print(f"🎯 Account: {account_id}")

    # 1. Get chart metadata using chart_data()
    print("\n" + "-" * 70)
    print("1️⃣  Using chart_data() - Returns Metadata")
    print("-" * 70)

    try:
        metadata = client.analytics.chart_data(
            chart_id=chart_id,
            account_id=account_id,
            from_date=from_str,
            to_date=to_str,
        )
        print("\n✅ Chart metadata retrieved:")
        print(f"   Chart ID: {metadata.chart_id}")
        print(f"   Data type: {type(metadata.data)}")
        print(f"   Data keys: {list(metadata.data.keys()) if isinstance(metadata.data, dict) else 'N/A'}")
        print("\n   ⚠️  This returns chart configuration, NOT data points!")

    except Exception as e:
        print(f"\n❌ Error getting metadata: {str(e)}")

    # 2. Get actual time-series data using get_chart_time_series()
    print("\n" + "-" * 70)
    print("2️⃣  Using get_chart_time_series() - Returns Actual Data Points")
    print("-" * 70)

    try:
        time_series = client.analytics.get_chart_time_series(
            chart_id=chart_id,
            account_id=account_id,
            from_date=from_str,
            to_date=to_str,
        )

        print("\n✅ Time-series data retrieved:")
        print(f"   Chart ID: {time_series.chart_id}")
        print(f"   Number of data points: {len(time_series.data)}")
        print(f"   Period: {time_series.period}")

        if time_series.data:
            print("\n   📈 Sample data points:")
            # Show first 5 and last 5 data points
            sample_size = min(5, len(time_series.data))
            for i in range(sample_size):
                point = time_series.data[i]
                print(f"      {point.date}: {point.value}")

            if len(time_series.data) > 10:
                print("      ...")
                for i in range(-sample_size, 0):
                    point = time_series.data[i]
                    print(f"      {point.date}: {point.value}")

            print("\n   ✨ This data can be used to create visualizations!")
        else:
            print("\n   ⚠️  No data points available")
            if time_series.metadata:
                print(f"   Metadata: {time_series.metadata}")

    except Exception as e:
        print(f"\n❌ Error getting time-series data: {str(e)}")
        print("   This may indicate:")
        print("   - The chart ID is not valid for this account")
        print("   - The API endpoint structure is different than expected")
        print("   - The account doesn't have data for this chart type")


def try_multiple_charts(client, account_id: str):
    """
    Try fetching time-series data for multiple chart types.
    """
    print_section("Testing Multiple Chart Types")

    # Common chart IDs to try
    chart_ids = [
        "followers",
        "engagement",
        "reach",
        "impressions",
        "profile_views",
        "post_reach",
        "post_engagement",
    ]

    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)
    from_str = from_date.strftime("%Y-%m-%d")
    to_str = to_date.strftime("%Y-%m-%d")

    print(f"\n📅 Date Range: {from_str} to {to_str}")
    print(f"🎯 Account: {account_id}")
    print(f"\n🔍 Testing {len(chart_ids)} chart types...\n")

    successful = []
    failed = []

    for chart_id in chart_ids:
        try:
            time_series = client.analytics.get_chart_time_series(
                chart_id=chart_id,
                account_id=account_id,
                from_date=from_str,
                to_date=to_str,
            )

            if time_series.data:
                successful.append((chart_id, len(time_series.data)))
                print(f"✅ {chart_id:20s} - {len(time_series.data):3d} data points")
            else:
                failed.append((chart_id, "No data"))
                print(f"⚠️  {chart_id:20s} - No data available")

        except Exception as e:
            failed.append((chart_id, str(e)[:50]))
            print(f"❌ {chart_id:20s} - {str(e)[:50]}")

    # Summary
    print("\n" + "-" * 70)
    print(f"📊 Summary: {len(successful)} successful, {len(failed)} failed")
    print("-" * 70)


def visualize_data_example(client, chart_id: str, account_id: str):
    """
    Example of how to use the time-series data for visualization.
    """
    print_section("Example: Using Time-Series Data for Visualization")

    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)
    from_str = from_date.strftime("%Y-%m-%d")
    to_str = to_date.strftime("%Y-%m-%d")

    try:
        time_series = client.analytics.get_chart_time_series(
            chart_id=chart_id,
            account_id=account_id,
            from_date=from_str,
            to_date=to_str,
        )

        if not time_series.data:
            print("\n⚠️  No data available for visualization")
            return

        print(f"\n📊 Creating simple ASCII chart for '{chart_id}'")
        print(f"   Data points: {len(time_series.data)}\n")

        # Extract values
        values = [point.value for point in time_series.data if point.value is not None]

        if not values:
            print("⚠️  No numeric values available")
            return

        # Simple ASCII bar chart
        max_value = max(values)
        min_value = min(values)
        value_range = max_value - min_value if max_value != min_value else 1

        print(f"   Max: {max_value:.0f}")
        print(f"   Min: {min_value:.0f}")
        print(f"   Range: {value_range:.0f}\n")

        # Show every nth point to fit in terminal
        step = max(1, len(time_series.data) // 20)
        for i in range(0, len(time_series.data), step):
            point = time_series.data[i]
            if point.value is not None:
                bar_length = int(((point.value - min_value) / value_range) * 40)
                bar = "█" * bar_length
                print(f"   {point.date} │{bar} {point.value:.0f}")

        print("\n   ✨ This data can be exported to CSV, plotted with matplotlib,")
        print("      or used in any data visualization library!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def main():
    """Main function."""
    api_key = os.getenv("PUBLER_API_KEY")

    if not api_key:
        print("❌ Error: PUBLER_API_KEY not found in environment variables")
        print("\nPlease set your API key:")
        print("  export PUBLER_API_KEY='your_api_key_here'")
        return

    client = PublerClient(api_key=api_key)

    print("=" * 70)
    print("  Publer Analytics - Time-Series Chart Data Example")
    print("=" * 70)

    try:
        # Set up workspace
        workspaces = client.workspaces.list()
        if not workspaces:
            print("\n❌ No workspaces found")
            return

        client.set_workspace(workspaces[0].id)
        print(f"\n✓ Active workspace: {workspaces[0].name}")

        # Get accounts
        accounts = client.accounts.list()
        if not accounts:
            print("\n❌ No accounts found")
            return

        print(f"✓ Found {len(accounts)} account(s)")
        account_id = accounts[0].id
        print(f"✓ Using account: {accounts[0].name} ({accounts[0].type})")

        # Get available charts
        print("\n📊 Fetching available charts...")
        charts = client.analytics.available_charts()
        if charts:
            print(f"✓ Found {len(charts)} available chart types")
            chart_id = charts[0].id if hasattr(charts[0], "id") else "followers"
        else:
            chart_id = "followers"  # Default fallback

        # Demonstrate the difference
        demonstrate_chart_metadata_vs_data(client, chart_id, account_id)

        # Try multiple chart types
        try_multiple_charts(client, account_id)

        # Visualization example
        visualize_data_example(client, chart_id, account_id)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 70)
    print("  Example complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
