# Publer API Python Client

A modern, type-safe Python client library for the [Publer API](https://publer.com/docs). This library provides a clean, Pythonic interface to interact with Publer's social media management platform.

## 🚀 Features

- **Complete API Coverage**: 100% of Publer API endpoints implemented (24/24)
- **Type-safe**: Built with Pydantic v2 for automatic validation and type checking
- **Modern HTTP**: Uses `httpx` for HTTP/2 support and async capabilities
- **Well-documented**: Full docstrings, examples, and guides
- **Error handling**: Custom exceptions for better error management
- **Job polling**: Automatic handling of asynchronous operations
- **Async support**: Both synchronous and asynchronous interfaces
- **Media management**: Upload from files or URLs with automatic MIME detection
- **Analytics**: Complete analytics suite with insights, charts, and competitor analysis

## 📋 Requirements

- Python 3.8+
- Publer Business or Enterprise plan
- Publer API key

## 🔧 Installation

```bash
pip install publer-api
```

Or install from source:

```bash
git clone https://github.com/yourusername/publer-api.git
cd publer-api
pip install -e .
```

## 🎯 Quick Start

```python
from publer import PublerClient

# Initialize the client
client = PublerClient(api_key="your_api_key_here")

# List workspaces
workspaces = client.workspaces.list()

# Set active workspace
client.set_workspace(workspaces[0].id)

# Create a post
post = client.posts.create(
    text="Hello from Publer API!",
    accounts=["account_id_1", "account_id_2"],
    scheduled_at="2025-10-15T10:00:00+00:00"
)

# Get post analytics
analytics = client.analytics.post_insights(post_id=post.id)
```

## 🏗️ Architecture

This library follows a modular design pattern optimized for REST API clients:

### Core Components

```
publer/
├── __init__.py          # Package exports
├── client.py            # Main PublerClient class
├── session.py           # HTTP session management (httpx wrapper)
├── exceptions.py        # Custom exception classes
├── models/              # Pydantic models
│   ├── __init__.py
│   ├── posts.py         # Post-related models
│   ├── accounts.py      # Account models
│   ├── analytics.py     # Analytics models
│   ├── media.py         # Media models
│   └── workspaces.py    # Workspace models
├── resources/           # API resource classes
│   ├── __init__.py
│   ├── base.py          # Base resource class
│   ├── posts.py         # Posts endpoints
│   ├── accounts.py      # Accounts endpoints
│   ├── analytics.py     # Analytics endpoints
│   ├── media.py         # Media endpoints
│   └── workspaces.py    # Workspaces endpoints
└── utils/               # Utility functions
    ├── __init__.py
    ├── rate_limit.py    # Rate limiting logic
    └── polling.py       # Job polling utilities
```

### Design Decisions

1. **httpx over requests**
   - HTTP/2 support for better performance
   - Native async/await support
   - Modern, actively maintained
   - Better connection pooling

2. **Pydantic for data models**
   - Automatic validation
   - Type safety
   - JSON serialization/deserialization
   - IDE autocomplete support

3. **Resource-based organization**
   - Each API category (posts, analytics, etc.) is a separate resource class
   - Cleaner namespace: `client.posts.create()` vs `client.create_post()`
   - Easier to maintain and extend

4. **Async job handling**
   - Automatic polling for async operations
   - Configurable timeout and retry logic
   - Optional manual job status checking

5. **Rate limit management**
   - Automatic rate limit detection
   - Configurable retry with exponential backoff
   - Rate limit info exposed to users

## 📚 API Coverage - 100% Complete! 🎉

| Resource | Endpoints | Status |
|----------|-----------|--------|
| **Workspaces** | 2/2 | ✅ Complete |
| **Accounts** | 2/2 | ✅ Complete |
| **Posts** | 6/6 | ✅ Complete |
| **Media** | 5/5 | ✅ Complete |
| **Job Status** | 1/1 | ✅ Complete |
| **Analytics** | 8/8 | ✅ Complete |

**Total: 24/24 endpoints (100%)**

### Workspaces
- ✅ List workspaces
- ✅ Get workspace details
- ✅ Workspace switching

### Accounts
- ✅ List connected accounts (all platforms)
- ✅ Get account details

### Posts
- ✅ Create posts (single & bulk)
- ✅ List posts (with filters, pagination, sorting)
- ✅ Get post details
- ✅ Update posts
- ✅ Delete posts
- ✅ Schedule posts with media

### Media
- ✅ Upload from local files
- ✅ Upload from URLs
- ✅ List media library
- ✅ Get media details
- ✅ Delete media

### Job Status
- ✅ Check job status
- ✅ Automatic polling with timeout

### Analytics
- ✅ Available charts
- ✅ Chart data retrieval
- ✅ Post insights (filtering, sorting, pagination)
- ✅ Hashtag analysis
- ✅ Best times to post
- ✅ Member performance
- ✅ Competitor tracking
- ✅ Competitor analysis

## 🔐 Authentication

Get your API key from [Publer Settings → Access & Login → API Keys](https://publer.com/help/en/article/how-to-access-the-publer-api-1w08edo/).

```python
# Method 1: Pass directly
client = PublerClient(api_key="your_api_key")

# Method 2: Environment variable
import os
client = PublerClient(api_key=os.getenv("PUBLER_API_KEY"))

# Method 3: Config file (recommended for production)
from publer import PublerClient
from publer.config import load_config

config = load_config("config.yaml")
client = PublerClient(**config)
```

## 🎨 Usage Examples

### Working with Posts

```python
# Create a scheduled post
post = client.posts.create(
    text="Check out our new product!",
    accounts=["account_id"],
    scheduled_at="2025-10-15T14:00:00+00:00",
    media_urls=["https://example.com/image.jpg"]
)

# Create a bulk post
bulk_result = client.posts.create_bulk([
    {
        "text": "Post 1",
        "accounts": ["account_id"],
        "scheduled_at": "2025-10-15T10:00:00+00:00"
    },
    {
        "text": "Post 2",
        "accounts": ["account_id"],
        "scheduled_at": "2025-10-15T14:00:00+00:00"
    }
])

# List scheduled posts
scheduled = client.posts.list(state="scheduled", limit=50)

# Update a post
updated = client.posts.update(
    post_id="post_id",
    text="Updated text"
)

# Delete a post
client.posts.delete(post_id="post_id")
```

### Media Management

```python
# Upload an image
media = client.media.upload(
    file_path="/path/to/image.jpg",
    title="Product Photo"
)

# Upload from URL
media = client.media.upload_from_url(
    url="https://example.com/image.jpg",
    title="Remote Image"
)

# List media library
media_list = client.media.list(limit=100)

# Delete media
client.media.delete(media_id="media_id")
```

### Analytics

```python
# Get post insights
insights = client.analytics.post_insights(
    from_date="2025-01-01",
    to_date="2025-01-31",
    sort_by="engagement",
    order="desc",
    limit=50
)

# Get hashtag analysis
hashtags = client.analytics.hashtag_analysis(
    from_date="2025-01-01",
    to_date="2025-01-31"
)

# Get best times to post
best_times = client.analytics.best_times_to_post(
    account_id="account_id"
)

# Get competitor analysis
competitors = client.analytics.competitors.list()
comparison = client.analytics.competitors.compare(
    competitor_ids=["comp_id_1", "comp_id_2"],
    from_date="2025-01-01",
    to_date="2025-01-31"
)
```

### Async Usage

```python
import asyncio
from publer import AsyncPublerClient

async def main():
    async with AsyncPublerClient(api_key="your_api_key") as client:
        # All methods are async
        workspaces = await client.workspaces.list()
        accounts = await client.accounts.list()
        
        # Concurrent requests
        posts, analytics = await asyncio.gather(
            client.posts.list(),
            client.analytics.post_insights()
        )

asyncio.run(main())
```

## ⚠️ Error Handling

```python
from publer.exceptions import (
    PublerAPIError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError
)

try:
    post = client.posts.create(text="Hello!")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Invalid data: {e.errors}")
except NotFoundError:
    print("Resource not found")
except PublerAPIError as e:
    print(f"API error: {e.message}")
```

## 🧪 Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=publer --cov-report=html

# Run specific test
pytest tests/test_posts.py -v
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/publer-api.git
cd publer-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Publer API Documentation](https://publer.com/docs)
- [Publer Website](https://publer.com)
- [Issue Tracker](https://github.com/yourusername/publer-api/issues)
- [Changelog](CHANGELOG.md)

## 📚 Documentation

- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Project Status**: See [PROJECT_STATUS.md](PROJECT_STATUS.md)
- **Changelog**: See [CHANGELOG.md](CHANGELOG.md)

## 🙏 Acknowledgments

- Built with [httpx](https://www.python-httpx.org/)
- Data validation by [Pydantic](https://docs.pydantic.dev/)
- Inspired by best practices from well-designed API clients

---

**Note**: This library is not officially affiliated with Publer. It's a community-driven project to make working with the Publer API easier for Python developers.
