#!/usr/bin/env python3
"""
Publer Analytics Explorer for Crib Correspondent
Explore various analytics endpoints and insights
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from publer import PublerClient

# Load environment variables
load_dotenv()


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def explore_available_charts(client):
    """Get list of available analytics charts"""
    print_section("📊 Available Analytics Charts")

    try:
        charts = client.analytics.available_charts()

        if charts:
            print(f"\n✅ Found {len(charts)} available chart(s):")
            for idx, chart in enumerate(charts, 1):
                chart_id = chart.id if hasattr(chart, "id") else "unknown"
                chart_type = chart.type if hasattr(chart, "type") else "unknown"
                print(f"  {idx}. {chart_id} ({chart_type})")
            
            # Return first chart for testing
            return charts[0].id if charts else None
        else:
            print("\n⚠️  No charts available")
            return None

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def get_post_insights(client, account_id, days_back=30):
    """Get insights for posts over a date range"""
    print_section(f"📈 Post Insights")

    try:
        # Try multiple date ranges to find data
        # Including specific range around October 11, 2025
        date_ranges = [
            (7, "Last 7 Days"),
            (days_back, "Last {} Days".format(days_back)),
            (60, "Last 60 Days"),
            (90, "Last 90 Days"),
            (180, "Last 6 Months"),
            (365, "Last Year"),
        ]
        
        # Also try a specific date range around Oct 11, 2025
        specific_ranges = [
            ("2025-10-01", "2025-10-16", "October 1-16, 2025"),
            ("2025-10-11", "2025-10-12", "October 11-12, 2025 (specific)"),
            ("2025-10-10", "2025-10-13", "October 10-13, 2025"),
        ]
        
        insights = None
        
        # Try specific date ranges first
        print("\n🔍 Trying specific date ranges around Oct 11, 2025...")
        for from_str, to_str, label in specific_ranges:
            print(f"\n📅 Trying: {label} ({from_str} to {to_str})")
            
            # Try with specific account first
            print(f"🎯 With account: {account_id}")
            try:
                insights = client.analytics.post_insights(
                    account_id=account_id, from_date=from_str, to_date=to_str, 
                    sort_by="engagement", sort_type="DESC", page=0
                )
                
                if insights:
                    print(f"✅ Found {len(insights)} posts!")
                    break
                else:
                    print("⚠️  No data with account filter (empty list returned)...")
            except Exception as e:
                print(f"⚠️  Error with account filter: {e}")
                if hasattr(e, 'status_code'):
                    print(f"     Status: {e.status_code}")
                insights = None
                
            # Try without account filter (all workspace accounts)
            print(f"🎯 Trying without account filter (all workspace accounts)")
            insights = client.analytics.post_insights(
                from_date=from_str, to_date=to_str, 
                sort_by="engagement", sort_type="DESC", page=0
            )
            
            if insights:
                print(f"✅ Found {len(insights)} posts!")
                break
            else:
                print("⚠️  No data without account filter either...")
        
        # If not found, try relative date ranges
        if not insights:
            print("\n🔍 Trying relative date ranges...")
        
        for days, label in date_ranges:
            if insights:
                break
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days)

            from_str = from_date.strftime("%Y-%m-%d")
            to_str = to_date.strftime("%Y-%m-%d")

            print(f"\n📅 Trying: {label} ({from_str} to {to_str})")
            print(f"🎯 Account: {account_id}")

            # Get insights sorted by engagement
            insights = client.analytics.post_insights(
                account_id=account_id, from_date=from_str, to_date=to_str, 
                sort_by="engagement", sort_type="DESC", page=0
            )
            
            if insights:
                print(f"✅ Found {len(insights)} posts!")
                break
            else:
                print("⚠️  No data in this period, trying longer range...")

        if insights:
            print(f"\n✅ Top {len(insights)} posts by engagement:")
            for idx, post in enumerate(insights, 1):
                text = post.text if hasattr(post, "text") and post.text else "No text"
                engagement = post.engagement if hasattr(post, "engagement") else "N/A"
                impressions = post.impressions if hasattr(post, "impressions") else "N/A"
                reach = post.reach if hasattr(post, "reach") else "N/A"

                print(f"\n  {idx}. {text[:60]}...")
                print(f"     Engagement: {engagement}, Reach: {reach}, Impressions: {impressions}")
                if hasattr(post, 'post_id'):
                    print(f"     Post ID: {post.post_id}")
        else:
            print("\n⚠️  No post insights available in any period tried")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("     (This endpoint may require a Business/Enterprise plan)")


def get_hashtag_analysis(client, account_id, days_back=30):
    """Analyze hashtag performance"""
    print_section(f"#️⃣ Hashtag Analysis (Last {days_back} Days)")

    try:
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)

        from_str = from_date.strftime("%Y-%m-%d")
        to_str = to_date.strftime("%Y-%m-%d")
        
        print(f"📅 Date Range: {from_str} to {to_str}")
        print(f"🎯 Account: {account_id}")

        hashtags = client.analytics.hashtag_analysis(
            account_id=account_id, from_date=from_str, to_date=to_str, page=0
        )

        if hashtags:
            print(f"\n✅ Found {len(hashtags)} hashtag(s):")
            for idx, tag in enumerate(hashtags, 1):
                print(f"\n  {idx}. {tag}")
        else:
            print("\n⚠️  No hashtag data available")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("     (This endpoint may require specific permissions)")


def get_best_times(client, account_id, days_back=30):
    """Get best times to post for an account"""
    print_section(f"⏰ Best Times to Post (Last {days_back} Days)")

    try:
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)

        from_str = from_date.strftime("%Y-%m-%d")
        to_str = to_date.strftime("%Y-%m-%d")
        
        print(f"\n📅 Date Range: {from_str} to {to_str}")
        print(f"🎯 Analyzing for account: {account_id}")

        best_times = client.analytics.best_times_to_post(
            from_date=from_str, to_date=to_str, account_id=account_id
        )

        if best_times:
            print("\n✅ Best times data retrieved:")
            print(best_times)
        else:
            print("\n⚠️  No best times data available")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        # Show full error details if available
        if hasattr(e, 'response'):
            print(f"     Response: {e.response}")
        if hasattr(e, 'status_code'):
            print(f"     Status Code: {e.status_code}")
        print("     (This endpoint may not be available for this account type)")


def get_member_performance(client, days_back=30):
    """Get team member performance metrics"""
    print_section(f"👥 Member Performance (Last {days_back} Days)")

    try:
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)

        from_str = from_date.strftime("%Y-%m-%d")
        to_str = to_date.strftime("%Y-%m-%d")

        performance = client.analytics.member_performance(from_date=from_str, to_date=to_str)

        if performance:
            print(f"\n✅ Found {len(performance)} member(s) with performance data:")
            # Handle raw dict data if model validation fails
            if isinstance(performance, list):
                for idx, member in enumerate(performance, 1):
                    reach = member.reach if hasattr(member, "reach") else "N/A"
                    engagement = member.engagement if hasattr(member, "engagement") else "N/A"
                    impressions = member.impressions if hasattr(member, "impressions") else "N/A"
                    print(f"\n  {idx}. Reach: {reach}, Engagement: {engagement}, Impressions: {impressions}")
            else:
                print(performance)
        else:
            print("\n⚠️  No member performance data available")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("     (This endpoint may have data format issues)")


def get_chart_data(client, chart_id, account_id, days_back=30):
    """Get specific chart data"""
    print_section(f"📊 Chart Data: {chart_id}")

    try:
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)

        from_str = from_date.strftime("%Y-%m-%d")
        to_str = to_date.strftime("%Y-%m-%d")

        print(f"\n📅 Date Range: {from_str} to {to_str}")
        print(f"🎯 Account: {account_id}")

        chart_data = client.analytics.chart_data(
            chart_id=chart_id, account_id=account_id, from_date=from_str, to_date=to_str
        )

        if chart_data:
            print("\n✅ Chart data retrieved:")
            print(chart_data)
        else:
            print("\n⚠️  No chart data available")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("     (Check if chart name is valid)")


def main():
    """Main function to explore analytics"""

    # Initialize client
    api_key = os.getenv("PUBLER_API_KEY")

    if not api_key:
        print("Error: PUBLER_API_KEY not found in environment variables")
        return

    client = PublerClient(api_key=api_key)

    print("=" * 70)
    print("  Publer Analytics Explorer - Crib Correspondent")
    print("=" * 70)

    try:
        # Set up workspace
        workspaces = client.workspaces.list()
        if workspaces:
            client.set_workspace(workspaces[0].id)
            print(f"\n✓ Active workspace: {workspaces[0].name}")
            print(f"✓ Workspace ID: {workspaces[0].id}")
            print(f"✓ Publer-Workspace-Id header is set for all API requests")

        # Get accounts for reference
        accounts = client.accounts.list()
        if accounts:
            print(f"\n📱 Available accounts:")
            for idx, account in enumerate(accounts, 1):
                print(f"  {idx}. {account.name} ({account.type}) - ID: {account.id}")

            # Store first account ID for analytics that need it
            first_account_id = accounts[0].id
        else:
            print("\n⚠️  No accounts found")
            return

        # Explore various analytics endpoints
        first_chart_id = explore_available_charts(client)

        get_post_insights(client, first_account_id, days_back=30)

        get_hashtag_analysis(client, first_account_id, days_back=30)

        get_best_times(client, first_account_id)

        get_member_performance(client, days_back=30)

        # Try getting specific chart data with first available chart
        if first_chart_id:
            get_chart_data(client, first_chart_id, first_account_id, days_back=30)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 70)
    print("  Analytics exploration complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
