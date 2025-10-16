"""
Advanced usage examples for the Publer API client.

Demonstrates:
- Job status polling
- Media upload
- Creating posts with media
- Error handling
"""

from publer import PublerClient
from publer.exceptions import JobFailedError, JobTimeoutError, PublerAPIError


def job_polling_example() -> None:
    """Demonstrate job status polling for async operations."""
    print("=== Job Polling Example ===\n")

    try:
        with PublerClient() as client:
            # Get workspace and accounts
            workspaces = client.workspaces.list()
            if not workspaces:
                print("No workspaces found")
                return

            client.set_workspace(workspaces[0].id)
            accounts = client.accounts.list()

            if not accounts:
                print("No accounts found")
                return

            # Create a post (returns job_id)
            print("Creating post...")
            result = client.posts.create(
                text="Testing job polling! 🚀",
                accounts=[accounts[0].id],
                state="draft",  # Use draft to avoid actually posting
            )

            job_id = result.get("job_id")
            print(f"✓ Post creation initiated (Job ID: {job_id})")

            # Method 1: Manual polling
            print("\nMethod 1: Manual job status check...")
            status = client.job_status(job_id)
            print(f"  Status: {status.status}")

            # Method 2: Auto-poll until complete
            print("\nMethod 2: Auto-poll until complete...")
            final_status = client.job_status(job_id, poll=True, timeout=30)
            print(f"  ✓ Job completed!")
            print(f"  Final status: {final_status.status}")
            if final_status.payload:
                print(f"  Payload: {final_status.payload}")

    except JobTimeoutError as e:
        print(f"✗ Job timed out: {e}")
    except JobFailedError as e:
        print(f"✗ Job failed: {e}")
        if e.errors:
            print(f"  Errors: {e.errors}")
    except PublerAPIError as e:
        print(f"✗ API error: {e}")


def media_upload_example() -> None:
    """Demonstrate media upload and usage in posts."""
    print("\n=== Media Upload Example ===\n")

    try:
        with PublerClient() as client:
            # Setup workspace
            workspaces = client.workspaces.list()
            if not workspaces:
                print("No workspaces found")
                return

            client.set_workspace(workspaces[0].id)

            # Method 1: Upload from URL
            print("Uploading media from URL...")
            media_result = client.media.upload_from_url(
                url="https://picsum.photos/800/600",
                title="Sample Image from URL",
            )
            print(f"✓ Media uploaded: {media_result}")

            # List media library
            print("\nListing media library...")
            media_list = client.media.list(limit=5)
            print(f"✓ Found {len(media_list)} media file(s)")
            for media in media_list:
                print(f"  - {media.title or 'Untitled'} ({media.type})")

            # Method 2: Upload local file (example - file must exist)
            # print("\nUploading local file...")
            # result = client.media.upload(
            #     "/path/to/your/image.jpg",
            #     title="My Local Image"
            # )
            # print(f"✓ Uploaded: {result}")

    except FileNotFoundError as e:
        print(f"✗ File not found: {e}")
    except PublerAPIError as e:
        print(f"✗ API error: {e}")


def create_post_with_media_example() -> None:
    """Demonstrate creating a post with media."""
    print("\n=== Create Post with Media Example ===\n")

    try:
        with PublerClient() as client:
            # Setup
            workspaces = client.workspaces.list()
            if not workspaces:
                print("No workspaces found")
                return

            client.set_workspace(workspaces[0].id)
            accounts = client.accounts.list()

            if not accounts:
                print("No accounts found")
                return

            # Get media from library
            media_list = client.media.list(limit=1)

            if media_list:
                print(f"Using media: {media_list[0].title or 'Untitled'}")

                # Create post with media from library
                result = client.posts.create(
                    text="Check out this awesome image! 📸",
                    accounts=[accounts[0].id],
                    media_ids=[media_list[0].id],
                    state="draft",
                )

                print(f"✓ Post created with media (Job ID: {result.get('job_id')})")

                # Poll for completion
                status = client.job_status(result["job_id"], poll=True)
                print(f"✓ Job completed: {status.status}")

            else:
                # Create post with media URL
                print("No media in library, using URL...")
                result = client.posts.create(
                    text="Posting with media URL! 🖼️",
                    accounts=[accounts[0].id],
                    media_urls=["https://picsum.photos/800/600"],
                    state="draft",
                )

                print(f"✓ Post created (Job ID: {result.get('job_id')})")

    except PublerAPIError as e:
        print(f"✗ API error: {e}")


def error_handling_example() -> None:
    """Demonstrate comprehensive error handling."""
    print("\n=== Error Handling Example ===\n")

    try:
        with PublerClient() as client:
            workspaces = client.workspaces.list()
            client.set_workspace(workspaces[0].id)

            # Try to get a non-existent post
            try:
                post = client.posts.get("invalid_post_id")
            except PublerAPIError as e:
                print(f"Expected error caught: {e}")
                print(f"  Status code: {e.status_code}")
                if e.errors:
                    print(f"  Errors: {e.errors}")

            # Try to create post with invalid data
            try:
                result = client.posts.create(
                    text="Test",
                    accounts=[],  # Empty accounts list - should fail
                )
            except PublerAPIError as e:
                print(f"\nValidation error caught: {e}")

    except PublerAPIError as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    # Run all examples
    job_polling_example()
    media_upload_example()
    create_post_with_media_example()
    error_handling_example()

    print("\n" + "=" * 60)
    print("✓ All advanced examples completed!")
    print("=" * 60)
