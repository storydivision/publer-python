# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-10-07

### Added
- **Analytics Resource** - Complete analytics suite with 8 endpoints
  - Available charts listing
  - Chart data retrieval with filtering
  - Post insights with sorting and pagination
  - Hashtag performance analysis
  - Best times to post recommendations
  - Team member performance metrics
  - Competitor tracking
  - Competitor analysis and comparison
- **Analytics Models** - Pydantic models for all analytics data types
  - `Chart` - Available chart information
  - `ChartData` - Chart data with time periods
  - `PostInsight` - Post performance metrics
  - `HashtagPerformance` - Hashtag analytics
  - `BestTime` - Optimal posting times
  - `MemberPerformance` - Team member stats
  - `Competitor` - Competitor account info
  - `CompetitorAnalysis` - Competitor metrics
- **Job Status Polling** - Automatic job completion tracking
  - `client.job_status()` method with auto-poll option
  - `poll_job_status()` utility function
  - `poll_job_status_async()` for async operations
  - Configurable timeout and interval
  - Automatic completion/failure detection
- **Media Management** - Complete media upload and management
  - Upload from local files with MIME detection
  - Upload from URLs
  - List media library with pagination
  - Get media details
  - Delete media files
- **Enhanced Documentation**
  - `FEATURES.md` - Complete feature list
  - `CHANGELOG.md` - Version history
  - `examples/advanced_usage.py` - Advanced patterns
  - Updated README with 100% API coverage
  - Updated PROJECT_STATUS with completion metrics

### Changed
- Updated `PROJECT_STATUS.md` to reflect 100% API coverage (24/24 endpoints)
- Enhanced README with complete API coverage table
- Improved error messages for job failures
- Better ID validation across all models

### Fixed
- ID type conversion (API returns integers, converted to strings)
- Pydantic v2 compatibility for all models
- Async session cleanup in context managers

## [0.1.0] - 2025-10-07

### Added
- **Core Infrastructure**
  - `PublerClient` - Synchronous API client
  - `AsyncPublerClient` - Asynchronous API client
  - HTTP session layer using `httpx`
  - Environment variable support via `.env` files
  - Context manager support for resource cleanup
- **Workspaces Resource** - Workspace management
  - List all accessible workspaces
  - Get workspace details
  - Workspace switching
- **Accounts Resource** - Social media account management
  - List connected accounts (all platforms)
  - Get account details
- **Posts Resource** - Post creation and management
  - Create single posts
  - Create bulk posts
  - List posts with filtering and pagination
  - Get post details
  - Update posts
  - Delete posts
  - Media attachment support
- **Exception Handling** - Custom exception hierarchy
  - `PublerAPIError` - Base exception
  - `AuthenticationError` - 401 errors
  - `ValidationError` - 400 errors
  - `ForbiddenError` - 403 errors
  - `NotFoundError` - 404 errors
  - `RateLimitError` - 429 errors with retry_after
  - `ServerError` - 500+ errors
  - `JobTimeoutError` - Job polling timeout
  - `JobFailedError` - Job execution failure
- **Pydantic Models** - Type-safe data models
  - `Workspace` - Workspace data
  - `Account` - Account data
  - `Post`, `PostCreate`, `PostUpdate` - Post models
  - `JobStatus` - Job status tracking
  - `Media`, `MediaUpload` - Media models
- **Documentation**
  - Comprehensive README
  - QUICKSTART guide
  - CONTRIBUTING guidelines
  - PROJECT_STATUS tracking
  - Code examples (basic and async)
  - Setup verification script
- **Testing**
  - pytest configuration
  - Test fixtures
  - Client and exception tests
  - Real API integration testing

### Technical Details
- Python 3.8+ support
- httpx for HTTP/2 and async
- Pydantic v2 for validation
- python-dotenv for environment variables
- Full type hints throughout
- Both sync and async interfaces

---

## Future Plans

### v0.3.0 (Planned)
- Rate limiting with automatic retry
- Pagination helpers
- Response caching
- More comprehensive unit tests

### v1.0.0 (Planned)
- Production-ready release
- Complete test coverage
- Performance optimizations
- CLI tool
- Sphinx documentation

---

**Note**: This library is not officially affiliated with Publer. It's a community-driven project.
