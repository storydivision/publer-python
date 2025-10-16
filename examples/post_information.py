#!/usr/bin/env python3
"""
Show Post Details from List
Get detailed information from posts.list() since posts.get() is restricted
"""

import os
import json
from dotenv import load_dotenv
from publer import PublerClient

load_dotenv()


def show_post_details(post, index=None):
    """Display detailed information about a post"""

    header = f"Post #{index}" if index else "Post Details"
    print("\n" + "=" * 70)
    print(f"  {header}")
    print("=" * 70)

    # Basic Information
    print("\n📄 BASIC INFORMATION")
    print(f"  ID: {getattr(post, 'id', 'N/A')}")
    print(f"  State: {getattr(post, 'state', 'N/A')}")

    # Dates
    created = getattr(post, "created_at", None)
    scheduled = getattr(post, "scheduled_at", None)
    published = getattr(post, "published_at", None)

    if created:
        print(f"  Created: {created}")
    if scheduled:
        print(f"  Scheduled: {scheduled}")
    if published:
        print(f"  Published: {published}")

    # Content
    print("\n📝 CONTENT")
    text = getattr(post, "text", None)
    if text:
        print(f"  Text: {text}")
    else:
        print("  Text: [No text]")

    # Link information
    link = getattr(post, "link", None)
    if link:
        print(f"\n🔗 LINK")
        print(f"  URL: {link}")

        link_title = getattr(post, "link_title", None)
        if link_title:
            print(f"  Title: {link_title}")

        link_desc = getattr(post, "link_description", None)
        if link_desc:
            print(f"  Description: {link_desc}")

    # Accounts
    accounts = getattr(post, "accounts", None)
    if accounts:
        print(f"\n📱 ACCOUNTS ({len(accounts)})")
        for idx, account in enumerate(accounts, 1):
            if isinstance(account, dict):
                name = account.get("name", "Unknown")
                platform = account.get("type", "Unknown")
                acc_id = account.get("id", "N/A")
                status = account.get("status", "N/A")
            else:
                name = getattr(account, "name", "Unknown")
                platform = getattr(account, "type", "Unknown")
                acc_id = getattr(account, "id", "N/A")
                status = getattr(account, "status", "N/A")

            print(f"  {idx}. {name} ({platform})")
            print(f"     ID: {acc_id}")
            if status != "N/A":
                print(f"     Status: {status}")

    # Media
    media = getattr(post, "media", None)
    if media:
        print(f"\n🖼️  MEDIA ({len(media)})")
        for idx, m in enumerate(media, 1):
            if isinstance(m, dict):
                media_type = m.get("type", "Unknown")
                url = m.get("url", "N/A")
                title = m.get("title", "Untitled")
                thumb = m.get("thumbnail", None)
            else:
                media_type = getattr(m, "type", "Unknown")
                url = getattr(m, "url", "N/A")
                title = getattr(m, "title", "Untitled")
                thumb = getattr(m, "thumbnail", None)

            print(f"  {idx}. {title}")
            print(f"     Type: {media_type}")
            if url != "N/A":
                print(f"     URL: {url[:60]}..." if len(url) > 60 else f"     URL: {url}")
            if thumb:
                print(
                    f"     Thumbnail: {thumb[:60]}..."
                    if len(thumb) > 60
                    else f"     Thumbnail: {thumb}"
                )

    # Additional metadata
    print("\n📊 METADATA")

    # Check for various fields
    fields_to_check = {
        "first_comment": "First Comment",
        "labels": "Labels",
        "notes": "Notes",
        "approval_status": "Approval Status",
        "creator": "Creator",
        "workspace_id": "Workspace ID",
        "post_type": "Post Type",
        "is_video": "Is Video",
        "video_thumbnail": "Video Thumbnail",
    }

    found_metadata = False
    for field, label in fields_to_check.items():
        if hasattr(post, field):
            value = getattr(post, field)
            if value is not None and value != "":
                print(f"  {label}: {value}")
                found_metadata = True

    if not found_metadata:
        print("  [No additional metadata available]")

    # Show all available attributes
    print("\n🔧 ALL AVAILABLE FIELDS")
    if hasattr(post, "model_dump"):
        post_dict = post.model_dump()
    elif hasattr(post, "dict"):
        post_dict = post.dict()
    else:
        post_dict = vars(post)

    print(f"  Available fields: {', '.join(post_dict.keys())}")

    # Raw JSON
    print("\n📋 RAW JSON")
    print("  " + "-" * 66)
    print(json.dumps(post_dict, indent=2, default=str))


def main():
    """Main function"""

    api_key = os.getenv("PUBLER_API_KEY")
    if not api_key:
        print("Error: PUBLER_API_KEY not found")
        return

    client = PublerClient(api_key=api_key)

    print("=" * 70)
    print("  Post Details Viewer - Crib Correspondent")
    print("=" * 70)

    # Setup workspace
    workspaces = client.workspaces.list()
    if workspaces:
        client.set_workspace(workspaces[0].id)
        print(f"\n✓ Workspace: {workspaces[0].name}")

    # Get recent posts
    print("\n📝 Fetching recent posts...")

    try:
        posts = client.posts.list(limit=5, state="all")

        if posts:
            print(f"✅ Found {len(posts)} post(s)")

            # Show summary
            print("\n" + "=" * 70)
            print("  📋 Posts Summary")
            print("=" * 70)

            for idx, post in enumerate(posts, 1):
                text = getattr(post, "text", "No text")
                state = getattr(post, "state", "Unknown")
                post_id = getattr(post, "id", "N/A")

                print(f"\n  {idx}. {text[:50] if text else '[No text]'}...")
                print(f"     State: {state} | ID: {post_id}")

            # Show detailed info for latest post
            print("\n" + "=" * 70)
            print("  🔍 DETAILED VIEW: Latest Post")
            print("=" * 70)

            show_post_details(posts[0], index=1)

            # Option to see more
            if len(posts) > 1:
                print("\n" + "=" * 70)
                print("  💡 More Posts Available")
                print("=" * 70)
                print(f"\n  You have {len(posts)} posts loaded.")
                print("  To see details of other posts, modify the script")
                print("  or use: show_post_details(posts[INDEX])")
        else:
            print("\n⚠️  No posts found")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
