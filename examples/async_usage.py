"""
Async usage examples for the Publer API client.

Before running this example:
1. Copy .env.example to .env
2. Add your Publer API key to the .env file
3. Install the package: pip install -e .
"""

import asyncio

from publer import AsyncPublerClient
from publer.exceptions import AuthenticationError, PublerAPIError


async def basic_async_example() -> None:
    """Demonstrate basic async client usage."""

    try:
        async with AsyncPublerClient() as client:
            # List workspaces
            print("\nFetching workspaces...")
            workspaces = await client.workspaces.list()
            print(f"✓ Found {len(workspaces)} workspace(s)")

            if workspaces:
                client.set_workspace(workspaces[0].id)

                # List accounts
                print("\nFetching accounts...")
                accounts = await client.accounts.list()
                print(f"✓ Found {len(accounts)} account(s)")

                # List posts
                print("\nFetching posts...")
                posts = await client.posts.list(limit=5)
                print(f"✓ Found {len(posts)} post(s)")

    except ValueError as e:
        print(f"Error: {e}")
        print("Make sure to set PUBLER_API_KEY in your .env file")
    except AuthenticationError:
        print("✗ Authentication failed. Check your API key.")
    except PublerAPIError as e:
        print(f"✗ API error: {e}")


async def concurrent_requests_example() -> None:
    """Demonstrate making concurrent requests."""

    try:
        async with AsyncPublerClient() as client:
            print("Making concurrent requests...")

            # Get workspaces first
            workspaces = await client.workspaces.list()
            if not workspaces:
                print("No workspaces found")
                return

            client.set_workspace(workspaces[0].id)

            # Make multiple requests concurrently using asyncio.gather
            accounts, posts = await asyncio.gather(
                client.accounts.list(),
                client.posts.list(limit=10),
            )

            print(f"✓ Accounts: {len(accounts)}")
            print(f"✓ Posts: {len(posts)}")

    except PublerAPIError as e:
        print(f"✗ API error: {e}")


async def main() -> None:
    """Run all async examples."""
    print("=== Basic Async Example ===\n")
    await basic_async_example()

    print("\n=== Concurrent Requests Example ===\n")
    await concurrent_requests_example()


if __name__ == "__main__":
    asyncio.run(main())
