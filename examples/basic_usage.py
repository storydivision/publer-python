"""
Basic usage examples for the Publer API client.

Before running this example:
1. Copy .env.example to .env
2. Add your Publer API key to the .env file
3. Install the package: pip install -e .
"""

from publer import PublerClient
from publer.exceptions import AuthenticationError, PublerAPIError


def main() -> None:
    """Demonstrate basic client usage."""

    # Initialize client (loads API key from .env file)
    try:
        client = PublerClient()
    except ValueError as e:
        print(f"Error: {e}")
        print("Make sure to set PUBLER_API_KEY in your .env file")
        return

    try:
        # List workspaces
        print("\nFetching workspaces...")
        workspaces = client.workspaces.list()
        print(f"✓ Found {len(workspaces)} workspace(s)")
        for workspace in workspaces:
            print(f"  - {workspace.name} (ID: {workspace.id})")

        # Set active workspace if available
        if workspaces:
            client.set_workspace(workspaces[0].id)
            print(f"\n✓ Set active workspace to: {workspaces[0].name}")

            # List connected accounts
            print("\nFetching connected accounts...")
            accounts = client.accounts.list()
            print(f"✓ Found {len(accounts)} account(s)")
            for account in accounts:
                print(f"  - {account.name} ({account.type})")

            # List scheduled posts
            print("\nFetching scheduled posts...")
            posts = client.posts.list(state="scheduled", limit=5)
            print(f"✓ Found {len(posts)} scheduled post(s)")
            for post in posts:
                text_preview = (post.text[:50] + "...") if post.text and len(post.text) > 50 else post.text
                print(f"  - {text_preview} (scheduled: {post.scheduled_at})")

    except AuthenticationError:
        print("✗ Authentication failed. Check your API key.")
    except PublerAPIError as e:
        print(f"✗ API error: {e}")
    finally:
        # Always close the client
        client.close()


def context_manager_example() -> None:
    """Demonstrate using the client as a context manager."""

    # Using context manager (automatically closes the client)
    try:
        with PublerClient() as client:
            workspaces = client.workspaces.list()
            print(f"Found {len(workspaces)} workspace(s)")
    except ValueError as e:
        print(f"Error: {e}")
    except PublerAPIError as e:
        print(f"API error: {e}")


def custom_configuration_example() -> None:
    """Demonstrate custom client configuration."""

    # Custom configuration without loading .env
    client = PublerClient(
        api_key="your_api_key_here",
        workspace_id="your_workspace_id",
        timeout=60.0,
        load_env=False,  # Don't load from .env file
    )

    try:
        workspaces = client.workspaces.list()
        print(f"Found {len(workspaces)} workspace(s)")
    finally:
        client.close()


def create_post_example() -> None:
    """Demonstrate creating a post."""

    try:
        with PublerClient() as client:
            # Get workspaces and accounts
            workspaces = client.workspaces.list()
            if not workspaces:
                print("No workspaces found")
                return

            client.set_workspace(workspaces[0].id)
            accounts = client.accounts.list()

            if not accounts:
                print("No accounts connected")
                return

            # Create a scheduled post
            print("Creating a scheduled post...")
            result = client.posts.create(
                text="Hello from Publer API! 🚀",
                accounts=[accounts[0].id],
                scheduled_at="2025-10-15T10:00:00+00:00",
                state="scheduled",
            )

            print(f"✓ Post creation initiated")
            print(f"  Job ID: {result.get('job_id')}")
            print("  Use job_status endpoint to check progress")

    except ValueError as e:
        print(f"Error: {e}")
    except PublerAPIError as e:
        print(f"API error: {e}")


if __name__ == "__main__":
    print("=== Basic Usage Example ===\n")
    main()

    print("\n=== Context Manager Example ===\n")
    context_manager_example()

    print("\n=== Create Post Example ===\n")
    create_post_example()
