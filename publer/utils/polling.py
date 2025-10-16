"""
Job polling utilities for async operations.
"""

import asyncio
import time
from typing import TYPE_CHECKING, Any, Dict, Optional

from publer.exceptions import JobFailedError, JobTimeoutError
from publer.models.posts import JobStatus

if TYPE_CHECKING:
    from publer.session import AsyncPublerSession, PublerSession


def poll_job_status(
    session: "PublerSession",
    job_id: str,
    timeout: float = 60.0,
    interval: float = 2.0,
) -> JobStatus:
    """
    Poll job status until completion or timeout.

    Args:
        session: HTTP session for making requests
        job_id: Job ID to poll
        timeout: Maximum time to wait in seconds
        interval: Polling interval in seconds

    Returns:
        JobStatus object when complete

    Raises:
        JobTimeoutError: If job doesn't complete within timeout
        JobFailedError: If job fails
        PublerAPIError: If API request fails

    Example:
        >>> result = client.posts.create(text="Hello", accounts=["acc_1"])
        >>> job_status = poll_job_status(client._session, result["job_id"])
        >>> print(job_status.status)
        completed
    """
    start_time = time.time()

    while True:
        # Check timeout
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise JobTimeoutError(
                f"Job {job_id} did not complete within {timeout} seconds",
                response={"job_id": job_id, "elapsed": elapsed},
            )

        # Poll job status
        response = session.request("GET", f"/job_status/{job_id}")
        job_status = JobStatus(**response)

        # Check if complete
        if job_status.status == "completed":
            return job_status

        # Check if failed
        if job_status.status == "failed":
            raise JobFailedError(
                f"Job {job_id} failed",
                response=response,
                errors=[str(job_status.failures)] if job_status.failures else None,
            )

        # Wait before next poll
        time.sleep(interval)


async def poll_job_status_async(
    session: "AsyncPublerSession",
    job_id: str,
    timeout: float = 60.0,
    interval: float = 2.0,
) -> JobStatus:
    """
    Asynchronously poll job status until completion or timeout.

    Args:
        session: Async HTTP session for making requests
        job_id: Job ID to poll
        timeout: Maximum time to wait in seconds
        interval: Polling interval in seconds

    Returns:
        JobStatus object when complete

    Raises:
        JobTimeoutError: If job doesn't complete within timeout
        JobFailedError: If job fails
        PublerAPIError: If API request fails

    Example:
        >>> result = await client.posts.create(text="Hello", accounts=["acc_1"])
        >>> job_status = await poll_job_status_async(client._session, result["job_id"])
        >>> print(job_status.status)
        completed
    """
    start_time = time.time()

    while True:
        # Check timeout
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise JobTimeoutError(
                f"Job {job_id} did not complete within {timeout} seconds",
                response={"job_id": job_id, "elapsed": elapsed},
            )

        # Poll job status
        response = await session.request("GET", f"/job_status/{job_id}")
        job_status = JobStatus(**response)

        # Check if complete
        if job_status.status == "completed":
            return job_status

        # Check if failed
        if job_status.status == "failed":
            raise JobFailedError(
                f"Job {job_id} failed",
                response=response,
                errors=[str(job_status.failures)] if job_status.failures else None,
            )

        # Wait before next poll
        await asyncio.sleep(interval)
