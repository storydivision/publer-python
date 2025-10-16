#!/usr/bin/env python3
"""
Quick test script to verify the Publer API client works with your API key.

This script will:
1. Connect to the API
2. Fetch your user info
3. List workspaces
4. List accounts
5. List posts

Run: python test_api.py
"""

from publer import PublerClient
from publer.exceptions import AuthenticationError, PublerAPIError


def main() -> None:
    """Test the API client."""
    print("=" * 60)
    print("Publer API Client - Quick Test")
    print("=" * 60)

    try:
        # Initialize client
        print("\n1. Initializing client...")
        client = PublerClient()
        print("   ✓ Client initialized")

        # Test authentication by fetching workspaces
        print("\n2. Testing authentication (fetching workspaces)...")

        # List workspaces
        print("\n3. Fetching workspaces...")
        workspaces = client.workspaces.list()
        print(f"   ✓ Found {len(workspaces)} workspace(s)")

        if workspaces:
            for i, workspace in enumerate(workspaces, 1):
                print(f"   {i}. {workspace.name} (ID: {workspace.id})")

            # Set first workspace as active
            client.set_workspace(workspaces[0].id)
            print(f"\n   ✓ Set active workspace: {workspaces[0].name}")

            # List accounts
            print("\n4. Fetching connected accounts...")
            accounts = client.accounts.list()
            print(f"   ✓ Found {len(accounts)} account(s)")

            if accounts:
                for i, account in enumerate(accounts, 1):
                    print(f"   {i}. {account.name} ({account.type})")
            else:
                print("   No accounts connected yet")

            # List posts
            print("\n4. Fetching posts...")
            posts = client.posts.list(limit=5)
            print(f"   ✓ Found {len(posts)} post(s)")

            if posts:
                for i, post in enumerate(posts, 1):
                    text = post.text or "(no text)"
                    text_preview = text[:40] + "..." if len(text) > 40 else text
                    print(f"   {i}. {text_preview}")
                    print(f"      State: {post.state}, Scheduled: {post.scheduled_at}")
            else:
                print("   No posts found")

        else:
            print("   No workspaces found")

        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)

        client.close()

    except ValueError as e:
        print(f"\n✗ Configuration error: {e}")
        print("\nMake sure to:")
        print("1. Copy .env.example to .env")
        print("2. Add your Publer API key to .env")
        return

    except AuthenticationError:
        print("\n✗ Authentication failed")
        print("\nPlease check:")
        print("1. Your API key is correct")
        print("2. You have a Business or Enterprise Publer plan")
        print("3. The API key hasn't been revoked")
        return

    except PublerAPIError as e:
        print(f"\n✗ API error: {e}")
        if hasattr(e, "status_code"):
            print(f"   Status code: {e.status_code}")
        if hasattr(e, "errors") and e.errors:
            print(f"   Errors: {', '.join(e.errors)}")
        return

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
